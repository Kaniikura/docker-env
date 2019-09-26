# nvidia cudaイメージからビルドするとcuDNN関係でエラーが起きたので公式を利用
FROM tensorflow/tensorflow:2.0.0rc0-gpu-py3-jupyter

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

# "dockuser"という名前の非rootユーザーを作成
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

# その他もろもろのインストール
RUN pip install --user tensorboard \
    jupyter \
    opencv-python \
    scikit-learn \
    matplotlib \
    pandas

# 既に走っているnotebookセッションを止める
CMD jupyter notebook stop 8888; bash
