# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose Gradio's default port
EXPOSE 7860

# Tell Gradio to listen on all network interfaces so Render can route traffic
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Command to launch the app
CMD ["python", "app.py"]