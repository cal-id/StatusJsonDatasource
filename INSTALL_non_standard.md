# Non Standard installation instructions

## Introduction

In README.md, the instructions for setting this up on python2.6, SL6
and yum are given. You should only use these instructions if:
1) you want to use pip to get the latest packages
2) you want to use python2.7 or python3+
3) you are using Ubuntu

After running these instructions you can run 'Instructions for All'
in README.md

## Using apt (Ubuntu)
```
# Install simple stuff
sudo apt install python python3 git python3-pip python-pip

# Install PostgreSQL requirements
sudo apt install libpq-dev PostgreSQL python-dev python3-dev

# Install pyldap requirements
sudo apt install libsasl2-dev python3-dev python-dev libldap2-dev libssl-dev

# Install apache
sudo apt install apache2
```

## Using yum (SL6)
```
# Install the simple stuff
# Note that on SL6, python is python2.6 not python2.7 so you must use python3
sudo yum install git python python34 python-pip
# Yum doesn't provide pip3, instead:
sudo yum install -y python34-setuptools  # install easy_install-3.4
sudo easy_install-3.4 pip

# Install PostgreSQL requirements
sudo yum install libpqxx-devel postgresql python-devel python3-devel gcc

# Install pyldap requirements
sudo yum install python-devel openldap-devel-2.4.40-12.el6 gcc
# Had to use version number because -16 depended on openldap-16 which wasn't installed

# Install apache2
sudo yum install httpd
```




