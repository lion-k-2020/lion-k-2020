from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.String(50), primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, name='article_title')
    describe = db.Column(db.String(200), unique=True, nullable=False)
    read_count = db.Column(db.Integer, default=0)
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.now(), default=datetime.now())
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())
