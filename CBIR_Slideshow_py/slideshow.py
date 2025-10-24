import cv2
import numpy as np
import random
from datetime import datetime

class Transitions:
    def __init__(self) -> None:
        self._out = None
        self._img_list = []
        self._k = 10

    def _to_down(self, img1, img2):
        for i in range(img1.shape[0]):
            self._replace_pixels_updown(img1, img2, i)

    def _to_up(self, img1, img2):
        for i in reversed(range(img1.shape[0])):
            self._replace_pixels_updown(img1, img2, i)

    def _to_left(self, img1, img2):
        for i in range(img1.shape[1]):
            self._replace_pixels_leftright(img1, img2, i)

    def _to_mid_vertical(self, img1, img2):
        for i in range(img1.shape[1]):
            self._replace_pixels_leftright(img1, img2, i//2)
            self._replace_pixels_leftright(img1, img2, -i//2)

    def _to_mid_horizontal(self, img1, img2):
        for i in range(img1.shape[0]):
            self._replace_pixels_updown(img1, img2, i//2)
            self._replace_pixels_updown(img1, img2, -i//2)

    def _to_right(self, img1, img2):
        for i in reversed(range(img1.shape[1])):
            self._replace_pixels_leftright(img1, img2, i)
    
    def _savable_condition(self, i):
        return i % self._k == 0
    
    def _replace_pixels_updown(self, img1, img2, i):
        img1[:, i] = img2[:, i]

        if self._savable_condition(i):
            self._out.write(img1)

    def _replace_pixels_leftright(self, img1, img2, i):
        img1[i, :] = img2[i, :]

        if self._savable_condition(i):
            self._out.write(img1)
    
    def resize_imgs(self, imgs, img_w, img_h):
        for img in imgs:
            self._img_list.append(cv2.resize(img, (img_w, img_h)))

    def make_slideshow(self, img_list):
        img_w, img_h = 256, 256
        self.resize_imgs(img_list, img_w, img_h)
        last_img = np.zeros((img_h, img_w, 3), np.uint8)
        
        date_time = datetime.now()
        string = date_time.strftime('%Y-%m-%d_%H-%M-%S')

        slide_show_name = f'slideshow_at_{string}.avi'

        self._out = cv2.VideoWriter(slide_show_name, cv2.VideoWriter_fourcc(*'MJPG'), 45, (img_w, img_h))
        transactions = [self._to_right, self._to_left, self._to_up, self._to_down,
                       self._to_mid_vertical, self._to_mid_horizontal]

        for img in self._img_list:
            random_value = random.randint(0, len(transactions) - 1)
            func = transactions[random_value - 1]
            func(last_img, img)

            for _ in range(240):
                self._out.write(img)

            last_img = img

        self._out.release()

        return slide_show_name


