from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid, delete_articlebyid, query_articlebyid, insert_article, update_articlebyid, get_tabs, get_videos
from wxcloudrun.model import Counters, Article, Tab, Video
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.sys import suid


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/get_data', methods=['POST'])
def get_data():
    """
    :return: 小程序的tabs和videos
    """
    tabs = get_tabs()
    videos = get_videos()
    tabs_format = []
    videos_format = []
    if (len(tabs)):
        for x in range(len(tabs)):
            tabs_format.append({})
            tabs_format[x]['id'] = tabs[x]['id']
            tabs_format[x]['name'] = tabs[x]['name']
            tabs_format[x]['index'] = tabs[x]['index']
    if (len(videos)):
        for x in range(len(videos)):
            videos_format.append({})
            videos_format[x]['tab_id'] = tabs[x]['tab_id']
            videos_format[x]['name'] = tabs[x]['name']
            videos_format[x]['cover_src'] = tabs[x]['cover_src']
            videos_format[x]['src'] = tabs[x]['src']
            videos_format[x]['index'] = tabs[x]['index']
    return make_succ_response({"tabs" : tabs_format, "videos" : videos_format})

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')
    if 'openid' not in params:
        return make_err_response('缺少openid参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']
    # 获取微信用户openid
    openid = params['openid']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(openid)
        if counter is None:
            counter = Counters()
            counter.id = openid
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = openid
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(openid)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
    
@app.route('/api/article', methods=['POST'])
def article():
    """
    :return:结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')
    if 'openid' not in params:
        return make_err_response('缺少openid参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']
    # 获取微信用户openid
    openid = params['openid']

    # 执行自增操作
    if action == 'add':
        article = Article()
        article.id = suid()
        article.title = params['title']
        article.describe = params['describe']
        article.read_count = params['read_count']
        article.created_at = datetime.now()
        article.updated_at = datetime.now()
        insert_article(article)
        return make_succ_empty_response()

    # 执行编辑操作
    elif action == 'edit':
        article = query_articlebyid(params['id'])
        article.id = params['id']
        article.title = params['title']
        article.describe = params['describe']
        article.read_count = params['read_count']
        article.updated_at = datetime.now()
        update_articlebyid(article)
        return make_succ_empty_response()
        
    # 执行删除操作
    elif action == 'delete':
        delete_articlebyid(params['id'])
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')
