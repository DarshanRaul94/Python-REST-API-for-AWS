from bottle import route, run,hook, response
from bottle import post, get, put, delete
import boto3
import json
s3=boto3.client('s3')
ec2 = boto3.client('ec2')

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


######################################S3 SECTION##########################
	
@get('/buckets/all')
def getbuckets():
    buckets=s3.list_buckets()
    bucketlist=[]
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
    
    return  str(bucketlist)


@get('/buckets/<bucketname>')
def getobjects(bucketname):
    objects=s3.list_objects(Bucket=str(bucketname))
    return str(objects)



@post('/buckets/<bucketname>')
def createbucket(bucketname):
    s3.create_bucket(Bucket=str(bucketname), CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    })
    return "bucket created successfully"
    
	
@delete('/buckets/<bucketname>')
def deletebucket(bucketname):
	s3.delete_bucket(Bucket=str(bucketname))
	return "bucket "+ bucketname + " deleted successfully"
	
	
######################################S3 SECTION END ##########################



######################################EC2 SECTION START###########################
osdict={"Amazon_Linux":"ami-0937dcc711d38ef3f","Ubuntu":"ami-0d773a3b7bb2bb1c1","Red Hat Enterprise Linux 7.5":"ami-5b673c34"}
userdatadict={"Docker":docker_script,"Nginx":nginx_script,"Jenkins":jenkins_script,"Elk":elk_script,"Mean":mean_script}

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

@get('/instances/all')
def getinstances():
	serverlist=[]
    servers=ec2.describe_instances()
    for i in servers['Reservations']:
        for inst in i['Instances']:
            name="Instance Id=>" +str(inst['InstanceId'])
            serverlist.append(name)
	return str(serverlist)


if __name__== '__main__':
    run( debug=True, reloader= True)

