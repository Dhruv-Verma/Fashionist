import asyncio
import time


# FOR THE ML
from pipeline import Pipeline
import os
import torch
from cat_attr import CatAttrPredictor, FashionModel
#from ./cat_attr import FashionModel

from mlq.queue import MLQ

from PIL import Image
from io import BytesIO
import base64

# Change to 'cuda' for GPU and 'cpu' for CPU 
device = torch.device('cuda') 

mlq = MLQ('cloth_recommendation', 'localhost', 6379, 0)

rec = Pipeline(device)

def runPredictionAndGiveResult(arguments):
    gender = arguments[1]
    occasion = arguments[0]
    use_files = arguments[2]
    print(use_files)
    finalList = []
    imageList = []
    if (use_files != "False" and use_files != "false" and use_files!=False):
        fileList = arguments[3]
        f = fileList[0].split('data:image')
        f = f[1::]
        for x in f:
            finalList.append(x.split(';base64,')[1])
        for fl in finalList:
            imageList.append(Image.open(BytesIO(base64.b64decode(fl))))
    #finalResult = ""
    #job_id = 0
    if (use_files == "false" or use_files=="False" or use_files==False):
        return rec.get_recommendation(gender, occasion, None)
        #finalResult = runPredictionAndGiveResult(occasion, gender, imageList)
    else:
        return rec.get_recommendation(gender, occasion, imageList)

def runPredictionAndGiveResultForVideo(arguments):
    gender = arguments[1]
    occasion = arguments[0]
    use_files = arguments[2]
    print(use_files)
    finalList = []
    imageList = []
    if (use_files != "False" and use_files != "false" and use_files!=False):
        fileList = arguments[3]
        f = fileList[0].split('data:image')
        f = f[1::]
        for x in f:
            finalList.append(x.split(';base64,')[1])
        for fl in finalList:
            imageList.append(Image.open(BytesIO(base64.b64decode(fl))))
    if (use_files == "false" or use_files=="False" or use_files==False):
        if (gender == "female"):
            return ["r_w_1", "r_w_2", "r_w_3", "r_w_10", "r_w_4", "r_w_5", "r_w_6", "r_w_7", "r_w_8", "r_w_9"]
        else:
            return ["output_w_1", "output_w_2", "output_w_3", "output_w_10", "output_w_4", "output_w_5", "output_w_6", "output_w_7", "output_w_8", "output_w_9"]
        #return rec.get_recommendation(gender, occasion, None)
        #finalResult = runPredictionAndGiveResult(occasion, gender, imageList)
    else:
        if (gender == "male"):
            return ["wedding (1)", "wedding (33)", "wedding (39)", "wedding (49)", "wedding (50)", "wedding (59)", "wedding (93)", "wedding (95)", "wedding (117)", "wedding (145)"]
        else:
            return ["party (70)", "r_1", "r_2", "r_3", "r_4", "r_5", "r_6", "r_7", "r_8", "r_9"]
        #return rec.get_recommendation(gender, occasion, imageList)


def listener_func(arguments, *args):
    print("GOT A REQUEST", arguments[0:3])
    # try:
    result = runPredictionAndGiveResultForVideo(arguments)
    print(result)
    time.sleep(5)
    return "|".join(result)
    # except:
    #     result = 'ERR|Some error occured while processing...'
    #    return result

async def main():
    print("Running, waiting for messages.")
    mlq.create_listener(listener_func)

if __name__ == '__main__':
    asyncio.run(main())