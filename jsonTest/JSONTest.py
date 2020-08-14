import json
import requests

url = "http://115.68.37.90/api/logs/latest"

payload = {}
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIxM2M3YzhmMzYwMDAzNGExZDVhNDkzZWI5NWVkZGY4MDIwMzI4YzU4ZGM1ODMxY2JhYWI5YTU1ZTE2YTA4YTk5YWUyNzVmYmVlM2NlYTc2In0.eyJhdWQiOiIxIiwianRpIjoiYjEzYzdjOGYzNjAwMDM0YTFkNWE0OTNlYjk1ZWRkZjgwMjAzMjhjNThkYzU4MzFjYmFhYjlhNTVlMTZhMDhhOTlhZTI3NWZiZWUzY2VhNzYiLCJpYXQiOjE1NzI0Mjc0NTAsIm5iZiI6MTU3MjQyNzQ1MCwiZXhwIjoxNTg4MjM4NjUwLCJzdWIiOiIxMDAwMDAwMDAwMSIsInNjb3BlcyI6W119.IQj7AjsyRpX9Y8jJI2HJJOL221m95YRbbbX_VpvH-Nfb2NjF6w1E43qbv7tzLJqOPlsz0OkzmEDbp0405FMMan8K8Z1NdBhjaRPFDAdCaosudMUZXsovOP0buJWtoR-pcaG5MQ46wVbjBeSBJFqMzDgSrFQyjf_71Tk0MH4JLVPQVyVuTKdh_a3AWYi0BOAf6Mu31erd7i0ArkOSXeRvGnsh64qWHMuoLThy83wN7D2eTnKqHeOAbhXIJhRYWJrLI0pEzsQTy1-TC0oftKntAVVJIFx2HTOyHnCacgA2MVv8SKDu_Y6ZAoFkDv9t0KjsB7ZQKesoGUA5VHDOVdyQvtivCaNBJRLqF6r6DJhM8qP4AyDooZ5x9kfBV607MeKGm6dSFx-2EBKyqB9HSyjEBq-kD5S_iJ4Vw7MGHsh8qHjivUNXMYXcY70jktfk-OMeQ4EZz1J5WMur1jsU4rTaVFipWaF7l4-Q4kfsnBS4nMt6Gq3mCFgjEkgF0QfhpPYiNEUcpmUqG61wfgl1TQ6q2OPvYtpsxVff89TLvXriV0CfBePlw6rfr3hg8wZnkH0P7BirGA6RfTHDlXOG6432528pgZeowYpJtQBmey1iP7P1aQGmIeeeWrI2RbM8Eat_oQMoT0RShx66lmKlg8zxaXsDDSWcfdYlRC53s_0RfNE'
}
#동국대 센서 api 연결 정보
response = requests.request("GET", url, headers=headers, data = payload)
# response: request 모듈을 이용해서 api에 연결을 요청해서 JSON데이터를 가져옴

writeFile = open('test.json','w')
writeFile.write(response.text)
#writeFile : 요청해서 받아온 데이터가 json인데 text형태라서 json 파일로 만듦 

with open('test.json','r') as f:
    json_data = json.load(f) # test.json을 f로 하여 열고 json_data에 json파일 내용을 로드함

IoTDevices = json_data['result'] # json파일 내에 result에 있는 IoT 센서 정보를 IoTDevices 배열에 저장 

for i in IoTDevices:
#DGU 0004, 07, 08, 12만 데이터를 가져올 수 있슴
# scode : 장치 코드(DGU~)
# seq : 장치 일련번호
# send_time : 마지막으로 정보를 전송받은 시각
# smodel : 장치 모델명(현재는 SME20u만 있슴)
  if i['DEVICE_SCODE'] == "DGU0004":
    scode = i['DEVICE_SCODE']
    seq = i['DEVICE_SEQ']
    send_time = i['DEVICE_DATA_REG_DTM']
    smodel = i['DEVICE_MODEL']

    #print 
    print("디바이스 모델명 : " + smodel)
    print("디바이스 코드 : " + scode)
    print("디바이스 일련번호 : " + str(seq))
    print("디바이스 마지막 로그 전송 시각 : " + send_time + "\n")
  elif i['DEVICE_SCODE'] == "DGU0007":
    scode = i['DEVICE_SCODE']
    seq = i['DEVICE_SEQ']
    send_time = i['DEVICE_DATA_REG_DTM']
    smodel = i['DEVICE_MODEL']

    #print 
    print("디바이스 모델명 : " + smodel)
    print("디바이스 코드 : " + scode)
    print("디바이스 일련번호 : " + str(seq))
    print("디바이스 마지막 로그 전송 시각 : " + send_time + "\n")
  elif i['DEVICE_SCODE'] == "DGU0008":
    scode = i['DEVICE_SCODE']
    seq = i['DEVICE_SEQ']
    send_time = i['DEVICE_DATA_REG_DTM']
    smodel = i['DEVICE_MODEL']

    #print 
    print("디바이스 모델명 : " + smodel)
    print("디바이스 코드 : " + scode)
    print("디바이스 일련번호 : " + str(seq))
    print("디바이스 마지막 로그 전송 시각 : " + send_time + "\n")
  elif i['DEVICE_SCODE'] == "DGU0012":
    scode = i['DEVICE_SCODE']
    seq = i['DEVICE_SEQ']
    send_time = i['DEVICE_DATA_REG_DTM']
    smodel = i['DEVICE_MODEL']

    #print 
    print("디바이스 모델명 : " + smodel)
    print("디바이스 코드 : " + scode)
    print("디바이스 일련번호 : " + str(seq))
    print("디바이스 마지막 로그 전송 시각 : " + send_time + "\n") 
"""
DGU0012 gap : 0:10:00
DGU0004 gap : 0:10:00
DGU0008 gap : 0:10:00
DGU0007 gap : 0:09:59
"""