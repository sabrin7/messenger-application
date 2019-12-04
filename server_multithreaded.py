import socket
import threading
import queue
import time

ENCODING = 'utf-8'
HOST = ''
PORT = 8888


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__(daemon=False, target=self.run)
        self.user_id = 0
        self.ident_list = []
        self.host = host
        self.port = port
        self.histo_id= 1
        self.buffer_size = 2048
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection_list = []
        self.login_list = {}
        self.queue = queue.Queue()

        self.shutdown = False
        try:
            self.sock.bind((str(self.host), int(self.port)))
            self.sock.listen(10)
            self.sock.setblocking(False)
        except socket.error:
            self.shutdown = True

        if not self.shutdown:
            listener = threading.Thread(target=self.listen, daemon=True)
            receiver = threading.Thread(target=self.receive, daemon=True)
            sender = threading.Thread(target=self.send, daemon=True)
            self.lock = threading.RLock()

            listener.start()
            receiver.start()
            sender.start()
            self.start()


    def QUIT(self,add,string):

        for part in self.ident_list:
            x = part.split(";")
            if x[0] == str(add):
                pos = 0
                File1 = open('participant.txt', 'r')
                for participant in File1:
                    pos += 1
                    if participant.strip() == "":
                        x
                        continue;

                    else:
                        L = participant.split()

                        if (x[1] == L[0]):
                            File2 = open('participant.txt', 'r')
                            data = File2.readlines()
                            data[pos - 1] = '       ' + x[1] + '                   ' + string + '    \n'
                            File2.close()
                            File3 = open('participant.txt', 'w')
                            File3.writelines(data)
                            File3.close()
                            if (string != "connected"):
                                with open("histo.txt", "a") as myfile:
                                    myfile.write('     ' + str(self.histo_id) + '          QUIT          ' + x[
                                        1] + '          0          \n')
                                self.histo_id = +1
                File1.close()


    def UpdateRecv(self, add):

        for part in self.ident_list:
            x = part.split(";")
            if x[0] == str(add):
                pos = 0
                File1 = open('Repporting.txt', 'r')
                for participant in File1:
                    pos += 1
                    if participant.strip()== "":
                            x
                            continue;

                    else:
                        L = participant.split()

                        if (x[1] == L[0]):
                            File2 = open('Repporting.txt', 'r')
                            data = File2.readlines()
                            data[pos - 1] = '   ' + x[1] + '   ' + L[1] + '   '+ L[2] +'   ' + str(int(L[3])+1)  + '      \n'
                            File2.close()
                            File3 = open('Repporting.txt', 'w')
                            File3.writelines(data)
                            File3.close()
                File1.close()

    def  UpdateSend(self, add):
        pos = 0
        File1 = open('Repporting.txt', 'r')
        for participant in File1:
            pos += 1
            if participant.strip() == "":
                continue;

            else:
                L = participant.split()

                if (add == L[0]):
                    File2 = open('Repporting.txt', 'r')
                    data = File2.readlines()
                    data[pos - 1] = '   ' + add + '   ' + L[1] + '   ' + str(int(L[2]) + 1) + '   ' + L[3] + '      \n'
                    File2.close()
                    File3 = open('Repporting.txt', 'w')
                    File3.writelines(data)
                    File3.close()
        File1.close()





    def updateSes(self,add):

        for part in self.ident_list:
            x = part.split(";")
            if x[0] == str(add):
                pos = 0
                File1 = open('Repporting.txt', 'r')
                for participant in File1:
                    pos += 1
                    if participant.strip()== "":
                            x
                            continue;

                    else:
                        L = participant.split()

                        if (x[1] == L[0]):
                            File2 = open('Repporting.txt', 'r')
                            data = File2.readlines()
                            data[pos - 1] = '   ' + x[1] + '   ' + str(int(L[1])+1) + '   '+ L[2]  +'   ' + L[3]  + '      \n'
                            File2.close()
                            File3 = open('Repporting.txt', 'w')
                            File3.writelines(data)
                            File3.close()
                File1.close()


    def JOIN(self,add):
        x=[]
        File1 = open('participant.txt', 'r')
        data = File1.readlines()
        File2 = open('histo.txt', 'r')
        data2 = File2.readlines()
        for part in self.ident_list:
            x=part.split(";")
            if x[0] == str(add):
                self.QUIT(add, "connected")
                self.updateSes(add)
                with open("histo.txt", "a") as myfile:
                    myfile.write('     ' + str(self.histo_id) + '          JOIN          ' + str(x[1]) + '          0          \n')
                self.histo_id = +1
                return

        with open("Repporting.txt", "a") as myfile:
            myfile.write('   ' +str(self.user_id) + '       1            0            0       \n')

        data.append('       ' + str(self.user_id) + '                   Connected ' + '    \n')
        File1.close()
        File1 = open('participant.txt', 'w')
        File1.writelines(data)
        File1.close()
        File2.close()
        with open("histo.txt", "a") as myfile:
            myfile.write('     ' + str(self.histo_id) + '          JOIN          '+ str(self.user_id) +'          0          \n')
        self.histo_id = +1


    def id_getter(self, add):

        for part in self.ident_list:
            x = part.split(";")
            if x[0] == str(add):
                return x[1]

    def run(self):
        """Main thread method"""
        print("Enter \'quit\' to exit")
        while not self.shutdown:
            message = input()
            if message == "quit":
                self.sock.close()
                open("participant.txt", 'w').close()
                open("histo.txt", 'w').close()
                open("Repporting.txt", 'w').close()
                self.shutdown = True

    def listen(self):
        """Listen for new connections"""
        print('Initiated listener thread')
        while True:
            try:
                self.lock.acquire()
                connection, address = self.sock.accept()
                connection.setblocking(False)
                if connection not in self.connection_list:
                    self.connection_list.append(connection)
                    self.user_id += 1
                    self.JOIN(address[0])
                    print(address[0])

                    self.ident_list.append(str(address[0])+";"+str(self.user_id))

                    """JOIN"""

            except socket.error:
                pass
            finally:
                self.lock.release()
            time.sleep(0.050)

    def receive(self):
        """Listen for new messages"""
        print('Initiated receiver thread')
        while True:
            if len(self.connection_list) > 0:
                for connection in self.connection_list:

                    try:
                        self.lock.acquire()
                        data = connection.recv(self.buffer_size)

                    except socket.error:
                        data = None
                    finally:
                        self.lock.release()

                    self.process_data(data, connection)


    def send(self):
        """Send messages from server's queue"""
        print('Initiated sender thread')
        while True:
            if not self.queue.empty():
                target, origin, data = self.queue.get()
                message = data.decode(ENCODING)
                message1 = message.split(";", 3)

                ta_int = "*"
                oa_int = self.id_getter(HOST)
                if origin != 'server':
                    origin_address = self.login_list[origin]
                    oa = origin_address.getpeername()[0]
                    oa_int = self.id_getter(oa)
                if target != 'all':
                    target_address = self.login_list[target]
                    ta = target_address.getpeername()[0]
                    ta_int = self.id_getter(ta)


                if target == 'all':

                    self.send_to_all(origin, data)
                    if (message1[0] == "msg"):
                        with open("histo.txt", "a") as myfile:
                            myfile.write('     ' + str(self.histo_id) + '          SEND          ' + str(
                                oa_int) + '          '+ str(ta_int) +'          \n')
                        self.histo_id = +1


                else:
                    self.send_to_one(target, data)
                    if (message1[0] == "msg"):
                        with open("histo.txt", "a") as myfile:
                            myfile.write('     ' + str(self.histo_id) + '          SEND          ' + str(
                                oa_int) + '          ' + str(ta_int) + '          \n')
                        self.histo_id = +1
                        self.UpdateSend(oa_int)

                self.queue.task_done()
            else:
                time.sleep(0.05)

    def send_to_all(self, origin, data):
        """Send data to all users except origin"""
        if origin != 'server':
            
            
            
            
            
            
            
            
            
            
            
            
            
            origin_address = self.login_list[origin]
        else:
            origin_address = None

        for connection in self.connection_list:
            if connection != origin_address:
                try:
                    self.lock.acquire()
                    connection.send(data)
                except socket.error:
                    self.remove_connection(connection)
                finally:
                    self.lock.release()




    def send_to_one(self, target, data):
        """Send data to specified target"""
        target_address = self.login_list[target]

        try:
            self.lock.acquire()
            target_address.send(data)
        except socket.error:
            self.remove_connection(target_address)
        finally:
            self.lock.release()

    def process_data(self, data, connection):
        """Process received data"""
       # print(connection.getpeername())
        if data:
            message = data.decode(ENCODING)
            ms=message
            message = message.split(";", 3)

            if message[0] == 'login':
                tmp_login = message[1]

                while message[1] in self.login_list:
                    message[1] += '#'
                if tmp_login != message[1]:
                    prompt = 'msg;server;' + message[1] + ';Login ' + tmp_login \
                             + ' already in use. Your login changed to ' + message[1] + '\n'
                    self.queue.put((message[1], 'server', prompt.encode(ENCODING)))

                self.login_list[message[1]] = connection

                print(message[1] + ' has logged in')

                self.update_login_list()

            elif message[0] == 'logout':
                self.connection_list.remove(self.login_list[message[1]])
                if message[1] in self.login_list:
                    del self.login_list[message[1]]
                print(ms)
                print(message[1] + ' has logged out')
                self.QUIT(connection.getpeername()[0],"disconnected")
                self.update_login_list()

            elif message[0] == 'msg' and message[2] != 'all':
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                print(data)
                self.queue.put((message[2], message[1], data))
                oa = connection.getpeername()[0]
                oa_int = self.id_getter(oa)
                target_address = self.login_list[message[2]]
                ta = target_address.getpeername()
                ta_int = self.id_getter(ta)
                if message[2] != message[1]:
                    self.UpdateRecv(oa)
                    with open("histo.txt", "a") as myfile:
                        myfile.write('     ' + str(self.histo_id) + '          RECV         ' + str(
                            oa_int) + '          ' + str(ta_int) + '          \n')
                    self.histo_id = +1


            elif message[0] == 'msg':
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                self.queue.put(('all', message[1], data))

    def remove_connection(self, connection):
        """Remove connection from server's connection list"""
        self.connection_list.remove(connection)
        for login, address in self.login_list.items():
            if address == connection:
                del self.login_list[login]
                break
        self.update_login_list()

    def update_login_list(self):
        """Update list of active users"""
        logins = 'login'
        for login in self.login_list:
            logins += ';' + login
        logins += ';all' + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING)))


# Create new server with (IP, port)
if __name__ == '__main__':
    server = Server(HOST, PORT)
