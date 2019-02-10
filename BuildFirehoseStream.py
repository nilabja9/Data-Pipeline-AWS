import boto3
import awscred

if __name__ == '__main__':
    client = boto3.client('firehose', aws_access_key_id = awscred.accesskey, aws_secret_access_key = awscred.accesssecret)

    response = client.create_delivery_stream(
        DeliveryStreamName = 'kinesisnilabja',
        DeliveryStreamType = 'DirectPut',
        S3DestinationConfiguration = {
            'RoleARN': 'arn:aws:iam::626027370572:role/firehose_delivery_role',
            'BucketARN': 'arn:aws:s3:::kinesisbucketnilabja',
            'Prefix': 'nilabjatwitter022019',
            'BufferingHints': {
                'SizeInMBs': 10,
                'IntervalInSeconds': 300
            }

        }
    )

    print(response)