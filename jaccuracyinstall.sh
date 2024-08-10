#!/bin/bash

#Jaccuracy Scope Installation Bash Script
#Hello! If you edit this installing script, use the following: 
#compile with: sudo chmod +x JaccuracyInstaller.sh
#execute with: sudo ./JaccuracyInstaller.sh
#Don't forget the sudo!



#Commented out updates/Upgrades for user to do. 
#needs: updates and  upgrade
#echo "Starting System Update for Packages..."
#apt update
#apt upgrade 



#edit the boot/config.txt to pullup resisitors 
#gpio=6,19,5,23,24,26,13,21,20,16=pu

if ! grep -q 'gpio=6,19,5,23,24,26,13,21,20,16=pu' /boot/config.txt
then 
echo "
gpio=6,19,5,23,24,26,13,21,20,16=pu
" | sudo tee -a /boot/config.txt
fi 





####################################################
# _______  _____  _______          
#|_   __ \|_   _||_   __ \         
#  | |__) | | |    | |__) |.--.    
#  |  ___/  | |    |  ___/( (`\]   
# _| |_    _| |_  _| |_    `'.'.   
#|_____|  |_____||_____|  [\__) )                                  
###################################################
#WORKS? Pip Prep (since its 'externally managed...') 
rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

#PIP installs for Python 3.11 
echo "Starting pip installs" 
apt install -y python3-picamera2
pip install adafruit-circuitpython-lsm6ds 
pip install numpy 
pip install pillow 
pip install st7789 
pip install ctypes 
pip install adafruit-circuitpython-thermal-printer 
apt install -y python3-pil.imagetk 
apt install -y python3-libcamera 
pip3 install adafruit-circuitpython-seesaw 
pip install --force-reinstall numpy==1.26.4  
#1.18.5



##Fix for SPidev installation buffer size setting.
###edit the start command line with new buff size 
#5: had to add 65536
# spidev.bufsiz=65536  /boot/cmdline.txt
#cat /sys/module/spidev/parameters/bufsiz 
#need an if statement if it doesn't include this thang...
#echo -n "spidev.bufsiz=65536" >> /boot/cmdline.txt



#Seems to work! 

if ! grep -q 'spidev.bufsiz' /boot/cmdline.txt
then
#echo -n "YouNeedToLeave" |> /boot/cmdline.txt
sed -i 's/$/ \spidev.bufsiz=65536/' /boot/cmdline.txt
echo "Ok wrote to the thang."
else
echo "Boot CMDline.txt File did not write, already there? Check with cat"
fi

echo "Ok done"
echo "The Spiddev buffer size is set to:"
cat /sys/module/spidev/parameters/bufsiz





########################################################
#  ______        _       ____    ____  ______        _       
#.' ____ \      / \     |_   \  /   _||_   _ \      / \      
#| (___ \_|    / _ \      |   \/   |    | |_) |    / _ \     
# _.____`.    / ___ \     | |\  /| |    |  __'.   / ___ \    
#| \____) | _/ /   \ \_  _| |_\/_| |_  _| |__) |_/ /   \ \_  
# \______.'|____| |____||_____||_____||_______/|____| |____|
#########################################################
#WORKS?   samba share directory woo  

samba_not_installed=$(dpkg -s samba 2>&1 | grep "not installed")
if [ -n "$samba_not_installed" ];then
  echo "Installing Samba"
  sudo apt-get install samba -y
  sudo apt-get install samba-common-bin
fi


mkdir /home/pi/share
#mkdir /home/pi/share/Display


#if for configure share folder 
#This will add these lines of code the configure script 
if ! grep -q '\[ScopeShare\]' /etc/samba/smb.conf
then 
echo "
[ScopeShare]
path = /home/pi/share
writeable=Yes
create mask=0777
directory mask=0777
public=Yes
force user =pi 
force group =pi 
" | sudo tee -a /etc/samba/smb.conf
fi 

#give permission lol 
chmod -R 777 /home/pi/share


echo "Enter the Same Password for your Pi here for permissions: "
sudo smbpasswd -a pi


#restart service after configure 
sudo systemctl restart smbd


# Message to the User
 echo "Samba Sharing set up! Use a computer or Phone to access files"
 echo "To access the shared machine, enter \\[your ip address]"


#################### STOP HERE TO MAKE USER MOVE FILES OVER 


