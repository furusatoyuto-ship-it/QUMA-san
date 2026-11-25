import subprocess
from datetime import datetime
import sys
import pandas as pd

def run_programs():
    programs = [
        #前回の記録を行う
        ["python", "./program_file/analysis_program/log.py"],
        #QUMAを使い解析
        ["python", "./program_file/analysis_program/ans_all.py"],
        #メチル化を〇に置換
        ["python", "./program_file/MU_program/MUex_txt.py"],
        ["python", "./program_file/MU_program/MUex_xlsx.py"],
        #写真解析
        ["python", "./program_file/photo_program/stats.py"],
        #エクセルファイルを編集
        ["python", "./program_file/edit_program/sort_exel.py"],
        ["python", "./program_file/edit_program/summarize_data_file.py"],
        ["python", "./program_file/edit_program/processing_exel.py"],
        #エクセルファイルを一つにまとめる
        ["python", "./program_file/write_exel.py"],
        ["python", "./program_file/photo_program/write_exel_photo.py"],
        ["python", "./program_file/summarize_csv.py"]
    ]

    for program in programs:
        print(f"{program[1]} start")
        try:
            subprocess.run(program, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {program[1]}: {e}")
            sys.exit(1)  # エラーが発生した場合はプログラムを終了


def main():
    # 現在の時間を出力
    current_time_s = datetime.now()
    print("解析開始時間:", current_time_s)
    
    # 設定ファイルのパスを指定
    region_list = ["sample_reference"]
    print("解析する領域は" + str(region_list) + "です")
    setting_csv_path = "./setting.csv"

    for region in region_list:
        print(f"現在解析中の領域: {region}")
        # 設定ファイルのgenomicの配列名を対象領域に更新
        setting_df = pd.read_csv(setting_csv_path, header=None)
        setting_df.iloc[1, 1] = region
        setting_df.to_csv(setting_csv_path, header=False, index=False)

        # 1つの領域に対して解析を行う
        run_programs()

    # 解析完了時間を出力
    current_time_e = datetime.now()
    print("解析完了時間:", current_time_e)


    # 解析にかかった時間を計算
    elapsed_time = current_time_e - current_time_s
    print("解析にかかった時間:", elapsed_time)


# このファイルが直接実行された場合に限り、メイン処理を開始
if __name__ == "__main__":
    main()