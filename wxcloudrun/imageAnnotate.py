import mediapipe as mp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math 
import os
from PIL import Image, ImageDraw,ImageFont
import random

### 该模块主要是对图片进行标注

# 根据标准化之后的df,标注pose---在原始图片中标注出需要的关键点以及点和点之间的连线
def mark_pose(img_path,df):

    def linedashed(x0, y0, x1, y1, dashlen=4, ratio=3): 
        dx=x1-x0 # delta x
        dy=y1-y0 # delta y
        # check whether we can avoid sqrt
        if dy==0: len=dx
        elif dx==0: len=dy
        else: len=math.sqrt(dx*dx+dy*dy) # length of line
        xa=dx/len # x add for 1px line length
        ya=dy/len # y add for 1px line length
        step=dashlen*ratio # step to the next dash
        a0=0
        while a0<len:
            a1=a0+dashlen
            if a1>len: a1=len
            draw.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = (123, 174, 218))
            a0+=step 

    img = Image.open(img_path)
    img_save_path = os.path.dirname(img_path) + '/' + os.path.basename(img_path).split('.')[0] + '_marked.png'
    draw = ImageDraw.Draw(img)
    width,height = img.size
    
    #点序号
    point= [0,11,12,13,14,15,16,23,24,25,26,27,28,33,34]
    connections = [(11,12),(12,14),(14,16),(11,13),(13,15),(12,24),(24,26),(26,28),(25,27),(23,25),(11,23),(23,24)]
    for i in point:
        # 根据i取得position_id,然后根据position_id取得x,y 画出点并标号
        # x = df[df['position_id']==i]['oringin_lm'].values[0][0]
        # y = df[df['position_id']==i]['oringin_lm'].values[0][1]
        x = df.loc[i]['oringin_lm'][0]
        y = df.loc[i]['oringin_lm'][1]
       
        font = ImageFont.truetype('/home/ubuntu/Code/BD/input/ZCOOLKuaiLe-Regular.ttf', 12)
        draw.text((x*width+15,y*height),str(i),fill="red",font=font)
        draw.ellipse((x*width-4,y*height-4,x*width+4,y*height+4),fill=(246,246,94),outline ='black')
    

    #画线
    for i in connections:
        # x1 = df[df['position_id']==i[0]]['oringin_lm'].values[0][0]
        # y1 = df[df['position_id']==i[0]]['oringin_lm'].values[0][1]
        # x2 = df[df['position_id']==i[1]]['oringin_lm'].values[0][0]
        # y2 = df[df['position_id']==i[1]]['oringin_lm'].values[0][1]
        x1 = df.loc[i[0]]['oringin_lm'][0]
        y1 = df.loc[i[0]]['oringin_lm'][1]
        x2 = df.loc[i[1]]['oringin_lm'][0]
        y2 = df.loc[i[1]]['oringin_lm'][1]
        linedashed(x1*width,y1*height,x2*width,y2*height,dashlen=10,ratio=3)
    
    img.save(img_save_path)
    return img

# 标注前top_num个错误的角度
def mark_angle(img,df,top_num):

    draw = ImageDraw.Draw(img)
    width,height = img.size
    # fontpath = '/home/ubuntu/Code/BD/input/ZCOOLKuaiLe-Regular.ttf'
    # font = ImageFont.truetype(fontpath, 13)
    ## 存放错误角度的描述
    angle_des = []

    draw.rectangle([(0,0),(top_num*20,40)],fill=(252,252,252))

    df = df.iloc[:top_num,:]
    # x_text,y_text = 10,10

    for i in range(len(df)):
        # 颜色
        c = 0
        color = (random.randint(128, 250), random.randint(c, c+30), random.randint(0, 255))
        #point_start坐标
        x_start,y_start = df.loc[i]['false_start_lm'][0]*width,df.loc[i]['false_start_lm'][1]*height
        #point_middle坐标
        x_middle,y_middle = df.loc[i]['false_middle_lm'][0]*width,df.loc[i]['false_middle_lm'][1]*height
        #point_end坐标
        x_end,y_end = df.loc[i]['false_end_lm'][0]*width,df.loc[i]['false_end_lm'][1]*height
        # 画两条线
        draw.line((x_start,y_start,x_middle,y_middle),fill=color,width=3)
        draw.line((x_middle,y_middle,x_end,y_end),fill=color,width=3)
        # 获取描述
        if df.iloc[i]['angle_true_2d']>df.iloc[i]['angle_false_2d']:
            text = f"角 {df.iloc[i]['angle']}过小:{str(df.iloc[i]['angle_true_3d'])[:5]}--{str(df.iloc[i]['angle_false_3d'])[:5]}"
        else:
            text = f"角 {df.iloc[i]['angle']}过大:{str(df.iloc[i]['angle_true_3d'])[:5]}--{str(df.iloc[i]['angle_false_3d'])[:5]}"
        angle_des.append(text)
        #draw.text((x_text,y_text),text,fill=color,font=font)
        #y_text += 18
        #c += 30
    return img,angle_des


def mark_distance(img,df,top_num):

    draw = ImageDraw.Draw(img)
    width,height = img.size
    #fontpath = '/home/ubuntu/Code/BD/input/ZCOOLKuaiLe-Regular.ttf'
    #font = ImageFont.truetype(fontpath, 18)
    ## 存放错误距离的描述
    distance_des = []
    # 原点的坐标
    oringin = df[df.position_id==34]['position_false_lm'].values[0]
    X,Y = oringin[0]*width,oringin[1]*height
    df = df.iloc[:top_num,:]

    #x_text,y_text = width-100,10

    for i in range(len(df)):
        #颜色
        c = 0
        color = (random.randint(0, 128), random.randint(0, 255), random.randint(c, c+30))
        # 点的坐标
        x_p,y_p = df.iloc[i]['position_false_lm'][0]*width,df.iloc[i]['position_false_lm'][1]*height
        # 文字的坐标
        #x_t,y_t = int((X+x_p)/2),int((Y+y_p)/2)
        # text
        if df.iloc[i]['distance_true']>df.iloc[i]['distance_false']:
            text = f"Middle_HIP到{df.iloc[i]['position_name']}距离过小"
        else:
            text = f"Middle_HIP到{df.iloc[i]['position_name']}距离过大"
        distance_des.append(text)
        draw.line((X,Y,x_p,y_p),fill="#000",width=3)
        #draw.text((x_text,y_text),text,fill="#000",font=font)
        #width = font.getsize(text)[0]
        #print(width)
        #y_text += 18
        c += 30
    
    return img,distance_des












