FROM debian:12

ENV DEFAULT_ANSWER_FILE_PATH=/config/default.toml
ENV ANSWER_FILE_DIR=/config/answers

RUN apt-get update && \
	apt-get install -y \
		python3-aiohttp \
		python3-tomlkit \
	&& \
	apt-get clean

WORKDIR /auto-install-server

RUN chmod 700 /auto-install-server

RUN mkdir /config

COPY --chmod=755 server.py /auto-install-server/server.py

CMD ["/auto-install-server/server.py"]
