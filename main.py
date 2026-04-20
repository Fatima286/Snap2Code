
from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from trial1 import preprocess
from gemini_ocr import extractcode
import uuid #generates unique filename
import os
import asyncio
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/upload")  #the address your React frontend will send the image to.
async def extract_code(file: UploadFile = File(...)):
    #read image in bytes
    contents = await file.read() #That gives you the raw bytes. 
    #convert to numpy array
    nparr = np.frombuffer(contents, np.uint8)  #converts the raw bytes into a numpy array of unsigned 8-bit integers 
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) #decodes that numpy array into an actual OpenCV image (BGR format)
    #pass to preprocessing here
    pre_processed=preprocess(img)
    # pass to gemini here
    newName=f"temp_{uuid.uuid4().hex}.png"
    cv2.imwrite(newName,pre_processed)
    try:
        result=await asyncio.wait_for(asyncio.to_thread(extractcode,newName),
                                      timeout=30)
        os.remove(newName)
    
    except asyncio.TimeoutError:
        os.remove(newName)
        return("Exception:Extraction Failed! Please try again")
    
    except Exception as e:
        os.remove(newName)
        return {"Error:":str(e)}
    # return result here
    #converts dictionaries to JSON, which is the standard format for sending data between backend and frontend. 
    parts=result.split("Code:")
    language=parts[0].replace("Language:","").strip()
    code=parts[1].strip()

    return {"language": language, "code": code} 