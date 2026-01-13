"""
lizzyさんに頼まれたプログラム
qumaの三つ目によって出力されるtsvファイルの特定の行を抽出してcsvファイルとして保存していく
"""
import os
import csv

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

tsv_files = get_specific_files_recursively('output_file3.tsv')

output_file = "./output/merged_output.csv" # 出力CSVファイル名
start_line = 14                   # 抽出開始行（1始まり）
end_line = 22                     # 抽出終了行（1始まり）

# tsvファイルを処理して指定行をcsvに書き込む関数
def process_tsv_file(file_path, writer):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 行数チェック
        if len(lines) < end_line:
            print(f"⚠ {file_path} は行数が足りないためスキップしました")
            continue

        # 1行目にfile_pathを書き込み
        writer.writerow([file_path])
        # 指定範囲の行を抽出
        selected_lines = lines[start_line-1:end_line]

        # TSVをCSVに変換して書き込み
        for line in selected_lines:
            row = line.strip().split("\t")
            writer.writerow(row)
        # 区切りの空行を挿入
        writer.writerow([])

# リスト内のtsvファイルから行を抽出してcsvファイルに書き込むメイン処理
def process_tsv_files():
    # 出力ファイルをUTF-8で開く
    with open(output_file, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.writer(out_csv)
        # 各ファイルを処理
        for file_path in tsv_files:
            try:
                # ファイルを処理
                process_tsv_file(file_path, writer)
            except Exception as e:
                print(f"❌ {file_path} の処理中にエラー: {e}")


# 参照するtsvファイルが存在すれば実行、なければエラーログを残して終了
if not tsv_files:
    print("エラー：参照するtsvファイルが見つかりませんでした。")
else:
    process_tsv_files()
    print(f"処理が完了しました。出力ファイル: {output_file}")
    