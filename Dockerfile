FROM ubuntu:20.04

ARG http_proxy
ARG https_proxy

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    TZ=Europe/Moscow

WORKDIR /usr/src/app

# Set locale and timezone in one RUN to reduce layers
RUN apt-get update && apt-get install -y locales tzdata \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

# Install all required packages in one RUN to reduce layers and update only once
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip xvfb apt-utils wget build-essential \
        libgl1-mesa-glx libgtk-3-dev bzip2 libxtst6 libgtk-3-0 \
        libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev \
        libcanberra-gtk-module libcanberra-gtk3-module \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src src
COPY *.py config.json ./
COPY pages/*.py pages/

# Download and install Firefox and Geckodriver in one RUN for efficiency
ARG FIREFOX_VERSION=122.0
ARG GK_VERSION=v0.34.0
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
    && rm -rf /opt/firefox \
    && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
    && rm /tmp/firefox.tar.bz2 \
    && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
    && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox \
    && wget --no-verbose -O /tmp/geckodriver.tar.gz http://github.com/mozilla/geckodriver/releases/download/$GK_VERSION/geckodriver-$GK_VERSION-linux64.tar.gz \
    && rm -rf /opt/geckodriver \
    && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
    && rm /tmp/geckodriver.tar.gz \
    && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
    && chmod 755 /opt/geckodriver-$GK_VERSION \
    && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

RUN mkdir -p log

CMD pytest -sv --metrics=${METRICS} --headless=true --no-header --capture=tee-sys --alluredir=/var/opt/allure-results