![Screenshot](img/pplogo64.png?raw=true)
# TrivialPiper
TFTP (Trivial File Transfer Protocol) GUI client implemented with Pyqt5 
Based on the client and server implementation of pyTFTP (https://github.com/m4tx/pyTFTP)

![Screenshots](img/trivialpiper-client.png?raw=true)

## Features
RFCs supported:
* 1350 - The TFTP Protocol (Revision 2)
* 2347 - TFTP Option Extension
* 2348 - TFTP Blocksize Option
* 7440 - TFTP Windowsize Option

Additional features:
* Block ID rollover for sending large files

Limitations:
* Only octet transfer mode is supported
* Timeouts will work incorrectly in case of a malicious client sending invalid
  packets (after receiving an invalid packet, the timeout timer will be reset)

## Requirements
* Python 3.6+
* PyQT5

Installing Pyqt5 on Debian/Ubuntu based systems:
```sudo apt install python3-pip
pip3 install pyqt5
```


## Usage

Client:
```
python3 trivialPiper.py
```
Server:
```
server.py [-p <port>] <server-root>
```
Example:
```
python server.py -H 192.168.2.20 -p 69 -u /home/user/server
```

You can also use the original CLI mode for the client

CLI Client:
```
client.py -g <filename> <server-hostname> [port]
```
Use `-p` instead of `-g` to upload (`--put`) the file instead of downloading
(`--get`).



There is also `--help` option available that explains all the options
available, such as block and window size for the client and disabling uploads
for the server.
