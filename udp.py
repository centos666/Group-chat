# -*- coding:utf-8 -*-
import sys
import socket
import threading
import time
class rcvmsg(threading.Thread):
    try:
        def __init__(self,HOSTRCV,PORT,BUFSIZE):
            threading.Thread.__init__(self)
            self.hostrcv=HOSTRCV
            self.port=PORT
            self.bufsize=BUFSIZE
    except Exception,e:
        print "Error!%s"%e
        print "Quiting..."
        SOC.close()
        sys.exit()

    def run(self):
        global MSG
        global SOC
        self.addrrcv=(self.hostrcv,self.port)
        try:
            SOC.bind(self.addrrcv)
        except:
            print "Please modify your port!"
            print "Quiting..."
            SOC.close()
            sys.exit()
        while MSG != 2:
            try:
                self.rcvdata,self.addr=SOC.recvfrom(self.bufsize)
                print '%s :%s'%(self.addr,self.rcvdata)
            except Exception,e:
                print "Error!%s"%e
                print "Quiting..."
                SOC.close()
                sys.exit()

class sndmsg(threading.Thread):
    try:
        def __init__(self,PORT,BUFSIZE,SOC,CON):
            threading.Thread.__init__(self)
            self.port=PORT
            self.bufsize=BUFSIZE
            self.soc=SOC
            self.con=CON
    except Exception,e:
        print "Error!%s"%e
        print "Quiting..."
        SOC.close()
        sys.exit()

    def run(self):
        global MSG
        global SOC
        self.con.acquire()
        self.con.wait()
        while MSG != 2:
            if MSG == 1:
                try:
                    self.hostsnd=raw_input('Ip>>>')
                    self.addrsnd=(self.hostsnd,self.port)
                    self.snddata=raw_input("Messages>>>")
                    SOC.sendto(self.snddata,self.addrsnd)
                    MSG=0
                    self.con.notify()
                    self.con.wait()
                except Exception,e:
                    print "Error!%s"%e
                    print "Quiting..."
                    self.con.release()
                    SOC.close()
                    sys.exit()
            else:
                self.con.wait()
        self.con.release()
        print 'Quiting...'
        close()
        sys.exit()

class inputmsg(threading.Thread):
    try:
        def __init__(self,MSG,CON,SOC):
            threading.Thread.__init__(self)
            self.con=CON
            self.soc=SOC
    except Exception,e:
        print "Error!%s"%e
        print "Quiting..."
        SOC.close()
        sys.exit()

    def run(self):
        global MSG
        global SOC
        time.sleep(1)
        self.con.acquire()
        while MSG != 2:
            try:
                if MSG == 0:
                    self.keyword=raw_input(">>>")
                    self.keyword=self.keyword.strip()
                    if self.keyword=='\\t':
                        MSG=1
                        self.con.notify()
                        self.con.wait()
                    elif self.keyword=='\\q':
                        MSG=2
                        self.con.notify()
                        self.con.release()        
                    else:
                        print "Please use '\\t'"
            except Exception,e:
                print "Error!%s"%e
                print "Quiting..."
                SOC.close()
                sys.exit()

if __name__ == '__main__':
    #MSG==0时,执行input线程;MSG==1时,执行send命令;MSG==2时,退出程序
    global MSG
    global SOC
    HOSTRCV=''
    MSG=0
    PORT=7715
    BUFSIZE=4096
    SOC=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    CON=threading.Condition()
    rcv=rcvmsg(HOSTRCV,PORT,BUFSIZE)
    ipt=inputmsg(MSG,CON,SOC)
    snd=sndmsg(PORT,BUFSIZE,SOC,CON)
    print "System running..."
    print "Use '\\t' to send messages,and use '\\q' to quit!"
    rcv.start()
    ipt.start()
    snd.start()

