# 2020-1-CECD3-Generator-8
RPA를 활용한 IoT 디바이스 제어 및 관리 서비스  
[웹 사이트](http://teamgenerator.pythonanywhere.com/dashboard)  
[웹 호스팅 설정 링크](https://www.pythonanywhere.com/user/teamGenerator/)
## Recent Update
* 센서값 꺾은선그래프로 시각화 기능 구현
  * Dashboard 페이지의 테이블 우측에 센서 데이터 보여주는 버튼 추가
![visualizer](https://i.imgur.com/SM2Vn4A.png)

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

## Sensor API
command getting each sensor's values by curl
```
curl --location --request GET 'http://115.68.37.90/api/logs/latest?fi' --header 'Authorizationearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIxM2M3YzhmMzYwMDAzNGExZDVhNDkzZWI5NWVkZGY4MDIwMzI4YzU4ZGM1ODMxY2JhYWI5YTU1ZTE2YTA4YTk5YWUyNzVmYmVlM2NlYTc2In0.eyJhdWQiOiIxIiwianRpIjoiYjEzYzdjOGYzNjAwMDM0YTFkNWE0OTNlYjk1ZWRkZjgwMjAzMjhjNThkYzU4MzFjYmFhYjlhNTVlMTZhMDhhOTlhZTI3NWZiZWUzY2VhNzYiLCJpYXQiOjE1NzI0Mjc0NTAsIm5iZiI6MTU3MjQyNzQ1MCwiZXhwIjoxNTg4MjM4NjUwLCJzdWIiOiIxMDAwMDAwMDAwMSIsInNjb3BlcyI6W119.IQj7AjsyRpX9Y8jJI2HJJOL221m95YRbbbX_VpvH-Nfb2NjF6w1E43qbv7tzLJqOPlsz0OkzmEDbp0405FMMan8K8Z1NdBhjaRPFDAdCaosudMUZXsovOP0buJWtoR-pcaG5MQ46wVbjBeSBJFqMzDgSrFQyjf_71Tk0MH4JLVPQVyVuTKdh_a3AWYi0BOAf6Mu31erd7i0ArkOSXeRvGnsh64qWHMuoLThy83wN7D2eTnKqHeOAbhXIJhRYWJrLI0pEzsQTy1-TC0oftKntAVVJIFx2HTOyHnCacgA2MVv8SKDu_Y6ZAoFkDv9t0KjsB7ZQKesoGUA5VHDOVdyQvtivCaNBJRLqF6r6DJhM8qP4AyDooZ5x9kfBV607MeKGm6dSFx-2EBKyqB9HSyjEBq-kD5S_iJ4Vw7MGHsh8qHjivUNXMYXcY70jktfk-OMeQ4EZz1J5WMur1jsU4rTaVFipWaF7l4-Q4kfsnBS4nMt6Gq3mCFgjEkgF0QfhpPYiNEUcpmUqG61wfgl1TQ6q2OPvYtpsxVff89TLvXriV0CfBePlw6rfr3hg8wZnkH0P7BirGA6RfTHDlXOG6432528pgZeowYpJtQBmey1iP7P1aQGmIeeeWrI2RbM8Eat_oQMoT0RShx66lmKlg8zxaXsDDSWcfdYlRC53s_0RfNE' -w %{http_code} -o response.json
```

## Reference
[Django Tutorial](https://tutorial.djangogirls.org/ko/installation/)   
[Sensor API Docs](https://documenter.getpostman.com/view/527712/SW14WcyW?version=latest#9b1079ca-8760-457f-8e38-bb8f6b8ef6ad)   
[django_table2 Docs](https://django-tables2.readthedocs.io/en/latest/)   

## Demo
### Dashboard 화면
![dashboard](/res/dashboard.png)
### 층별 표 출력 화면
![dashboard_map](/res/floorview_table.png)
### 층별 약도 출력 화면
![dashboard_map](/res/floorview_map.png)
### Monitoring 출력 화면
![monitoring](/res/monitoring.png)