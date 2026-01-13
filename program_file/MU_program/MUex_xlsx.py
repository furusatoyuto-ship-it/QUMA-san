"""
outputにあるすべてのディレクトリの"output_file3.tsv"を読み込みメチル化状態を○と●で出力する。
結果は"analysis.xlsx"に保存する。
"""
import pandas as pd
import os

# 解析済みのファイルを取得
analysis_directory_path = './output'

# ディレクトリ内のすべてのフォルダーを取得
folders = [f for f in os.listdir(analysis_directory_path) if os.path.isdir(os.path.join(analysis_directory_path, f))]

# すべてのフォルダーでループ
for folder in folders:

    if not folder == "output_log":


        # 解析するファイルパスを指定
        file_path = os.path.join(analysis_directory_path, folder, 'detail', 'output_file3.tsv')

        # ファイルが存在しない場合はスキップ
        if not os.path.exists(file_path):
            print(f"ファイルが見つかりません: {file_path}")
            continue

        print(f"処理中: {folder}")

        try:
            # TSVファイルを読み込む（エンコーディングを指定）
            df = pd.read_csv(file_path, sep='\t', skiprows=24, encoding='utf-8')

            # メチル化パターンの列を抽出
            column_name = 'methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch, -: gap)'
            if column_name not in df.columns:
                print(f"列が見つかりません: {column_name}")
                continue

            selected_column = df[column_name]

            # 置換処理（M → ●、U → ○、その他はそのまま）
            selected_column = selected_column.str.replace("M", "●")
            selected_column = selected_column.str.replace("U", "○")

            # 'excluded' を含む行は、そのまま1セルに保存し、それ以外は1文字ずつ分割
            processed_data = []
            for value in selected_column:
                if "excluded" in str(value):  # 'excluded' の場合
                    processed_data.append([value])  # 1セルだけ
                else:  # 通常のメチル化データの場合
                    processed_data.append(list(str(value)))  # 1文字ずつ分割

            # データフレーム化
            df_expanded = pd.DataFrame(processed_data)

            # 列名を "位置1", "位置2", ... のように設定
            df_expanded.columns = [f"位置{i+1}" for i in range(df_expanded.shape[1])]

            # 結果をExcelに保存
            output_file_path = os.path.join(analysis_directory_path, folder, 'analysis.xlsx')
            df_expanded.to_excel(output_file_path, index=False, engine='openpyxl')

        except Exception as e:
            print(f"エラーが発生しました ({folder}): {e}")