FROM debian:12

RUN apt update && \
	apt install -y \
		python3-aiohttp \
		python3-tomlkit

WORKDIR /srv/proxmox/auto-install-server

RUN chmod 700 /srv/proxmox/auto-install-server

RUN mkdir /srv/proxmox/auto-install-server/config

COPY --chmod=755 server.py /srv/proxmox/auto-install-server/server.py

CMD ["/srv/proxmox/auto-install-server/server.py"]
