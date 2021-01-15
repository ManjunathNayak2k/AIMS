import cv2,os
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import Output
from aims_.table_recog_ocrapi import table_data_extract, itemparser
import pandas as pd
import io,requests
import pandas as pd
import json,math
from aims_ import app

fields = 0
totalconf = 0

ocrspace_url_api = "https://api.ocr.space/parse/image"

def get_annotations_xlsx(path):
    df = pd.read_csv(path,header=None)
    annotate_dict = {}
    number_of_rows = df.shape[0]
    for r in range(1,number_of_rows):
        row1 = df.iloc[r,:]
        curr_row = row1.tolist()
        annotate_dict['page '+str(r+1)] = []
        label = curr_row[4]
        x1 = int(curr_row[2])
        x2 = x1 + int(curr_row[0])
        y1 = int(curr_row[3])
        y2 = y1 + int(curr_row[1])
        annotate_dict['page '+str(r+1)].append(
                    {
                        label:(x1,y1,x2,y2)
                    }
                )
    return annotate_dict

def plot_image(img):
    global fields
    global totalconf
    fields += 1
    try:
        acttext = pytesseract.image_to_string(img)
        text = pytesseract.image_to_data(img, output_type=Output.DICT)
    except Exception as e:
        return ""
    conf = 0
    validfields = 0
    extrvals = text['text']
    confvals = text['conf']
    for i in range(len(extrvals)):
        if extrvals[i] != '':
            conf += confvals[i]
            validfields += 1
    if validfields != 0:
        conf = conf//validfields
    totalconf += conf
    return acttext

def predict_invoice(path,excel_path):
    global totalconf
    img = cv2.imread(path,0)
    bboximg = np.copy(img)
    annotations = get_annotations_xlsx(excel_path)
    # for now the text will be in list
    # further change it to json or as required
    data = []
    columns = 0
    table_img = None
    ts_first = None
    ts_second = None    
    table_data_exists = False
    for k in annotations.keys():
        annotations_list = annotations[k]
        for i in range(len(annotations_list)):
            
            for label in annotations_list[i]:
                x1,y1,x2,y2 = annotations_list[i][label]

                sub_image = img[y1:y2,x1:x2]
                cv2.rectangle(bboximg, (x1-1, y1-1),(x2+1, y2+1), (0, 0, 255), 2)
                if label != "Start of Table" and label!='No of Columns' and label!='End of Table':
                    temp_dict = {}
                    text = plot_image(sub_image)
                    newtext = text.strip().replace('\x0c','').replace('\n',' ')
                    temp_dict[label] = newtext
                    data.append(temp_dict)
                    
                if label == 'No of Columns':
                    columns = x1
                    
                if label == "Start of Table":
                    table_data_exists = True
                    table_img1 = img[y1:, x1:]
                    table_img = np.stack((table_img1,)*3, axis=-1)
                    ts_first = y1
                    ts_second = x1

                if label == "End of Table":
                    table_img2 = img[ts_first:y2, ts_second:x2]
                    table_img = np.stack((table_img2,)*3, axis=-1)
                    # print(ts_first,y2,ts_second,x2)
    picture_fn = path.strip().split('\\')[-1]
    picture_path = os.path.join(app.root_path, 'static/bounding_boxes')
    if os.path.exists(os.path.join(picture_path, picture_fn)):
        os.remove(os.path.join(picture_path, picture_fn))
    cv2.imwrite(os.path.join(picture_path, picture_fn), bboximg)
    if table_data_exists:
        table_data = table_data_extract(table_img, columns)  # ocr-api
        getproducts = itemparser(table_data, columns)
    else:
        table_data=None
        getproducts = None
    if len(data)!=0:
        totalconf = totalconf//len(data)
    return (data,getproducts,totalconf) 