#########################################################              
#|_   __  |(_) [  |               
#  | |_ \_|__   | | .---.  .--.   
#  |  _|  [  |  | |/ /__\\( (`\]  
# _| |_    | |  | || \__., `'.'.  
#|_____|  [___][___]'.__.'[\__) ) 
#########################################################                                

#once all of this is ready.... 
#copy files over to the pi

#1. go into the 0.100 folder and compile the ballistics 
 #Works
 cd /home/pi/share/JaccuracyScope/Display/Balls
 gcc -fPIC -shared -o GNUball3.so exportme3.c -lm
 cp /home/pi/share/JaccuracyScope/Display/Balls/GNUball3.so /home/pi/share/JaccuracyScope/Display/
 
#2. go into the SPIDev folder and install the new modified files with 
 #works 
 cd /home/pi/share/JaccuracyScope/modded_spidev-3.6
 python3 setup.py install
 cd 
 #takes back to executed place

#3. edit the st7789 libary... based on python version installed 
#used to edit the ST7789 Library 
#This will edit the ST7789 Installation to replace the 
#SPI buffer limit of 4096 with 655539 or whateverrrr
#This allows the TFT screen to run at lightning speeds :) 
echo "Starting to Modify the ST7789 Library"

#Go into the ST7789 folder path and change functions to FASTDISPLAY and such at /usr/local/lib/python3.11/dist-packages/ST7789 
		#just replace the original file with this one.... check the python version first?

#this sucks for checking python version....
 
ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" == "31" ]; then
    ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\)\([0-9]\).*/\1\2\3/')
    echo "file lives in /usr/local/lib/python3.11/dist-packages/ST7789"
    cp /home/pi/share/JaccuracyScope/st7789mod/__init__.py /usr/local/lib/python3.11/dist-packages/st7789
elif [ "$ver" == "39" ]; then
    echo "file lives in /usr/local/lib/python3.9/dist-packages/ST7789"
    cp /home/pi/share/JaccuracyScope/st7789mod/__init__.py /usr/local/lib/python3.9/dist-packages/st7789
fi


#mine existed here for some reason! super weird, that didnt happen before.. check this works ! 
#cp /home/pi/share/JaccuracyScope/st7789mod/__init__.py /home/pi/.local/lib/python3.11/site-packages/st7789 





#For User to Install Manually: 


########################################################
#   ______                           _          __        
# .' ___  |                         / |_       [  |       
#/ .'   \_| _ .--.   .--.   _ .--. `| |-',--.   | |.--.   
#| |       [ `/'`\]/ .'`\ \[ `.-. | | | `'_\ :  | '/'`\ \ 
#\ `.___.'\ | |    | \__. | | | | | | |,// | |, |  \__/ | 
# `.____ .'[___]    '.__.' [___||__]\__/\'-;__/[__;.__.'  
########################################################                                                         


#Checking the crontab for its 
#sudo crontab -e
#@reboot cd /home/pi/share/Display && python3 disptest_cameraonlyzoom.py & 
#maybe do this manually ......... after all installs...........


#########################################################                  
#   ___                              ______  ____   ____  
# .'   `.                          .' ___  ||_  _| |_  _| 
#/  .-.  \ _ .--.   .---.  _ .--. / .'   \_|  \ \   / /   
#| |   | |[ '/'`\ \/ /__\\[ `.-. || |          \ \ / /    
#\  `-'  / | \__/ || \__., | | | |\ `.___.'\    \ ' /     
# `.___.'  | ;.__/  '.__.'[___||__]`.____ .'     \_/      
#         [__|   
########################################################
#OpenCV install for Python 3.11 (Takes a while) 
#from https://www.instructables.com/Install-OpenCV-on-Raspberry-Pi-in-Less-Than-10-Min/

#echo "Starting CV2 Headless install... takes a while"

#edit the swap size from 100 to 2048  CONF_SWAPSIZE=1024
#location: /etc/dphys-swapfile

#reboot 


#
#sudo pip install opencv-contrib-python==4.5.3.56
#pip install opencv-python-headless
#pip install opencv-contrib-python==3.4.6.27


#### Ignoring this to install open CV separately due to how long it takes... 



########################################################   
#Pi 5 is not recommended as the GPIO frame rate blows... you will need to run these if you have a Pi 5.  just expect bad performance on the display.

#apt remove python3-rpi.gpio
#pip3 install rpi-lgpio



