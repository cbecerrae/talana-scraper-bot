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
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
SNS_TOPIC_ARN=
AWS_REGION=
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

Alternatively, you can download the latest container image directly from [**GitHub Packages**](https://github.com/cbecerrae/talana-scraper-bot/pkgs/container/talana-scraper-bot) and run the bot without needing to build it manually. Use the following commands to pull the latest Docker image:

```bash
docker login ghcr.io

docker pull ghcr.io/cbecerrae/talana-scraper-bot:latest
```

Then, proceed with running the bot starting from **Step 3** by setting the necessary environment variables. This method can save time and ensure you are using the most up-to-date version of the bot.

## GitHub Actions

[![Build and Push Docker Image](https://github.com/cbecerrae/talana-scraper-bot/actions/workflows/docker-build-and-push.yml/badge.svg)](https://github.com/cbecerrae/talana-scraper-bot/actions/workflows/docker-build-and-push.yml)

In the [`.github/workflows/docker-build-and-push.yml`](.github/workflows/docker-build-and-push.yml) file, you'll find the "Build and Push Docker Image" workflow, which implements CI/CD for changes pushed to the `main` branch, excluding updates to markdown files (`.md`) or GitHub Actions files within `.github/`. This workflow can also be triggered manually and has a concurrency limit of 1, with in-progress jobs being canceled if a new job is triggered. 

The CI/CD pipeline consists of a `build` job that builds the Docker image and stores it as an artifact. This artifact is then passed to the `push-ghcr` and `push-ecr` jobs. These jobs depend on the successful completion of the `build` job. Once the build job finishes, the push jobs download the artifact, tag it as ***latest***, log in to both the GitHub Container Registry and Amazon Elastic Container Registry (ECR), and push the image to these registries.

You can disable this workflow, but if you have forked this repository and want to use it, configure the following repository secrets in GitHub Secrets:
- **AWS_ACCESS_KEY_ID**: AWS access key.
- **AWS_SECRET_ACCESS_KEY**: AWS secret access key.
- **ECR_REPOSITORY_URI**: Amazon ECR repository URI.