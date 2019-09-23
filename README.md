Dockerで実験環境を管理する

## [リソースの管理(Memory, CPUs, and GPUs)](https://docs.docker.com/config/containers/resource_constraints/)
Dockerコンテナを起動するときのオプションで、コンテナ(アプリケーション)が使用できるリソースに
制限をかけることができます。内部的にはCgroupsによって動作しています。
### Memory
Host上のメモリをコンテナが食い尽くし、Out of Memoryを引き起こすことを未然に防ぐために以下の方法を試します。
コマンドでは数字＋単位(e.g. `b`,`k`,`m`,`g`)で容量を指定します。

* **コンテナのメモリ使用量制限**  
`-m` or `--memory=` e.g. `--memory="4g"` (4GBのメモリ制限)
* **スワップ領域**  
`--memory-swap`
ディスクに退避できる容量の大きさを指定する。  
--memoryコマンドと併用され、例えば`--memory="300m"`および`--memory-swap="1g"`としたときコンテナは300MBのメモリ、
700MB(1GB-300MB)のスワップ領域を使えることになる。もしswapを指定しなかった場合、コンテナはメモリ容量の２倍のスワップ領域をデフォルトで使用する。

### CPUs
デフォルトでコンテナのCPU利用は制限されていません。
DockerのCPUオプションを使って、ハードにCPUリソースを管理できます。
* **CPU利用量の制限**  
`--cpus=<value>` e.g. `--cpus="1.5"` (CPU1個半)
* **特定のCPUを利用する**  
`--cpuset-cpus` e.g. `--cpuset-cpus="0-3"` (1~4番目のCPU), `--cpuset-cpus="1,3"` (2, 4番目のCPU)

### GPUs
NVIDIA-CONTAINER-RUNTIMEがインストールされていることが前提。
`apt-get install nvidia-container-runtime`でインストールできる(PATHも忘れずに通す)。
* **GPU利用制限なし(all GPUs)**  
`docker run -it --rm --gpus all ubuntu nvidia-smi`
* **特定のGPUを利用**  
`docker run -it --rm --gpus device="0,2"`
#### CUDA images
nvidia-driverのversionが合っていれば、cuda toolkit不要でCUDAを各コンテナで個別に設定できる。
https://github.com/NVIDIA/nvidia-docker/wiki/CUDA
#### nvidia-smiについて
Dockerではコンテナ内部からHost側のプロセスを見ることができないため、`nvidia-smi`を叩けません。  
解決策は①Host側で叩くか、②runオプションで`--pid=host`を使うかの２つです。 
