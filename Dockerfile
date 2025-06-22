FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.78/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
