import cv2
import os
import io
import requests
import json
url_api = "https://api.ocr.space/parse/image" 
# keys : 085b54acf688957 , ecb470d5e888957

def table_data_extract(image_file,actcolumns):
    _, compressedimage = cv2.imencode(".jpg", image_file)
    file_bytes = io.BytesIO(compressedimage)
    try:
        result = requests.post(url_api,
                        files={"screenshot.jpg": file_bytes},
                               data={"apikey": "085b54acf688957",  "language": "eng", "isOverlayRequired": False, "detectOrientation": False, 'isTable': True, "scale": True})  # get your api key at https://ocr.space/OCRAPI
    except Exception as e:
        return None
    result = result.content.decode()
    result = json.loads(result)
    allitems = []
    if result != None and "ParsedResults" in result:
        if len(result.get("ParsedResults"))==0:
            return None
        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        table_items = text_detected.strip().split('\n')
        for item in table_items:
            fields = item.strip().split('\t')
            if len(fields) == actcolumns:
                flag=0
                for ele in fields:
                    if ele == "" or " " in ele:
                        flag=1
                        break
                if flag==0:allitems.append(fields)
    return allitems

def itemparser(allitems,num_columns):
    products = []
    for item in allitems:
        ll = [None for _ in range(num_columns)]
        ll[0]= item[0].lower()
        try:
            x = item[1]
            x = x.replace('$','')
            x = x.replace(',', '')
            x = x.split('.')[0]
            x=  int(x)
        except Exception as e:
            continue
        ll[1]=x
        try:
            x = int(item[2])
        except Exception as e:
            continue
        ll[2]=x
        try:
            x = item[3]
            x = x.replace('$', '')
            x = x.replace(',', '')
            x = x.split('.')[0]
            x = int(x)
        except Exception as e:
            continue
        ll[3]=x
        products.append(ll)
    return products

