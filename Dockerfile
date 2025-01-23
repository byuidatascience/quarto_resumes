FROM python:3.9.6-slim
EXPOSE 8888
WORKDIR /app
COPY . .

VOLUME /mnt/src

RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libcairo2 libcairo2-dev libpangocairo-1.0-0 weasyprint && \
    apt clean && \
    rm -rf /var/cache/apt/*

RUN set -e -x && \
    apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    pandoc-citeproc \
    curl \
    gdebi-core \
    librsvg2-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG QUARTO_VERSION="1.5.56"
ARG QUARTO_VERSION
RUN set -e -x && \
  curl -o quarto-${QUARTO_VERSION}-linux-arm64.deb -L https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-arm64.deb \
  && gdebi --non-interactive quarto-${QUARTO_VERSION}-linux-arm64.deb \
  && rm -f quarto-${QUARTO_VERSION}-linux-arm64.deb    


RUN apt-get update && apt-get install -y build-essential libc6-dev bash
RUN python3 -m pip install jupyter
RUN pip install --upgrade pip ipython ipykernel
RUN ipython kernel install --name "python3" --user
RUN pip3 install -r requirements.txt

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
