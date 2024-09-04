# Use an official Python runtime as a parent image
FROM python:3.12.4-slim
# Set the working directory in the container to /app
COPY . /app
WORKDIR /app
# Add the current directory contents into the container at /app
ADD . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -q -U google-generativeai &&\
    apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt install tesseract-ocr-vie &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["fastapi", "run", "api/app.py", "--port", "80"]