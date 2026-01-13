"""
input内のfastaファイルを一つのファイルに統合するプログラム
"""
import os

#merged.fastaがすでに存在するかを確認し、存在する場合は削除
merged_fasta_path = "./input/genomic/merged.fasta"
if os.path.exists(merged_fasta_path):
    print("merged.fastaがすでに存在します。")
    try:
        os.remove(merged_fasta_path)
        print("既存のmerged.fastaを削除しました。")
    except Exception as e:
        print("merged.fastaの削除中にエラーが発生しました:", e)

# ゲノムフォルダを指定し、フォルダ内のすべてのfastaファイルを取得する
genome_folder_path = "./input/genomic/" # バイサルファイト処理前の配列
genome_datas = [os.path.join(genome_folder_path, f) for f in os.listdir(genome_folder_path) if f.endswith('.fasta')]
print(genome_datas)

# 新しいfastaファイルを作成して追記
with open(merged_fasta_path, "a") as outfile:
    for genome_data in genome_datas:
        with open(genome_data, "r") as infile:
            outfile.write(infile.read() + "\n")