import pandas as pd
import csv
import os


class Csv_operate:
    def __init__(self, file):
        self.csv_path = file

    def fill(self, *data):
        file_csv = open(self.csv_path, "a", newline='', encoding="utf_8_sig")
        w = csv.writer(file_csv)

        data_array = []
        for data_temp in data:
            data_array.append(data_temp)

        w.writerow(data_array)
        file_csv.close()

    def insert(self, data, delete_time):
        # csv_path2 = r"C:\Users\foryou\pixiv_model2.csv"
        # csv_path3 = r"C:\Users\foryou\pixiv_above.csv"
        # csv_path4 = r"C:\Users\foryou\pixiv_below.csv"
        df = pd.read_csv(self.csv_path)
        head = ["時間", "作者", "圖片名稱", "Pixiv網址", "圖片網址", "儲存位置", "寬", "長", "像素", "灰階率"]
        times = []

        for index, row in df.iterrows():
            if type(row['時間']) == type(''):
                try:
                    row['時間'] = int(row['時間'])
                except ValueError:
                    continue
            if int(delete_time) == row['時間']:
                times.append(index)
        print(times, delete_time)
        above_row = df.loc[:times[0] - 1]
        if data is None:
            above_row.to_csv(self.csv_path, encoding='utf_8_sig', index=False, header=True)
            return

        insert_row = pd.DataFrame([data], columns=head)
        if times[len(times) - 1] == len(df):
            below_row = df.loc[times[len(times)]:]
            df = above_row.append(insert_row).append(below_row)
            df.to_csv(self.csv_path, encoding='utf_8_sig', index=False, header=True)
            return
            # df.to_csv(csv_path2, encoding='utf_8_sig', index=False, header=True)
            # belowRow.to_csv(csv_path4, encoding='utf_8_sig', index=False, header=True)
        else:
            df = above_row.append(insert_row)
            df.to_csv(self.csv_path, encoding='utf_8_sig', index=False, header=True)
            return
            # df.to_csv(csv_path3, encoding='utf_8_sig', index=False, header=True)

    def test(self):
        csv_path2 = r"C:\Users\foryou\pixiv_mo.csv"
        csv_path3 = r"C:\Users\foryou\pixiv_above.csv"
        csv_path4 = r"C:\Users\foryou\pixiv_below.csv"
        df = pd.read_csv(self.csv_path)

        head = ["時間", "作者", "圖片名稱", "Pixiv網址", "圖片網址", "儲存位置", "寬", "長", "像素"]
        insertRow = pd.DataFrame([head], columns=head)
        time = []
        for index, row in df.iterrows():
            if 20170503 == row['時間']:
                time.append(index)
        above = df.loc[:time[0] - 1]
        below = df.loc[time[0]:]
        print(time[0], time[len(time) - 1])
        # print(insertRow.index[[time[0], time[len(time)-1]]])
        print(insertRow.index)
        # for del_index in insertRow.index[[time[0],time[len(time)-1]]]:
        # insertRow = insertRow.drop(insertRow.index[[time]])
        print(insertRow)

        # df.set_value(1,'作者',9)

        df.to_csv(self.csv_path, encoding='utf_8_sig', index=False, header=True)
        insertRow.to_csv(csv_path2, encoding='utf_8_sig', index=False, header=True)
        above.to_csv(csv_path3, encoding='utf_8_sig', index=False, header=True)
        below.to_csv(csv_path4, encoding='utf_8_sig', index=False, header=True)
        return True

    def read(self, *columns):
        if not os.path.isfile(self.csv_path):
            return

        file_csv = open(self.csv_path, "r", newline='', encoding="utf_8_sig", errors='ignore')
        r = csv.DictReader(file_csv)
        rows = {}
        while True:
            try:
                row = next(r)
                for column in columns:
                    if column in rows:
                        rows[column].append(row[column])
                    else:
                        rows[column] = [row[column]]
            except csv.Error:
                continue
            except StopIteration:
                break

        return rows

    def csv_from_excel(self, xlsx_path):
        import xlsxwriter

        workbook = xlsxwriter.Workbook(xlsx_path)
        worksheet = workbook.add_worksheet()
        with open(self.csv_path, 'r', encoding="utf_8_sig") as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    if (c == 0 or c == 6 or c == 7 or c == 8) and r > 0:
                        worksheet.write_number(r, c, int(col))
                    else:
                        worksheet.write(r, c, col)
        workbook.close()


if __name__ == "__main__":
    csv_path = r"C:\Users\foryou\pixiv_model.csv"
    csv_operate = Csv_operate(csv_path)
    csv_file = open(csv_path, "a", newline='', encoding="utf_8_sig")
    csv_operate.create("時間", "作者", "圖片名稱", "Pixiv網址", "圖片網址", "儲存位置", "寬", "長", "像素")
    read_date = csv_operate.read('時間')
    csv_operate.csv_fill("a")
    csv_operate.read('時間')
