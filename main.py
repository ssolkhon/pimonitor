#!/usr/bin/env python3

import boto3
import botocore
import logging
import time
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_aws_client(access_key_id, secret_access_key, region, service):
    logging.debug("Creating AWS client for service: %s in region %s",
                  service, region)
    return boto3.client(
        service,
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )


def send_cloudwatch_metric(client, namespace, metric_name, value, dimensions):
    logging.debug("Sending metric to CloudWatch")
    try:
      response = client.put_metric_data(
          Namespace=namespace,
          MetricData=[
              {
                  'MetricName': metric_name,
                  'Value': value,
                  'Dimensions': dimensions
              },
          ]
      )
      if response['ResponseMetadata']['HTTPStatusCode'] == 200:
          logging.info("Successfully sent metric to CloudWatch")
          return True
      else:
          logging.error("Failed to send metric to CloudWatch")
          return False
    
    except botocore.exceptions.ClientError as e:
        msg = f"Client Error: {e}"
        logging.error(msg)
        return False
    
    except botocore.exceptions.EndpointConnectionError as e:
        msg = f"AWS Connection Error: {e}"
        logging.error(msg)
        return False
    
    except botocore.exceptions.NoCredentialsError as e:
        msg = f"AWS credentials not found: {e}"
        logging.error(msg)
        return False


def run(client):
    logging.info("Starting pimonitor heartbeat")
    try:
        while True:
            send_cloudwatch_metric(client, 'pimonitor',
                                   'Heartbeat', 1,
                                   [{'Name': 'Instance',
                                    'Value': 'RaspberryPi'}])
            time.sleep(60)
    except KeyboardInterrupt:
        client.close()
        logging.info("Stopping pimonitor heartbeat")


if __name__ == '__main__':
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    client = get_aws_client(aws_access_key_id, aws_secret_access_key,
                            'eu-west-2', 'cloudwatch')

    run(client)
