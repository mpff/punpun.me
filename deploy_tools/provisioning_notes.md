Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.
* virtualenv + pip
* Git

on Ubuntu:
    
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.conf.j2
* replace {{ host }} with, e.g., staging.my-domain.com
* replace {{ ansible_user }} with, e.g., username

## Systemd service

* see gunicorn.service.j2
* replace {{ host }} with, e.g., staging.my-domain.com
* replace {{ ansible_user }} with, e.g., username 

## Folder structure:

Asume we have a user account at /home/username

```/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
```
