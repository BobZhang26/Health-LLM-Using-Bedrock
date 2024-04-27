# Use an existing Docker image with Python as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

RUN pip install --upgrade pip

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container at /app
COPY . .

# Configure AWS environment variables
ENV AWS_ACCESS_KEY_ID=AKIAYEHRFYABVQY7CXMA
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_DEFAULT_REGION=us-east-1

# Expose port 8501 to the outside world. This is the port Streamlit runs on the container
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
