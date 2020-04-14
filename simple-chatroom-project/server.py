import socket
import threading

host = input('input the server ip address:')
port = 8080
data = ''

lock = threading.Condition()  #条件变量同步
s = socket.socket()
print("socket have been created")
s.bind((host, port))
s.listen(3)
print("socket is listening")

def NotifyAll(sss):
    global data
    if lock.acquire():
        data = sss
        lock.notifyAll() #如果wait状态线程比较多，notifyAll的作用就是通知所有线程
        #notify(n=1):通知其他线程，那些挂起的线程接到这个通知之后会开始运行，
        # 默认是通知一个正等待该condition的线程,最多则唤醒n个等待的线程。
        lock.release()

def threadout(conn, nike):
    global data
    while True:
        if lock.acquire():
            lock.wait() #线程挂起，直到收到一个notify通知或者超时（可选的，浮点数，单位是秒s）才会被唤醒继续运行。
                        # wait()必须在已获得Lock前提下才能调用，否则会触发RuntimeError。
                        # 调用wait()会释放Lock，直至该线程被Notify()、NotifyAll()或者超时线程又重新获得Lock.
                        #这里主要是等消息来了，再发送，没有信息来就会在这里阻塞
            if data:
                try:
                    conn.send(data.encode())
                    lock.release()
                except:
                    lock.release()
                    return
            
def threadin(conn, nike):
    while True:
        try:
            temp = conn.recv(1024).decode()
            if not temp:
                conn.close()
                return
            NotifyAll(temp)
            print(data)
        except:
            NotifyAll(nike + 'error')
            print(data)
            return

while True:
    conn, addr = s.accept()
    print("connect with" + addr[0] + ":" +str(addr[1]))
    nike = conn.recv(1024).decode()
    NotifyAll("welcome" + nike + "to the room")
    print(data)
    conn.send(data.encode())
    threading.Thread(target=threadout, args=(conn, nike)).start()
    threading.Thread(target=threadin,args=(conn, nike)).start()


