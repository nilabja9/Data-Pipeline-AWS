#!/bin/bash
# Configures spark-default.conf for dedicate/maximum cluster use
#   Set num executors to number to total instance count at time of creation (spark.executor.instances)
#   Set vcores per executor to be all the vcores for the instance type of the core nodes (spark.executor.cores)
#   Set the memory per executor to the max available for the node (spark.executor.memory)
#   Set the default parallelism to the total number of cores available across all nodes at time of cluster creation  (spark.default.parallelism)
#
# Limitations:
#   Assumes a homogenous cluster (all core and task instance groups the same instance type)
#   Is not dynamic with cluster resices
#
set -x
#
#determine the current region and place into REGION
EC2AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
REGION="`echo \"$EC2AZ\" | sed -e 's:\([0-9][0-9]*\)[a-z]*\$:\\1:'`"


if [ "$SparkS3SupportingFilesPath" == "" ]
then
       if [ "$REGION" == "eu-central-1" ]
       then
               SparkS3SupportingFilesPath=s3://eu-central-1.support.elasticmapreduce/spark
       else
               SparkS3SupportingFilesPath=s3://support.elasticmapreduce/spark
       fi
fi
SparkS3SupportingFilesPath=${SparkS3SupportingFilesPath%/}

VCOREREFERENCE="$SparkS3SupportingFilesPath/vcorereference.tsv"
CONFIGURESPARK="$SparkS3SupportingFilesPath/configure-spark.bash"
#
echo "Configuring Spark default configuration to the max memory and vcore setting given configured number of cores nodes at cluster creation"

#Set the default yarn min allocation to 256 to allow for most optimum memory use
/usr/share/aws/emr/scripts/configure-hadoop -y yarn.scheduler.minimum-allocation-mb=256

#Gather core node count
NUM_NODES=$(grep /mnt/var/lib/info/job-flow.json -e "instanceCount" | sed 's/.*instanceCount.*:.\([0-9]*\).*/\1/g')
NUM_NODES=$(expr $NUM_NODES - 1)

if [ $NUM_NODES -lt 2 ]
then
	#set back to default to be safe
	NUM_NODES=2
fi

SLAVE_INSTANCE_TYPE=$(grep /mnt/var/lib/info/job-flow.json -e "slaveInstanceType" | cut -d'"' -f4 | sed  's/\s\+//g')

if [ "$SLAVE_INSTANCE_TYPE" == "" ]
then
	SLAVE_INSTANCE_TYPE="m3.xlarge"
fi

hadoop fs -get $VCOREREFERENCE

if [ ! -e "vcorereference.tsv" ]
then
	echo "Reference file vcorereference.tsv not available, failing quietly."
	exit 0
fi

NUM_VCORES=$(grep vcorereference.tsv -e $SLAVE_INSTANCE_TYPE | cut -f2)

MAX_YARN_MEMORY=$(grep /home/hadoop/conf/yarn-site.xml -e "yarn\.scheduler\.maximum-allocation-mb" | sed 's/.*<value>\(.*\).*<\/value>.*/\1/g')

EXEC_MEMORY=$(echo "($MAX_YARN_MEMORY - 1024 - 384) - ($MAX_YARN_MEMORY - 1024 - 384) * 0.07 " | bc | cut -d'.' -f1)
EXEC_MEMORY+="M"

PARALLEL=$(expr $NUM_VCORES \* $NUM_NODES)

#--- Now use configure-spark.bash to set values

hadoop fs -get $CONFIGURESPARK

bash configure-spark.bash spark.executor.instances=$NUM_NODES spark.executor.cores=$NUM_VCORES spark.executor.memory=$EXEC_MEMORY

if [ $PARALLEL -gt 2 ]
then
	#only set/change this if it looks reasonable
	bash configure-spark.bash spark.default.parallelism=$PARALLEL
fi