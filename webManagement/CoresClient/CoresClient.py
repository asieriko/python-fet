import subprocess
import time
import requests
import re
import random  
import datetime
import sys
    
    
HOST = "https://zerbimendi.educacion.navarra.es/fet"
HOST = "http://127.0.0.1:8000/fet"
#HOST = "http://asieriko.pythonanywhere.com/fet"

CHECK_TIME = 300
    
def getServerInfo(computer, thread):
    data={}
    data["computer"] = computer
    data["thread"] = thread
    url = HOST + '/fetfiles/'
    r = requests.get(url+computer+"/"+thread)
    print(r.url,r.status_code,r.content)
    r = r.json()
    return r

def downloadfile(fid):
    url = HOST + '/fetfiles/'
    r = requests.get(url+fid)
    print(r.url,r.status_code,r.headers['content-disposition'])
    d = r.headers['content-disposition']
    fname = re.findall("filename=(.+)", d)[0]
    with open(fname, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return fname

def sendFilestoServer(computer,thread,fetfile,teachersfile,time):
    data={}
    data["computer"] = computer
    data["thread"] = thread
    data["time"] = time
    url = HOST + '/fetfiles/upload/'
    
    files = {'fet_file': open(fetfile,'rb'),'teachers_file': open(teachersfile,'rb')}
    
    r = requests.post(url, files=files,data=data)
    print(r.url,r.status_code)
    
def tarfiles(fet,teacher):
    n = fet.split("/")[-1].split("_data_and_timetable.fet")[0]
    print(n)
    tarfile = "tars/"+n+"_"+str(int(datetime.datetime.timestamp(datetime.datetime.today())*100000))+".tgz"
    cmd = ["tar","cvzf",tarfile,fet,teacher]
    print(" ".join(cmd))
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=False)    
    
def launchfet(inputfile, outputdir,computer,thread,file_id="0"):
    fetstart = time.time()
    cmd = ["./fet-cl","--inputfile="+inputfile,"--outputdir="+outputdir]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=False)
    print("------------------------------------------------------------------------------")
    print("process:", " ".join(cmd))
    while process.poll() == None:
        try:
            SI = getServerInfo(computer,thread)
            print(SI)
            if SI["status"] == "Stop":
                print("Server send stop signal")
                process.terminate()
                return {"status":"stoped"}
            if (SI["status"] == "active") and (SI["file_id"] != file_id):
                file_id = SI["file_id"]
                print("Server send newfile to generate")
                process.terminate()
                return {"status":"newfile","file":SI["file_id"]}        #FIXME hobetu behar, ziurtatu id, filename...
            time.sleep(CHECK_TIME)
        except Exception:
            print("An error ocurred  while getServerInfo()")
            time.sleep(CHECK_TIME)
    tunit = 0
    tmag = 'seconds'
    success = False
    for line in process.stdout.read().split(b'\n'):
        strline = line.decode(encoding='UTF-8')
        if 'Total searching time' in strline:
            tunit = re.search(r'\((.*?)\)',strline).group(1)
            tmag = re.search(r'[0-9]',strline).group()
        if 'Simulation successful' in strline:
            success = True
        if 'Simulation stopped' in strline:
            print(strline)
    print("Process return code",process.returncode)#0 if success, and None if terminate
    if success:
        fetend = time.time()
        fetend - fetstart
        return {"status":"success","timem":int(fetend - fetstart),"timeu":"seconds"}
    else:
        print("Simulation did not found a solution")
        return {"status":"ended"}
    print("End")
    
def main(computer,thread):
    #fetfile="mendifetoutput.fet"
    fetfile="Horario1718-Erl.fet"
    outputdir = "."
    file_id=0
    while True:
        try:
            r = launchfet(fetfile,outputdir,computer,thread,file_id)
            if r["status"] == "newfile":
                print("Received new file from server, starting again")
                fetfile = downloadfile(r["file"])
                file_id=r["file"]
            if r["status"] == "success":
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("Received success: timetable found")
                print("Sucessful simulation in ",r["timem"],r["timeu"])
                print("Fetfile: ",fetfile)
                prefix = outputdir + "/timetables/" + fetfile[:-4] + "/" + fetfile[:-4]
                gfetfile = prefix + "_data_and_timetable.fet"
                teachersfile = prefix + "_teachers.xml"
                print(gfetfile)
                print(teachersfile)
                tarfiles(gfetfile,teachersfile)
                sendFilestoServer(computer,thread,gfetfile,teachersfile,r["timem"])
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            if r["status"] == "stoped":
                print("Received stoped")
                SI = getServerInfo(computer,thread)
                while SI["status"] == "Stop":
                    print("Waiting until new file is send")
                    SI = getServerInfo(computer,thread)
                fetfile = SI
            if r["status"] == "ended":
                print("Received ended")
        except Exception:
            print("An error ocurred")

if __name__=="__main__":
    computer = sys.argv[1]
    thread = sys.argv[2] 
    
    main(computer,thread)
