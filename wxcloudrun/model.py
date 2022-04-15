from datetime import datetime
from run import app
import json
from wxcloudrun import db
from flask import Response


class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        
        return fields


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
    id = db.Column(db.String(50), primary_key=True, autoincrement=False)
    title = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(200), unique=False, nullable=False)
    read_count = db.Column(db.Integer, default=0)
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.now(), default=datetime.now())
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())

class Tab(db.Model, EntityBase):
    __tablename__ = 'tab'
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)
    index = db.Column(db.Integer, unique=True, autoincrement=True)
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())
    update_time = db.Column(db.TIMESTAMP, default=datetime.now())
    deleted = db.Column(db.SmallInteger, default=0)

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    tab_id = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cover_src = db.Column(db.String(100), nullable=False)
    src = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, unique=True, autoincrement=True)
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())
    update_time = db.Column(db.TIMESTAMP, default=datetime.now())
    deleted = db.Column(db.SmallInteger, default=0)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True, autoincrement=False)
    user_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_vip = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())
    update_time = db.Column(db.TIMESTAMP, default=datetime.now())
    deleted = db.Column(db.SmallInteger, default=0)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.String(32), primary_key=True, autoincrement=False)
    user_id = db.Column(db.String(32), nullable=False)
    video_id = db.Column(db.String(32), nullable=False)
    is_favorite = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.TIMESTAMP, default=datetime.now())
    update_time = db.Column(db.TIMESTAMP, default=datetime.now())
    deleted = db.Column(db.SmallInteger, default=0)
	
db.create_all()

@app.route('/api/get_data', methods=['POST'])
def get_data():
    """
    :return: 小程序的tabs和videos
    """
    tabs = db.session.query(Tab.id, Tab.index).filter(Tab.deleted == 0).first()
    users_output = []
#     for tab in tabs:
#         users_output.append(tab.to_json())
    data = json.dumps({'code': 0, 'data': tabs}, ensure_ascii=False)
#     data = json.dumps({'code': 0, 'data': users_output}, ensure_ascii=False)
    return Response(data, mimetype='application/json')
	
	

