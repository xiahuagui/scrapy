import cv2
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform
import numpy as np
def get_init_process_img(roi_img):
    """
    对图片进行初始化处理，包括，梯度化，高斯模糊，二值化，腐蚀，膨胀和边缘检测
    :param roi_img: ndarray
    :return: ndarray
    """
    h = cv2.Sobel(roi_img, cv2.CV_32F, 0, 1, -1)
    v = cv2.Sobel(roi_img, cv2.CV_32F, 1, 0, -1)
    img = cv2.add(h, v)
    img = cv2.convertScaleAbs(img)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=2)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=2)
    img = imutils.auto_canny(img)
    return img

def get_max_area_cnt(img):
    """
    获得图片里面最大面积的轮廓
    :param img: ndarray
    :return: ndarray
    """
    cnts, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key=lambda c: cv2.contourArea(c))
    return cnt

def detect_cnt_again(poly, base_img):
    """
    继续检测已截取区域是否涵盖了答题卡区域
    :param poly: ndarray
    :param base_img: ndarray
    :return: ndarray
    """
    # 该多边形区域是否还包含答题卡区域的flag
    flag = False

    # 计算多边形四个顶点，并且截图，然后处理截取后的图片
    top_left, bottom_left, top_right, bottom_right = get_corner_node_list(poly)
    roi_img = get_roi_img(base_img, bottom_left, bottom_right, top_left, top_right)
    img = get_init_process_img(roi_img)

    # 获得面积最大的轮廓
    cnt = get_max_area_cnt(img)

    # 如果轮廓面积足够大，重新计算多边形四个顶点
    if cv2.contourArea(cnt) > roi_img.shape[0] * roi_img.shape[1] * SHEET_AREA_MIN_RATIO:
        flag = True
        poly = cv2.approxPolyDP(cnt, cv2.arcLength((cnt,), True) * 0.1, True)
        top_left, bottom_left, top_right, bottom_right = get_corner_node_list(poly)
        if not poly.shape[0] == 4:
            print("多边形顶点个数错误")
            return

    # 多边形顶点和图片顶点，主要用于纠偏
    base_poly_nodes = np.float32([top_left[0], bottom_left[0], top_right[0], bottom_right[0]])
    base_nodes = np.float32([[0, 0],
                            [base_img.shape[1], 0],
                            [0, base_img.shape[0]],
                            [base_img.shape[1], base_img.shape[0]]])
    transmtx = cv2.getPerspectiveTransform(base_poly_nodes, base_nodes)

    if flag:
        img_warp = cv2.warpPerspective(roi_img, transmtx, (base_img.shape[1], base_img.shape[0]))
    else:
        img_warp = cv2.warpPerspective(base_img, transmtx, (base_img.shape[1], base_img.shape[0]))
    return img_warp

