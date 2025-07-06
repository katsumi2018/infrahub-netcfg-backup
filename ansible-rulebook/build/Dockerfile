FROM python:3.12-slim

# 非対話モード設定（apt-get などでプロンプトを抑制）
ENV DEBIAN_FRONTEND=noninteractive

# システムパッケージのインストール
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git \
       sshpass \
       curl \
       openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python パッケージのインストール
RUN pip install --no-cache-dir \
    ansible-core \
    ansible-rulebook \
    ansible-pylibssh \
    ansible \
    paramiko \
    infrahub-sdk

# Ansible コレクションをインストール
COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install \
    -r /tmp/requirements.yml \
    -p /usr/share/ansible/collections

# コンテナ起動時のデフォルト動作を設定、メインコマンドを ansible-rulebook に設定
ENTRYPOINT ["ansible-rulebook"]
CMD ["--help"]
