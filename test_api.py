from urllib import response
import requests

result = requests.get('http://0.0.0.0:8000/classes')
print(result.json())


result = requests.get('http://0.0.0.0:8000/description')
print(result.json())


result = requests.get('http://0.0.0.0:8000/image_batch')
print(result.json())


#download image
result = requests.get('http://0.0.0.0:8000/dataset2/shine211.jpg', stream=True)
#print(result.json())
import shutil

if result.status_code == 200:
    with open('123.jpg', 'wb') as f:
        result.raw.decode_content = True
        shutil.copyfileobj(result.raw, f)    

annotation_result = [{'imageid': 10, 'label': 1}, {'imageid': 20, 'label': 3}]
result = requests.post('http://0.0.0.0:8000/annotation_result', json=annotation_result)
print(result.json())

#test public
result = requests.get('http://192.168.1.23:8000/description')
print(result.json())

result = requests.get('http://c402-95-104-63-130.ngrok.io/description')
print(result.json())
