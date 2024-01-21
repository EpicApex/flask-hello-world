# Stage 1: Build stage ( reduce docker images layers - reduced size )
# problem here is we lose visability on the docker image build layers ( as it doesnt save the build layer ) 
FROM ubuntu:22.04 as builder

# Making sure that python stdout and stderr are sent to terminal without being buffered out.
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies
# decrease docker image with removing cached dir coming from pip "--no-cache-dir"
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY app.py .

# Stage 2: Run stage
FROM ubuntu:22.04

# Install Python (pip is not needed in this stage)
RUN apt-get update && apt-get install -y python3

# Copy built artifacts from the builder stage 
# Issue - using build stage and moving /usr/src/app inside the container didnt move the installed flask module. so i've moved all the /usr folder to include it.
COPY --from=builder /usr /usr

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the working directory
WORKDIR /usr/src/app

# Set the default command to execute the Flask app
CMD ["python3", "app.py"]
