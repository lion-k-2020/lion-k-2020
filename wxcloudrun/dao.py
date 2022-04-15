import logging

from sqlalchemy.exc import OperationalError
from builtins import str
from wxcloudrun import db
from wxcloudrun.model import Counters, Article, Tab, Video

# 初始化日志
logger = logging.getLogger('log')


def get_tabs():
    """
    查询已定义Tabs
    :return: Tabs
    """
    try:
        tabs = db.session.query(Tab.id, Tab.index).filter(Tab.deleted == 0).all()
        print(tabs)
        print(type(tabs))
        return tabs
    except OperationalError as e:
        logger.info("get_tabs errorMsg= {} ".format(e))
        return None
    

def get_videos():
    """
    查询已定义Videos
    :return: Videos
    """
    try:
        return {}
        return db.session.query(Video.tab_id, Video.name, Video.cover_src, Video.src, Video.index).filter(Video.deleted == 0).all()
    except OperationalError as e:
        logger.info("get_videos errorMsg= {} ".format(e))
        return None


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


def query_articlebyid(id):
    """
    根据ID查询article实体
    :param id: article的ID
    :return: article实体
    """
    try:
        return Article.query.filter(Article.id == id).first()
    except OperationalError as e:
        logger.info("query_articlebyid errorMsg= {} ".format(e))
        return None


def delete_articlebyid(id):
    """
    根据ID删除article实体
    :param id: article的ID
    """
    try:
        article = Article.query.get(id)
        if article is None:
            return
        db.session.delete(article)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_articlebyid errorMsg= {} ".format(e))


def insert_article(article):
    """
    插入一个article实体
    :param article: article实体
    """
    try:
        db.session.add(article)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_article errorMsg= {} ".format(e))


def update_articlebyid(article):
    """
    根据ID更新article的值
    :param article实体
    """
    try:
        article = query_articlebyid(article.id)
        if article is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_articlebyid errorMsg= {} ".format(e))
