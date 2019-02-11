#!/usr/bin/env bash
aws s3 cp s3://nilabjascripts/EMRJobCreation.py .
aws s3 cp s3://nilabjascripts/awscred.py .
python3 EMRJobCreation.py