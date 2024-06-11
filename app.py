import boto3
import hashlib
import psycopg2
from psycopg2 import sql
import json

# Constants
QUEUE_URL = "http://localhost:4566/000000000000/login-queue"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
AWS_REGION = "us-east-1"  # You can use any valid AWS region

# Initialize SQS client
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name=AWS_REGION)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
cursor = conn.cursor()

# Function to mask PII
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Function to process messages
def process_messages():
    response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10)
    messages = response.get('Messages', [])
    
    for message in messages:
        data = json.loads(message['Body'])
        
        user_id = data['user_id']
        device_type = data['device_type']
        masked_ip = mask_pii(data['ip'])
        masked_device_id = mask_pii(data['device_id'])
        locale = data['locale']
        app_version = data['app_version']
        create_date = data['create_date']
        
        cursor.execute(sql.SQL("""
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """), [user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date])
        
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])
    
    conn.commit()

if __name__ == "_main_":
    process_messages()
    cursor.close()
    conn.close()