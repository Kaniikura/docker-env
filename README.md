## How to use
1. **jupyter notebookのパスワード取得**    
`python generate_token.py --password <設定したいパスワード>`を実行し出力されたトークンをメモしておく。  
2. **docker imageのビルド**(※ 汎用イメージ(pytorch1.5.1、 tf2.3)は作成済なので、オリジナルのイメージを作りたい人のみ)  
使用したい環境の方に入ります(`cd tf2` or `cd pytorch`)  
vimなどでDockerfileの編集。  
`sudo docker build . -t <イメージ名>`でビルド。
3. **コンテナの起動**  
`sudo docker run -it --user $UID -d -v $(pwd):/work/share -p <ポート番号>:8888 --rm --ipc=host --memory="32g" --memory-swap="-1" --cpus="8." --gpus="0,1" <イメージID> `
4. **リモートマシンからjupyter notebookに接続**  
`sudo docker exec -it <コンテナのID> /bin/bash`でコンテナに入る。  
`jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.password=<設定したトークン>`  
で起動。「Ctrl + p」 -> 「Ctrl + q」でコンテナから抜ける。    
ローカルマシンからnotebookにアクセス。
5. **コンテナの削除**  
`sudo docker stop <コンテナのID>`で停止。  
`--rm`オプションを付けずに起動した場合、stopしても再起動可能な状態で残るので`docker rm`コマンドで後始末します。  
消し忘れが多いと`docker container ls -a`を打ったときにお化けコンテナが大量に現れたりするので注意。

## テスト
作成したDockerイメージが、GPUを利用した機械学習に対応するかテストするときは、
```bash
sudo docker run -it -d -v <このdocker-envディレクトリへのPATH>:/work/share -u `id -u $USER` --rm --gpus="2" <イメージID>
sudo docker exec -it <コンテナID> /bin/bash/
```
の後、コンテナの中で
```bash
python share/tests/pytorch_test.py #tfは'tensorflow_test.py' (tf2.0以上が必要)
````
でMNISTを例とした動作が確認できます。(GPUが利用できない場合はエラーで止まります)

  
## 以下参考
runコマンドのオプション説明  
`-it` コンテナの標準出力をshellにつなぐ  
`-d` 起動後にデタッチ    
`-v <Host上のマウントしたいディレクトリ>:<コンテナの場所>` コンテナでHost上のファイルを触れるようにする。この場所以外に保存したデータは、コンテナを削除したとき一緒に消えてしまいます。  
`-u` 指定したユーザーでコマンドを実行する、マウントしたvolumeの権限周りで問題が起きたときは``-u `id -u $USER` ``で解決するやり方もある。  
`--rm` コンテナをstopした時に自動で削除  

<イメージID>は`docker images`、<コンテナID>は`docker ps`コマンドでそれぞれ確認できます。

### [リソースの管理(Memory, CPUs, and GPUs)](https://docs.docker.com/config/containers/resource_constraints/)
Dockerコンテナを起動するときのオプションで、コンテナ(アプリケーション)が使用できるリソースに
制限をかけることができます。内部的にはCgroupsによって動作しています。
#### Memory
Host上のメモリをコンテナが食い尽くし、Out of Memoryを引き起こすことを未然に防ぐために以下の方法を試します。
コマンドでは数字＋単位(e.g. `b`,`k`,`m`,`g`)で容量を指定します。

* **コンテナのメモリ使用量制限**  
`-m` or `--memory=` e.g. `--memory="4g"` (4GBのメモリ制限)
* **スワップ領域**  
`--memory-swap`
ディスクに退避できる容量の大きさを指定する。  
--memoryコマンドと併用され、例えば`--memory="300m"`および`--memory-swap="1g"`としたときコンテナは300MBのメモリ、
700MB(1GB-300MB)のスワップ領域を使えることになる。もしswapを指定しなかった場合、コンテナはメモリ容量の２倍のスワップ領域をデフォルトで使用する。

#### CPUs
デフォルトでコンテナのCPU利用は制限されていません。
DockerのCPUオプションを使って、ソフトorハードにCPUリソースを管理できます。
* **CPU利用量の制限**  
`--cpus=<value>` e.g. `--cpus="1.5"` (CPU1個半)
* **特定のCPUを利用する**  
`--cpuset-cpus` e.g. `--cpuset-cpus="0-3"` (1~4番目のCPU), `--cpuset-cpus="1,3"` (2, 4番目のCPU)

#### GPUs
NVIDIA-CONTAINER-RUNTIMEがインストールされていることが前提。
`apt-get install nvidia-container-runtime`でインストールできる(PATHも忘れずに通す)。
* **GPU利用制限なし(all GPUs)**  
`docker run -it --rm --gpus all ubuntu nvidia-smi`
* **特定のGPUを利用**  
`docker run -it --rm --gpus device="0,2"`
##### CUDA images
nvidia-driverのversionが合っていれば、cuda toolkit不要でCUDAを各コンテナで個別に設定できる。
https://github.com/NVIDIA/nvidia-docker/wiki/CUDA
##### nvidia-smiについて
Dockerではコンテナ内部からHost側のプロセスを見ることができないため、`nvidia-smi`を叩けません。  
解決策は①Host側で叩くか、②runオプションで`--pid=host`を使うかの２つです。 
