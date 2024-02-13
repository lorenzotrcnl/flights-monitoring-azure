FROM --platform=linux/amd64 debian:stable-slim
WORKDIR /
USER root
RUN apt-get update
RUN apt-get install -y curl libicu-dev python3 python3-pip python3-venv postgresql postgresql-contrib
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN az bicep install
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
RUN sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/dotnetdev.list'
RUN apt-get update
RUN apt-get install azure-functions-core-tools-4