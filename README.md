# 2020-1-CECD3-Generator-8
RPA를 활용한 IoT 디바이스 제어 및 관리 서비스  
[웹 사이트](http://ec2-18-206-198-8.compute-1.amazonaws.com)
## Recent Update
* 사이드메뉴 트리구조 완성 - bootstrap의 collapse 클래스 이용

## 1. Installation
### 1.1. Django project
#### 1. Check python3 version
```
python3 --version
```
*Python 3.6.9* or later
***
#### 2. Make a virtual environment
Linux
```
cd djagno_iot
python3 -m venv venv # Make a virtual environment named 'venv'
```
Windows
```
cd djagno_iot
python -m venv .\venv
```
***
#### 3. Check venv's default python version
Linux
```
source venv/bin/activate # Activate venv
```
Windows (cmd)
```
venv\Scripts\activate.bat
```
***
```
(venv) python --version
```
*Python 3.6.9* or later
***
#### 4. Install required packages
```
(venv) python -m pip install --upgrade pip
(venv) pip install -r requirements.txt
```

## 2. Useful Commands
 Activating / Deactivating virtual environment: 장고 프로그램은 항상 가상 환경 위에서 실행되어야 함 (각종 모듈도 가상 환경에만 설치하였음)
   > Activating
   >  > Linux
   >  >```
   >  >source venv/bin/activate
   >  >```
   >  > Windows (cmd)
   >  >```
   >  >venv\Scripts\activate.bat
   >  >```
   > Deactivating
   > ```
   > (venv) deactivate
   > ```
***
Collecting logs and saving them into db: API 이용해서 json으로 긁어와 DB에 저장
```
(venv) python manage.py autocollect
```
***
Dump database into dbdump.json: 현재 데이터베이스를 dbdump.json파일로 저장
```
(venv) python manage.py dumpdata --natural-foreign --natural-primary --indent=4 -o dbdump.json
```
***
Load database from dumped file: 데이터베이스를 덤프한 파일에서 데이터베이스를 불러옴
```
(venv) python manage.py flush
(venv) python manage.py loaddata dbdump.json
```
***
 Running web server (default: http://127.0.0.1:8000)
 ```
 (venv) python manage.py runserver [PORT_NUMBER]
 ```
 ***
 Collecting static files: CSS, 이미지 파일 등 장고에 쓰이는 정적 파일들을 불러오는 명령어
 ```
 (venv) python manage.py collectstatic
 ```
 ***
 Running django shell: 장고 쉘 실행
 ```
 (venv) python manage.py shell
 ```
 ***
 After update models.py (Migrating to database)
 ```
 (venv) python manage.py makemigrations [APP_NAME]
 (venv) python manage.py migrate [APP_NAME]
 ```
***
Updating requirements.txt: 패키지를 추가하거나 삭제 등 수정이 이루어지면, 업데이트 할 것
```
(venv) pip freeze > requirements.txt
```
***
Get Log model's data in json: curl을 사용하여 Log의 데이터를 json 형식으로 가져오기
```
curl -X GET http://127.0.0.1:8000/json
```
***
Creating admin account: 어드민 페이지에 사용할 계정 새로 생성
```
(venv) python manage.py createsuperuser
```
***

## TroubleShooting
### 1. pip 에서 django-bootstrap-modal-forms 가 UnicodeDecodeError로 인하여 설치되지 않는 경우
예시
```
Collecting django-bootstrap-modal-forms==2.0.0
  Using cached django-bootstrap-modal-forms-2.0.0.tar.gz (30 kB)
    ERROR: Command errored out with exit status 1:
     command: 'C:\Users\Jongyeon Yoon\Documents\GitHub\2020-1-CECD3-Generator-8\django_iot\venv\Scripts\python.exe' -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'C:\\Users\\Jongyeon Yoon\\AppData\\Local\\Tehizd4fbo\\django-bootstrap-modal-forms\\setup.py'"'"'; __file__='"'"'C:\\Users\\Jongyeon Yoon\\AppData\\Local\\Temp\\pip-install-hizd4fbo\\django-bootstrap-modal-forms\\setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"');code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base 'C:\Users\Jongyeon Yoon\AppData\Local\Temp\pip-pip-egg-info-vz8gad2i'
         cwd: C:\Users\Jongyeon Yoon\AppData\Local\Temp\pip-install-hizd4fbo\django-bootstrap-modal-forms\
    Complete output (5 lines):
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "C:\Users\Jongyeon Yoon\AppData\Local\Temp\pip-install-hizd4fbo\django-bootstrap-modal-forms\setup.py", line 5, in <module>
        README = readme.read()
    UnicodeDecodeError: 'cp949' codec can't decode byte 0xe2 in position 24855: illegal multibyte sequence
    ----------------------------------------
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
```
해결법
1. 2020-1-CECD3-Generator-8/res/django-bootstrap-modal-forms-2.0.0 으로 이동 (인코딩 문제를 해결한 버전의 설치파일)
2. pip install . 실행

## Sensor API
command getting each sensor's values by curl
```
curl --location --request GET 'http://115.68.37.90/api/logs/latest?fi' --header 'Authorizationearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIxM2M3YzhmMzYwMDAzNGExZDVhNDkzZWI5NWVkZGY4MDIwMzI4YzU4ZGM1ODMxY2JhYWI5YTU1ZTE2YTA4YTk5YWUyNzVmYmVlM2NlYTc2In0.eyJhdWQiOiIxIiwianRpIjoiYjEzYzdjOGYzNjAwMDM0YTFkNWE0OTNlYjk1ZWRkZjgwMjAzMjhjNThkYzU4MzFjYmFhYjlhNTVlMTZhMDhhOTlhZTI3NWZiZWUzY2VhNzYiLCJpYXQiOjE1NzI0Mjc0NTAsIm5iZiI6MTU3MjQyNzQ1MCwiZXhwIjoxNTg4MjM4NjUwLCJzdWIiOiIxMDAwMDAwMDAwMSIsInNjb3BlcyI6W119.IQj7AjsyRpX9Y8jJI2HJJOL221m95YRbbbX_VpvH-Nfb2NjF6w1E43qbv7tzLJqOPlsz0OkzmEDbp0405FMMan8K8Z1NdBhjaRPFDAdCaosudMUZXsovOP0buJWtoR-pcaG5MQ46wVbjBeSBJFqMzDgSrFQyjf_71Tk0MH4JLVPQVyVuTKdh_a3AWYi0BOAf6Mu31erd7i0ArkOSXeRvGnsh64qWHMuoLThy83wN7D2eTnKqHeOAbhXIJhRYWJrLI0pEzsQTy1-TC0oftKntAVVJIFx2HTOyHnCacgA2MVv8SKDu_Y6ZAoFkDv9t0KjsB7ZQKesoGUA5VHDOVdyQvtivCaNBJRLqF6r6DJhM8qP4AyDooZ5x9kfBV607MeKGm6dSFx-2EBKyqB9HSyjEBq-kD5S_iJ4Vw7MGHsh8qHjivUNXMYXcY70jktfk-OMeQ4EZz1J5WMur1jsU4rTaVFipWaF7l4-Q4kfsnBS4nMt6Gq3mCFgjEkgF0QfhpPYiNEUcpmUqG61wfgl1TQ6q2OPvYtpsxVff89TLvXriV0CfBePlw6rfr3hg8wZnkH0P7BirGA6RfTHDlXOG6432528pgZeowYpJtQBmey1iP7P1aQGmIeeeWrI2RbM8Eat_oQMoT0RShx66lmKlg8zxaXsDDSWcfdYlRC53s_0RfNE' -w %{http_code} -o response.json
```

## Reference
### Installation & Settings
* [Django Tutorial](https://tutorial.djangogirls.org/ko/installation/)   
* [장고 - EC2에 장고 배포하기](https://chohyeonkeun.github.io/2019/06/06/190606-django-EC2-django-deploy/)
* [EC2 인스턴스 세팅과 Nginx + uWSGI로 Django 앱 배포하기 (2/2)](https://rainsound-k.github.io/deploy/2018/05/02/instance-setting-and-django-deploy-part2.html)
### Module Guide
* [Sensor API Docs](https://documenter.getpostman.com/view/527712/SW14WcyW?version=latest#9b1079ca-8760-457f-8e38-bb8f6b8ef6ad)   
* [django_tables2 Docs](https://django-tables2.readthedocs.io/en/latest/)   
* [bootstrap Docs](https://getbootstrap.com/docs/4.5/getting-started/introduction/)  
* [Kakao Map API Docs](https://apis.map.kakao.com/web/guide/)  
* [Kakao Developer Docs](https://developers.kakao.com/docs/latest/ko/)  
* [EmailJS Docs](https://www.emailjs.com/docs/)  
* [Chart.js Docs](https://www.chartjs.org/docs/latest/)  

## Demo
### Dashboard 화면
![dashboard](/res/dashboard.png)
### 데이터 시각화 화면
![dashboard_chart](/res/dashboard_chart.png)
### Monitoring 출력 화면
![monitoring](/res/monitoring.png)
### 층별 표 출력 화면
![floor_map](/res/floorview_table.png)
### 층별 약도 출력 화면
![floor_map](/res/floorview_map.png)
