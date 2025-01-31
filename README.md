# Talana Attendance Bot with Python and Selenium

This repository contains a Python-based scraper bot that uses Selenium to automate the process of marking attendance on [Talana](https://peru.talana.com/es/remuneraciones/), a platform for managing employee attendance. The bot automates check-ins and check-outs by interacting with the Talana web interface, simulating user actions for attendance logging.

Additionally, the bot integrates with AWS S3 for storing screenshots captured when errors occur during the attendance marking process. These screenshots serve as a valuable tool for troubleshooting and identifying issues. The bot also uses AWS SNS to send real-time alerts whenever an error happens, including the path to the S3 screenshot for further investigation and resolution.

## Usage

### GitHub

To get started, clone the repository:

```bash
git clone https://github.com/cbecerrae/talana-scraper-bot.git
```

### Build Docker Image

Once cloned, navigate to the repository folder and build the Docker image:

```bash
docker build . -t talana_scraper_bot
```

### Environment Variables

Before running the bot, you need to edit the `.env` file and fill in the required values:

```env
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
SNS_TOPIC_ARN=""
S3_BUCKET_NAME=""
AWS_REGION=""
```

### Run the Bot

To run the bot, use the following command with the appropriate flags for the `--type`, `--email`, and `--password`:

```bash
docker run --rm --env-file .env talana_scraper_bot --type <'In' or 'Out'> --email <user email> --password <user password>
```

### Input Parameters

- `--type`: Specifies the attendance type (`'In'` for check-in, `'Out'` for check-out).
- `--email`: Specifies the user email for login authentication.
- `--password`: Specifies the user password for login authentication.

## Important Notes

It is **strongly recommended** to run the scraper bot in a Docker container rather than directly with Python to ensure proper environment setup and avoid dependency issues.
