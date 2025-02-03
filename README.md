# Talana Attendance Bot with Python and Selenium

This repository contains a Python-based scraper bot that uses Selenium to automate the process of marking attendance on [Talana](https://peru.talana.com/es/remuneraciones/), a platform for managing employee attendance. The bot automates check-ins and check-outs by interacting with the Talana web interface, simulating user actions for attendance logging.

Additionally, the bot integrates with AWS S3 for storing screenshots captured when errors occur during the attendance marking process. These screenshots serve as a valuable tool for troubleshooting and identifying issues. The bot also uses AWS SNS to send real-time alerts whenever an error happens, including the path to the S3 screenshot for further investigation and resolution.

## Usage

### 1. Clone the Repository

To get started, clone the repository:

```bash
git clone https://github.com/cbecerrae/talana-scraper-bot.git
```

### 2. Build the Docker Image

Once cloned, navigate to the repository folder and build the Docker image:

```bash
docker build . -t talana_scraper_bot
```

> It is **strongly recommended** to run the scraper bot in a Docker container rather than directly with Python to ensure proper environment setup and avoid dependency issues.

### 3. Set Environment Variables

Before running the bot, you need to create an `.env` file and fill in the required values:

```env
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
S3_BUCKET_NAME=""
SNS_TOPIC_ARN=""
AWS_REGION=""
```

You will need the AWS credentials of an IAM user, an S3 bucket, and an SNS topic. The IAM user should have `s3:PutObject` permission for the S3 bucket and `sns:Publish` permission for the SNS topic. Don't forget to specify the AWS region where the S3 bucket and SNS topic were created.

### 4. Run the Bot

To run the bot, use the following command with the appropriate flags for the `--type`, `--email`, and `--password`:

```bash
docker run --rm --env-file .env talana_scraper_bot --type <'In' or 'Out'> --email <user email> --password <user password>
```

#### Input Parameters

- `--type`: Specifies the attendance type (`'In'` for check-in, `'Out'` for check-out).
- `--email`: Specifies the user email for login authentication.
- `--password`: Specifies the user password for login authentication.

## GitHub Packages

[![Build and Push Docker Image to GitHub Container Registry](https://github.com/cbecerrae/talana-scraper-bot/actions/workflows/docker-build-and-push.yml/badge.svg)](https://github.com/cbecerrae/talana-scraper-bot/actions/workflows/docker-build-and-push.yml)

Alternatively, you can download the latest container image directly from GitHub Packages and run the bot without needing to build it manually. Use the following command to pull the latest Docker image:

```bash
docker pull ghcr.io/cbecerrae/talana-scraper-bot:latest
```

Then, proceed with running the bot starting from **Step 3** by setting the necessary environment variables. This method can save time and ensure you are using the most up-to-date version of the bot.