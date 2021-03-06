# Creation of a Batch-Input Data Pipeline using AWS Services

## Objective
The goal of this project is to create and end to end data pipeline
fetching unstructured JSON data from twitter at specific time intervals
and transforming them into readable, relational format 
for analytics and data visualization

## Solution and Architecture

### This has two parts 
#### Ingestion and Storage

For Data Ingestion, a Kinesis Data Firehose is created with Boto3 API. The python application calls twitter API to fetch tweets on a particular topic. The tweets are written into the firehose, which delivers them into S3 in specific buffer time intervals.
![CollectionIngestion](https://user-images.githubusercontent.com/35825748/56085637-3bf45e80-5e0c-11e9-9475-41d9805f59df.JPG)

#### Processing
For processing we have used AWS Glue - which will crawl the S3 bucket for unstructured data schema and then create a job mapping the JSON nodes into relational targets and save the data in S3 in parquet/csv format.
![Processing](https://user-images.githubusercontent.com/35825748/56085638-3eef4f00-5e0c-11e9-878d-13042b9d47af.JPG)

#### Alternative Processing
An alternative way of processing would be to run a spark application using a EMR cluster. The Spark application could be run from any local system using AWS CLI, specifying steps - and schedule cluster termination once the job is completed. The same can be automated by running the Command Line Script by AWS Data Pipeline.

## Process and End Result
The Script Ingestion.py contains the code for creating the Kinesis Firehose, fetch twitter data and write into the same. After this has been done for a certain period of time, the Kinesis Firehose is terminated. A Glue crawler is setup which crawls the S3 bucket and determines schema on its own. After this process is complete - we create a job, map input and output, and execute the same.Glue transforms the JSON files into CSV and stores them in S3.

Mapping:-
![GlueMapping](https://user-images.githubusercontent.com/35825748/56086222-8deeb180-5e17-11e9-965e-0006e32dcab3.JPG)

CSV Output:-
![ExcelOutput](https://user-images.githubusercontent.com/35825748/56086221-8deeb180-5e17-11e9-8123-2ab904a94d57.JPG)

If you would like a detailed process review please follow the youtube links:
https://www.youtube.com/watch?v=JDy3QWVz8Ws&t=49s  

https://www.youtube.com/watch?v=jkO9wdpHt4w&t=534s

Alternative Process:

An EMR cluster can be spun up with the script - EMRJobcreation.py(using boto3) or by using cli_bash.sh


