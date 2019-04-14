#!/bin/bash
aws configure set aws_access_key_id XXXXXXXXXXXXXXXXXX
aws configure set aws_secret_access_key XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
aws configure set default.region us-east-1
aws emr create-cluster --name "MySparkTestCluster" --release-label emr-5.23.0 --applications Name=Spark --instance-type m4.large --instance-count 3 --steps Type=CUSTOM_JAR,Name="first",Jar="command-runner.jar",ActionOnFailure=CONTINUE,Args=["spark-submit","--deploy-mode","cluster","s3://nilabjascripts/sparkprocess_v2.py"] --use-default-roles --auto-terminate
