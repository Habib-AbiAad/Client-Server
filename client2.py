import socket
from datetime import datetime
import time
import uuid

website_ip=input("Enter the website ip :")
# Connect to the proxy server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('127.0.0.1', 4780)) # the first argument is for the proxy host and the second one
    # for the proxy port

    # Send a request to the proxy server
    request = f"GET / HTTP/1.1\r\nHost: {website_ip}\r\n\r\n" # here i am using info.cern.ch because it is the best for http for me
    client_socket.send(request.encode()) # sending an HTTP request message to the proxy server using the client socket

    exact_timeSent = time.time()
    print("Request: " + request)
    print("Exact time sent: " + datetime.utcfromtimestamp(exact_timeSent).strftime('%Y-%m-%d %H:%M:%S'))

    # Receive the response from the proxy server
    response = b''
    while True:
        data = client_socket.recv(4096)   # here the client socket is receiving data with a capacity of 4096 bytes
        if not data:
            break
        response += data # here we are storing all the data in the response

    exact_timeReceived=time.time()
    print("Response: "+response.decode()) # here we have to decode the response because it is in bytes as done by the recv method
    print("Exact time received: " + datetime.utcfromtimestamp(exact_timeReceived).strftime('%Y-%m-%d %H:%M:%S'))
    print(f"Total round-trip time: {((exact_timeReceived - exact_timeSent) * 1000):.2f} ms") # round trip time

    mac_address = ':'.join(("%012X" % uuid.getnode())[i:i + 2] for i in range(0, 12, 2))
    print(f"Physical MAC address: {mac_address}")

    # the syntax for finding the exact time and the mac address were taking form an outside source (google)
