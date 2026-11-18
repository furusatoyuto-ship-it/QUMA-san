import os
from datetime import datetime
import shutil
import pathlib as Path


def run(output_dir):
    # outputフォルダを作成する。すでに存在する場合は何もしない
    output_dir.mkdir(parents=True, exist_ok=True)

    # output_logフォルダ以外のファイル・フォルダを前回の解析結果として取得する
    existing_item = [item for item in output_dir.iterdir() if item.name != "output_log"]
    if not existing_item:
        print("前回の解析結果はありません。")
        return None

    # 現在時刻から保存先を作る
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    log_dir = output_dir / "output_log" / timestamp
    log_dir.mkdir(parents=True)


    # ファイルとフォルダをコピー
    for item in existing_item:
        destination = log_dir / item.name
        try:
            shutil.move(item,destination)
            print(f" {item} を移動しました。") 
        except Exception as e:
            print(f"エラー: {item} を移動できませんでした。理由: {e}")
    
    return log_dir

# 前回の解析結果を保存する
run(Path.Path("./output"))