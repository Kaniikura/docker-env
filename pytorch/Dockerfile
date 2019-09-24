FROM nvidia/cuda:10.0-base-ubuntu16.04

# 主要なユーティリティをインストール
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    bzip2 \
    libfontconfig1 \
    libxrender1 \
    libsm6 \
    libxext6

# ワークディレクトリを作成
RUN mkdir /work
WORKDIR /work

# "user"という名前の非rootユーザーを作成しスイッチする
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /work
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# コンテナ内の全ユーザーのhomeディレクトリとして"/home/user"を設定
ENV HOME=/home/user
RUN chmod 777 /home/user

# Minicondaのインストール
RUN curl -so ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Python 3.6 仮想環境
RUN /home/user/miniconda/bin/conda create -y --name py36 python=3.6.9 \
 && /home/user/miniconda/bin/conda clean -ya
ENV CONDA_DEFAULT_ENV=py36
ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
RUN /home/user/miniconda/bin/conda install conda-build=3.18.9=py36_3 \
 && /home/user/miniconda/bin/conda clean -ya

# CUDA 10.0 & pytorch、その他もろもろのインストール
RUN conda install -y -c pytorch \
    cudatoolkit=10.0 \
    "pytorch=1.2.0=py3.6_cuda10.0.130_cudnn7.6.2_0" \
    "torchvision=0.4.0=py36_cu100" \
    jupyter \
 && conda clean -ya
 
RUN pip install opencv-python \
    scikit-learn \
    matplotlib
