import boto3

ec2 = boto3.client('ec2')
instance = ec2.start_instances(InstanceIds=["i-0e17ad1f5d932c99f"])
