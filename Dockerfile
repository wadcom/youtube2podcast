# vim: set ft=Dockerfile:
FROM alpine:3.5

RUN \
	apk add --update ca-certificates python3 gcc python3-dev libxml2-dev musl-dev \
        libxslt-dev ffmpeg && \
	pip3 install --upgrade pip && \
	pip3 install feedparser feedgen pytube && \
	mkdir -p /y2p/output

COPY [              \
    "convert.py",   \
    "/y2p/"         \
]

WORKDIR /y2p

ENTRYPOINT  [ "/y2p/convert.py" ]
