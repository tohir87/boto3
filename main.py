#!/usr/bin/env python3

import subprocess
import boto3
import sys
from botocore.exceptions import ClientError

def createAndCheckSecurityGroup():
	ec2 = boto3.resource('ec2')
	# response = ec2.describe_vpcs()
	# vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
	try:

		response = ec2.create_security_group(
			Description = 'Public access group',
			GroupName = 'public-access2')

		security_group_id = response['id']
		print('Secirity group created successfully: %s', security_group_id)
		print(response)
		exit(0)

		rules = ec2.authorize_security_group_ingress(
			GroupId=security_group_id,
			IpPermissions=[
				{'IpProtocol': 'tcp',
				'FromPort': 80,
				'ToPort': 80,
				'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
				{'IpProtocol': 'tcp',
				'FromPort': 22,
				'ToPort': 22,
				'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
			])
		print('Secuirty rules successfully set %s' % rules)
		return security_group_id

	except ClientError as e:
		print(e)

def createInstance(security_group_id):
	print('Initiate instance creation in %s security group', security_group_id)
	try:
		
		ec2 = boto3.resource('ec2')
		instance = ec2.create_instances(
			ImageId = 'ami-0bdb1d6c15a40392c',
			MinCount = 1,
			MaxCount = 1,
			InstanceType = 't2.micro')	
		print (instance[0].id)
	except:
		print("Unexpected error has occured while creating a resource:", sys.exc_info()[0])

def InstallApachePhp():
	try:
		# Check if apache is running
		cmd = 'ps -A | grep apache2'
		subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	except subprocess.CalledProcessError:
		print("Apache and PHP is currently not installed, Installing apache2 ...")
		try:
			install_cmd = 'apt-get install apache2'
			subprocess.run(install_cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except subprocess.CalledProcessError:
			print("Unable to install apache2")

def createBucket():
	s3 = boto3.resource("s3")
	for bucket_name in sys.argv[1:] :
		try:
			response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
			print (response)
		except Exception as error:
			print (error)



# Define a main() function.
def main():
    security_group_id = createAndCheckSecurityGroup()
    # createInstance(security_group_id)
	# getSshKey()
	# InstallApachePhp()
	# createBucket()
	# putHtmlFile()
	# DisplayIPAddress()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()