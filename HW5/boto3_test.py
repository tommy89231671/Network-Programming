# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 01:05:35 2019

@author: tommy
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:28:07 2019

@author: tommy
"""
import boto3
import time

ec2 = boto3.resource('ec2')
th=ec2.instances("i-04ae2115c47a20248")

user_data="""#!/bin/bash
/home/ubuntu/anaconda3/bin/python3 /home/ubuntu/app_server.py 0.0.0.0 22222
"""

ec2 = boto3.resource('ec2')
ec2.instances.filter(InstanceIds="i-05b88085d4a2bb33c").terminate()
a=ec2.create_instances(
    BlockDeviceMappings=[
      {
          'DeviceName':"/dev/sda1",
          'Ebs':{
              'DeleteOnTermination':True,
	      #'SnapshotId':'snap-07a5307a919c1486b'	
          }
      }
    ],
    ImageId='ami-075ffa341f20cef5e', 
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
	    'Groups': ["sg-0bf4d9509f30873e7"],
            
            'SubnetId': 'subnet-d9690ff7'
        }
    ],
    MinCount=1, 
    MaxCount=1,
    KeyName='ec2_key',
    
    InstanceType="t2.micro",

    UserData=user_data
)


iid=a[0].instance_id
#print(iid)
time.sleep(3)
b=ec2.Instance(iid)
time.sleep(10)


#print(b.public_ip_address)
#running_instances = ec2.instances.

#response = ec2.describe_instances(InstanceId=a['InstanceId'])
#print(response.get())
#ec2.terminate_instances(InstanceId=a['InstanceId'])

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 01:05:35 2019

@author: tommy
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:28:07 2019

@author: tommy
"""
import boto3
import time

user_data="""#!/bin/bash
/home/ubuntu/apache-activemq-5.15.8/bin/activemq start
/home/ubuntu/anaconda3/bin/python3 /home/ubuntu/login_server.py 0.0.0.0 22222
"""

ec2 = boto3.resource('ec2')
#ec2.instances.filter(InstanceIds="i-05b88085d4a2bb33c").terminate()
a=ec2.create_instances(
    BlockDeviceMappings=[
      {
          'DeviceName':"/dev/sda1",
          'Ebs':{
              'DeleteOnTermination':True,
	      #'SnapshotId':'snap-07a5307a919c1486b'	
          }
      }
    ],
    ImageId='ami-0dfb3c1fd8de54ac4', 
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
	    'Groups': ["sg-0bf4d9509f30873e7"],
            
            'SubnetId': 'subnet-d9690ff7'
        }
    ],
    MinCount=1, 
    MaxCount=1,
    KeyName='ec2_key',
    
    InstanceType="t2.micro",

    UserData=user_data
)


iid=a[0].instance_id
#print(iid)
#time.sleep(3)
b=ec2.Instance(iid)
#time.sleep(10)


#print(b.public_ip_address)
#running_instances = ec2.instances.

#response = ec2.describe_instances(InstanceId=a['InstanceId'])
#print(response.get())
#ec2.terminate_instances(InstanceId=a['InstanceId'])





