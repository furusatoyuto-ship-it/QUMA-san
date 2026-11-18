# QUMAsan

QUMAのコマンドライン版をDocker内で実行し、バイサルファイト配列のメチル化解析からExcel・CSVへの集計までを行うプログラム群です。B6・JF1それぞれの参照配列を使い分け、メチル化状態を `●`（メチル化）・`○`（非メチル化）で出力します。

## フォルダ構成

```text
QUMAsan/
├── Dockerfile                      # 解析環境の構築
├── Docker導入方法~QUMA編~.docx       # Docker導入の補足資料
├── execute.py                      # 解析・集計を順番に実行
├── Preparatory.py                  # FASTQの前処理（利用前に調整が必要）
├── setting.csv                     # 解析設定
├── input/
│   ├── genomic/                    # バイサルファイト処理前の参照配列
│   │   ├── sample_reference_B6.fasta
│   │   └── sample_reference_JF1.fasta
│   └── bisulfite/                  # 解析するバイサルファイト配列
│       ├── TAG001_sample_reference_B6.fasta
│       └── TAG001_sample_reference_JF1.fasta
└── program_file/
    ├── analysis_program/           # 過去の結果の退避・QUMA実行
    ├── MU_program/                 # メチル化状態を記号に変換
    ├── edit_program/               # Excelの並べ替え・集計・数式追加
    ├── photo_program/              # 表示用Excel作成・統合
    ├── write_exel.py               # サンプルごとの解析Excelを統合
    └── lizzy.py                    # QUMAの要約行をCSVに抽出
```

`output/` は解析開始時に自動作成されます。同梱のFASTAは、動作確認用の人工配列です。

## 実行環境

Dockerをインストールし、起動しておいてください。WindowsではDocker DesktopでLinuxコンテナを利用できる環境を用意します。

DockerfileはUbuntu 22.04をベースに、Miniconda、Biopython、pandas、openpyxl、PerlとStatistics::Lite、EMBOSS、BLAST、FASTQ関連ツール（fastq-tools・fqgrep・seqtk・PEAR）、QUMA CUI 1.0.0を導入します。イメージの作成にはインターネット接続が必要です。

補足資料は [Docker導入方法~QUMA編~.docx](Docker導入方法~QUMA編~.docx) を参照してください。入力・設定・実行方法は、現在の実装に合わせた以下の説明を使用してください。

## 初回のセットアップ

### 1. QUMAsanフォルダへ移動し、イメージを作成

WindowsのPowerShellでの例です。パスは実際の保存場所に合わせて変更してください。

```powershell
cd QUMAsan
docker build -t quma .
```

### 2. 作業フォルダを共有してコンテナを作成

PowerShellでは、QUMAsanフォルダで次のコマンドを実行します。

```powershell
docker run -d --name quma --mount "type=bind,source=$($PWD.Path),target=/QUMA" quma
```

macOS・Linuxのターミナルでは、同じフォルダで次のコマンドを使用します。

```bash
docker run -d --name quma --mount "type=bind,source=$(pwd),target=/QUMA" quma
```

ホスト側のQUMAsanフォルダがコンテナ内の `/QUMA` と共有されるため、入力・設定の変更と解析結果をホスト側から確認できます。以下の操作にはコンテナ名 `quma` を使います。

## 入力データと設定

### 入力ファイル

1. `input/genomic/` に参照配列をFASTA形式で置きます。
2. `input/bisulfite/` に解析対象の配列をFASTA形式で置きます。
3. `execute.py` 内の `region_list` を解析対象の領域名に合わせます。

同梱データの場合は、次の設定で実行できます。

```python
region_list = ["sample_reference"]
```

領域名に拡張子や `_B6`・`_JF1` は付けません。参照配列は `<領域名>_B6.fasta` と `<領域名>_JF1.fasta` の名前で用意します。

解析対象ファイルは、名前に領域名を含み、末尾が `B6.fasta` または `JF1.fasta` になるようにしてください。例えば `TAG001_sample_reference_B6.fasta` は `sample_reference_B6.fasta` と対応します。拡張子は小文字の `.fasta` を使用してください。

