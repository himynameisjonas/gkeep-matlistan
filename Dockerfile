FROM python:3.11-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

COPY sync.py ./

CMD [ "python", "./sync.py" ]
