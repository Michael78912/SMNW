#!/bin/bash

# install stickmanranger on the machine.
echo "stickmanranger installation for linux... "
installer='a'

if [ "$(whoami)" != "root" ]
then
	echo please enter your password to install stickmanranger
    sudo su -s "$0"
    exit
fi

function copy_dir(){
	dir_install=/opt/stickmanranger
	custom_dir=$dir_install

	cd ..
	if [ -d stickmanranger ]
	then
		cp -r stickmanranger $custom_dir
	fi

	echo installation complete
}

function shortcut(){
	echo create desktop shortcut?
	read choice
	if [ $choice = 'y' ] || [ $choice = 'Y' ]
	then
		echo please enter your user name:
		read name
		home='/home/$name/Desktop'
		ln launcher.desktop $home
	fi
}

until [ $installer = 'y' ] || [ $installer = 'n' ] || [ $installer = 'Y' ] || [ $installer = 'n' ]
do
	echo "install? [y/n]"
	read installer
done

if [ $installer = 'y' ] || [ $installer = 'Y' ]
then
	copy_dir
fi



