URL = "opc.tcp://0.0.0.0:4840"
import json
import time
import threading
import json, ast
import flask

import gzip 
import sys
import random
from flask import request
from flask import abort
from flask import Flask
from flask import make_response
from flask import jsonify
import requests
from requests.exceptions import HTTPError

from opcua import Server
from opcua import Client
# https://python-opcua.readthedocs.io/en/latest/
all_data = { "k1td1" :'NaN', "k1td2" : 'NaN', "k1td3" : 'NaN', "k1pg" : 'NaN', "k1sbr" : 0,
            "k1vanna" : 'NaN', "k1bo1" : 'NaN', "k1bo2" : 'NaN', "k1t1" : 'NaN', "k1t5" : 'NaN',
            "k1t9" : 'NaN', "k1t13" : 'NaN', "k1t2" : 'NaN', "k1t6" : 'NaN', "k1t10" : 'NaN', "k1t3" : 'NaN', 
            "k1t7" : 'NaN', "k1t11" : 'NaN', "k1t4" : 'NaN', "k1t8" : 'NaN', "k1t12" : 'NaN', "k1t181" : 'NaN', 
            "k1t191" : 'NaN', "k1t201" : 'NaN', "k1t211" : 'NaN', "k1t182" : 'NaN', "k1t192" : 'NaN', "k1t202" : 
            'NaN', "k1t212" : 'NaN', "k1dt5t6" : 'NaN', "k1dt3t4" : 'NaN', "k2td1" : 0, "k2td2" : 0, 
            "k2td3" : 0, "k2pg" : 0, "k2sbr" : 0, "k2vanna" : 0, "k2bo1" : 0, "k2bo2" : 66.13, "k2t1" : 226.48, 
            "k2t5" : 83.21, "k2t9" : 219.68, "k2t13" : 290.39, "k2t2" : 222.17, "k2t6" : 84.53, "k2t10" : 136.55,
            "k2t3" : 83.27, "k2t7" : 212.99, "k2t11" : 243.51, "k2t4" : 77.73, "k2t8" : 242.33, "k2t12" : 244.91,
            "k2t181" : 294.27, "k2t191" : 294.08, "k2t201" : 294.34, "k2t211" : 293.14, "k2t182" : 93.91,
            "k2t192" : 93.73, "k2t202" : 93.73, "k2t212" : 93.91, "k2dt5t6" : -1.32, "k2dt3t4" : 5.54, 
            "01LEC01CT022": "23.8", "01LEC01CT021": "23.2", "01LEC02CT001": "241.663", "01LEC02CT002": "243.4245",
            "01LEC02CT003": "227.4688", "01LEC02CT004": "215.0447", "01LEC02CT005": "232.25", "01LEC02CT006": "225.6014",
            "01LEC01CT181": "77.29478", "01LEC01CT191": "77.00449", "01LEC02CT201": "76.95843", "01LEC02CT211": "76.5208", 
            "01LEC11CT181": "294.9173", "01LEC11CT191": "294.8793", "01LEC12CT201": "294.8161", "01LEC12CT211": "294.5023", 
            "01LEC01CT007": "269.9237", "01LEC01CT008": "292.9348", "01LEC01CT009": "292.5246", "01LCM11CT001": "293.3338",
            "01LEC01CT011": "292.4903", "01LEC01CT012": "290.867", "01LEC01CT013": "292.7522", "01LCM31CL001": "0.025089", 
            "01LCM21CL001": "92.51619", "01LCM22CL001": "0.517215", "01LCM11CL001": "0", "00LCM11CL001": "10.9",
            "00LCM51CL001": "23.07075", "01LMP01DS001": "0", "01LMP02DS001": "0", "01LMP03DS001": "0", "01LMN01DS001": "0", 
            "00LCM01CP001": "0.198825", "00LEC01CP001": "2.298314", "01LEC01CP005": "2.843902", "00LWP01CP005": "2.295872", 
            "01LEC02CP001": "0.001755", "01LEC01CP001": "-0.00267", "01LCM11CP001": "2.805752", "01LEC02CP002": "0.004196", 
            "01LEC02CP004": "0.001755", "01LEC02CP006": "0.002594", "01LMP01CP003": "-0.000238", "01LMP02CP003": "0.004864", 
            "01LMP03CP003": "0.003481", "01LEC02CP003": "0.004053", "01LEC02CP005": "0.003204", "01LAV01CP002": "0.00206", 
            "01LEC01CP006": "0.000458", "01LEC01CP016": "0.006027", "01LEC01CP007": "2.655065", "01LMN01CP003": "2.986962", 
            "01LAW04CP002": "0.003529", "01LAW04CP001": "-0.007019", "01LMN04CP004": "-0.000458", "01LAW01CP002": "0.007296", 
            "01LAW02CP002": "0.015974", "01LMP01CP004": "0.002365", "01LAW01CP001": "0.005102", "01LMP02CP004": "0.002432", 
            "01LAW02CP001": "0.017786", "01LMP03CP004": "0.003281", "01LCL01CP001": "-0.115969", "01LEC01CP004": "0.000763", 
            "01LCL02CP001": "-0.045776", "01LEC01CP014": "0.004044", "01LEC02CP014": "0.004959", "01LEC01CP011": "0.004501",
            "01LEC01CP008": "3.284508", "01LEC01CP012": "0.003281", "01LEC01CP010": "0.007439", "01LCM21CP001": "0.015259", 
            "01LEC01CP101": "7.6*E-05", "01LEC01CP102": "0.002518", "01LEC01CP009": "0.03624", "00LCM51CP001": "0.199664", 
            "00LCM01CP002": "11.05333" 
            ,    "LD1": 0.35119,    "LD2": 1.099206,    "LD3": 0.747024,    "LDD1": -0.007439,    "LDD2": -0.011635,    "LT1": 290.623796,    "LT2": 269.516873,    "LT2d": 290.493386,    "LT3": 285.065231,    "LT3d": 263.202925,    "LT4": 342.209633,    "RD1": 0.008927,    "RD2": 0.683532,    "RD3": 0.698413,    "RDD1": -0.005436,    "RDD2": 0.005245,    "RT1": 308.813574,    "RT2": 306.647215,    "RT2d": 287.712732,    "RT3": 289.205933,    "RT3d": 289.925169,    "RT4": 288.201721 }
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
wrok = 0
insatData='{"status":"empry"}'
lastInsatData = {}

