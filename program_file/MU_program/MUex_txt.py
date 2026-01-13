"""
outputにあるすべてのディレクトリの"output_file3.tsv"を読み込みメチル化状態を○と●で出力する。
結果は"analysis.txt"に保存する。
"""

import pandas as pd
import os

# 解析済みのファイルを取得
analysis_directory_path = './output'

# ディレクトリ内のすべてのフォルダーを取得
folders = [f for f in os.listdir(analysis_directory_path) if os.path.isdir(os.path.join(analysis_directory_path, f))]

#すべてのフォルダーでループさせる
for folder in folders:

    if not folder == "output_log":



        #解析するディレクトリパスを指定
        file_path = ('./output/' + folder + '/detail/output_file3.tsv')
        #print(folder)

        # TSVファイルを読み込む（エンコーディングを指定）
        df = pd.read_csv(file_path, sep='\t', skiprows=24, encoding='utf-8')

        # 特定の列を抽出する（例：'methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch, -: gap)'という列）
        selected_column = df['methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch, -: gap)']

        # MとUの置換を定義
        old_char_M = "M"
        new_char_M = "●"
        old_char_U = "U"
        new_char_U = "○"


        # 上記で定義した文字を置換
        selected_column = selected_column.str.replace(old_char_M, new_char_M)
        selected_column = selected_column.str.replace(old_char_U, new_char_U)

        # データフレームに戻す
        df_selected = pd.DataFrame(selected_column)

        # 列名を変更する
        new_column_name = "メチル化パターン"
        df_selected.rename(columns={'methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch, -: gap)': new_column_name}, inplace=True)
        #print(df_selected)

        # 抽出した列を新しいTXTファイルに保存する（エンコーディングを指定）
        last_file_path = ('./output/' + folder + '/alalysis.txt')
        df_selected.to_csv(last_file_path, index=False, encoding='utf-8')