from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid, \
    delete_articlebyid, query_articlebyid, insert_article, update_articlebyid, get_tabs, get_videos
from wxcloudrun.model import Counters, Article, Tab, Video
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.sys import suid
from wxcloudrun.uploadFile import upload_file
from wxcloudrun.downloadFile import download_file
# from wxcloudrun.imageAnalyze import *
# from wxcloudrun.imageAnnotate import *


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
    return make_succ_response({"tabs": tabs, "videos": videos})


@app.route('/api/action_analyze', methods=['POST'])
def action_analyze():
    """
    :return: 分析后的带标注视频
    """
    # 获取请求体参数
    params = request.get_json()

    # 检查参数
    if 'openid' not in params:
        return make_err_response('缺少openid参数')
    if 'type' not in params:
        return make_err_response('缺少type参数')
    if 'correct_data' not in params:
        return make_err_response('缺少correct_data参数')
    if 'wrong_data' not in params:
        return make_err_response('缺少wrong_data参数')
    if 'is_vip' not in params:
        return make_err_response('缺少is_vip参数')
#     local_path = download_file(params['openid'], params['wrong_data'], "2")
#     src = upload_file(local_path, params['openid'])
    res = {"score": 90, "describe": [{"idx": 1, "word": "温馨提示：请不要弯腰哦^-^"},
                                     {"idx": 2, "word": "智能分析评价：亲，您的动作标准度较高，再接再厉哦~"}], 
           "src": "cloud://prod-4gbd4dc41c3a1678.7072-prod-4gbd4dc41c3a1678-1310533907/0c85b8f0f5e8ca2c9c0c2cd5e89deea7.mp4"}
    return make_succ_response(res)


#     mp_pose = mp.solutions.pose
#     pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2)

#     df1 = detectPose_df(path1,pose)
#     df2 = detectPose_df(path2,pose)

#     df_true = standardization(df1)
#     df_false = standardization(df2)

#     df_distance_comparison = make_distance_comparison(df_true, df_false)
#     df_angle_comparison = make_angle_comparison(df_true, df_false, 0.2)

#     img = mark_pose(path2,df_false)

#     img1 = mark_distance(img,df_distance_comparison,3)
#     #img1.save('/home/ubuntu/Code/BD/input/深蹲错误_标准距离.png')
#     img2 = mark_angle(img1,df_angle_comparison,4)

#     # 存储标注后的图片
#     img2.save('/home/ubuntu/Code/BD/input/深蹲错误_标准角度.png')


#     return make_succ_response({"tabs" : tabs, "videos" : videos})

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
