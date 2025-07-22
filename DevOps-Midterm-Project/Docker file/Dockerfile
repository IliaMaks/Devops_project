
FROM ubuntu:20.04


RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install streamlit pandas


WORKDIR /app

COPY ../Website/app.py .
COPY ../Pythoncode/functions.py .


EXPOSE 8501


CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]