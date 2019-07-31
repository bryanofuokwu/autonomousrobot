import cv2
import numpy as np
import matplotlib.pyplot as plt

def line_follow(image,lines):
        #line_image = np.zeros_like(image)
        x1 = int((lines[0][0] + lines[1][0]) / 2)
        x2 = int((lines[0][2] + lines[1][2]) / 2)
        y1 = int((lines[0][1] + lines[1][1]) / 2)
        y2 = int((lines[0][3] + lines[1][3]) / 2)
        return np.array([x1,y1,x2,y2])



def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image,right_fit_average)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10 )
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    print(height,width)
    polygons = np.array([
    [0, 250 ], [width, 250 ], [width, height ], [0, height ]
    ])
    #polygons = np.array([
    #[0, 250 ], [750, 250 ], [0, height ], [750, height ]
    #])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, np.int32([polygons]), 255)
    masked_image = cv2.bitwise_and(image, mask)
    #cv2.imshow("masked", mask)
    return masked_image


image = cv2.imread('IMG_1962.PNG')
#print(image.shape)
lane_image = np.copy(image)
canny_image = canny(lane_image)
cropped_image = region_of_interest(canny_image)
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
averaged_lines = average_slope_intercept(lane_image, lines)
mid_line = line_follow(image,averaged_lines)
#print(mid_line)
#print(mid_line[1])
#print((mid_line[0],mid_line[1]))
x1 = mid_line[0]
y1 = mid_line[1]
x2 = mid_line[2]
y2 = mid_line[3]
#print(x1)
#print(y2)
#print(averaged_lines)
#print(averaged_lines[0][0])
line_image = display_lines(lane_image, averaged_lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.line(combo_image, (x1, y1), (x2, y2), (0, 255, 0), 5 )

cv2.imshow("result", combo_image)
cv2.waitKey(0)
