FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "python", "src/wake_word.py" ]