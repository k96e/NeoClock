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


def handleTraceback(errStr):
    global root
    if "SystemExit: 0" in errStr:
        return
    tkinter.messagebox.showerror('This is a bug, not feature.',errStr)
    root.quit()
    exit(0)


def getCountdown():
    delta = (1686099600-time.time())/86400
    if delta >= 0:
        return "距高考还有 %.4f 天" % delta
    else:
        return ""
    
def getConf():
    global scheText
    with open(r"D:\clock\conf.ini",encoding='utf-8') as f:
        wday = time.localtime(time.time()).tm_wday
        dat = json.load(f)
        if time.localtime(time.time()).tm_hour >= 21:
            wday = wday+1 if not wday == 6 else 0
            schData = dat['sche'][wday]
            scheText = "明天"+wdayList[wday]+" "+schData
        else:
            schData = dat['sche'][wday]
            scheText = wdayList[wday]+"  "+schData
        
def setConf(newd=None):
    with open(r"D:\clock\conf.ini", "r+",encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        if newd:
            data["countd"] = newd
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
    global t,root,countdownLabel
    try:
        ctime = time.localtime(time.time())
        t.config(text=time.strftime('%H:%M:%S',ctime))
        countdownLabel.config(text=getCountdown())
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


def getData():
    global scheText,root
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
            elif key=="setPos":
                try:
                    x,y=value.split(',')
                    root.geometry("+"+x+"+"+y)
                except:
                    root.geometry(defaultPos)
        os.remove(r"D:\clock\.dataTrans")


def timedWork(autoUpdate=True):
    global scheText,dateLabel,weatherLabel,scheLable
    if autoUpdate:
        updateWeather()
    else:
        getConf()
        scheLable.config(text=scheText)
        dateLabel.config(text=time.strftime(' %m{m}%d{d}',
            time.localtime(time.time())).format(m='月',d='日'))
 
def quitWin(events):
    global root
    if tk.messagebox.askyesno("info","是否关闭？"):
        root.quit()
        exit(0)

try:
    scheText=""
    getConf()
    root = tk.Tk("NeoClock")
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
        text=getCountdown(),
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
    time.sleep(1)
    #requests.get("http://192.168.40.143:5835",timeout=1)
    updateWeather()
    setTime()
    root.bind("<Double-Button-1>",quitWin)
    #root.wm_attributes('-topmost', 1)
    root.lower()
    root.mainloop()
except:
    handleTraceback(traceback.format_exc())
