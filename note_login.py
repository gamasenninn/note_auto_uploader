from playwright.sync_api import Playwright, sync_playwright
import os
import argparse
from dotenv import load_dotenv
import pickle

load_dotenv()
NOTE_ID = os.environ.get("NOTE_ID")
NOTE_PASS = os.environ.get("NOTE_PASS")

def run_login(playwright: Playwright) -> None:
    # --------------------
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://note.com/
    page.goto("https://note.com/login?redirectPath=https%3A%2F%2Fnote.com%2F")
    print("ログインします")
    # IDの入力
    print("IDを入力します")
    page.wait_for_selector("[placeholder='mail@example.com or note ID']")
    page.click("[placeholder=\"mail@example.com or note ID\"]")
    # Fill [placeholder="mail@example.com or note ID"]
    page.fill("[placeholder=\"mail@example.com or note ID\"]", NOTE_ID)
    #page.press("[placeholder=\"mail@example.com or note ID\"]", "Tab")
    # Fill [aria-label="パスワード"]
    page.fill("[aria-label=\"パスワード\"]", NOTE_PASS)
    # Click button:has-text("ログイン")
    # with page.expect_navigation(url="https://note.com/"):
    with page.expect_navigation():
        page.click("button:has-text(\"ログイン\")")

    page.wait_for_selector("[aria-label=\"投稿\"]", timeout=120000)

    # ブラウザの状態を取得
    storage_state = context.storage_state()

    # 状態をpickleファイルに保存
    with open('browser_state.pkl', 'wb') as file:
        pickle.dump(storage_state, file)

    # ---------------------
    context.close()
    browser.close()

def login_play():
    with sync_playwright() as playwright:
        run_login(playwright)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Run Playwright script for only login")

    # Add the arguments

    # Execute the parse_args() method
    args = parser.parse_args()

    # Call main_play with the provided file_path and mode arguments
    login_play()