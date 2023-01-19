import tkinter as tk
import tkinter.messagebox
import requests
import json
import os
import time
import datetime
import traceback
import subprocess


defaultPos = "+1405+15"
# defaultPos = "+905+15"
link = "http://www.nmc.cn/rest/real/58436"
wdayList = ["周一","周二","周三","周四","周五","周六","周日"]


def getExtraMsg():
    try:
        print("upd")
        keywords = ["台海","台岛","解放军","演练","军演","台湾","佩洛西","窜台","涉台",
            "访台","七国集团","台独","战区","演习","演训","解放军","一个中国","一中","G7"]
        results = []
        r = requests.get("https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?"+
            "offset=&host_mid=483787858&timezone_offset=-480",timeout=0.5).json()
        for item in r["data"]["items"]:
            if item["modules"]["module_dynamic"]["major"]["type"]=="MAJOR_TYPE_DRAW":
                desc = item["modules"]["module_dynamic"]["desc"]["text"].replace(" ",'')
                if any(k in desc for k in keywords):
                    if "【"in desc and "】" in desc:
                        timestr = item["modules"]["module_author"]["pub_ts"]
                        results.append(time.strftime('%H:%M',time.localtime(timestr))+
                            "-"+desc.split("】")[0].split("【")[-1])
            elif item["modules"]["module_dynamic"]["major"]["type"]=="MAJOR_TYPE_ARCHIVE":
                desc = item["modules"]["module_dynamic"]\
                    ["major"]["archive"]["title"].replace(" ",'')
                if any(k in desc for k in keywords):
                    timestr = item["modules"]["module_author"]["pub_ts"]
                    results.append(time.strftime('%H:%M',time.localtime(timestr))+
                        "-"+desc)
        return '\n'.join(results[:3])
    except:
        return 'err'             

def handleTraceback(errStr):
    global root
    if "SystemExit: 0" in errStr:
        return
    tkinter.messagebox.showerror('This is a bug, not feature.',errStr)
    root.quit()
    exit(0)

'''
倒计时文本生成
20307江南十校
0:  消息类型  0:禁用 1-3:年份(2021-2023)
1-4:生效时间mmdd
5+: 文本
'''
def getCountdown(data):
    if len(data)==0:
        return ''
    elif data[0]=='0':
        return ''
    elif data[0] in ['1','2','3']:
        delta = (datetime.datetime.strptime('202'+data[0:5],"%Y%m%d")-\
            datetime.datetime.strptime(\
            time.strftime('%Y%m%d',time.localtime(time.time())),"%Y%m%d")).days
        if delta > 0:
            return "距 "+data[5:]+" 还有 "+str(delta)+" 天"
        elif delta >= -1:
            return data[5:]+"day"+str(-delta)
    else:
        return data
    
def getConf():
    global scheText,countdownText,extraFlag
    with open(r"D:\clock\conf.ini",encoding='utf-8') as f:
        wday = time.localtime(time.time()).tm_wday
        dat = json.load(f)
        countdownText = getCountdown(dat['countd'])
        extraFlag = False if dat["extraFlag"] == '0' else True
        if time.localtime(time.time()).tm_hour >= 21:
            wday = wday+1 if not wday == 6 else 0
            schData = dat['sche'][wday]
            scheText = "明天"+wdayList[wday]+" "+schData
        else:
            schData = dat['sche'][wday]
            scheText = wdayList[wday]+"  "+schData
        
