# Dockerfile

FROM python:3.10-slim

# Install ffmpeg for audio extraction
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure cookies.txt is in the final image
COPY cookies.txt ./cookies.txt

# Set Cloud Run expected port
ENV PORT=8080

# Start the app
CMD ["python", "main.py"]
