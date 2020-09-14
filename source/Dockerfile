FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
        libgl1-mesa-dev \
        libglib2.0-0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "tracker.py" ]
CMD [ "--help" ]