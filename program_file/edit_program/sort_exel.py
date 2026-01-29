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
        file_path = os.path.join(analysis_directory_path, folder, 'analysis.xlsx')
        df = pd.read_excel(file_path)

        # 新しいデータフレームを作成
        new_df = pd.DataFrame()

        # 行ごとにループ
        for index, row in df.iterrows():
            # 初期のスコアを設定
            row_score = 0
            cell_no = 0
            me_mass = 0
            unme_mass = 0
            total_score = 0
            ans_score = 0

            # 最初のセルを取得
            first_cell = str(row.iloc[0])

            # 処理をスキップする条件
            excluded_items = ["excluded", "位置1"]
            if first_cell in excluded_items:
                # 行の最後にスコアを追加
                new_row = row.tolist() + [-1]
                new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)    

            else:
                # 行ごとにループ(実質セルごと)
                for col_index, value in enumerate(row):
                    # セルの値を文字列に変換
                    cell_values = str(value)

                    # セルごとにループ
                    for cell_value in cell_values:
                        # cell_noに+1
                        cell_no += 1
                        
                        # ●と○でスコアを産出
                        if cell_value == "●":
                            # 二進数の様にカウント一列目は2^0
                            row_score += 2 ** cell_no
                            me_mass += 1
                        else:
                            row_score += 0
                            unme_mass += 1
                    
                    total_mass = me_mass + unme_mass

                    # スコアに質量の影響を追加
                    total_score = 2 ** total_mass * me_mass
                    ans_score = row_score + total_score
                
                # 行の最後にスコアを追加
                new_row = row.tolist() + [ans_score]
                new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)    

        if new_df.empty:
            print(folder, "のデータフレームは空です")
        else:
            # スコアをもとにデータフレームを並べ替え
            sorted_df = new_df.sort_values(by=new_df.columns[-1], ascending=False).reset_index(drop=True)
            #最後の列を削除する
            sorted_df = sorted_df.drop(sorted_df.columns[-1], axis=1)
            #ヘッダーを再度作成
            sorted_df.columns = [f"位置{i+1}" for i in range(sorted_df.shape[1])]
            #変更を保存
            sorted_df.to_excel(file_path, index=False, engine='openpyxl')
            print(folder, "のエクセルファイルを並べ替えました")