#Holatu
Testing how to create a deb package 

#Links
http://askubuntu.com/questions/90764/how-do-i-create-a-deb-package-for-a-single-python-script

#To create pkg:
debuild -uc -us

#To sign try:
debuild -S -rfakeroot -k<your_gpg_key_id>

