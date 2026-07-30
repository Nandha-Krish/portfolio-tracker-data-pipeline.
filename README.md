# Automated Financial Data Pipeline

An automated, serverless ETL data pipeline built on AWS to fetch daily financial market closing prices and automatically ingest them into an Amazon RDS MySQL relational database.

## Tech Stack
* **Language:** Python 3.12 (`urllib`, `pymysql`)
* **Compute:** AWS Lambda (Serverless)
* **Scheduler:** Amazon EventBridge (Cron trigger)
* **Database:** Amazon RDS (MySQL)
