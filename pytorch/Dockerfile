FROM nvidia/cuda:10.1-base-ubuntu16.04

# 主要なユーティリティをインストール
RUN apt-get update && apt-get install -y \
   curl \
   sudo \
   git \
   bzip2 \
   screen \
   libfontconfig1 \
   libxrender1 \
   libsm6 \
   libxext6 \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

# ワーク＆ホームディレクトリを作成
RUN mkdir /work /home/user
WORKDIR /work

# "dockuser"という名前の非rootユーザーを作成(Host側でのuid, gidは61000番)
ENV USERNAME "dockuser"
RUN groupadd -g 61000 ${USERNAME} \
   && useradd -g 61000 -l -M -s /bin/false -u 61000 ${USERNAME} \
   && echo "${USERNAME}:*" | chpasswd \
   && chown -R ${USERNAME}:${USERNAME} /work
# コンテナ内の全ユーザーのhomeディレクトリとして"/home/user"を設定
ENV HOME=/home/user
RUN chmod 777 /home/user
# ユーザーをスイッチ
USER ${USERNAME}

# Minicondaのインストール
RUN curl -so /home/user/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh \
   && chmod +x /home/user/miniconda.sh \
   && /home/user/miniconda.sh -b -p /home/user/miniconda \
   && rm /home/user/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Python 3.7 仮想環境
RUN conda create -y --name py37 python=3.7 \
   && conda clean -ya
ENV CONDA_DEFAULT_ENV=py37
ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
RUN conda install conda-build \
   && conda clean -ya

# CUDA 10.1 & pytorch=1.5.1、その他もろもろのインストール
RUN conda install -y -c pytorch \
   cudatoolkit=10.1 \
   pytorch=1.5.1 \
   torchvision \
   jupyter \
   && conda clean -ya \
   && pip install opencv-python \
   easydict \
   scikit-learn \
   matplotlib \
   pandas \
   pretrainedmodels \
   albumentations \
   tensorboardx \
