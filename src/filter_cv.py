import cv2
import numpy as np


class CVFilter:
    def __init__(self, file):
        self.img = self.bts_to_img(bts=file)

    @staticmethod
    def bts_to_img(bts):
        '''
        :param bts: results from image_to_bts
        '''
        buff = np.fromstring(bytes(bts), np.uint8)
        buff = buff.reshape(1, -1)
        img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        return img

    @staticmethod
    def read_file(filename):
        return cv2.imread(filename)

    @staticmethod
    def color_quantization(img, k):
        # Transform the image
        data = np.float32(img).reshape((-1, 3))

        # Determine criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        # Implementing K-Means
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    @staticmethod
    def edge_mask(img, line_size, blur_value):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, blur_value)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size,
                                      blur_value)
        return edges

    @staticmethod
    def image_to_bytes(image):
        return cv2.imencode('.jpg', image)[1].tobytes()

    def set_filter(self):
        img_edges = self.edge_mask(img=self.img, line_size=9, blur_value=5)
        img_blurred = cv2.bilateralFilter(src=self.img, d=9, sigmaColor=200, sigmaSpace=200)
        img_cartoon = cv2.bitwise_and(img_blurred, img_blurred, mask=img_edges)
        return self.image_to_bytes(img_cartoon)
