"""
Enhanced Automated Data Entry Bot
---------------------------------
Adds robust error handling for:
  1. Process-launch issues (Notepad missing)
  2. Focus/UI automation failures
  3. File-system errors
  4. Environment/platform checks
  5. Graceful interruption (Ctrl+C)

Dependencies:
    pip install requests pyautogui pygetwindow
"""

import sys
import os
import time
import subprocess
import traceback

# ----- Import third-party libs with ImportError guard -----
try:
    import requests
    import pyautogui
    import pygetwindow as gw
except ImportError as e:
    sys.stderr.write(
        f"[FATAL] Missing dependency: {e.name}\n"
        "Run: pip install requests pyautogui pygetwindow\n"
    )
    sys.exit(1)

# ---------------- Configuration ----------------
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "tjm_project_posts")
POSTS_LIMIT = 10
WAIT_AFTER_LAUNCH = 2.5
WAIT_AFTER_TYPING = 0.5
TYPING_INTERVAL = 0.008

pyautogui.FAILSAFE = True  # allow mouse-corner abort

# ---------------- Helpers ----------------
def setup_directory():
    """Create the output directory if it doesn't exist."""
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        print(f"[+] Output directory: {SAVE_DIR}")
    except OSError as e:
        sys.stderr.write(f"[FATAL] Cannot create save directory: {e}\n")
        sys.exit(1)

def close_all_notepads():
    """Force-close all Notepad instances (safety net)."""
    subprocess.run(["taskkill", "/F", "/IM", "notepad.exe"], capture_output=True, check=False)
    subprocess.run(["taskkill", "/F", "/IM", "Notepad.exe"], capture_output=True, check=False)

def fetch_posts(limit=POSTS_LIMIT):
    url = f"https://jsonplaceholder.typicode.com/posts?_limit={limit}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"[!] Network error fetching posts: {e}")
        return []

def launch_notepad():
    """Launch Notepad and return the process object or raise FileNotFoundError."""
    try:
        return subprocess.Popen(["notepad"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise FileNotFoundError("Notepad executable not found. Is it installed or on PATH?")

def verify_notepad_focus():
    """Ensure the foreground window is Notepad before typing."""
    try:
        active = gw.getActiveWindow()
        if not active or "Notepad" not in active.title:
            raise RuntimeError("Active window is not Notepad. Typing aborted.")
    except Exception as e:
        raise RuntimeError(f"Focus check failed: {e}")

def safe_type_text(text):
    """Type text into the active window, handle FailSafeException."""
    try:
        pyautogui.typewrite(text, interval=TYPING_INTERVAL)
    except pyautogui.FailSafeException:
        raise RuntimeError("Typing aborted by user (pyautogui FAILSAFE).")
    except Exception as e:
        raise RuntimeError(f"Typing error: {e}")

def save_text_to_file(post_id, text):
    filename = os.path.join(SAVE_DIR, f"post {post_id}.txt")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[+] Saved file: {os.path.basename(filename)}")
    except OSError as e:
        raise RuntimeError(f"File-system error saving '{filename}': {e}")

# ---------------- Main loop ----------------
def process_single_post(post):
    pid = post.get("id", "unknown")
    content = f"Title: {post.get('title','')}\n\n{post.get('body','')}"
    proc = None
    try:
        proc = launch_notepad()
        print(f"[+] Notepad launched (pid={proc.pid})")
        time.sleep(WAIT_AFTER_LAUNCH)

        verify_notepad_focus()
        print(f"[~] Typing post {pid}...")
        safe_type_text(content)

        save_text_to_file(pid, content)
        time.sleep(WAIT_AFTER_TYPING)

    except Exception as e:
        print(f"[!] Error processing post {pid}: {e}")
        traceback.print_exc()
    finally:
        print("[~] Closing Notepad for this post...")
        # kill by name to catch modern Notepad host process
        close_all_notepads()
        # also try pid if still alive
        if proc and proc.poll() is None:
            subprocess.run(["taskkill", "/F", "/PID", str(proc.pid)], capture_output=True, check=False)

def main():
    if os.name != "nt":
        sys.stderr.write("[FATAL] This script is for Windows only.\n")
        sys.exit(1)

    setup_directory()
    close_all_notepads()

    posts = fetch_posts()
    if not posts:
        print("[!] No posts fetched, exiting.")
        return

    for p in posts:
        process_single_post(p)
        time.sleep(0.8)

    close_all_notepads()
    print("\n=== Completed successfully. Files in 'tjm-project' on Desktop. ===")

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Cleaning up...")
        close_all_notepads()
        sys.exit(1)
    except Exception as e:
        print("[!] Unhandled exception:", e)
        traceback.print_exc()
        close_all_notepads()
        sys.exit(1)
