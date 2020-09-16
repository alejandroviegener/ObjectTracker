FROM python:3.8-slim

# Define working directory
WORKDIR /usr/src/app

# Install libs requiered by open cv
RUN apt-get update && apt-get install -y \
        libgl1-mesa-dev \
        libglib2.0-0

# Copy requirements file
COPY requirements.txt ./

# Install requirements and make in/out directory
RUN pip install --no-cache-dir -r requirements.txt && \
        mkdir in_out

# Copy to working directoty
COPY . .

# Give permissions to execute
RUN chmod +x test.sh

# Define entry and cmd
ENTRYPOINT [ "python", "tracker.py" ]
CMD [ "--help" ]
