FROM ubuntu:noble

ENV PYTHONPATH "${PYTHONPATH}:/jg_webtext"

WORKDIR /jg_webtext

COPY requirements.txt requirements.txt

RUN : \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install \
	-y \
	--no-install-recommends \
	python3-pip=24.0+dfsg-1ubuntu1.1 \
	vim \
	&& pip install -r requirements.txt --break-system-packages \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

COPY . /jg_webtext

# Spot to save out data
VOLUME /outputs /outputs


CMD ["tail", "-F", "anything"]
#CMD ["python3", "-u", "analysis.py"]
#CMD python3 -u scrape_ops/scheduler.py

