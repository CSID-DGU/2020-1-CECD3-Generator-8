# 2020-1-CECD3-Generator-8

## 1. Installation (Linux)
### 1.1. Django project
#### 1. Check python3 version
```
python3 --version
```
*Python 3.6.9* or later
***
#### 2. Make a virtual environment
```
cd djagno_iot
python3 -m venv venv # Make a virtual environment named 'venv'
```
***
#### 3. Check venv's default python version
```
source venv/bin/activate # Activate venv
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
 Activating / Deactivating virtual environment
   > Activating
   > ```
   > source venv/bin/activate
   > ```
   > Deactivating
   > ```
   > (venv) deactivate
   > ```
***
 Running web server (default: http://127.0.0.1:8000)
 ```
 (venv) python manage.py runserver
 ```
 ***
 Collecting static files
 ```
 (venv) python manage.py collectstatic
 ```
 ***
 Running django shell
 ```
 (venv) python manage.py shell
 ```
 ***
 After update models.py (Migrating to database)
 ```
 (venv) python manage.py makemigrations [APP_NAME]
 (venv) python manage.py migrate [APP_NAME]
 ```

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
### Main Page
![Alt test](/res/main_page.png)