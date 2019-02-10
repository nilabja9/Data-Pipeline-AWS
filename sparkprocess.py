import findspark

findspark.init('/home/nilabja/spark-2.4.0-bin-hadoop2.7')

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import json
import boto3
import awscred



def main():
    conf = SparkConf().setAppName("first")
    sc = SparkContext(conf=conf)

    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", awscred.accesskey)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", awscred.accesssecret)
    config_dict = {"fs.s3n.awsAccessKeyId": awscred.accesskey, "fs.s3n.awsSecretAccessKey": awscred.accesssecret }
    bucket = "kinesisbucketnilabja"
    prefix = "nilutwitter2019/01/21/00/*"
    filename = "s3n://{}/{}".format(bucket, prefix)

    rdd = sc.hadoopFile(filename,
                        'org.apache.hadoop.mapred.TextInputFormat',
                        'org.apache.hadoop.io.Text',
                        'org.apache.hadoop.io.LongWritable',
                        conf=config_dict)

    spark = SparkSession.builder.appName("TweetAnalysis").config("spark.files.overwrite", "true").getOrCreate()

    df = spark.read.json(rdd.map(lambda x: x[1]))

    df.show()


if __name__=='__main__':
    main()





