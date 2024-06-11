# Fetch Rewards ETL

## Overview

This project reads JSON data from an AWS SQS Queue, masks PII fields, and writes the transformed data to a Postgres database.

## Setup

1. Install Docker and Docker Compose.
2. Run the following command to start the environment:

    ```sh
    docker-compose up
    ```

3. Execute the ETL application:

    ```sh
    docker build -t fetch_rewards_etl .
    docker run --network="host" fetch_rewards_etl
    ```

## Implementation Details

- **Reading Messages**: The application reads messages from an AWS SQS Queue using boto3.
- **Masking PII**: The `device_id` and `ip` fields are masked using SHA-256 hashing.
- **Writing to Postgres**: The transformed data is written to a Postgres database using psycopg2.

## Future Improvements

- **Error Handling**: Add comprehensive error handling and logging.
- **Batch Processing**: Implement batch processing to handle larger volumes of data.
- **CI/CD Pipeline**: Set up a CI/CD pipeline for automated testing and deployment.

## Questions

1. **Production Deployment**: I would deploy this application using a managed container orchestration service like AWS ECS or Kubernetes.
2. **Additional Components**: Add monitoring, logging, and alerting for better observability and maintenance.
3. **Scaling**: Use message batching and parallel processing to handle a growing dataset.
4. **PII Recovery**: Store the original PII data in a secure and encrypted data store.
5. **Assumptions**: Assumed the input data schema is consistent and that AWS SQS and PostgreSQL services are reliable.
