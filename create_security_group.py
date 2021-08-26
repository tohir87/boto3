#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')
security_group = ec2.create_security_group(
		Description = 'Public access group',
		GroupName = 'public-access',
		DryRun = True)	
print (security_group)
