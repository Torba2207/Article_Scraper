FROM python:3.11-slim

WORKDIR /code

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends

# Detect architecture and install appropriate Chrome/ChromeDriver
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then \
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
        apt-get update && apt-get install -y google-chrome-stable --no-install-recommends && \
        wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.78/linux64/chromedriver-linux64.zip && \
        unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
        rm /tmp/chromedriver.zip; \
    elif [ "$arch" = "aarch64" ]; then \
        echo "Installing Chromium for ARM64 instead of Chrome..." && \
        apt-get update && apt-get install -y chromium chromium-driver --no-install-recommends; \
    fi


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app


RUN arch=$(uname -m) && \
    if [ "$arch" = "aarch64" ]; then \
        sed -i 's/webdriver.Chrome/webdriver.chromium.Chrome/g' /code/app/services/scraper.py || true; \
    fi

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]