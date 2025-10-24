
import cv2
from glob import glob


class Image:
    def __init__(self, path: str):
        self.img = cv2.imread(path)
        self.__name = path[path.rindex("\\") + 1:] if path.__contains__("\\") else path

    def __str__(self):
        return self.__name


class CBIR:
    def __init__(self, path: str):
        self.__images = self.__get_data("{}/*.jpg".format(path))
        self.__rgb_hists_with_img = list()
        self.__set_calc_hist()

    @staticmethod
    def __get_data(path: str):
        return [Image(file) for file in glob(path)]

    @staticmethod
    def __calc_rgb_hist(image):
        rgb_hist = list()

        for channel, _ in enumerate(('b', 'g', 'r')):
            rgb_hist.append(cv2.calcHist([image], [channel], None, [256], [0, 256]))

        return rgb_hist

    @staticmethod
    def __calc_dif(img1, img2):
        _sum = 0
        for i in range(3):
            _sum += sum([abs(a_i - b_i) for a_i, b_i in zip(img1[i], img2[i])])[0]
        return _sum

    @staticmethod
    def __img_interval(img_value: int) -> tuple:
        last_digit = int(str(img_value)[0])
        value_len = len(str(img_value))

        if 0 <= img_value <= 99:
            return 0, 99
        else:
            max_interval = ((last_digit + 1) * pow(10, value_len - 1)) - 1
            min_interval = (max_interval - pow(10, value_len - 1)) + 1

        return min_interval, max_interval

    @staticmethod
    def __img_category(img_name: str) -> int:
        return int(img_name[0: img_name.index(".")])

    def __set_calc_hist(self):
        for image in self.__images:
            self.__rgb_hists_with_img.append((self.__calc_rgb_hist(image.img), image.img))


    def most_similar_image_names_with_acc(self, image: Image, k: int):
        rgb_img_hist = self.__calc_rgb_hist(image.img)
        rgb_hist_point = list()

        img_index = 0
        for rgbhist_img in self.__rgb_hists_with_img:
            rgb_hist, img = rgbhist_img

            rgb_hist_point.append((self.__calc_dif(rgb_hist, rgb_img_hist), img))
            img_index += 1

        
        rgb_hist_point.sort(key=lambda test_list: test_list[0])

        if len(rgb_hist_point) < k:
            k = len(rgb_hist_point) // 2

        top_k_image_names = list()
        for i in range(1, abs(k) + 1):
            top_k_image_names.append(rgb_hist_point[i][1])

        return top_k_image_names

