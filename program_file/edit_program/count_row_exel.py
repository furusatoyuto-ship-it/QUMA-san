"""
行ごとにメチル化率を計算するプログラム
"""
import pandas as pd
import os

# 解析済みのファイルを取得
analysis_directory_path = './output'
# ディレクトリ内のすべてのフォルダーを取得
folders = [f for f in os.listdir(analysis_directory_path) if os.path.isdir(os.path.join(analysis_directory_path, f))]
# すべてのフォルダーでループさせる
for folder in folders:
    if not folder == "output_log":
        # 解析するディレクトリパスを指定
        file_path = ('./output/' + folder + '/analysis.xlsx')
        df = pd.read_excel(file_path, engine='openpyxl')
        # データフレームの行数を取得
        num_rows = len(df.rows)
        print("行の数:", num_rows)
        # データフレームの特定の行を取得（行インデックスを使用）
        for row_index in range(0, num_rows):
            if row_index < num_rows:
                row = df.iloc[:, row_index]
                # ○の数を数える
                target_U = "○"
                count_U = row.value_counts().get(target_U, 0)
                print("非メチル化数", count_U)
                # ●の数を数える
                target_M = "●"
                count_M = row.value_counts().get(target_M, 0)
                print("メチル化数", count_M)
                # excludedの数を数える
                target_excluded = "excluded"
                count_excluded = row.value_counts().get(target_excluded, 0)
                print("excluded数", count_excluded)
                # count_MUを計算し、メチル化率を求める
                count_MU = count_M + count_U
                methylation_rate = count_M / count_MU if count_MU != 0 else 0
                print("メチル化率", methylation_rate)
                # count_allを計算し、excluded率を求める
                count_all = count_M + count_U + count_excluded
                excluded_rate = count_excluded / count_all if count_all != 0 else 0
                print("excluded率", excluded_rate)
            else:
                print(f"行インデックス {row_index} は範囲外です。")

        # 変更をエクセルファイルに保存する
        df.to_excel(file_path, index=False)