現在の処理では、領域名をファイル名の部分一致で抽出し、末尾でB6・JF1を判定します。領域名が互いに重複する名前や、対応する末尾のないファイルは避けてください。出力フォルダ名は最初の `.` より前の部分になるため、ファイル名の途中に `.` を含めないでください。また、この名前をExcelのシート名にも使うため、31文字以内に収め、`[]:*?/\` は使わないでください。

### setting.csv

設定は `setting.csv` の2列目（`input` 列）を編集します。プログラムは行の位置で値を読み取るため、ヘッダー・行順・列構成を維持し、UTF-8のCSVとして保存してください。

| 項目 | 現在の値 | 実装での扱い |
| --- | --- | --- |
| genomicの配列名 | `sample_reference` | 実行時に `region_list` の各領域名で上書き |
| 出力オプション | `3` | 現在は設定値によらず要約形式 `-f 3` のみ出力 |
| ゲノム配列の変換方法 | `2` | `-d` に渡す値。CSVの説明では両方向を検索 |
| 未変換のCpHの上限 | `6` | `-u` に渡す値 |
| 変換されたCpHの上限（CSV上の表記） | `90` | `-c` に渡す値 |
| アライメントのミスマッチの上限 | `10` | `-m` に渡す値 |
| アライメントのミスマッチの下限（CSV上の表記） | `85` | `-p` に渡す値 |
| genomicの配列名1・2 | `sample_reference_B6.fasta` / `sample_reference_JF1.fasta` | 現在の解析処理では未使用 |

項目名はCSVの表記に合わせています。QUMAの各オプションの厳密な意味は、コンテナ内の `/opt/quma_cui/` に展開されるQUMAの付属資料で確認してください。参照配列名は、CSV末尾の配列名1・2ではなく、領域名と `_B6.fasta`・`_JF1.fasta` から自動生成されます。

## 解析の実行

入力と設定を準備したら、ホスト側のターミナルから実行します。

```powershell
docker exec -w /QUMA quma python execute.py
```

コンテナ内で操作する場合は、次のように実行します。

```bash
docker exec -it -w /QUMA quma /bin/bash
python execute.py
exit
```

相対パスを使用しているため、Pythonスクリプトは `/QUMA` を作業ディレクトリとして実行してください。

`execute.py` は次の順序で処理します。

1. 前回の解析結果を `output/output_log/<日時>/` へ移動。
2. 対象領域・アレルに対応する参照配列でQUMAを実行。
3. メチル化状態を `●`・`○` に変換し、テキスト・Excelを作成。
4. 表示用Excel、並べ替え、集計、数式追加を実行。
5. 解析Excel・表示用Excelをそれぞれ統合し、要約CSVを作成。

複数領域を処理する場合は、例えば `region_list = ["regionA", "regionB"]` とします。退避処理は領域ごとに実行されるため、`output/` 直下には最後の領域の結果が残り、それ以前の領域の結果は `output/output_log/` に移動します。`setting.csv` の領域名も最後に処理した値になります。

### 結果の保存先

```text
output/
├── <入力ファイル名から拡張子を除いた名前>/
│   ├── detail/output_file3.tsv     # QUMAの要約出力
│   ├── analysis.txt                # メチル化状態を記号に変換したデータ
│   ├── analysis.xlsx               # 記号化・並べ替え・数式追加後のデータ
│   └── photo.xlsx                  # メチル化パターンの表示用Excel
├── analysis_all_data.xlsx          # サンプル別のanalysis.xlsxをシートに統合
├── data_file.xlsx                  # データ数・メチル化率などの集計
├── photo_data.xlsx                 # サンプル別のphoto.xlsxをシートに統合
├── merged_output.csv               # 各要約TSVの14～18行目を抽出
└── output_log/
    └── <日時>/                     # 前回までの解析結果
```

`photo.xlsx` は画像ファイルではなく、メチル化位置のセルを黒く塗ったExcelファイルです。有効なデータがない場合などは、一部の成果物が作成されないことがあります。

## 終了と2回目以降の実行

作業後にコンテナを停止します。

```powershell
docker stop quma
```

次回はDockerを起動し、既存のコンテナを開始してから解析します。

```powershell
docker start quma
docker exec -w /QUMA quma python execute.py
```

入力データ・設定・Pythonスクリプトの変更は共有フォルダ経由で反映されます。Dockerfileや導入パッケージを変更した場合は、イメージの再ビルドとコンテナの再作成が必要です。

## Preparatory.pyについて

`Preparatory.py` はNGSデータの前処理用スクリプトです。`pre/` 内の `.gz` の解凍、PEARによるペアエンドリードのマージ、`fastq-grep` による配列抽出、seqtkによるFASTA変換を行います。`execute.py` からは呼び出されません。

現在のファイルは、利用するデータに合わせた編集が必要です。

- `pre/` は同梱されていません。利用する場合は作成し、入力の `.gz` を配置してください。
- サンプル番号は11～36、入力名は `TAG11_S11_L001_R1_001.fastq` などに固定されています。
- 抽出する配列と領域名は、IG・H19・SnrpnのB6/JF1用に固定されています。
- マージ結果を `pre/fastq/TAG<i>.fq` に改名した後、抽出処理は作業ディレクトリ直下の `TAG<i>.assembled.fastq` を参照しており、パスと名前が一致していません。実行前に修正してください。
- FASTA変換結果は作業ディレクトリ直下に出力されます。QUMA解析に利用する際は、`input/bisulfite/` に配置し、対応する参照配列と `region_list` を用意してください。

既にFASTA形式の解析対象配列がある場合は、前処理を実行せず、`input/` に配置して解析できます。

## 困ったとき

- コンテナの状態は `docker ps -a` で確認できます。停止していれば `docker start quma` で起動します。
- コンテナ作成時に名前の重複が出る場合は、既存の `quma` コンテナを確認してください。2回目以降は `docker run` ではなく `docker start` を使います。
- 入力が処理されない場合は、`region_list`、ファイル名に含まれる領域名、`B6.fasta`・`JF1.fasta` の末尾、参照配列の配置を確認してください。
- `execute.py` は、呼び出したプログラムがエラー終了するとそこで停止します。一部の子スクリプトはエラーを表示して処理を続けるため、完了時刻だけでなく、実行ログと出力ファイルも確認してください。
- 再実行すると既存の結果は退避されます。過去の結果は `output/output_log/` を確認してください。
