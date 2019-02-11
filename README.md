# Data-Pipeline-AWS
Creation of a Data Pipeline using AWS Services

The goal of this project is to create and end to end data pipeline
fetching unstructured JSON data from twitter at specific time intervals
and transforming them into readable, relational format 
for analytics and data visualization

For Data Ingestion, AWS Kinesis Firehose has been used which
delivers data in JSON format to AWS S3 bucket. At intervals
an EMR cluster is created to process the accumulated files
and the data is processed through Apache Spark for storage 
in AWS S3 again as csv ready for analytics.

The script "BuildFirehoseStream.py" helps to create a Kinesis
Firehose Delivery Stream with the help of Boto3 scripting.
Once created, with the help of "TwitterGrabData.py" script
data is written on to the Kinesis Firehose, which delivers 
JSON files to an S3 bucket.

Then with the help of "EMRJobCreation.py" script an EMR cluster
is spun up and the JSON files stored in S3 are processed and transformed into
relational format as csv files and stored in S3 bucket for further
analysis.

Currently I'm trying to automate the entire flow, with AWS Data Pipeline