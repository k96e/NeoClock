from flask import Flask, send_from_directory, request, make_response
import pygetwindow as gw
import webbrowser
import pyautogui
import pyperclip
import time
import subprocess
import os
pyautogui.FAILSAFE = False
app = Flask("WebSupport")
ftpd = False
#app.config["SEND_FILE_MAX_AGE_DEFAULT"]=0
import time


def writeLog(data):
    with open('log.txt','a') as f:
        f.write(time.strftime("%m-%d %H:%M:%S    ", time.localtime())+data+'\n')

def sendData(key, value):
    with open(r"D:\clock\.dataTrans",'w') as f:
        f.write(key+' '+value)

@app.route('/')
def indexPage():
    return send_from_directory('',"index.html")

@app.route("/api", methods=['GET'])
def commAPI():
    key = request.args.get('k','')
    value = request.args.get('v','')
    sendData(key,value)
    return "ok"

@app.route("/Mapi", methods=['GET'])
def MAPI():
    global ftpd
    key = request.args.get('k','')
    value = request.args.get('v','')
    try:
        if key=="sendURL":
            webbrowser.open(value)
        elif key=="test":
            return 'ok'
        elif key=="clearLog":
            open(r"D:/clock/log/log.txt", 'w').close()
            return 'ok'
        elif key=="readCopy":
            return pyperclip.paste()
        elif key=="capImg":
            subprocess.Popen("D:\\clock\\CommandCam.exe",cwd="D:\\clock\\")
            return "capturing..."
        elif key=="ftp":
            if not ftpd:
                ftpd = subprocess.Popen("python -m pyftpdlib -w -d "+value,cwd="D:\\clock\\")
                return "ok"
            else:
                return "ftp already started"
        elif key=="ftp_stat":
            if ftpd:
                return str(ftpd.poll())
            else:
                return "ftp not running"
        elif key=="ftp_kill":
            if ftpd:
                ftpd.kill()
                ftpd = False
                return "ok"
            else:
                return "ftp not running"
        elif key=="writeCopy":
            pyperclip.copy(value)
        elif key=="getWindows":
            return "\n".join(gw.getAllTitles())
        elif key=="setKey":
            keys = []
            for k in value.split(' '):
                if k in KeyboardList:
                    keys.append(k)
                else:
                    return k+" is not a key"
            eval("pyautogui.hotkey("+str(keys).strip('[').strip(']')+")")
        elif key.split('_')[0]=="ctrWindow":
            wins = gw.getWindowsWithTitle(value)
            if len(wins)==0:
                return "no window called "+value+" found."
            if key.split('_')[1]=="max":
                wins[0].maximize()
            elif key.split('_')[1]=="act":
                wins[0].activate()
            elif key.split('_')[1]=="min":
                wins[0].minimize()
            elif key.split('_')[1]=="rst":
                wins[0].restore()
            elif key.split('_')[1]=="ext":
                wins[0].close()
    except Exception as e:
        return repr(e),500
    return "ok"
    
@app.route('/getNewScreenshot')
def getScreenshot():
    pyautogui.screenshot(r"D:\clock\screenshot.png")
    resp = make_response(send_from_directory('',"screenshot.png"))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
        
@app.route('/takenImg')
def gettakenImg():
    resp = make_response(send_from_directory('',"image.bmp"))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
    
@app.route('/log')
def getLog():
    resp = make_response(send_from_directory('',"log.txt"))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
        
@app.route('/keys')
def getKeys():
    return str(KeyboardList)

@app.route('/source', methods=['GET'])
def getSource():
    FileName = request.args.get('FileName')
    if not FileName:
        return str(os.listdir())
    resp = make_response(send_from_directory('',FileName))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
    
@app.route('/favicon.ico')
def favico():
    return send_from_directory('static',"favicon.ico")

KeyboardList = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

if __name__ == '__main__':
    app.run('0.0.0.0','5835',debug=True)
