# Automated Data Entry Bot

This project automates data entry into Windows Notepad:

* Fetches the first 10 posts from [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
* Opens Notepad, types each post, saves it to `Desktop/tjm_project_posts/post <id>.txt`.
* Closes Notepad after every post.
* Includes robust error handling.

## Run the Standalone App (No Python Required)

1. Download the latest `tjm-project.exe` from the [Releases](https://github.com/BardeesKhaled/automated-data-entry-bot/releases) page.
2. Double-click the `.exe` on Windows 10/11.

## Run From Source (Optional)

```bash
git clone https://github.com/BardeesKhaled/automated-data-entry-bot.git
cd automated-data-entry-bot
pip install -r requirements.txt
python tjm-project.py
