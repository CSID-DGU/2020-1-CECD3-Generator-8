# AWS 가이드 문서

## 인스턴스 정보
* Type: EC2 t2.2xlarge  
* Public IPv4 DNS: ec2-54-158-177-31.compute-1.amazonaws.com
* Public IPv4 address: 54.158.177.31

## 파일 구조
.  
├── /srv/www/django/  
│   ├── run/  
│   │   └── uwsgi.sock  
│   ├── ini/  
│   │   └── uwsgi.ini  
│   ├── logs/  
│   │   ├── dev-nginx-access.log  
│   │   ├── dev-nginx-errors.log  
│   │   └── uwsgi.log  
│   ├── venv/  
│   └── 2020-1-CECD3-Generator/  
│
└── /etc/  
    ├── systemd/  
    │   └── system/  
    │       └── uwsgi.service  
    └── nginx/  
        └── sites-available/  
            └── default  

## 명령어
Connect with SSH
```
chmod 400 generator_django_aws.pem # 읽기가 안 될 때만
ssh -i "generator_django_aws.pem" ubuntu@ec2-54-158-177-31.compute-1.amazonaws.com
```
***
Update web setting files
```
source aws_files/update_aws_settings.sh
```
***
screen commands
| Command                | Description                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------- |
| screen -list           | List all screens                                                                      |
| screen -r [SCREEN_NUM] | Connect to the screen whose number is SCREEN_NUM                                      |
| Ctrl + a, w            | List windows of this screen                                                           |
| Ctrl + a, c            | Create a new window (bash)                                                            |
| Ctrl + a, a            | Go to previous window                                                                 |
| Ctrl + a, d            | Exit from this screen                                                                 |
| exit                   | Terminate this window (if all windows are terminated, the screen will be deleted too) |


## Reference
[장고 - EC2에 장고 배포하기](https://chohyeonkeun.github.io/2019/06/06/190606-django-EC2-django-deploy/)
[EC2 인스턴스 세팅과 Nginx + uWSGI로 Django 앱 배포하기 (2/2)](https://rainsound-k.github.io/deploy/2018/05/02/instance-setting-and-django-deploy-part2.html)
