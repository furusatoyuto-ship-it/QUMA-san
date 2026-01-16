これはメチル化解析ツールQUMAを動かすためのDocker環境を作成する為のDockerfileとプログラム群です。
Dockerの導入方法やDockerfileの解説、ビルドのオプションに関してはQUMAファイル上にある"Docker導入方法~QUMA編~.docx"を参考にしてください。

Dockerをインストールし起動されたPC(windowsではWSL)にての説明を行う。
windowsではコマンドプロンプト、macではターミナルを開いて以下の手順を行う。
これらのターミナルに$以降のコマンドを実行する。($はその行の以降がコマンドであることを示す)


初回の設定方法

#cdを使いこのファイル(QUMA)が存在するディレクトリまで移動する。

$cd user


#DockerfileからDockerimageを作成

$docker build -t quma .


#DockerimageからDockercontenaを作成

$docker run -d -v $(pwd):/QUMA --name quma quma


#実行中のコンテナを検索

$docker ps

C:\Users\user\docker\QUMA>docker ps
CONTAINER ID   IMAGE     COMMAND               CREATED      STATUS          PORTS     NAMES
eca84de8f9fb   quma      "tail -f /dev/null"   3 days ago   Up 17 seconds             quma

#コンテナとターミナル(CMD)を同機させる

$docker exec -it <container_id> /bin/bash

<container_id>にはeca84de8f9fbなどを入れるこれはすべて異なるIDであるので注意


#QUMAの実行
inputに解析したいファイルを正しく置く。
setting.xlsxに解析オプションなどを設定する。

$python execute.py

#コンテナの終了
メモリなどを使用しパソコンが重くなる可能性があるためDockerdesktopを開きContainersを開きコンテナqumaのActionsの■をクリックする。



二回目以降の設定方法

#コンテナの起動
Dockerdesktopを開きContainersを開く。
すでにできているコンテナqumaのActionsの▶をクリックしてコンテナを起動させる。
■となっている場合は何もする必要はない。

#実行中のコンテナを検索

$docker ps

C:\Users\user\docker\QUMA>docker ps
CONTAINER ID   IMAGE     COMMAND               CREATED      STATUS          PORTS     NAMES
eca84de8f9fb   quma      "tail -f /dev/null"   3 days ago   Up 17 seconds             quma

#コンテナとターミナル(CMD)を同機させる

$docker exec -it <container_id> /bin/bash

<container_id>にはeca84de8f9fbなどを入れるこれはすべて異なるIDであるので注意


#QUMAの実行
inputに解析したいファイルを正しく置く。
setting.xlsxに解析オプションなどを設定する。

$python execute.py



