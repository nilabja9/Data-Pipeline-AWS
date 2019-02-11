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

Work in Progress