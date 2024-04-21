FROM python:3.12-slim

ENV TZ=Asia/Makassar
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    --mount=type=bind,target=/app/requirements.txt,source=requirements.txt \
    pip install -r requirements.txt

COPY app app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
