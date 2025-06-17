# Base image
FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    fonts-liberation libnss3 libxss1 libappindicator3-1 \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libu2f-udev \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🔄 Download the matching ChromeDriver version (137)
RUN CHROME_VERSION=$(chromium --version | grep -oP '\d+\.\d+\.\d+') && \
    echo "Installing ChromeDriver for Chromium version $CHROME_VERSION" && \
    wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Set working dir and copy files
WORKDIR /app
COPY . .

# Default command
CMD ["python", "test.py"]
