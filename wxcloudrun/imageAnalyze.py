import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
import math 

# '''
# 此模块主要是对输入的两幅图片进行处理
# 1. 提取pose关键点坐标
# 2. 标准化
# 3. 计算角度差值
# 4. 计算距离差值

# 生成3个df表格,1是标准化后的df,用于计算角度df和距离df,以及对图片标注
# 2是角度差值对比的df
# 3是距离差值对比的df

# '''


# 对图片检测，提取所有人体关键点的坐标，返回一个df表格
def detectPose_df(path, pose):
    
    image = cv2.imread(path)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    
    if results.pose_landmarks:
        
        df = pd.DataFrame(columns=['position','x','y','z','visibility'])
        count = 0
        for i in mp_pose.PoseLandmark:
            t = i.value
            df.loc[count] = [str(i),results.pose_landmarks.landmark[t].x,results.pose_landmarks.landmark[t].y,results.pose_landmarks.landmark[t].z,results.pose_landmarks.landmark[t].visibility]
            count += 1
        df['position'] = df['position'].str.replace('PoseLandmark.','',regex=True)
        df.insert(0,'position_id',range(len(df)))

    
    return df

# 对df进行初步标准化处理，补充两个点；将坐标原点转换为臀部中点；剔除可见性低的点；计算各个点相对于原点的距离,同时保留原始坐标
def standardization(df):

    p_ls = df.iloc[11]
    p_rs = df.iloc[12]
    p_lh = df.iloc[23]
    p_rh = df.iloc[24]
    #肩膀
    x_ms = (p_ls['x']+p_rs['x'])/2
    y_ms = (p_ls['y']+p_rs['y'])/2
    z_ms = (p_ls['z']+p_rs['z'])/2
    v_ms = (p_ls['visibility']+p_rs['visibility'])/2
    #ms = pd.Series(['MIDDLE_SHOULDER',x_ms,y_ms,z_ms,v_ms], index=p_ls.index)
    # 臀部
    x_mh = (p_lh['x']+p_rh['x'])/2
    y_mh = (p_lh['y']+p_rh['y'])/2
    # 以臀部中点为原点
    z_mh = 0
    v_mh = (p_lh['visibility']+p_rh['visibility'])/2
    #hs = pd.Series(['MIDDLE_HIP',x_mh,y_mh,z_mh,v_mh], index=p_ls.index)
    
    # 补两个点
    df = pd.concat([df,pd.DataFrame([[33,'MIDDLE_SHOULDER',x_ms,y_ms,z_ms,v_ms],[34,'MIDDLE_HIP',x_mh,y_mh,z_mh,v_mh]],columns=df.columns)],ignore_index=True)
    # 保留原始坐标
    df['oringin_lm'] = list(zip(df.x,df.y,df.z))
    # 转换坐标
    df['x'] = df.iloc[34]['x'] - df['x']
    df['y'] = df.iloc[34]['y'] - df['y']

    # 保留可见性大于0.8的点
    # df = df[df['visibility']>0.8]
    # print(f'去除不可见的点后，剩余{len(df)}个点')
    # 计算相对于臀部中点的距离

    distance_hip = np.sqrt((p_lh['x']-p_rh['x'])**2+(p_lh['y']-p_rh['y'])**2+(p_lh['z']-p_rh['z'])**2)
    df['distance'] = (np.sqrt(df['x']**2 + df['y']**2+df['z']**2))/distance_hip
    
    df = df[['position_id','position','x','y','z','visibility','distance','oringin_lm']]
    return df

# 根据两个标准化后的df，计算距离差值并按大小排序
def make_distance_comparison(df_true,df_false):

    df = pd.DataFrame(columns=['position_id','position_name','visibility','distance_true','distance_false','distance_diff','position_true_lm','position_false_lm'])
    # 在df_true中选择可见性高，index在list中的点
    l = [0,11,12,13,14,15,16,23,24,25,26,27,28,33,34]
    df_true = df_true[df_true['position_id'].isin(l)]
    df_true = df_true[df_true['visibility']>0.5]
    df_false = df_false.loc[df_true.index]

    df['position_id'] = df_true['position_id']
    df['position_name'] = df_true['position']
    
    df['visibility'] = df_true['visibility']
    df['distance_true'] = df_true['distance']
    df['distance_false'] = df_false['distance']
    df['distance_diff'] = abs(df_true['distance']-df_false['distance'])

    df['position_true_lm'] = df_true['oringin_lm']
    df['position_false_lm'] = df_false['oringin_lm']
    df = df.sort_values(by='distance_diff',ascending=False)
    df.reset_index(inplace=True)
    return df

