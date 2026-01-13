"""
QUMAを解析するためのプログラム。
出力は全ての形式が出力される。
"""
import subprocess
import os
import pandas as pd
#import sys

"""
# merged.fastaファイルを取得する
merged_fasta_path = "./input/genomic/merged.fasta" # バイサルファイト処理前の配列

# BLASTを実行する関数
def run_blast(genome_files, query_file):
    genome_db_path = "./output/genome_db"
    if not os.path.exists(genome_db_path):
        subprocess.run(["makeblastdb", "-in", genome_files, "-dbtype", "nucl", "-out", genome_db_path])

    evalue_threshold = "100000"
    result = subprocess.run(
        ["blastn", "-query", query_file, "-db", genome_db_path, "-outfmt", "6", "-max_target_seqs", "1", "-evalue", evalue_threshold],
        capture_output=True, text=True
    )
    print("e-valueは", evalue_threshold)
    
    print("標準出力(stdout)")
    print(result.stdout)
    print("標準エラー(stderr)")
    print(result.stderr)
    print("終了コード(returncode)")
    print(result.returncode)

    best_score = -1
    best_genome = None
    
    for line in result.stdout.strip().split("\n"):
        cols = line.split("\t")
        print(cols)
        score = int(cols[11])  # bit score
        if score > best_score:
            best_score = score
            best_genome = cols[1]

    return best_genome
"""

# settingファイルのパスを指定
setting_file_path = './setting.xlsx'

# オプションデータを読み込む
df = pd.read_excel(setting_file_path)

# バイサルファイト処理前のファイル名を取得
b2_value = df.iloc[0, 1]
genomic_name = str(b2_value)
print("バイサルファイト処理前のファイルは" + genomic_name)

# 入力ファイルと出力ファイルを指定
genomic_data = "./input/genomic/" + genomic_name  # バイサルファイト処理前の配列
output_file_path = "./output/output_file.txt"

# bisulfiteフォルダを指定し、フォルダ内のすべてのfastaファイルを取得する
bisulfite_folder = "./input/bisulfite/"  # バイサルファイト処理後の配列
bisulfite_files = [os.path.join(bisulfite_folder, f) for f in os.listdir(bisulfite_folder) if f.endswith('.fasta')]

# オプションの値を取得
f_option = str(df.iloc[1, 1])
d_option = str(df.iloc[2, 1])
u_option = str(df.iloc[3, 1])
c_option = str(df.iloc[4, 1])
m_option = str(df.iloc[5, 1])
p_option = str(df.iloc[6, 1])

print("全ての出力形式で出力")
#print("-fオプションは" + f_option)
print("-dオプションは" + d_option)
print("-uオプションは" + u_option)
print("-cオプションは" + c_option)
print("-mオプションは" + m_option)
print("-pオプションは" + p_option)

# 実行するコマンドを作成する関数
def command_def(genomic_data_sample, bisulfite_data_sample):
    command_sample = [
        "/opt/quma_cui/quma.pl",
        "-g", genomic_data_sample,
        "-q", bisulfite_data_sample,
        "-f", str(mass),
        "-d", d_option,
        "-u", u_option,
        "-c", c_option,
        "-m", m_option,
        "-p", p_option,
    ]

    # ディレクトリnameを作成
    bisulfite_data_sample_split_1 = bisulfite_data_sample.split("/")
    bisulfite_data_sample_split_2 = bisulfite_data_sample_split_1[-1].split(".")
    new_directory_sample = bisulfite_data_sample_split_2[0]

    # 1つ下の階層に移動してフォルダを作って戻ってくる
    os.chdir("./output")
    if not os.path.exists(new_directory_sample):
        os.makedirs(new_directory_sample)
    os.chdir("..")

    # 2つ下の階層に移動してフォルダを作って戻ってくる
    os.chdir("./output")
    os.chdir("./" + new_directory_sample)
    if not os.path.exists("detail"):
        os.makedirs("detail")
    os.chdir("..")
    os.chdir("..")

    if str(mass) == "3" :
        # outputフォルダの中のそれぞれのデータごとのフォルダの中のoutput_file.txtを指定
        output_file_path_sample = ("./output/" + new_directory_sample + "/detail/output_file" + str(mass) + ".tsv")

    else:
        # outputフォルダの中のそれぞれのデータごとのフォルダの中のoutput_file.txtを指定
        output_file_path_sample = ("./output/" + new_directory_sample + "/detail/output_file" + str(mass) + ".txt")

    return command_sample, output_file_path_sample


# bisulfite_dataの数だけ繰り返す
for bisulfite_data in bisulfite_files:
    print("バイサルファイト処理後のファイルは" + bisulfite_data)
    #genomic_data = run_blast(merged_fasta_path, bisulfite_data)
    #genomic_data_path = "./input/genomic/" + "_".join(genomic_data.split("_")[:2]) + ".fasta"
    #print("バイサルファイト処理前のファイルは" + genomic_data)
    #print("パス名は" + genomic_data_path)
    #解析番号を付与
    #masss = [0, 1, 2, 3]
    masss = [3]
    for mass in masss:
        #command, output_file_path = command_def(genomic_data_path, bisulfite_data)
        command, output_file_path = command_def(genomic_data, bisulfite_data)


        # QUMAコマンドを実行し、出力をファイルにリダイレクト
        with open(output_file_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, check=True)
        
        #どのファイルのどの解析が終わったかをプリント
        print(f"analysis_complete {bisulfite_data}-{mass}")
    print("")