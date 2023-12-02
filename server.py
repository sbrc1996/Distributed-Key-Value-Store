import mysql.connector

# https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported

# Select Host,User,plugin from mysql.user; type this in mysql terminal & get the plugin for mysql root user
db = mysql.connector.connect(user ='root', password= 'subham123', host = '127.0.0.1',port='3306',
                                                                auth_plugin='mysql_native_password')

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE db1")