def setConf(newd=None,newFlag='hold'):
    with open(r"D:\clock\conf.ini", "r+",encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        if newd:
            data["countd"] = newd
        if type(newFlag) == bool:
            data["extraFlag"] = '1' if newFlag else '0'
        jsonFile.seek(0)
        json.dump(data, jsonFile,ensure_ascii=False)
        jsonFile.truncate()

def updateWeather():
    global weatherLabel
    for i in range(3):
        try:
            resp = requests.get(link,timeout=0.8).json()['weather']
            weatherLabel.config(text=resp['info']+' '+"%.1fK "%(resp['temperature']+273.2))
            return
        except:
            time.sleep(0.4)

def setTime():
    global t,root,extraLabel,extraText,extraFlag
    try:
        ctime = time.localtime(time.time())
        t.config(text=time.strftime('%H:%M:%S',ctime))
        # if (ctime.tm_sec == 0) and extraFlag:
            # extraText = getExtraMsg()
            # if not extraText=='err':
                # extraLabel.config(text=extraText)
        if (ctime.tm_min%10 == 0 and ctime.tm_sec == 0):
            timedWork()
            if (ctime.tm_hour == 21 and (ctime.tm_min == 10 or ctime.tm_min == 20) and ctime.tm_sec == 0):
                timedWork(False)
            if (ctime.tm_hour == 0 and ctime.tm_min == 0 and ctime.tm_sec == 0):
                timedWork(False)
        #root.after(int((1-time.time()+int(time.time()))*1000-100), setTime)
        getData()
        root.after(1000, setTime)
    except:
        handleTraceback(traceback.format_exc())

'''
处理远程控制请求
data:
key value
''' 
def getData():
    global scheText,countdownText,root,extraFlag,extraLabel,extraText
    if os.path.isfile(r"D:\clock\.dataTrans"):
        with open(r"D:\clock\.dataTrans",'r') as f:
            data = f.read()
            if len(data)==0:
                return
            [key, value] = data.split(' ',1)
            print('update')
            if key=='updateNow':
                timedWork()
                timedWork(False)
            elif key=="setCountdownMsg":
                countdownText = getCountdown(value)
                timedWork(False)
                setConf(newd=value)
            elif key=="setExtraFlag":
                extraFlag = not extraFlag
                if not extraFlag:
                    extraText = ""
                    extraLabel.config(text="")
                else:
                    extraText = getExtraMsg()
                    extraLabel.config(text=extraText)
                setConf(newFlag=extraFlag)
            elif key=="setPos":
                try:
                    x,y=value.split(',')
                    root.geometry("+"+x+"+"+y)
                except:
                    root.geometry(defaultPos)
        os.remove(r"D:\clock\.dataTrans")


def timedWork(autoUpdate=True):
    global scheText,countdownText,\
        dateLabel,weatherLabel,scheLable,countdownLabel
    if autoUpdate:
        updateWeather()
    else:
        getConf()
        countdownLabel.config(text=countdownText)
        scheLable.config(text=scheText)
        dateLabel.config(text=time.strftime(' %m{m}%d{d}',
            time.localtime(time.time())).format(m='月',d='日'))
 
def quitWin(events):
    global root
    if tk.messagebox.askyesno("info","是否关闭？"):
        root.quit()
        exit(0)

try:
    countdownText=""
    scheText=""
    extraText=""
    extraFlag=False
    getConf()
    root = tk.Tk("NewClock")
    root.overrideredirect(True)
    root.geometry(defaultPos)
    root.geometry("500x280")
    #root.geometry("500x450")
    root['background']='black'
    headFrame = tk.Frame(
        bg='black')
    headFrame.pack(fill='x')
    dateLabel = tk.Label(headFrame, 
        text=time.strftime(' %m{m}%d{d}',
            time.localtime(time.time())).format(m='月',d='日'),
        fg='white',
        bg='black',
        font=('Yahei Consolas Hybrid', 20)
        )
    dateLabel.pack(side='left',anchor='w')
    weatherLabel = tk.Label(headFrame, 
        text="",
        fg='white',
        bg='black',
        font=('Yahei Consolas Hybrid', 20)
        )
    weatherLabel.pack(side='right',anchor='e')
    t = tk.Label(root, 
        text='--:--:--',
        fg='white',
        bg='black',
        font=('Yahei Consolas Hybrid', 80)
        )
    t.pack()
    countdownLabel = tk.Label(root,
        text=countdownText,
        fg='white',     
        bg='black',
        font=('Yahei Consolas Hybrid', 28),
        )
    countdownLabel.pack()
    scheLable = tk.Label(root,
        text=scheText,
        fg='white',     
        bg='black',
        font=('Yahei Consolas Hybrid', 20),
        )
    scheLable.pack()
    extraLabel = tk.Label(root,
        text=extraText,
        fg='white',     
        bg='black',
        wraplength=480,
        anchor='w',
        justify='left',
        font=('Yahei Consolas Hybrid', 12),
        )
    extraLabel.pack()
    time.sleep(1)
    #requests.get("http://192.168.40.143:5835",timeout=1)
    updateWeather()
    if extraFlag:
        extraText=getExtraMsg()
        extraLabel.config(text=extraText)
    setTime()
    root.bind("<Double-Button-1>",quitWin)
    #root.wm_attributes('-topmost', 1)
    root.lower()
    root.mainloop()
except:
    handleTraceback(traceback.format_exc())
