"""
data_fileを作成するプログラム
各バイサルファイトデータから必要なデータをまとめた表を作る
"""
import openpyxl
import pandas as pd
import os

#output_pathの設定
output_path = './output/data_file.xlsx'
#workbookの新規作成
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "リスト"

# 解析済みのファイルを取得
analysis_directory_path = './output'
# 除外するフォルダのセット
exclude_folders = {'output_log'}

# 特定のファイルを再帰的に取得していく
def get_specific_files_recursively(target_file_name):
    get_files = []
    for root, dirs, files in os.walk(analysis_directory_path):
        # 除外するフォルダをスキップ
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        # ファイルをリスト内に取得
        for file in files:
            if file == target_file_name:
                get_files.append(os.path.join(root, file))
    return get_files

excel_files = get_specific_files_recursively('analysis.xlsx')

# ファイル名でソート(番号順に処理)
excel_files.sort()

# すべてのフォルダーでループさせる
for file_path in excel_files:
    print(" ")
    df = pd.read_excel(file_path, engine='openpyxl')
    # データフレームの行数を取得
    num_rows, num_cols = df.shape
    print("行の数:", num_rows)
    print("列の数", num_cols)
    number = sheet.max_row + 2
    count_M = 0
    count_U = 0
    count_excluded = 0
    num_used = 0
    # データフレームの特定の行を取得（行インデックスを使用）
    for row_index in range(0, num_rows):
        if row_index < num_rows:
            row = df.iloc[row_index,:]
            # ●の数を数える
            target_M = "●"
            count_M += row.value_counts().get(target_M, 0)
            # ○の数を数える
            target_U = "○"
            count_U += row.value_counts().get(target_U, 0)
            # excludedの数を数える
            target_excluded = "excluded"
            count_excluded += row.value_counts().get(target_excluded, 0)
            if df.iloc[row_index,0] != "excluded":
                num_used += 1
        else:
            print(f"行インデックス {row_index} は範囲外です。")

    try:
        #メチル化対象を求める
        count__MU = count_M + count_U
        # メチル化率を求める
        if count__MU == 0:
            methylation_rate = 0
        else:
            methylation_rate = count_M / count__MU * 100
        # excluded率を求める
        excluded_rate = count_excluded / num_rows * 100

        #data_fileにデータを入れる
        sheet[f'B{number}'] = file_path
        sheet[f'B{number+1}'] = "データ数"
        sheet[f'B{number+2}'] = num_rows
        sheet[f'C{number+1}'] = "used数"
        sheet[f'C{number+2}'] = num_used
        sheet[f'D{number+1}'] = "excluded数"
        sheet[f'D{number+2}'] = count_excluded
        sheet[f'E{number+1}'] = "メチル化率"
        sheet[f'E{number+2}'] = f"{methylation_rate:.3f}"
        sheet[f'F{number+1}'] = "excluded率"        
        sheet[f'F{number+2}'] = f"{excluded_rate:.3f}"
        sheet[f'G{number+1}'] = "メチル化個数"
        sheet[f'G{number+2}'] = count_M
        sheet[f'H{number+1}'] = "非メチル化個数"
        sheet[f'H{number+2}'] = count_U
        sheet[f'I{number+1}'] = "メチル化対象数"
        sheet[f'I{number+2}'] = count__MU
    except Exception as e:
                print(f"❌ {file_path} の処理中にエラー: {e}")

#一番最初の列を消去
sheet.delete_rows(1)
#エクセルファイルを保存
wb.save(output_path)