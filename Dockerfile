# syntax = docker/dockerfile:1.2
FROM python:3.8
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib64:/usr/local/nvidia/bin
COPY .cog/tmp/build3376673403/cog-0.0.1.dev-py3-none-any.whl /tmp/cog-0.0.1.dev-py3-none-any.whl
RUN --mount=type=cache,target=/root/.cache/pip pip install /tmp/cog-0.0.1.dev-py3-none-any.whl
RUN --mount=type=cache,target=/var/cache/apt apt-get update -qq && apt-get install -qqy tmux wget curl nano less && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip pip install   torch==1.12.1 torchaudio==0.12.1 rdkit==2022.3.5 openbabel-wheel==3.1.1.5 biopython==1.79 biopandas==0.4.1 pot==0.8.2 dgl==0.9.0 joblib==1.1.0 pyaml==21.10.1 icecream==2.1.3 matplotlib==3.5.3 tensorboard==2.10.0 psutil==5.9.2 dgllife==0.3.0
RUN echo env is ready!
WORKDIR /src
EXPOSE 5000
CMD ["python", "-m", "cog.server.http"]
COPY . /src
