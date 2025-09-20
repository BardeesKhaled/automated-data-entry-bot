# Automated Data Entry Bot

This project automates data entry into Windows Notepad:

* Fetches the first 10 posts from [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
* Opens Notepad, types each post, saves it to `Desktop/tjm_project_posts/post <id>.txt`.
* Closes Notepad after every post.
* Includes extensive error handling for network, process, focus, file-system, and user-interrupt issues.

## Error Handling & Edge Cases

The bot includes defensive code for common failure scenarios:

### Process-launch issues (Notepad missing)
- If Notepad is not installed or not on the PATH, launching with  
  `subprocess.Popen(["notepad"])` raises **FileNotFoundError**.  
- The script catches this and exits with a clear, user-friendly message.

### Focus / UI automation failures
- **Window focus check:** Uses **pygetwindow** to confirm the active window title contains “Notepad” before typing.  
- **User abort:** Moving the mouse to any screen corner during typing triggers PyAutoGUI’s **FailSafeException**.  
  The script catches it, logs a message, and closes Notepad safely.

### File-system errors
- Handles **OSError** when writing output (e.g., Desktop is read-only, disk full, or permission denied).  
- Reports the problem and cleans up without leaving stray Notepad windows.

### Environment / platform checks
- Verifies the OS is Windows (`os.name == "nt"`) before starting, because the automation depends on `notepad.exe` and `taskkill`.  
- Detects missing Python dependencies at startup and prints instructions to install them.

### Graceful interruption (Ctrl+C)
- A top-level `try/except KeyboardInterrupt` ensures that if the user stops the program with **Ctrl+C**,  
  all Notepad windows opened by the script are force-closed before exiting.

---

These safeguards mean the application **fails safely** and leaves the system clean even when something goes wrong.

## Run the Standalone App (No Python Required)

1. Download the latest `tjm-project.exe` from the [Releases](https://github.com/BardeesKhaled/automated-data-entry-bot/releases) page.
2. Double-click the `.exe` on Windows 10/11.

## Run From Source (Optional)

```bash
git clone https://github.com/BardeesKhaled/automated-data-entry-bot.git
cd automated-data-entry-bot
pip install -r requirements.txt
python tjm-project.py

