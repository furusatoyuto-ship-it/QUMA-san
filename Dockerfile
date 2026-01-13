# OSの指定
FROM ubuntu:22.04

# 作業ディレクトリを設定
WORKDIR /QUMA

# ファイルをコピー
COPY . /QUMA

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \ 
    wget \ 
    perl \ 
    emboss \ 
    build-essential \ 
    cpanminus \  
    && apt-get clean


#miniconda3をインストール
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh

# インストールスクリプトを実行
RUN bash /tmp/miniconda.sh -b -p /opt/miniconda

# パスを設定
ENV PATH="/opt/miniconda/bin:$PATH"

# Condaを初期化
RUN /opt/miniconda/bin/conda init bash

#解析に必要なツールbiopython&conda をインストール
RUN conda config --set channel_priority strict && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda update -n base -c defaults conda -y && \
    conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y biopython && \
    conda install -y blast && \
    conda clean --all -y

# pandasとopenpyxlをインストール
RUN pip install pandas openpyxl

# 必要なPerlモジュールをインストール
RUN cpanm Statistics::Lite

# QUMAのソースコードをダウンロードして展開
ADD http://quma.cdb.riken.jp/files/quma_cui-1.0.0.tar.gz /QUMA/quma_cui-1.0.0.tar.gz
RUN tar -xzf /QUMA/quma_cui-1.0.0.tar.gz -C /opt && rm /QUMA/quma_cui-1.0.0.tar.gz

# コンテナ起動時に実行するコマンドを指定
CMD ["tail", "-f", "/dev/null"]

