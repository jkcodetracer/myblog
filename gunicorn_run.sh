#!/bin/bash

# the service run when net device is running
start on net-device-up
stop on shutdown

# if process is killed, auto restart
respawn 

# enter the website root dir
chdir /home/ubuntu/sites/demo.zhengjie.tech/myblog

# run service
exec ../env/bin/gunicorn --bind unix:/tmp/demo.zhengjie.info.socket blogproject.wsgi:application