# 计算三个点的三维夹角
def angle_3d(a, b, c):       

    v1 = np.array([ a[0] - b[0], a[1] - b[1], a[2] - b[2] ])
    v2 = np.array([ c[0] - b[0], c[1] - b[1], c[2] - b[2] ])

    v1mag = np.sqrt([ v1[0] * v1[0] + v1[1] * v1[1] + v1[2] * v1[2] ])
    v1norm = np.array([ v1[0] / v1mag, v1[1] / v1mag, v1[2] / v1mag ])

    v2mag = np.sqrt(v2[0] * v2[0] + v2[1] * v2[1] + v2[2] * v2[2])
    v2norm = np.array([ v2[0] / v2mag, v2[1] / v2mag, v2[2] / v2mag ])
    res = v1norm[0] * v2norm[0] + v1norm[1] * v2norm[1] + v1norm[2] * v2norm[2]
    angle_rad = np.arccos(res)

    return math.degrees(angle_rad)

# 平面上三个点的2维夹角
def angle_2d(a,b,c):

    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

# 根据两个标准化后的df，计算角度差值并按大小排序
def make_angle_comparison(df_true, df_false,t):
    df_comparison = pd.DataFrame(columns=['angle','point_start','point_middle','point_end','angle_true_3d','angle_true_2d',
    'angle_false_3d','angle_false_2d','angle_3d_inacc','angle_2d_inacc','angle_3d_inacc_rate','angle_2d_inacc_rate','true_start_lm','true_middle_lm','true_end_lm','false_start_lm','false_middle_lm','false_end_lm'])
    
    angle_need = '''12-0-11,33-0-34,14-0-13,16-0-15,26-0-25,28-0-27,14-12-11,14-12-24,26-12-14,16-12-24,0-12-24,13-11-12,13-11-23,25-11-23,15-11-23,0-11-23,14-33-13,16-33-15,26-33-25,28-33-27,16-14-12,16-14-24,15-13-11,15-13-23,12-24-26,14-24-26,23-24-26,11-23-25,13-23-25,24-23-25,26-34-25,28-34-27,14-34-13,16-34-15,24-26-28,23-25-27'''
    #angle_need = '''12-0-11,33-0-34,12-0-24,12-0-26,14-0-24,11-0-23,11-0-25,11-0-13,13-0-23,14-0-13 ,16-0-15,26-0-25,28-0-27,14-12-11,14-12-24 ,26-12-14,26-12-11,0-12-11,0-12-14,16-12-24,13-11-12,13-11-23,25-11-23,25-11-12,0-11-12,0-11-13,15-11-23,14-33-13,16-33-15,0-33-34,26-33-25,28-33-27,16-14-12,12-14-24,12-14-26,24-14-26,16-14-26,16-14-24,15-13-11,11-13-23,11-13-25,23-13-25,15-13-25,15-13-23,12-24-26,14-24-26,12-24-28,26-24-28,14-24-28,14-24-12,23-24-26,23-24-28,0-24-26,0-24-14,11-23-25,13-23-25,11-23-27,25-23-27,13-23-27,13-23-11,24-23-25,24-23-27,0-23-25,0-23-13,26-34-25,28-34-27,14-34-13,16-34-15,0-34-26,0-34-25,0-26-28,0-26-24,24-26-28,12-26-28,14-26-28,12-26-24,14-26-24,14-26-12,16-26-24,16-26-12,0-25-27,0-25-23,23-25-27,11-25-27,13-25-27,11-25-23,13-25-23,13-25-11,15-25-23,15-25-11,26-28-24,26-28-12,14-28-26,25-27-23,25-27-11,13-27-25'''
    angle_need  = angle_need.replace(' ','').replace('\n','').split(',')
    print(f'计划需要计算{len(angle_need)}个角度')

    # 定义不可见的点属性为0.6
    angle_not_visible = list(df_true[df_true['visibility']<0.6]['position_id'].values)
    # angle_need中排除 angle_not_visible
    for angle in angle_need:
        for s in angle_not_visible:
            s = str(s)
            if angle.find(s) != -1:
                angle_need.remove(angle)
                break
    print(f'排除不可见点后，需要计算{len(angle_need)}个角度')

    for angle in angle_need:
        i,j,k = angle.split('-')
        i,j,k = int(i),int(j),int(k)
        
        point_start = df_true.iloc[i][1]
        point_middle = df_true.iloc[j][1]
        point_end = df_true.iloc[k][1]
        
        # 正确df的三个3D点(x,y,z)
        p1 = df_true.iloc[i].oringin_lm
        p2 = df_true.iloc[j].oringin_lm
        p3 = df_true.iloc[k].oringin_lm

        p1_3d = np.array(df_true.iloc[i][2:5])
        p2_3d = np.array(df_true.iloc[j][2:5])
        p3_3d = np.array(df_true.iloc[k][2:5])
        # 错误df的三个3D点(x,y,z)
        p4 = df_false.iloc[i].oringin_lm
        p5 = df_false.iloc[j].oringin_lm
        p6 = df_false.iloc[k].oringin_lm

        p4_3d = np.array(df_false.iloc[i][2:5])
        p5_3d = np.array(df_false.iloc[j][2:5])
        p6_3d = np.array(df_false.iloc[k][2:5])
        
        # 正确df的三个2D点(x,y)
        p1_2d = np.array(df_true.iloc[i][2:4])
        p2_2d = np.array(df_true.iloc[j][2:4])
        p3_2d = np.array(df_true.iloc[k][2:4])
        # 错误df的三个2D点(x,y)
        p4_2d = np.array(df_false.iloc[i][2:4])
        p5_2d = np.array(df_false.iloc[j][2:4])
        p6_2d = np.array(df_false.iloc[k][2:4])
        # 计算3D角度
        angle_1= angle_3d(p1_3d, p2_3d, p3_3d)
        angle_2= angle_3d(p4_3d, p5_3d, p6_3d)
        # 计算2D角度
        angle_3= angle_2d(p1_2d, p2_2d, p3_2d)
        angle_4= angle_2d(p4_2d, p5_2d, p6_2d)
        # 计算3D角度差值
        angle_3d_inacc = angle_1 - angle_2
        # 计算2D角度差值
        angle_2d_inacc = angle_3 - angle_4
        # 计算3D角度差值百分比
        if angle_1 == 0:
            angle_3d_inacc_rate = 0
        else:
            angle_3d_inacc_rate = abs(angle_3d_inacc) / angle_1
        # 计算2D角度差值百分比
        if angle_3 == 0:
            angle_2d_inacc_rate = 0
        else:
            angle_2d_inacc_rate = abs(angle_2d_inacc) / angle_3
        

        # 存入df
        if angle_3d_inacc_rate > t or angle_2d_inacc_rate > t:
            df_comparison = pd.concat([df_comparison,pd.DataFrame([[angle,point_start,point_middle,point_end,angle_1,angle_3,angle_2,angle_4,angle_3d_inacc,angle_2d_inacc,angle_3d_inacc_rate,angle_2d_inacc_rate,p1,p2,p3,p4,p5,p6]],columns=['angle','point_start','point_middle','point_end','angle_true_3d','angle_true_2d',
            'angle_false_3d','angle_false_2d','angle_3d_inacc','angle_2d_inacc','angle_3d_inacc_rate','angle_2d_inacc_rate','true_start_lm','true_middle_lm','true_end_lm','false_start_lm','false_middle_lm','false_end_lm'])],ignore_index=True)

    df_comparison.dropna(how = 'any',inplace=True)
    df_comparison.columns=df_comparison.columns.str.strip()
    df_comparison.sort_values(by=['angle_2d_inacc','angle_3d_inacc',],kind = 'mergesort',ascending=False,na_position='last',inplace=True)
    df_comparison.reset_index(inplace=True)
    print(f'共有{len(df_comparison)}条记录')
    return df_comparison







