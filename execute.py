import subprocess
from datetime import datetime

# 現在の時間を出力
current_time_s = datetime.now()
print("解析開始時間:", current_time_s)


#プログラムを実行したい
#print("mergedfasta.py start")
#subprocess.run(["python","./program_file/analysis_program/mergedfasta.py"])


#前回の記録を行う
print("log.py start")
subprocess.run(["python","./program_file/analysis_program/log.py"])
#qumaを使い解析
print("ans_all.py start")
subprocess.run(["python","./program_file/analysis_program/ans_all.py"])

#メチル化を〇に置換
print("MUex_txt.py start")
subprocess.run(["python","./program_file/MU_program/MUex_txt.py"])
print("MUex_xlsx.py start")
subprocess.run(["python","./program_file/MU_program/MUex_xlsx.py"])

print("stats.py start")
subprocess.run(["python","./program_file/photo_program/stats.py"])

#エクセルファイルを編集
print("sort_exel.py start")
subprocess.run(["python","./program_file/edit_program/sort_exel.py"])
print("nanpo_exel.py start")
subprocess.run(["python","./program_file/edit_program/nanpo_exel.py"])
print("processing_exel.py start")
subprocess.run(["python","./program_file/edit_program/processing_exel.py"])

#エクセルファイルを一つにまとめる
print("write_exel.py start")
subprocess.run(["python","./program_file/write_exel.py"])
print("write_exel_photo.py start")
subprocess.run(["python","./program_file/photo_program/write_exel_photo.py"])
print("lizzy.py start")
subprocess.run(["python","./program_file/lizzy.py"])


# 現在の時間を出力
print("解析開始時間:", current_time_s)


# 現在の時間を出力
current_time_e = datetime.now()
print("解析完了時間:", current_time_e)


# 解析にかかった時間を計算
elapsed_time = current_time_e - current_time_s
print("解析にかかった時間:", elapsed_time)