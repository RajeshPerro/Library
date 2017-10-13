#! /usr/bin/python3

from socket import *    # get socket constructor and constants
import signal, os       # for Control-C handling
import struct


myHost = 'localhost'
myPort = 5432
loginSize=30
nameSize=255
msgSize=819200


sockobj = socket(AF_INET, SOCK_STREAM)

def signal_handler(signum, frame):
    print('\nCaught signal %d. Exiting...' % signum)
    exitProgram(sockobj)

signal.signal(signal.SIGINT, signal_handler)

def exitProgram(sock):
    sock.close()
    exit(0)


def clear():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':

    try:
        sockobj.connect((myHost, myPort))
    except:
        print("Cannot connect to the server")
        exit(1)

    login = ''
    clear()
    do_continue = True
    while do_continue:

        if login != '':
            print("Your are loggedin as :", login)
        else:
            print("Sorry.! Please login first to do any operation.")

        print("***************--Welcome to Virtual Library--*****************")
        print("Please input data according to the rules.")
        print("login   -  for login [type : login username]")
        print("author  -  for searching book by author [ type : author AuthorName]")
        print("title   -  for searching book by title [type : title BookTitle]")
        print("borrow  -  for borrowing a book [type : borrow Signature]")
        print("return  -  for returning a book [type : return Signature]")
        print("To exit or terminate : press Ctrl+C ")
        print("***************--Copyright @susmita saha--*****************")

        answer = input("\>")
        try:
            action, what = answer.split(' ', 1)
        except:
            action = answer
            what=''

        if action == 'login':
            login = what
            clear()
        if action == 'author' or action == 'title':
            if action == 'author': act = b'a'
            else: act = b't'
            msg = struct.pack("".join(('s', str(loginSize), 's',
                str(nameSize), 's')), act, login.encode('utf8'),
                what.encode('utf8'))
            sockobj.send(msg)
            results = sockobj.recv(msgSize).decode()
            print(results)
        if action == 'borrow':
            msg = struct.pack("".join(('s', str(loginSize), 's',
                str(nameSize), 's')), b'b', login.encode('utf8'),
                what.encode('utf8'))
            sockobj.send(msg)
            results = sockobj.recv(msgSize).decode()
            print(results)


        if action == 'return':
            msg = struct.pack("".join(('s', str(loginSize), 's',
                str(nameSize), 's')), b'r', login.encode('utf8'),
                what.encode('utf8'))
            sockobj.send(msg)
            results = sockobj.recv(msgSize).decode()
            print(results)

        if action == 'exit':
            exitProgram(sockobj)
