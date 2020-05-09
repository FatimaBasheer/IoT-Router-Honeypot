Things I have tried and tested here

1. Fork from blacktop/docker-cuckoo
2. installed Docker-Hub for Mac
3. Changed ports in docker-compose.yml from 80 to 81
4. Changed some port from 8000 to 8080 .. will check and mention here
5. Tried writing python code for sending executable to cuckoo and recieve log file
    a. Got CSRF authentication error
    b. extracted session CSRF token from site. Still failing
    c. Downloaded POSTMAN. Analysis showed error 403
6. Checking if recieving the log file on submitting executable
    a. initially always on PENDING status
    b. updated fork with blacktop/docker-cuckoo
    c. Changing VirtualBox configurations (basically path to VBoxManage) to /Applications/VirtualBox.app/Contents/MacOS/VBoxManage for MACOS in virtualbox.conf in 2.0, 1.2 and ./modified. Still not working :(
    d. pip3 install cuckoo & cuckoo. After downloading this, will try to change virtualbox.conf here