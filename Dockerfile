FROM python:3.7.10-buster

ENV FILE_DEPOSITORY_PORT 8000
ENV FILE_DEPOSITORY_PASSWORD weak-default-password

COPY __init__.py .

EXPOSE $FILE_DEPOSITORY_PORT

ENTRYPOINT python3 __init__.py