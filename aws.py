from bottle import route, run,hook, response,request
from bottle import post, get, put, delete, error
import boto3
import json
import logging
s3=boto3.client('s3')
ec2 = boto3.client('ec2')
iam = boto3.client('iam')

######################################CORS POLICY ERROR SOLUTION#######################################
_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return
	
	
######################################CORS POLICY ERROR SOLUTION #######################################	



#####################################ERROR CODE HANDLING SECTION####################################
@error(404)
def error404(error):
    return '<h1> gharpe ja na shane<h1>'

@error(405)
def error405(error):
    return '<h1> gharpe ja na shane <h1>'


#####################################ERROR CODE HANDLING SECTION ####################################





######################################S3 SECTION##########################
	
@get('/buckets/all')
def getbuckets():
    buckets=s3.list_buckets()
    bucketlist=[]
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
    
    return {"buckets":bucketlist}


@get('/objects')
def getobjects():
    bucketname=request.query.bucketname
    objectlist=[]
    objects=s3.list_objects_v2(Bucket=str(bucketname))
    print(objects)
    if(objects['KeyCount']!=0):
            for object in objects['Contents']:
                objectlist.append(object['Key'])
        
    
    return {bucketname:objectlist}



########################FACING ERRORS IN THIS ONE####
@get('/objects/all') 
def getallobjects():
    buckets=s3.list_buckets()
    bucketlist=[]
    
    objectdict={}
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
        for bucket in bucketlist:
            print(bucket)
            objectlist=[]
            objects=s3.list_objects(Bucket=str(bucket))
            print(objects)

            for object in objects['Contents']:
                objectlist.append(object['Key'])
            objectdict.update({bucket:objectlist})
        

    return objectdict

########################FACING ERRORS IN THIS ONE####


@post('/buckets')
def createbucket():
    bucketname=request.query.bucketname
    s3.create_bucket(Bucket=str(bucketname), CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    return "bucket created successfully"
    
	
@delete('/buckets')
def deletebucket():
	bucketname= request.query.bucketname
	s3.delete_bucket(Bucket=str(bucketname))
	return "bucket "+ bucketname + " deleted successfully"
	
	
######################################S3 SECTION END ##########################



######################################EC2 SECTION START###########################
docker_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
"""
nginx_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
sudo docker run -d -p 80:80 nginx
"""
jenkins_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
sudo docker run -d -p 8080:8080 jenkinsci/blueocean
"""
elk_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
cd ~
git clone https://github.com/deviantony/docker-elk.git
cd docker-elk
sudo docker-compose up -d
"""

mean_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
docker run -i -t -d -p 80:3000 maccam912/meanjs 
"""

osdict={"Amazon_Linux":"ami-0937dcc711d38ef3f","Ubuntu":"ami-0d773a3b7bb2bb1c1","Red Hat Enterprise Linux 7.5":"ami-5b673c34"}
userdatadict={"Docker":docker_script,"Nginx":nginx_script,"Jenkins":jenkins_script,"Elk":elk_script,"Mean":mean_script}



@get('/instances/all')
def getinstances():
    serverlist=[]
    servers=ec2.describe_instances()
    for i in servers['Reservations']:
        for inst in i['Instances']:
            name="Instance Id=>" +str(inst['InstanceId'])
            serverlist.append(name)
    return str(servers['Reservations'])
	
@put('/instances/<os>/<instance_type>/<count>/<keyname>/<app>')
def create_instance(os,instance_type,count,keyname,app):
	ec2.run_instances( ImageId=str(osdict[str(os)]),
        InstanceType=str(instance_type),MaxCount=int(count),
        MinCount=int(count),KeyName=str(keyname),UserData=userdatadict[app])
	return "instance ran successfully"


@post('/instances/<action>/<instance_id>')
def start_stop_instances(action,instance_id):
	if action=='stop':
		ec2.stop_instances(InstanceIds=[
        str(instance_id)
    ])
		return "stopping instances"
	elif action=='start':
		ec2.start_instances(InstanceIds=[
        str(instance_id)
    ])
		return "starting instances"
	return "test"

##########################################EC2 SECTION END#############################



###########################################IAM SECTION#####################################
@get('/users/all')
def get_users():
	return str(iam.list_users())





###########################################IAM SECTION ENDS###################################
if __name__== '__main__':
    run( debug=True, reloader= True)

