import cv2
import numpy as np
from PIL import Image
import os
import sys

def generateData(contours):

    data = {}

    for id, contour in enumerate(contours):

        x, y, w, h = cv2.boundingRect(contour)
        data[id] = {"x":x, "y":y, "w":w, "h":h, "avgW":w, "avgH":h, "count":1}

    return data

def findSiblings(data, key):

    x = data[key]["x"]
    y = data[key]["y"]
    w = data[key]["w"]
    h = data[key]["h"]
    aw = data[key]["avgW"]
    ah = data[key]["avgH"]

    potentialSiblings = {}

    for skey in data:

        if skey == key:
            continue

        sx = data[skey]["x"]
        sy = data[skey]["y"]
        sw = data[skey]["w"]
        sh = data[skey]["h"]

        if  (sx > x + w and sx < x + w + aw and sy > y - (ah * 0.25) and sy < y + (ah * 0.25)) or\
            (sx + sw > x + w and sx + sw < x + w + aw and sy > y - (ah * 0.25) and sy < y + (ah * 0.25)):
            #or (sx > x and sx < x + w and sx < x + w + aw and sy > y - (ah * 0.5) and sy < y + (ah * 0.5)):

            potentialSiblings[skey] = data[skey]

    return potentialSiblings

def mergeSiblings(data, key, siblings):

    if siblings != {}:

        sx = data[key]["x"]
        sy = data[key]["y"]
        sw = data[key]["w"]
        sh = data[key]["h"]

        minX = sx
        minY = sy
        maxX = sx + sw
        maxY = sy + sh

        sumW = data[key]["avgW"]
        sumH = data[key]["avgH"]
        count = data[key]["count"] + len(siblings)

        for pid in siblings:

            minX = min(minX, siblings[pid]["x"])
            maxX = max(maxX, siblings[pid]["x"] + siblings[pid]["w"])
            minY = min(minY, siblings[pid]["y"])
            maxY = max(maxY, siblings[pid]["y"] + siblings[pid]["h"])
            sumW = sumW + siblings[pid]["w"]
            sumH = sumH + siblings[pid]["h"]

            del data[pid]

        data[key]["x"] = minX
        data[key]["y"] = minY
        data[key]["w"] = maxX - minX
        data[key]["h"] = maxY - minY
        data[key]["avgW"] = sumW / count
        data[key]["avgH"] = sumH / count
        data[key]["count"] = count

        siblings = findSiblings(data, key)
        data = mergeSiblings(data, key, siblings)

    #else:
    #
    #    if data[key]["count"] == 1:
    #
    #        del data[key]

    return data

def main():

    image = cv2.imread("input.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    blur = cv2.medianBlur(threshold, 1)
    fakeImage, contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imwrite("blur.jpg", blur)

    height, width = gray.shape
    blank = np.zeros((height, width, 3), np.uint8)
    output = blank.copy()
    test = blank.copy()

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)
        test = cv2.rectangle(test, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.imwrite("test.jpg", test)

    data = generateData(contours)
    dataSize = len(data)

    for key in range(0, dataSize - 1):

        if key not in data:
            continue

        siblings = findSiblings(data, key)
        data = mergeSiblings(data, key, siblings)

    for cid in data:

        x = data[cid]["x"]
        y = data[cid]["y"]
        w = data[cid]["w"]
        h = data[cid]["h"]

        output = cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.imwrite("output.jpg", output)

    print("done")

main()