def main():
	#读入图片
	image = cv2.imread("/usr/www/scrapy/py/test1.jpg")
	#转换为灰度图像
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


	# #高斯滤波
	# blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	# #自适应二值化方法
	# blurred = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,2)
	# '''
	# adaptiveThreshold函数：第一个参数src指原图像，原图像应该是灰度图。
	#     第二个参数x指当像素值高于（有时是小于）阈值时应该被赋予的新的像素值
	#     第三个参数adaptive_method 指： CV_ADAPTIVE_THRESH_MEAN_C 或 CV_ADAPTIVE_THRESH_GAUSSIAN_C
	#     第四个参数threshold_type  指取阈值类型：必须是下者之一  
	#                                  •  CV_THRESH_BINARY,
	#                         • CV_THRESH_BINARY_INV
	#      第五个参数 block_size 指用来计算阈值的象素邻域大小: 3, 5, 7, ...
	#     第六个参数param1    指与方法有关的参数。对方法CV_ADAPTIVE_THRESH_MEAN_C 和 CV_ADAPTIVE_THRESH_GAUSSIAN_C， 它是一个从均值或加权均值提取的常数, 尽管它可以是负数。
	# '''
	# #这一步可有可无，主要是增加一圈白框，以免刚好卷子边框压线后期边缘检测无果。好的样本图就不用考虑这种问题
	# #blurred = cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))

	blurred = get_init_process_img(gray)
	cv2.imwrite('/usr/www/scrapy/py/11.jpg', blurred)

	# 获取最大面积轮廓并和图片大小作比较，看轮廓周长大小判断是否是答题卡的轮廓
    cnt = get_max_area_cnt(blurred)

    cv2.imwrite('/usr/www/scrapy/py/22.jpg', cnt)

    cnt_perimeter = cv2.arcLength(cnt, True)
    base_img_perimeter = (image.shape[0] + image.shape[1]) * 2
    print("周长：", base_img_perimeter)
    print("轮廓：", cnt_perimeter)

    # if not cnt_perimeter > 0.35 * base_img_perimeter:
    #     raise ContourPerimeterSizeError

    # 计算多边形的顶点，并看是否是四个顶点
    poly_node_list = cv2.approxPolyDP(cnt, cv2.arcLength(cnt, True) * 0.1, True)
    if not poly_node_list.shape[0] == 4:
        print("多边形顶点个数错误")
        return

    # 根据计算的多边形顶点继续处理图片，主要是是纠偏
    processed_img = detect_cnt_again(poly_node_list, image)
    cv2.imwrite('/usr/www/scrapy/py/33.jpg', processed_img)


    return


	#canny边缘检测
	edged = cv2.Canny(blurred, 10, 100)

	cv2.imwrite('/usr/www/scrapy/py/11_1.jpg', edged)
	# 从边缘图中寻找轮廓，然后初始化答题卡对应的轮廓
	'''
	findContours
	image -- 要查找轮廓的原图像
	mode -- 轮廓的检索模式，它有四种模式：
	     cv2.RETR_EXTERNAL  表示只检测外轮廓                                  
	     cv2.RETR_LIST 检测的轮廓不建立等级关系
	     cv2.RETR_CCOMP 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，
	              这个物体的边界也在顶层。
	     cv2.RETR_TREE 建立一个等级树结构的轮廓。
	method --  轮廓的近似办法：
	     cv2.CHAIN_APPROX_NONE 存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max （abs (x1 - x2), abs(y2 - y1) == 1
	     cv2.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需
	                       4个点来保存轮廓信息
	      cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
	'''
	cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	docCnt = None
	# 确保至少有一个轮廓被找到
	if len(cnts) > 0:
	    # 将轮廓按大小降序排序
	    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	    # 对排序后的轮廓循环处理
	    for c in cnts:
	        # 获取近似的轮廓
	        peri = cv2.arcLength(c, True)
	        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	        # 如果近似轮廓有四个顶点，那么就认为找到了答题卡
	        if len(approx) == 4:
	            docCnt = approx
	            break
	elif len(cnts)<=0:
		print("未找到答题卡轮廓，重新扫描\n")
		return

	newimage = image.copy()
	for i in docCnt:
	    #circle函数为在图像上作图，新建了一个图像用来演示四角选取
		cv2.circle(newimage, (i[0][0],i[0][1]), 50, (255, 0, 0), -1)

	cv2.imwrite('/usr/www/scrapy/py/22.jpg', newimage)


	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))

	cv2.imwrite('/usr/www/scrapy/py/33.jpg', paper)
	cv2.imwrite('/usr/www/scrapy/py/44.jpg', warped)


	# 对灰度图应用二值化算法
	thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)

	width1 = 2400
	height1 = 2800

	#重塑可能用到的图像
	thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
	paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
	warped = cv2.resize(warped, (width1, height1), cv2.INTER_LANCZOS4)
	#均值滤波
	ChQImg = cv2.blur(thresh, (23, 23))
	#二进制二值化
	ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]

	cv2.imwrite('/usr/www/scrapy/py/55.jpg', thresh)
	cv2.imwrite('/usr/www/scrapy/py/66.jpg', ChQImg)
	'''
	    threshold参数说明
	    第一个参数 src    指原图像，原图像应该是灰度图。
	   第二个参数 x      指用来对像素值进行分类的阈值。
	   第三个参数 y      指当像素值高于（有时是小于）阈值时应该被赋予的新的像素值
	   第四个参数 Methods  指，不同的不同的阈值方法，这些方法包括：
	                •cv2.THRESH_BINARY        
	                •cv2.THRESH_BINARY_INV    
	                •cv2.THRESH_TRUNC        
	                •cv2.THRESH_TOZERO        
	                •cv2.THRESH_TOZERO_INV    
	'''


	# 在二值图像中查找轮廓
	cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	Answer = []

	for c in cnts:
	     # 计算轮廓的边界框，然后利用边界框数据计算宽高比
	      (x, y, w, h) = cv2.boundingRect(c)
	      #if (w > 60 & h > 20)and y>900 and y<2000:
	      if w > 60 and h > 20 and y>900 and y<2000:
	            M = cv2.moments(c)
	            cX = int(M["m10"] / M["m00"])
	            cY = int(M["m01"] / M["m00"])


	            #绘制中心及其轮廓
	            cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0)
	            cv2.circle(paper, (cX, cY), 7, (255, 255, 255), -1)

	            #保存选中模块的中心坐标
	            Answer.append((cX, cY))

	cv2.imwrite('/usr/www/scrapy/py/77.jpg', paper)
	        
	print(Answer)
	print(len(Answer))
	#return

	xt1 = [69, 132, 255, 378, 501, 651, 723, 846, 969, 1092, 1233, 1314, 1437, 1560, 1680, 1824, 1905, 2028, 2154, 2280, 2370]  #选项左侧x坐标 21
	yt1 = [948, 1017, 1089, 1155, 1227, 1317, 1383, 1455, 1524, 1593, 1683, 1752, 1821, 1893, 1962, 2001]                       #选项上测y坐标 16

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

	if len(IDAnswer) <= 0:
		print("白卷，没有任何结果\n")
		return
	result = {}
	for key in range(1, len(IDAnswer)+1): #之后改为总题数 没写的自然就定为：题号：空
		if key not in IDAnswer:
			result[key] = ""
			continue
		result[key] = IDAnswer[key]
		

	print(result)
	print(len(result))


def judgey0(y):
    if (y / 5 < 1):
        return  y + 1
    elif y / 5 < 2 and y/5>=1:
        return y % 5 + 20 + 1
    else:
        return y % 5 + 40 + 1
def judgex0(x):
    if(x%5==1):
        return 'A'
    elif(x%5==2):
        return 'B'
    elif(x%5==3):
        return 'C'
    elif(x%5==4):
        return 'D'
    elif(x%5==0):  #如果是题号 返回空
    	return ''
def judge0(x,y):
    if x/5<1 :
        #print(judgey0(y))
        return (judgey0(y),judgex0(x))
    elif x/5<2 and x/5>=1:
        #print(judgey0(y)+5)
        return (judgey0(y)+5,judgex0(x))
    elif x/5<3 and x/5>=2:
       # print(judgey0(y)+10)
        return (judgey0(y)+10,judgex0(x))
    else:
        #print(judgey0(y)+15)
        return (judgey0(y)+15,judgex0(x))

if __name__ == "__main__":
	main()