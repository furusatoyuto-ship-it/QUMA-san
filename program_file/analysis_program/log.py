import os
from datetime import datetime
import shutil

# 現在の時間を出力
log_time = datetime.now()

# log_time_sを文字列に変換
log_time_str = log_time.strftime("%Y-%m-%d_%H-%M-%S")

# output_logに移動してフォルダを作って戻ってくる
output_log_folder = "./output/output_log/"
if not os.path.exists(output_log_folder):
    os.makedirs(output_log_folder)
log_time_dir = os.path.join(output_log_folder, log_time_str)
if not os.path.exists(log_time_dir):
    os.makedirs(log_time_dir)

# outputフォルダを指定し、フォルダ内のすべてのファイルを取得する
output_folder = "./output/"
output_files_and_folders = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f != "output_log"]

# ファイルとフォルダをコピー
for item in output_files_and_folders:
    destination = os.path.join(log_time_dir, os.path.basename(item))
    try:
        shutil.move(item,destination)
        print(f" {item} を移動しました。")
        
    except Exception as e:
        print(f"エラー: {item} を移動できませんでした。理由: {e}")