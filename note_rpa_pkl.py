from playwright.sync_api import Playwright, sync_playwright
import os
import argparse
from dotenv import load_dotenv
import json
import pickle

load_dotenv()
VOICE_DIR = os.environ.get("VOICE_DIR")
NOTE_ID = os.environ.get("NOTE_ID")
NOTE_PASS = os.environ.get("NOTE_PASS")
TITLE_SUFFIX = os.environ.get("TITLE_SUFFIX")
tags = os.environ.get("TAGS")
tag_list = tags.split(',') if tags else []
GROUP = os.environ.get("GROUP")

def read_file_contents(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except Exception as e:
        print("An error occurred while reading the file:", e)
        return None

def run(playwright: Playwright,file_path,mode) -> None:

    dir_path = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    file_name_noext = os.path.splitext(filename)[0]
    content_filepath  = os.path.join(dir_path,file_name_noext+".json")
    json_txt = read_file_contents(content_filepath)

    #print(file_path)
    #print(dir_path)
    #print(content_filepath)
    #print(json_txt)

    title_content  = json.loads(json_txt)
    print(title_content)

    # --------------------
    browser = playwright.chromium.launch(headless=False)
    with open('browser_state.pkl', 'rb') as file:
        storage_state = pickle.load(file)
    context = browser.new_context(storage_state=storage_state)
    page = context.new_page()

    #context = browser.new_context()
    ## Open new page
    #page = context.new_page()
    # Go to https://note.com/
    page.goto("https://note.com/")
    page.wait_for_timeout(3000) #待つ必要あり

    page.wait_for_selector("[aria-label=\"投稿\"]")
    # Click [aria-label="投稿"]
    page.click("[aria-label=\"投稿\"]")
    # Click button:has-text("音声")
    page.click("button:has-text(\"音声\")")

    # 音声ファイルの投稿
    page.wait_for_selector("text=クリックしてファイルを追加")
    with page.expect_file_chooser() as file_chooser:
        print("ファイルを追加します")
        #abs_path = os.path.join(dirpath,imgfile)
        page.click("text=クリックしてファイルを追加")
        file_chooser.value.set_files(files=[file_path])
        print(f"ファイルを追加成功:{filename}")


    # 画像ファイルの投稿
    page.wait_for_selector("text=クリックして画像を追加")
    with page.expect_file_chooser() as file_chooser:
        print("画像を追加します")
        page.click("text=クリックして画像を追加")
        abs_path = os.path.join(dir_path,"image.png")
        file_chooser.value.set_files(files=[abs_path])
        print(f"画像を追加成功:{abs_path}")

    page.wait_for_timeout(3000) #待つ必要あり

    # タイトル
    page.click("[placeholder=\"例：オススメの曲\"]")
    page.fill("[placeholder=\"例：オススメの曲\"]", f"{title_content['title']}  {TITLE_SUFFIX} {filename}")

    # グループ
    page.click("[placeholder=\"例：私たちのグループ\"]")
    page.fill("[placeholder=\"例：私たちのグループ\"]", f"{GROUP}")

    # 説明文
    page.click("textarea")
    page.fill("textarea", f"{title_content['summary']}")

    # Select 1
    page.select_option("select", "1")
    # Select 6
    page.select_option("#secondaryCategories", "6")

    tag_list = tags.split(',') if tags else []

    # Loop over each tag and click the corresponding button
    for tag in tag_list:
        button_selector = f"button:has-text(\"{tag}\")"
        page.click(button_selector)

    # Click div[role="dialog"] button:has-text("投稿")
    if mode == "test":
        pass
        page.click("div[role=\"dialog\"] button:has-text(\"下書き保存\")")
    else:
        # Click [aria-label="閉じる"]
        # with page.expect_navigation(url="https://note.com/hikousen_agri/n/nb2b120ff4dd5"):
        page.click("div[role=\"dialog\"] button:has-text(\"投稿\")")
        with page.expect_navigation():
            page.click("[aria-label=\"閉じる\"]")

    # ---------------------
    context.close()
    browser.close()

def main_play(file_path,mode):
    with sync_playwright() as playwright:
        run(playwright, file_path,mode)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Run Playwright script with a file")

    # Add the arguments
    parser.add_argument("file_path", help="The file path to process")
    parser.add_argument("--mode", choices=['test', 'apply'], default='test', help="The mode to run the script in (test or apply). Default is 'test'.")

    # Execute the parse_args() method
    args = parser.parse_args()

    # Call main_play with the provided file_path and mode arguments
    main_play(args.file_path, args.mode)