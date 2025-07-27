FROM ubuntu:20.04


RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../Pythoncode/functions.py .
COPY ../Website/app.py .

RUN pip3 install --no-cache-dir streamlit pandas

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]