#import pytesseract
#import easyocr
from gemini_ocr import extractcode
import cv2
import numpy as np

STANDARD_WIDTH=1000
''' Image is a class 
it provides methods to:

Open images

Create images

Modify images'''

'''using PIL to read image
img=Image.open('code1.png')  
'''

def grayScale(image):
    grayed=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return grayed



#Image resizing here
def resise(grayed):
    h,w=grayed.shape[:2]
    if (w!=STANDARD_WIDTH):
        scale=STANDARD_WIDTH/w
        resized=cv2.resize(grayed,(STANDARD_WIDTH,int(h*scale)))# this dimensions are good for code.png rightnow
    return resized
    #print(h,w,scale)


# Noise removal here
def noiseRemoval(resized):
    denoised=cv2.medianBlur(resized,3) #3x3 kernal
   
    return denoised
    '''Median denoising looks at a 3 × 3 neighborhood around each pixel
        It replaces the center pixel with the median value of those 9 pixels'''

#Contrast
def Contrasts(denoised):
    alpha=1.2#contrast control
    beta=0 #brightness control
    gamma=0.7
    '''Instead of using the for loops to access each pixel, do this, it works like new_pixel=apha*pixel+beta but this linearity is
        not good so add gamma correction'''
    contrast_img = cv2.convertScaleAbs(denoised,alpha=alpha,beta=beta)
    table=np.array([(i/255.0)**gamma*255
                    for i in np.arange(256)]).astype("uint8")
    gamma_corrected=cv2.LUT(contrast_img,table)
    
    return gamma_corrected
#Thresholding
def Thresholding(denoised):
    #_,threshed=cv2.threshold(denoised,0,255,cv2.THRESH_BINARY+ cv2.THRESH_OTSU)# The first arg is T which i don't require right now
  
    #-------------ADAPTIVE THRESHOLD-----------------------------------------
    threshed=cv2.adaptiveThreshold(denoised,
                                     255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY,
                                     21,
                                     7)
    
   # cv2.imshow("threshed image",threshed)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return threshed

def preprocess(img):
    grayed = grayScale(img)
    resized = resise(grayed)
    denoised = noiseRemoval(resized)
    contrasted = Contrasts(denoised)
    threshed = Thresholding(contrasted)
    return threshed
# text read
'''
if __name__=='__main__':
    #using opencv to read image
    img=cv2.imread('code5zoom.png')
    
    threshed=preprocess(img)

    cv2.imwrite("temp_processed.png",threshed)
    result=extractcode('temp_processed.png')
    print(result)
'''

'''
    EASYOCR
    reader = easyocr.Reader(['en'], model_storage_directory='D:/MinorProject_II/easyocr_models')
    
    result = reader.readtext(threshed, detail=0, paragraph=False)
    for line in result:
        print(line)'''
    

'''
    TESSERACT
    config = r'--oem 3 --psm 6 '
    text=pytesseract.image_to_string(threshed,config=config)
    print(text)'''

#DROPPED OCR I WILL BE USING GEMINI API>>>>>>>>>>DONE 