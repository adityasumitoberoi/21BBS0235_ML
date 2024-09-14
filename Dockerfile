
FROM python:3.9-slim


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV TF_ENABLE_ONEDNN_OPTS=0


CMD ["python", "app.py"]
