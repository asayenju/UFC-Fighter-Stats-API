# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR C:\Users\ashwi\UFC-Fighter-Stats-API\ufc_fighter_stats

# Copy the requirements.txt file into the container
COPY ufc_fighter_stats/requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=ufc_fighter_stats/api/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
