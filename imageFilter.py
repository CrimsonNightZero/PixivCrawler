from PIL import Image
from PIL import ImageFile
from io import BytesIO
import os
from colorsConvert import Colors
from pixiv4_csv import Csv_operate

image_temp_size = 50

class Image_judge:
    def __init__(self, file_raw):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        self.file_raw = file_raw

        self.image_pixiv = Image.open(file_raw)
        self.failText = ""
        # HSV顏色
        self.colorss = [
            {'color': 'white', 'count': 0, 'angle': None}, {'color': 'gray', 'count': 0, 'angle': None},
            {'color': 'black', 'count': 0, 'angle': None}, {'color': 'red', 'count': 0, 'angle': 0},
            {'color': 'yellow', 'count': 0, 'angle': 60}, {'color': 'green', 'count': 0, 'angle': 120},
            {'color': 'cyan', 'count': 0, 'angle': 180}, {'color': 'deep blue', 'count': 0, 'angle': 240},
            {'color': 'magenta', 'count': 0, 'angle': 300}, {'color': 'orange', 'count': 0, 'angle': 30},
            {'color': 'light green', 'count': 0, 'angle': 90}, {'color': 'deep green', 'count': 0, 'angle': 150},
            {'color': 'light blue', 'count': 0, 'angle': 210}, {'color': 'indigo', 'count': 0, 'angle': 270},
            {'color': 'pink', 'count': 0, 'angle': 330}]
        # 灰階
        self.gray = [
            {'0': 16 * 0, 'count': 0}, {'1': 16 * 1, 'count': 0}, {'2': 16 * 2, 'count': 0}, {'3': 16 * 3, 'count': 0},
            {'4': 16 * 4, 'count': 0}, {'5': 16 * 5, 'count': 0}, {'6': 16 * 6, 'count': 0}, {'7': 16 * 7, 'count': 0},
            {'8': 16 * 8, 'count': 0}, {'9': 16 * 9, 'count': 0}, {'10': 16 * 10, 'count': 0}, {'11': 16 * 11, 'count': 0},
            {'12': 16 * 12, 'count': 0}, {'13': 16 * 13, 'count': 0}, {'14': 16 * 14, 'count': 0},
            {'15': 16 * 15, 'count': 0}, {'黑': 0, 'count': 0}, {'白': 255, 'count': 0}]

        self.image_data = {'black_white': 0, 'color_different': 0, 'points_total': 0}

        if type(file_raw) == BytesIO:
            self.file_size = len(file_raw.getvalue())
        elif type(file_raw) == str:
            self.file_size = os.path.getsize(file_raw)

    def get_error_message(self):
        return self.failText

    def image_get_size(self):
        return self.image_pixiv.size

    def image_get_file_size(self):
        return self.file_size

    def image_thumbnail(self):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))
        return self.image_pixiv

    def close(self):
        del self.image_pixiv

    def img_compare(self):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))
        image_pixiv_rgb = self.image_pixiv.convert('RGB')
        csv_path = r"C:\Users\foryou\pixiv_model.csv"
        csv_operate = Csv_operate(csv_path)
        csv_column = csv_operate.read('作者', '圖片名稱', 'Pixiv網址', '儲存位置', '灰階率')
        gray_rate = self.black_white_judge2()

        csv_column_index = 0
        rows = {'作者': [], '圖片名稱': [], 'Pixiv網址': [], '儲存位置': [], '灰階率': []}

        for gray_rate2 in csv_column['灰階率']:
            try:

                if type(gray_rate2) == type(''):
                    gray_rate2 = float(gray_rate2)
                if gray_rate2 < gray_rate + 0.05 and gray_rate2 > gray_rate - 0.05:
                    rows['作者'].append(csv_column['作者'][csv_column_index])
                    rows['圖片名稱'].append(csv_column['圖片名稱'][csv_column_index])
                    rows['Pixiv網址'].append(csv_column['Pixiv網址'][csv_column_index])
                    rows['儲存位置'].append(csv_column['儲存位置'][csv_column_index])
                    rows['灰階率'].append(gray_rate2)
                csv_column_index += 1
            except TypeError:
                csv_column_index += 1
            # 空白為0 待改
            except ValueError:
                csv_column_index += 1
                continue
        print(rows['灰階率'])
        csv_path = r"C:\Users\foryou\pixiv_search.csv"
        csv_operate2 = Csv_operate(csv_path);
        if not (os.path.isfile(csv_path)):
            csv_operate2.fill("尋找的圖", "找尋成功", "作者", "圖片名稱", "Pixiv網址", "儲存位置", "相似度", "灰階率")

        # path = r"E:\aa\20170502\【宣】ザ・ケージ.xml"

        #        網路圖片
        #        self.image_pixiv2 = Image.open(r'C:\Users\foryou\Desktop\62691442_p0_master1200.jpg')
        #        self.image_pixiv2.thumbnail((image_temp_size, image_temp_size))
        csv_column_index = 0

        rows_max = {'作者': None, '圖片名稱': None, 'Pixiv網址': None, '儲存位置': None, '灰階率': 0, '相似度': 0}
        for path in rows['儲存位置']:
            try:
                file = open(path, 'r')
            except TypeError:
                continue

            #        test
            #        path = r'C:\Users\foryou\Desktop\ザ・ケージ.xml'
            #        self.img_csv(path)

            points_total = 0
            data = {}
            #        網路圖片
            #        for item in self.image_pixiv.getdata():
            #            try :
            #                data[points_total] = item
            #                #data[points_total] = item
            #                points_total += 1
            #                #print(item)
            #            #單一數字被轉為int
            #            except TypeError:
            #                continue

            for item in file:
                try:
                    item = item.strip('\n').replace('(', '').replace(')', '').split(',')
                    index = 0
                    for value in item:
                        item[index] = int(value)
                        index += 1
                    data[points_total] = item
                    points_total += 1
                # 單一數字被轉為int
                except TypeError:
                    continue

            points_total = 0
            similar = 0
            for item in image_pixiv_rgb.getdata():
                try:
                    if (abs(item[0] - data[points_total][0]) < 20 and abs(
                            item[1] == data[points_total][1]) < 20 and abs(item[2] == data[points_total][2]) < 20):
                        points_total += 1
                        similar += 1
                    else:
                        points_total += 1
                # 單一數字被轉為int
                except TypeError:
                    continue
                #                (points_total == len(data))
                except KeyError:
                    break
                except IndexError:
                    break

            if similar == 0:
                print('diff_zero', 0, similar, points_total)
                # return True
            elif similar / points_total < 0.85:

                print('diff', similar / points_total)
                # return True
            elif similar / points_total > 1:
                print('my file is fake', similar / points_total)
                # return True
            else:
                print('same', similar / points_total)
                csv_operate2.fill(self.file_raw, True, rows['作者'][csv_column_index], rows['圖片名稱'][csv_column_index],
                                  rows['Pixiv網址'][csv_column_index], rows['儲存位置'][csv_column_index],
                                  similar / points_total, rows['灰階率'][csv_column_index])
                return False

            if not (similar == 0) and similar / points_total > rows_max['相似度']:
                rows_max['作者'] = rows['作者'][csv_column_index]
                rows_max['圖片名稱'] = rows['圖片名稱'][csv_column_index]
                rows_max['Pixiv網址'] = rows['Pixiv網址'][csv_column_index]
                rows_max['儲存位置'] = rows['儲存位置'][csv_column_index]
                rows_max['相似度'] = similar / points_total
                rows_max['灰階率'] = rows['灰階率'][csv_column_index]

            csv_column_index += 1
        csv_operate2.fill(self.file_raw, False, rows_max['作者'], rows_max['圖片名稱'], rows_max['Pixiv網址'], rows_max['儲存位置'],
                          rows_max['相似度'], rows_max['灰階率'])

    def img_xml(self, path):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))
        self.image_pixiv.convert('RGB')

        points_total = 0
        data = []
        content = ""
        for item in self.image_pixiv.getdata():
            try:
                data.append(item)
                points_total += 1
                # print(item)

            # 單一數字被轉為int
            except TypeError:
                continue
        for x in data:
            content += str(x) + "\n"

        return content

    def img_write_xml(self, path):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))
        self.image_pixiv.convert('RGB')
        file = open(path, "w")
        points_total = 0
        data = list()
        for item in self.image_pixiv.getdata():
            try:
                data.append(item)
                points_total += 1
                # print(item)

            # 單一數字被轉為int
            except TypeError:
                continue
        for x in data:
            file.write(str(x) + "\n")
        file.close()
        return True

    # 背景四個角取值平均
    def div_picture(self):
        width, height = self.image_pixiv.size
        pictures = list()
        pictures.append(self.image_pixiv.crop((0, 0, 1 / 3 * width, 1 / 3 * height)))
        pictures.append(self.image_pixiv.crop((2 / 3 * width, 0, width, 1 / 3 * height)))
        pictures.append(self.image_pixiv.crop((0, 2 / 3 * height, 1 / 3 * width, height)))
        pictures.append(self.image_pixiv.crop((2 / 3 * width, 2 / 3 * height, width, height)))
        color_data = list()
        data = 0
        for picture in pictures:
            for item in picture.getdata():
                color_data.append(item)
            color_data.sort()
            middle = int(len(color_data) / 2)
            data += color_data[middle]
        return data / 4

    # otsu演算法
    def otsu(self, gray_color, color_data, colors_total, points_total):
        # t 閥值
        variance = {}
        for t in gray_color.keys():
            u1 = 0
            u2 = 0
            u1_total = 0
            u2_total = 0
            for key in gray_color.keys():
                if key <= t:
                    u1_total += gray_color[key]
                else:
                    u2_total += gray_color[key]
                # print(u1_total,u2_total,t,key)
            for key in gray_color.keys():
                if u1_total == 0 or u2_total == 0:
                    u = 0
                    u1 = 0
                    u2 = 0
                else:
                    u = colors_total / points_total
                    if key <= t:
                        u1 += (gray_color[key] / u1_total) * key
                    else:
                        u2 += (gray_color[key] / u2_total) * key
                # print(u1,gray_color[key],u1_total,t,key)
                # print(u2,gray_color[key],u2_total,t,key)
            variance[t] = (u1_total / points_total) * (u1 - u) * (u1 - u) + (u2_total / points_total) * (u2 - u) * (
                        u2 - u)
            # print(u1_total,u1,u2_total,u2,variance[t],t,u)
        # print(variance)

        # v_max 取最大值
        # v_max = max(variance.values());
        # t = 0
        t_value = []
        for key, value in variance.items():
            t_value.append(value)
            # if(v_max == value):
            #  t = key
        # print(t)
        t_value.sort()

        # 取前兩個最大值平均
        keys = []
        for key, value in variance.items():
            if t_value[len(t_value) - 1] == value or t_value[len(t_value) - 2] == value:
                keys.append(key)
        if len(keys) > 1:
            t = (keys[0] + keys[1]) / 2
        else:
            t = keys[0] / 2
        color_data.sort()

        # 中值法
        middle = int(len(color_data) / 2)
        t = color_data[middle]
        print(color_data[middle])

        return t

    # 黑白otsu演算法過濾
    def black_white_judge2(self):
        # self.image_pixiv.thumbnail((self.image_pixiv.width * 0.3, self.image_pixiv.height * 0.3))
        self.image_pixiv = self.image_pixiv.convert("L")

        #        sample test
        #        pixels =[20, 120, 120, 20, 100, 100, 30, 30, 40]
        #        redim = Image.new('L', (3,3))
        #        redim.putdata(pixels)
        #        self.image_pixiv =redim
        #        print(list(redim.getdata()))
        # redim.show()

        div_data = self.div_picture()

        points_total = 0
        color_data = []
        gray_color = {}
        colors_total = 0

        for item in self.image_pixiv.getdata():
            # self.L_getcolors(item)
            color_data.append(item)
            try:
                # print(item[0],item[1],item[2])
                if item in gray_color:
                    gray_color[item] += 1
                else:
                    gray_color[item] = 1
                points_total += 1
                colors_total += item
            # 單一數字被轉為int
            except TypeError:
                continue;
        # 取閥值
        t = self.otsu(gray_color, color_data, colors_total, points_total)

        # 前景背景反轉
        binary_data = []
        white = 0
        # print(points_total, div_data)
        for item in self.image_pixiv.getdata():
            if div_data >= 128:
                if item > t:
                    binary_data.append(0)
                else:
                    binary_data.append(255)
                    white += 1
            else:
                if item > t:
                    binary_data.append(255)
                    white += 1
                else:
                    binary_data.append(0)
        print(points_total)
        print(white / points_total)
        return white / points_total
        # if(white/points_total < 0.3):
        #   return True
        redim = Image.new(self.image_pixiv.mode, self.image_pixiv.size)
        redim.putdata(binary_data)
        redim.show()

        # 黑白顏色量過濾

    def black_white_judge(self):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))

        if ('1' in self.image_pixiv.mode) or ('L' in self.image_pixiv.mode):
            self.failText = "黑白檔案:1&L"
            return True
        else:
            # item=(r,g,b,a)
            # print(image_pixiv.getdata())
            points_total = 0
            colors_black_white = 0
            for item in self.image_pixiv.getdata():
                try:
                    # print(len(item))
                    # print(item[0],item[1],item[2])
                    points_total += 1

                    if not (item[0] == item[1] == item[2]):
                        if (abs(item[0] - item[1]) <= 10) and (abs(item[0] - item[2]) <= 10) and (
                                abs(item[1] - item[2]) <= 10):
                            colors_black_white += 1
                    else:
                        colors_black_white += 1
                # 單一數字被轉為int
                except TypeError:
                    continue;

            if colors_black_white / points_total > 0.9:
                self.failText = "黑白檔案:RGB"
                return True

    # 各顏色量過濾
    def pixel_point_judge(self):
        self.image_pixiv.thumbnail((image_temp_size, image_temp_size))

        points_total = 0
        points = {}

        if ('1' in self.image_pixiv.mode) or ('L' in self.image_pixiv.mode):
            self.failText = "黑白檔案:1&L"
            return True
        else:
            for item in self.image_pixiv.getdata():
                try:
                    if str(item[0]) + str(item[1]) + str(item[2]) in points:
                        points[str(item[0]) + str(item[1]) + str(item[2])] += 1
                        point_create_boolean = False
                    else:
                        point_create_boolean = True

                    if point_create_boolean:
                        points[str(item[0]) + str(item[1]) + str(item[2])] = 1
                    points_total += 1
                except TypeError:
                    continue

        max_point = 0
        total = 0
        for point in points:
            if points[point] > max_point:
                max_point = points[point]
            if points[point] > points_total * 0.05:
                total += points[point]

        if max_point != 0 and ((max_point / points_total > 0.63) or (total / points_total > 0.64)):
            self.failText = "檔案像素量太一致"
            return True

    # 圖片size過濾
    def size_judge(self):
        if self.image_pixiv.width / self.image_pixiv.height > 4 \
                or self.image_pixiv.height / self.image_pixiv.width > 4 \
                or self.image_pixiv.width < 300 \
                or self.image_pixiv.height < 300 \
                or self.image_pixiv.width < 500 \
                and self.image_pixiv.height < 500 \
                or self.file_size < 51200:
            self.failText = "檔案過小"
            return True

    # HSV顏色過濾
    def HSV_judge(self):
        self.image_pixiv.thumbnail((self.image_pixiv.width * 0.3, self.image_pixiv.height * 0.3))

        if ('1' in self.image_pixiv.mode) or ('L' in self.image_pixiv.mode):
            self.failText = "黑白檔案:1&L"
            return True
        else:
            # print(self.image_pixiv.getdata(),self.image_pixiv)
            self.image_pixiv = self.image_pixiv.convert('RGB')
            # item=(r,g,b,a)

            points_total = 0
            for item in self.image_pixiv.getdata():
                try:
                    # print(item[0],item[1],item[2])
                    points_total += 1
                    self.HSV_getcolors(item[0], item[1], item[2])
                # 單一數字被轉為int
                except TypeError:
                    continue;
            black_white = 0

            for color in self.colorss[0:3]:
                black_white += color['count']
                # print("black_white :%s\n" %(black_white))
            color_same = False
            # 2017-03-01_21-30-30 0.84
            # 圖0.94
            # 圖0.89
            color_counts = 0
            color_max = 0
            for color in self.colorss[3:]:
                if color_max < color['count']:
                    color_max = color['count']
                if not color['count'] == 0 and color['count'] > 10:
                    color_counts += 1
                if color['count'] / points_total > 0.87:
                    print(self.image_pixiv.width, self.image_pixiv.height)
                    print("color %s\n%s %s\n" % (self.colorss, points_total, color_max / points_total))
                    color_same = True

            self.image_data['black_white'] = black_white / points_total
            self.image_data['color_different'] = color_max / points_total
            self.image_data['points_total'] = points_total
            # print(color_counts)
            # print("color_same :%s\n" %(color))
            # 2017-03-01_21-30-30 0.8
            # 圖0.87
            # 圖0.93 底91
            if black_white / points_total > 0.93:
                self.failText = "黑白檔案:1&L"
                print(self.image_pixiv.width, self.image_pixiv.height)
                print("black_white %s\n%s %s\n" % (self.colorss, black_white / points_total, points_total))
                return True
            elif color_counts < 4:
                print("color_counts short %s\n%s\n" % (self.colorss, points_total))
                return True
            elif (color_same):
                self.failText = "檔案像素量太一致"
                return True
            print(self.colorss, points_total, black_white / points_total, color_max / points_total)

    def HSV_getcolors(self, r, g, b):
        h, s, v = Colors.rgb_convert_hsv(r, g, b)
        if s <= 0.125 and v >= 0.9375:
            self.colorss[0]['count'] += 1
        elif v <= 0.25:
            self.colorss[2]['count'] += 1
        elif s <= 0.125:
            self.colorss[1]['count'] += 1
        else:
            # print(h)
            for color in self.colorss[3:]:
                if h > 345:
                    if color['angle'] + 15 + 360 >= h > color['angle'] - 15 + 360:
                        color['count'] += 1
                else:
                    if color['angle'] + 15 >= h > color['angle'] - 15:
                        color['count'] += 1

    def L_getcolors(self, g):
        if g == 0:
            self.gray[16]['count'] += 1
        elif g == 255:
            self.gray[17]['count'] = 10
        else:
            i = int(g / 16)
            self.gray[i]['count'] += 1

# if __name__ =="__main__":
