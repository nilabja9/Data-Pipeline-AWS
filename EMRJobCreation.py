import boto3
import awscred
import datetime

client = boto3.client('emr', aws_access_key_id = awscred.accesskey,
                      aws_secret_access_key = awscred.accesssecret, region_name ='us-east-1')

s3_bucket = 'nilabjascripts'
s3_key = 'sparkprocess_v2.py'
s3_URI = 's3://{a}/{b}'.format(a=s3_bucket, b=s3_key)

if __name__ == '__main__':
    currentDT = datetime.datetime.now()
    myformat = currentDT.strftime("%Y-%m-%d-%H-%M-%S")
    jobname = "TwitterAnalysisCluster" + myformat

    response = client.run_job_flow(
    Name = jobname,
    LogUri = 's3://nilabjaemrlogs',
    ReleaseLabel = 'emr-5.20.0',
    Instances = {
        'MasterInstanceType': 'm4.large',
        'SlaveInstanceType': 'm4.large',
        'InstanceCount': 2,
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False
    },
    Applications = [
        {
            'Name': 'Spark'
        }
    ],
    BootstrapActions= [
        {
            'Name': 'Maximize Spark Default Config',
            'ScriptBootstrapAction': {
                'Path': 's3://nilabjascripts/maximizeconfig.sh'
            }

        }
    ],
    Steps = [
        {
            'Name': 'Setup Debugging',
            'ActionOnFailure': 'TERMINATE_CLUSTER',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['state-pusher-script']
            }

        },
        {
            'Name': 'setup - copy files',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['aws', 's3', 'cp', s3_URI, '/home/hadoop']
            }
        },
        {
            'Name': 'Run Spark',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep':{
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit', '/home/hadoop/sparkprocess_v2.py']
            }
        }
    ],
    VisibleToAllUsers= True,
    JobFlowRole= 'EMR_EC2_DefaultRole',
    ServiceRole= 'EMR_DefaultRole',
    ScaleDownBehavior= 'TERMINATE_AT_TASK_COMPLETION'
    )

    print(response)

