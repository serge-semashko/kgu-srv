import socket
sendData ='\x01\x02\x03'
print(ord(sendData[0]))

address = '10.0.10.122'
port = 502  # port number is a number, not string
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
try:
    sock.connect((address, port)) 
    print("Connect")
    sock.settimeout(3)
    #                 id tran    proto       len        addr  fun    addr reg   reg count
    sendData = bytes([0x00,0x01, 0x00,0x00,  0x00,0x06,  0x1, 0x4, 0x00,0x0,  0x00,0x10 ,   0x0D])
    # except Exception, e: 
    res = sock.sendall(sendData)
    print(str(res))
    recBuff=[]
    num = 0
    while True:
        t=''
        if num in [0,1]:
            t='ptrans'   
        if num in [2,3]:
            t='proto'
        if num in [4,5]:
            t='len'
        if num in [6]:
            t='adr'
        if num in [7]:
            t='fun'
        if num in [8]:
            t='LEN'

        recD = sock.recv(1)
        recD = int.from_bytes(recD, "big")
        # str(type(recD))+
        if num<=8:
            print(str(recD)+' '+t)
        else:
            if (num % 2)==1:
                res=recD*256
            else:
                res+= recD
                print(str((num-8) /2)+' = '+str(res))

        # if not recD:
        #     break
        num+=1
    # but this syntax is not supported anymore. 
except Exception as e: 
    print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
finally:
    print("Close")
    sock.close()