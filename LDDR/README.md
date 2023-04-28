# COSC522LDR



## Using Visual Studio Code
https://code.visualstudio.com/docs/python/environments


Packages: venv
	Allows you to manage separate package installations for different projects and is installed with Python 3 by default (install python3-venv if you are using a Debian-based OS)

In Visual Studio Code: 
Create a virtual envirnment call `.venv`
Ctrl+Shift+P - Python Virtual Env 

Python: Select Intrepreter (pick the virtual env)

OR 
# macOS/Linux
# You may need to run sudo apt-get install python3-venv first
python3 -m venv .venv


.\.venv\Scripts\activate 


pip3 freeze > requirements.txt


Grabbing files off the pi: 
	scp pi@10.0.0.31:/home/pi/COSC522LDR/output_5.txt .
	scp pi@10.0.0.31:/home/pi/COSC522LDR/*.txt .


also...
	sudo apt-get update 
	sudo atp-get upgrade
	sudo reboot 
	
	sudo shutdown -h now
	--the following is how to install the OpenBlas library
	sudo apt-get install libatlas-base-dev

--Run command line predictions:
	python3 PredictLDR3.py

if you are going to build the new python versions:
	sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev