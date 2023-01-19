import os

if os.path.isfile("conf_bak.ini"):
    try:
        os.remove("conf.ini")
    except:
        pass
    os.system("copy conf_bak.ini conf.ini")
else:
    print("err!")
os.system('pause')
    