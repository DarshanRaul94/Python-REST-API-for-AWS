from flask_restplus import Namespace, Resource, fields
from flask import Flask, request
api = Namespace('IAM', description='Api\'s to interact with AWS IAM')

import boto3
import json
import logging
iam = boto3.client('iam')


@api.route('/users')    
class Users(Resource):
    def get(self):
        userdict={}
        count=0
        users=iam.list_users()
        userlist=[]
        print(users)
        for user in users['Users']:
            count+=1
            name=user['UserName']
            userid="user"+str(count)
            userlist.append({"Username":name})
            
        return {"users":userlist}

@api.route('/groups')    
class Groups(Resource):
    def get(self):
        groups=iam.list_groups()
        grouplist=[]
        
        for group in groups['Groups']:
            
            name=group['GroupName']
            arn=group['Arn']
            grouplist.append({"Name":name,"ARN":arn})
            
        return {"groups":grouplist}

@api.route('/roles')    
class Roles(Resource):
    def get(self):
        roles=iam.list_roles()
        roleslist=[]
        
        for role in roles['Roles']:
            
            name=role['RoleName']
            description=role['Description']
            roleslist.append({"Name":name,"Description":description})
            
        return {"roles":roleslist}
    
    
    
