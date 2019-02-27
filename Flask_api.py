from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS


import boto3
import json
import logging
s3=boto3.client('s3')
ec2 = boto3.client('ec2')
iam = boto3.client('iam')

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/buckets')
class Buckets(Resource):
    def get(self):
        """
        Get all the buckets
        """
        buckets=s3.list_buckets()
        bucketlist=[]
        for i in buckets['Buckets']:
            bucket= i['Name']
            bucketlist.append(bucket)
        print(bucketlist)
        return {"buckets":bucketlist}
        
@api.route('/objects')
class Objects(Resource):
    def get(self):
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
    
@api.route('/buckets/<string:bucket_name>')  
class BucketsOps(Resource): 
    def post(self,bucket_name):
        
        s3.create_bucket(Bucket=str(bucket_name), CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        return "bucket created successfully"
    def delete(self,bucket_name):
        s3.delete_bucket(Bucket=str(bucket_name))
        return "bucket "+ bucket_name + " deleted successfully"

@api.route('/objects/<string:bucket_name>')
class ObjectsOps(Resource):
    def get(self,bucket_name):
        
        objectlist=[]
        objects=s3.list_objects_v2(Bucket=str(bucket_name))
        print(objects)
        if(objects['KeyCount']!=0):
            for object in objects['Contents']:
                objectlist.append(object['Key'])
        
    
        return {bucket_name:objectlist}    
        
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

        
if __name__ == '__main__':
    app.run(debug=True)
