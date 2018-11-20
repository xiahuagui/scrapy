import cv2
import json
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform

def main(path):
	image = cv2.imread(path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	blurred = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,2)
	blurred = cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
	edged = cv2.Canny(blurred, 10, 100)
	cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	docCnt = None  
	docCnt1 = None 
	ss = 0
	if len(cnts) > 0:
	    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	    for c in cnts:
	        peri = cv2.arcLength(c, True)
	        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	        if len(approx) == 4 and ss <= 1:
	            ss = ss + 1
	            if ss == 1:
	                docCnt = approx
	            else:
	                docCnt1 = approx
	        elif ss > 1:
	            break
	elif len(cnts)<=0:
		print("答题卡不符合规范，清重新扫描\n")
		return {"status":0, "msg":"答题卡不符合规范，清重新扫描\n"}



	newimage = image.copy()
	for i in docCnt:
		cv2.circle(newimage, (i[0][0],i[0][1]), 50, (255, 0, 0), -1)

	for i in docCnt1:
		cv2.circle(newimage, (i[0][0],i[0][1]), 50, (255, 0, 0), -1)
	# cv2.imwrite('./22.jpg', newimage)
	# return
	rs = {}
	rs['admin'] = check_admission_ticket(image,gray,docCnt1)
	rs['data'] = check_choice_question(image,gray,docCnt)  #答题区域
	#print({"status":1, "data":rs})
	return json.dumps({"status":1, "data":rs})

def check_admission_ticket(image,gray,docCnt):
	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))
	thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
	width1 = 1140
	height1 = 1040
	thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
	paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
	#warped = cv2.resize(warped, (width1, height1), cv2.INTER_LANCZOS4)
	#均值滤波
	ChQImg = cv2.blur(thresh, (23, 23))
	ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]
	cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	Answer = []
	for c in cnts:
	      (x, y, w, h) = cv2.boundingRect(c)
	      if w > 62 and w < 108 and h > 18 and h < 45 and y>235 and y<1006:
	            M = cv2.moments(c)
	            cX = int(M["m10"] / M["m00"])
	            cY = int(M["m01"] / M["m00"])
	            cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0)
	            cv2.circle(paper, (cX, cY), 7, (255, 255, 255), -1)
	            Answer.append((cX, cY))
	#cv2.imwrite('/usr/www/scrapy/py/88.jpg', paper)   
	xt1 = [17, 140, 269, 396, 521, 649, 772, 900, 1024, 1129]  
	yt1 = [231, 311, 390, 473, 554, 635, 715, 793, 873, 953, 1016] 
	IDAnswer = {}
	for i in Answer:
	    for j in range(0,len(xt1)-1):
	        if i[0]>xt1[j] and i[0]<xt1[j+1]:
	            for k in range(0,len(yt1)-1):
	                if i[1]>yt1[k] and i[1]<yt1[k+1]:
	                    #rs = judge1(j,k)
	                    if j in IDAnswer:
	                    	#print(int(j)+1, "项学号选了多个值\n")
	                    	if int(k) < int(IDAnswer[j]):  #选了多选 取最大的数字
	                    	    continue
	                    	IDAnswer[j] = k
	                    else:
	                    	IDAnswer[j] = k

	result = ""
	for key in range(0, 9): #没写的默认为x
		if key not in IDAnswer:
			result = result+"x"
			continue
		result = result + str(IDAnswer[key])
	return result




def check_choice_question(image,gray,docCnt):
	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))
	thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
	width1 = 2400
	height1 = 2800
	thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
	paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
	#warped = cv2.resize(warped, (width1, height1), cv2.INTER_LANCZOS4)
	ChQImg = cv2.blur(thresh, (23, 23))
	ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]
	cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	Answer = []
	for c in cnts:
	      (x, y, w, h) = cv2.boundingRect(c)
	      if w > 50 and h > 16 and y>75 and y<2730:
	            M = cv2.moments(c)
	            cX = int(M["m10"] / M["m00"])
	            cY = int(M["m01"] / M["m00"])
	            cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0)
	            cv2.circle(paper, (cX, cY), 7, (255, 255, 255), -1)
	            Answer.append((cX, cY))

	#cv2.imwrite('/usr/www/scrapy/py/77.jpg', paper)
	xt1 = [15, 120, 225, 330, 435, 645, 747, 852, 954, 1059, 1260, 1365, 1470, 1572, 1674, 1878, 1983, 2088, 2190, 2295, 2376]  
	yt1 = [96, 192, 270, 351,429, 627, 735, 819, 900, 978, 1176, 1290, 1374, 1452, 1533, 1725, 1836, 1920, 1998, 2079, 2274, 2385, 2469, 2550, 2631, 2730] 
	IDAnswer = {}
	for i in Answer:
	    for j in range(0,len(xt1)-1):
	        if i[0]>xt1[j] and i[0]<xt1[j+1]:
	            for k in range(0,len(yt1)-1):
	                if i[1]>yt1[k] and i[1]<yt1[k+1]:
	                    rs = judge0(j,k)
	                    if rs[1] == "":
	                    	print("存在题号太宽的情况，即为无效值\n")
	                    	continue
	                    if rs[0] in IDAnswer:
	                    	IDAnswer[rs[0]].append(rs[1])
	                    	IDAnswer[rs[0]].sort()  
	                    else:
	                    	IDAnswer[rs[0]] = []
	                    	IDAnswer[rs[0]].append(rs[1])

	result = {}
	for key in range(1, 100+1): #没写的自然就定为：题号：空
		if key not in IDAnswer:
			result[key] = ""
			continue
		result[key] = IDAnswer[key]
	return result


#题号
def judgex0(x):
    if (x / 5 < 1):
        return  x + 1
    elif x / 5 < 2 and x/5>=1:
        return x % 5 + 5 + 1
    elif x / 5 < 3 and x/5>=2:
 	    return x % 5 + 10 + 1
    else:
        return x % 5 + 15 + 1

def judgey0(y):
    if(y%5==1):
        return 'A'
    elif(y%5==2):
        return 'B'
    elif(y%5==3):
        return 'C'
    elif(y%5==4):
        return 'D'
    elif(y%5==0):  #如果是题号 返回空
        return ''

def judge0(x,y):
    if y/5<1 :
        #print(judgey0(y))
        return (judgex0(x),judgey0(y))
    elif y/5<2 and y/5>=1:
        #print(judgey0(y)+5)
        return (judgex0(x)+20,judgey0(y))
    elif y/5<3 and y/5>=2:
        # print(judgey0(y)+10)
        return (judgex0(x)+40,judgey0(y))
    elif y/5<4 and y/5>=3:
        # print(judgey0(y)+10)
        return (judgex0(x)+60,judgey0(y))
    else:
        #print(judgey0(y)+15)
        return (judgex0(x)+80,judgey0(y))


#if __name__ == "__main__":
#	main()
