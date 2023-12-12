from v2txt import v2txt_sum
import glob
from dotenv import load_dotenv
import os

load_dotenv()
VOICE_DIR = os.environ.get("VOICE_DIR")  # 'get' メソッドを使用

flist = glob.glob(f"{VOICE_DIR}/*.mp3")

for file in flist:
    print(file)
    v2txt_sum(file)
