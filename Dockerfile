# Use the official Python 3.10 image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code to the working directory, excluding files in .dockerignore
COPY . .

# Expose the port on which the Streamlit app will run
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
