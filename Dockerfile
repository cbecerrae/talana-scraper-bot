# Use the official Python 3.12 image (based on Debian Bullseye) as the base image
FROM python:3.12-bullseye

# Set the timezone to 'America/Lima' for the container environment
ENV TZ="America/Lima"

# Set the working directory inside the container to /app
WORKDIR /app

# Update the package list and install required packages:
# - xvfb: Virtual framebuffer for running GUI applications in headless mode
# - chromium: The Chromium web browser
# - chromium-driver: The WebDriver for Chromium used in browser automation (e.g., with Selenium)
# - tzdata: Timezone data, needed to set the proper timezone for the container
RUN apt-get update && apt-get install -y xvfb chromium chromium-driver tzdata

# Copy the requirements file from the local machine to the working directory in the container
COPY requirements.txt ./

# Install Python dependencies listed in the requirements file
RUN pip install -r requirements.txt

# Copy all other files from the local directory to the container's working directory
COPY . .

# Create an entrypoint script that runs the application using xvfb (virtual display environment)
# 'CONTAINER=1' sets an environment variable that can be checked by the Python app if needed
# 'xvfb-run' allows running graphical applications in a headless environment
# 'python -u -m' ensures the Python script runs in unbuffered mode
RUN echo 'CONTAINER=1 xvfb-run python -u -m app "$@"' > ./entrypoint

# Set the entrypoint of the container to run the script via bash
# The 'bash' command will run the 'entrypoint' script that was created above
ENTRYPOINT [ "bash", "entrypoint" ]
