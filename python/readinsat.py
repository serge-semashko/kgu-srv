import time
import threading
import json, ast
import threading
import flask
from flask import request
from flask import abort
from flask import Flask
from flask import make_response
from flask import jsonify
import gzip
# dd = jsonify('{}')
reg_mutex = threading.Lock()
reg_mutex.acquire()
time.sleep(1)
reg_mutex.release()
wrok = 0
insatData='{}'
orignames = ('01LEC01CT022 01LEC01CT021 01LEC02CT001 01LEC02CT002 01LEC02CT003 01LEC02CT004'+
' 01LEC02CT005 01LEC02CT006 01LEC01CT181 01LEC01CT191 01LEC02CT201 01LEC02CT211'+
' 01LEC11CT181 01LEC11CT191 01LEC12CT201 01LEC12CT211 01LEC01CT007 01LEC01CT008 01LEC01CT009 01LCM11CT001'+
' 01LEC01CT011 01LEC01CT012 01LEC01CT013 '+
' 01LCM31CL001 01LCM21CL001 01LCM22CL001 01LCM11CL001 00LCM11CL001 00LCM51CL001'+
' 01LMP01DS001 01LMP02DS001 01LMP03DS001 01LMN01DS001'+
' 00LCM01CP001 00LEC01CP001 01LEC01CP005 00LWP01CP005 01LEC01CP005 01LEC02CP001 01LEC01CP001 01LCM11CP001 01LEC02CP002 01LEC02CP004 01LEC02CP006 01LMP01CP003 01LMP02CP003 01LMP03CP003 01LEC02CP003'+
' 01LEC02CP005 01LAV01CP002 01LEC01CP006 01LEC01CP016 01LEC01CP007 01LMN01CP003 01LAW04CP002 01LAV01CP002 01LAW04CP001 01LMN04CP004 01LAW01CP002 01LAW02CP002 01LAW02CP002 01LMP01CP004 01LAW01CP001'+
' 01LMP02CP004 01LAW02CP001 01LMP03CP004 01LAW02CP001 01LCL01CP001 01LEC01CP004 01LEC02CP004 01LCL02CP001 01LEC01CP014 01LEC02CP014 01LEC01CP011 01LEC01CP008 01LEC01CP012 01LEC01CP010 01LCM21CP001'+
' 01LEC01CP101 01LEC01CP102 01LEC01CP009 00LCM51CP001 00LCM01CP002 00LCM51CL001') 
res=''
for a in orignames:
    if a.isalpha():
        res += '*'+a
    else:
        res += a
names = res        
       
names = names.split(' ')
orignames = orignames.split(' ')
print(str(names))
print(str(orignames))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
def shutdown():
    shutdown_server()
    print('Server shutting down...')
    return 'Server shutting down...'
def run_flask():

    app = Flask(__name__)

    @app.route('/data', methods=['GET'])
    def get_alldata():

        resp = make_response(insatData,200)
        resp.headers['content-type']='text/html'
        resp.headers['Access-Control-Allow-Origin']= '*'
        resp.headers['Access-Control-Allow-Methods'] ='GET, POST, PUT, DELETE, OPTIONS'
        return resp    

    
    @app.route('/add', methods=['POST'])
    def add():
        global wrok
        global insatData
        wrok = 0
        request.get_data()
        compressed_data = request.data
        decom = gzip.decompress(compressed_data)
        data1 = decom.decode('UTF-8') 
        print( type(data1 ))
        ldata = {}
        print(str(len(names)))
        for ind  in range( len(names)):
	   	
            n1 = names[ind]
            print('CHECK '+str(ind)+' '+n1+' ')
            orig = orignames[ind]	
            p1 = data1.find(n1)
            if p1<0:
                print('No name in data '+n1+' '+orig)
                continue
            s1=''
            while (data1[p1]!=' '):
                p1+=1
            p1+=2
            while (data1[p1]!='\n'):
                s1+=data1[p1]
                p1+=1
            print(s1)
            name = s1.split('.')
            nm=''
            for i in range(3):
                nm += name[i]+'.'
            nm += name[3]
            print(nm)
            nm += '.Znachenie'
            p2 = data1.find(nm)
            if p2<0:
                print('!!!No value '+n1+' '+orig +' = '+nm)
                continue
            while(data1[p2-2]!='\n'):
                p2 -= 1
            sval=''
            while(data1[p2]!='\"'):
                sval += data1[p2]
                p2 += 1
            print('value['+orig + '] = '+sval)
            varval = sval.replace(',','.')

            try:
                nval = float(varval)
            except:
                nval = -13
            if orignames[ind].find('DS')>-1:
                varval = "%d"%(int(nval)*1000)

            ldata[orignames[ind]]= varval


            
            
                
        #print( len(data.decode('UTF-8') ))
        test1= "".join(str(ldata))
        insatData = test1.replace('\'','\"')
        print( insatData)
        
        print( len(names ))
        if wrok==0:
            f= open('insatJson.txt', 'w')
            f.write(insatData)
            f.close()
            wrok=1
#        shutdown()
        resp = make_response('hello')
        resp.headers['content-type']='text/html'
        resp.headers['Access-Control-Allow-Origin']= '*'
        resp.headers['Access-Control-Allow-Methods'] ='GET, POST, PUT, DELETE, OPTIONS'
        return resp 
    if __name__ == '__main__':
        # //from flask.logging import default_handler
        # app.logger.removeHandler(default_handler)
        print('app run')
        app.run(debug=False,host="0.0.0.0",port=8010)
    
thread_flask     = threading.Thread(target=run_flask, args=())
thread_flask.start()

print("after ad start")
aaa()
while 1==1:
        time.sleep(20);
    
