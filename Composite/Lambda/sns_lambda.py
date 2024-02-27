import boto3
import http.client
import json

def lambda_handler(event, context):
    # Parse the event
    booking_data = json.loads(event['body'])  # assuming the event body is JSON

    # Prepare the request to EC2 endpoint
    ec2_endpoint = 'ec2-3-144-93-114.us-east-2.compute.amazonaws.com'
    port = 8012
    url = '/bookings'
    headers = {'Content-type': 'application/json'}

    # Send an HTTP request to the EC2 endpoint
    connection = http.client.HTTPConnection(ec2_endpoint, port)
    connection.request('POST', url, json.dumps(booking_data), headers)

    response = connection.getresponse()

    if response.status == 200:
        # Read and parse the response from EC2
        response_data = response.read().decode()
        try:
            ec2_response_data = json.loads(response_data)
        except json.JSONDecodeError:
            # Handle the case where the response is not JSON
            connection.close()
            return {
                'statusCode': 500,
                'body': json.dumps('Invalid JSON from EC2')
            }

        # Extract email info or any other relevant detail

        # Send an email (using SNS or SES)
        sns_client = boto3.client('sns')
        snsArn = 'arn:aws:sns:us-east-1:321759190738:nestlyNotification'
        message = f"Dear host, Great news! We are thrilled to inform you that your property has been successfully booked through Nesty. Details: {ec2_response_data}"

        sns_response = sns_client.publish(
            TopicArn=snsArn,
            Message=message,
            Subject='New Booking Alert: Your Property has been Booked on Nesty!'
        )

        connection.close()
        return {
            'statusCode': 200,
            'body': json.dumps('Email sent successfully')
        }
    else:
        # Handle errors from EC2 request
        connection.close()
        return {
            'statusCode': response.status,
            'body': json.dumps('Error communicating with EC2')
        }