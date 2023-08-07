import cv2
import imutils
import pytesseract

i = 4
states = {"AN":"Andaman and Nicobar","AP":"Andhra Pradesh","MH":"maharastra","HR":"Haryana","KL":"Kerala","NH":"Maharastra","TN":"Tamil Nadu","AR":"Arunachal Pradesh","AS":"Assam","BR":"Bihar","CH":"Chandigarh","DL":"Delhi","GJ":"Gujarat","HP":"Himachal Pradesh","JK":"Jammu and Kashmir","MP":"Madhya Pradesh","PY":"Puducherry","RJ":"Rajasthan","PB":"Punjab","TS":"Telangana","UP":"Uttar Pradesh","WB":"West Bengal"}
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image = cv2.imread('D:/test/tamil.jpeg')
image = imutils.resize(image, width=300 )
cv2.imshow("original image", image)
cv2.waitKey(10)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("greyed image", gray_image)
cv2.waitKey(10)

gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
cv2.imshow("smoothened image", gray_image)
cv2.waitKey(10)

edged = cv2.Canny(gray_image, 200, 200) 
cv2.imshow("edged image", edged)
cv2.waitKey(10)

cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("contours",image1)
cv2.waitKey(0)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:10]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 contours", image2)
cv2.waitKey(0)

for c in cnts:
        approx = cv2.approxPolyDP(c, 10, True)
        if len(approx) == 4: 
                screenCnt = approx
                x, y, w, h = cv2.boundingRect(c)
                new_img=image[y:y+h, x:x+w]
                cv2.imwrite(r"D:\NUMBER PLATE DETECTION\photos\image"+str(i)+".png",new_img)
                i = i+1
                cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
                cv2.imshow("image with detected license plate", image)
                cv2.waitKey(0) 
                break
cv2.imshow("detected image", new_img)
cv2.waitKey(0)

Cropped_loc = r"D:\NUMBER PLATE DETECTION\photos\image4.png"
cv= cv2.imread(Cropped_loc)
cv2.imshow("cropped",cv)
read = pytesseract.image_to_string(Cropped_loc, lang='eng')
read = ''.join(e for e in read if e.isalnum())
stat = read[0:2]
try:
            print('CAR BELONGS TO',states[stat])
except:
            print('state not recognised!!')
if read:
         print("Number plate is:", read)
         
else:
         print("Number plate is: NOT DETECTED", read )
         cv2.waitKey(0)
         cv2.destroyAllWindows()