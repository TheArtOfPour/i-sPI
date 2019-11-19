import os
import cv2
import numpy as np
import importlib.util
from time import sleep

pkg = importlib.util.find_spec('tensorflow')
if pkg is None:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter


class ImageDetection:

    def __init__(self, modeldir):
        GRAPH_NAME = 'detect.tflite'
        LABELMAP_NAME = 'labelmap.txt'
        CWD_PATH = os.getcwd()
        PATH_TO_CKPT = os.path.join(CWD_PATH, modeldir, GRAPH_NAME)
        PATH_TO_LABELS = os.path.join(CWD_PATH, modeldir, LABELMAP_NAME)
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        if self.labels[0] == '???':
            del (self.labels[0])

        self.min_conf_threshold = 0.6
        self.input_mean = 127.5
        self.input_std = 127.5
        self.interpreter = Interpreter(model_path=PATH_TO_CKPT)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

    def detect(self, image_path):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im_h, im_w, _ = image.shape
        image_resized = cv2.resize(image_rgb, (self.width, self.height))
        input_data = np.expand_dims(image_resized, axis=0)
        if self.floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
        detect_text = ""
        for i in range(len(scores)):
            if self.min_conf_threshold < scores[i] <= 1.0:
                ymin = int(max(1, (boxes[i][0] * im_h)))
                xmin = int(max(1, (boxes[i][1] * im_w)))
                ymax = int(min(im_h, (boxes[i][2] * im_h)))
                xmax = int(min(im_w, (boxes[i][3] * im_w)))
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                object_name = self.labels[int(classes[i])]
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))
                label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, label_size[1] + 10)
                cv2.rectangle(image, (xmin, label_ymin - label_size[1] - 10),
                              (xmin + label_size[0], label_ymin + base_line - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                detect_text = detect_text + " " + object_name
        cv2.imshow('Detector', image)
        os.system('echo %s | festival --tts & ' % detect_text)
        sleep(5)
        cv2.destroyAllWindows()
        return
