from bottle import route, run
import boto3
import json
s3=boto3.client('s3')

@route('/buckets/all')
def getbuckets():
    buckets=s3.list_buckets()
    bucketlist=[]
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
    
    return  bucketlist


@route('/buckets/<bucketname>')
def getobjects(bucketname):
    objects=s3.list_objects(Bucket=str(bucketname))
    return objects



@route('/buckets/<bucketname>',method='POST')
def createbucket(bucketname):
    s3.create_bucket(Bucket=str(bucketname), CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    })
    return "bucket create successfully"
    
  

if __name__== '__main__':
    run( debug=True, reloader= True)

