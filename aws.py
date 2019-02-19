from bottle import route, run
import boto3
import json
s3=boto3.client('s3')
from bottle import hook, route, response

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

