FROM ubuntu:16.04


RUN apt-get update
 
RUN apt-get install -y language-pack-ko
 
# set locale ko_KR
RUN locale-gen ko_KR.UTF-8
 
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8
 
RUN apt-get install -y \
        python3 \
        python3-pip
 

# Install production dependencies.
RUN pip3 install Flask gunicorn
RUN pip3 install beautifulsoup4==4.8.2
RUN pip3 install selenium==3.141.0

# install chrome
RUN apt-get -y update
RUN apt-get install -yqq unzip curl
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get -y update
RUN apt-get install --allow-unauthenticated -y google-chrome-stable 
# install chormedirver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


CMD /bin/bash
