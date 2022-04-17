import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
