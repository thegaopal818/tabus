import numpy as np
import cv2 as cv
import sys

cnf_threshold = 0.5
nms = 0.4
width = 412
height = 412

IMG_SCALE = 0.5

classFile = 'coco.names'
classes = None

with open(classFile, 'rt') as file:
	classes = file.read().rstrip('\n').split('\n')

configuration = './yolov3.cfg'
weights = './yolov3.weights'
net = cv.dnn.readNetFromDarknet(configuration, weights)

def getOutputs(net):
	layersNames = net.getLayerNames()
	return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def drawBox(classId, conf, left, top, right, bottom):
	cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

	label = '%.2f' % conf

	if classes:
		assert(classId < len(classes))
		label = '%s:%s' % (classes[classId], label)

def postprocess(frame, outs):
	frameHeight = frame.shape[0]
	frameWidth = frame.shape[1]

	classIds = []
	confidences = []
	boxes = []
	for out in outs:
		for detection in out:
			scores = detection[5:]
			classId = np.argmax(scores)
			confidence = scores[classId]
			if confidence > cnf_threshold:
				center_x = int(detection[0] * frameWidth)
				center_y = int(detection[1] * frameHeight)
				width = int(detection[2] * frameWidth)
				height = int(detection[3] * frameHeight)
				left = int(center_x - width / 2)
				top = int(center_y - height / 2)
				classIds.append(classId)
				confidences.append(float(confidence))
				boxes.append([left, top, width, height])

	indices = cv.dnn.NMSBoxes(boxes, confidences, cnf_threshold, nms)
	for i in indices:
		i = i[0]
		box = boxes[i]
		left = box[0]
		top = box[1]
		width = box[2]
		height = box[3]
		drawBox(classIds[i], confidences[i], left, top, left + width, top + height)

cap = cv.VideoCapture(0)

while cap.isOpened():
	ret, frame = cap.read()

	if not ret:
		break

	frame = cv.resize(frame, dsize = (0, 0), fx = IMG_SCALE, fy = IMG_SCALE)

	blob = cv.dnn.blobFromImage(frame, 1 / 255, (width, height), [0, 0, 0], 1, crop = False)

	net.setInput(blob)

	outs = net.forward(getOutputs(net))

	postprocess(frame, outs)

	t, _ = net.getPerfProfile()
	label = 'Inference time : %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
	cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

	cv.imshow('YOLO', frame)

	if cv.waitKey(1) == ord('q'):
		break
