import glob
import json
from dotenv import load_dotenv
import os

load_dotenv()
VOICE_DIR = os.environ.get("VOICE_DIR")  # 'get' メソッドを使用

def check_json_files(directory):
    # 指定されたディレクトリ内のすべてのJSONファイルを取得
    file_paths = glob.glob(f'{directory}/*.json')
    results = []

    for file_path in file_paths:
        result = {"filepath": file_path}
        try:
            with open(file_path, 'r',encoding='utf-8') as f:
                data = json.load(f)
            # 'title' と 'summary' キーの存在と内容をチェック
            if 'title' not in data or not data['title']:
                result["error"] = "'title' キーが不足しているか空です"
            elif 'summary' not in data or not data['summary']:
                result["error"] = "'summary' キーが不足しているか空です"
            else:
                result["error"] = None  # エラーがない場合
        except json.JSONDecodeError:
            result["error"] = "JSONファイルが不正です"
        except Exception as e:
            result["error"] = f'読み込み中にエラーが発生しました: {e}'

        if result['error']:
            results.append(result)

    return results

# 使用例
directory = VOICE_DIR
result = check_json_files(directory)
print(result)
print("-------------------------")
err_cnt = 0
for r  in result:
    if r['error'] != None:
        print("ERROR:" ,r)
        err_cnt += 1
if err_cnt:
    print("エラーがあります:",err_cnt)
else:
    print("すべてのJSONデータに問題ありません。:",err_cnt)
