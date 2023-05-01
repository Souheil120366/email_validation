from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')   


class User:
    def __init__( self , data ):
        self.id= data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
      
    @staticmethod
    def validate_user( user ):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL('users_schema').query_db(query,user)
            
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if result: 
            flash("Email already exist!")
            is_valid = False
        return is_valid
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        emails = []
        for email in results:
            emails.append( cls(email) )
  
        return emails
    
    @classmethod
    def get_one(cls):
        query = "SELECT * FROM users ORDER BY ID DESC LIMIT 1"
        result = connectToMySQL('users_schema').query_db(query)
        if result:
           return cls(result[0])
        return result
    
    @classmethod
    def email_exist(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL('users_schema').query_db(query,data)
       
        return cls(result[0])
    
    @classmethod
    def del_email(cls,data):
        
        query = "DELETE FROM users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('users_schema').query_db(query,data)
        
        return result
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( email, created_at, updated_at ) VALUES ( %(email)s , NOW() , NOW() );"
        return connectToMySQL('users_schema').query_db( query, data )        
