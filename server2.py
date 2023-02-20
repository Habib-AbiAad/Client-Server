import socket
from datetime import datetime
import time


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostname()
serverSocket.bind(("", 4780)) # 4780 is the port number that i am using
serverSocket.listen(1)
print("Ready")

while True:
    connectionSocket, client_socket = serverSocket.accept() # server waits on accept() for incoming requests and a new socket is created on return
    sentence = connectionSocket.recv(4096).decode()  # contains the original request received from the client at a size of 4096 bytes
    connectionSocket.send(sentence.encode()) #send the modified request to the client who made the original request.

    try:
        for line in sentence.split("\r\n"):
            if line.startswith("Host:"):
                host = line.split(" ")[1].strip()
                break
        DestinationIp = socket.gethostbyname(host.split(":")[0]) # here we are getting the destination ip of the destination server


        print("IP: " + DestinationIp )
        print("Exact time of the request: " + datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))# to get the exact time of the request


        host = socket.gethostname() # here we are reinitialising host because it was slip before(to get the destination ip)

        request = sentence.replace(f"Host: {host}", f"Host: {DestinationIp}") # here we are copying the original request and replacing the host with the destination ip

        request_bytes = request.encode('utf-8') # this had to be use to send the modified request to the destination server.

        # Send the modified request to the destination server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as destination_socket:
            destination_socket.connect((DestinationIp, 80)) # this is done to establish a TCP connetion to the destination server
            destination_socket.send(request_bytes) # here we are sending the modified request to the destination server throught the TCP connection

            # Receive the response from the destination server
            response = b''
            while True:
                data = destination_socket.recv(4096) # here the destination socket is receiving data with a capacity of 4096 bytes
                if not data:
                    break
                response += data # here we are storing all the data in the response

        connectionSocket.send(response) # here we are sending the response from the destination server back to the client

        print("Response received at " + datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) # here we are getting the reponse time

    except Exception as e:
        print("Error connecting to destination server: {}".format(e))
        ErrorToBeSent = "Error connecting to destination server. Try again later.".encode()
        connectionSocket.send(ErrorToBeSent) # here we are sending an error if there is a problem connecting to the server

    connectionSocket.close()  # close connection to this client


    # the syntax for finding the exact time were taking for outside source (google) because the time were in Unix time
    # so i converted it into date time