startTime = time.strftime("%Y %m %d %H:%M:%S ")
# print(str(startTime))

for a in orignames:
    if a.isalpha():
        res += '*'+a
    else:
        res += a
names = res        
       
names = names.split(' ')
orignames = orignames.split(' ')
# print(str(names))
# print(str(orignames))

all_vars = {}
 
def run_flask():

    app = Flask(__name__)
    @app.route('/', methods=['GET'])
    def showStartTime():

        resp = make_response(str(startTime),200)
        resp.headers['content-type']='text/html'
        resp.headers['Access-Control-Allow-Origin']= '*'
        resp.headers['Access-Control-Allow-Methods'] ='GET, POST, PUT, DELETE, OPTIONS'
        return resp    

    @app.route('/insatdata', methods=['GET'])
    def get_alldata():
        resp = make_response(insatData,200)
        resp.headers['content-type']='text/html'
        resp.headers['Access-Control-Allow-Origin']= '*'
        resp.headers['Access-Control-Allow-Methods'] ='GET, POST, PUT, DELETE, OPTIONS'
        return resp    

    
    @app.route('/add', methods=['POST'])
    def add():
        global wrok
        global insatData, lastInsatData
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
            ldata[orignames[ind]]= sval.replace(',','.')

            
            
                
        #print( len(data.decode('UTF-8') ))
        lastInsatData = ldata.copy()
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
        resp = make_response('ok')
        resp.headers['content-type']='text/html'
        resp.headers['Access-Control-Allow-Origin']= '*'
        resp.headers['Access-Control-Allow-Methods'] ='GET, POST, PUT, DELETE, OPTIONS'
        return resp 
#    if __name__ == '__main__':
        # //from flask.logging import default_handler
        # app.logger.removeHandler(default_handler)
    print('app run')
    app.run(debug=False,host="0.0.0.0",port=9010)

 
def getHTTP():
    
    while (True):
        
        url = "http://159.93.126.233:9090/get_current&callback=?";
        url = "http://10.0.10.103:9092/get_current&callback=?";
        
        try:
            response = requests.get(url)
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
            
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            continue
            
        print('Success!http://159.93.126.233/')        
        res = response.text[1:-4].strip()
        print(res)
        indict = json.loads(res)
        print(indict)
        for i in indict:
            # print('el='+i+' '+str(indict[i]))
            try:
                var = all_vars[i]
                var.set_value(indict[i])
                # print('set '+i+' ok')
            except :
                print('set '+i+' exception')
                continue
        time.sleep(1)
            
# thread_flask  = threading.Thread(target=run_flask, args=())
# thread_flask.start()
    
server = Server()
server.set_endpoint(URL)
 
objects   = server.get_objects_node()
ns        = server.register_namespace("KGU")
ns1        = server.register_namespace("KGU1")
ns2        = server.register_namespace("KGU2")
kgu = objects.add_object(ns, "KGU")    
newval = []
value =1

# for name in all_data:
#     value  = kgu.add_variable(ns, name, 0.0)
for name in all_data:
    if name.find('k1')==0: 
        value  = kgu.add_variable(ns2, name, 0.0)
    else:
        value  = kgu.add_variable(ns1, name, 0.0)
    all_vars[name]=value
print(all_vars)
vvars = kgu.get_variables()    
print(type(vvars).__name__)
for i in vvars:
    # print((i.get_display_name().Text))
    print(str(i.get_browse_name()))
print('res =============')    
get_websrv  = threading.Thread(target=getHTTP, args=())
get_websrv.start()


server.start()
 
V = 220.0
while True:            

    time.sleep(1.33)
 
server.stop()
