#coding: utf-8
import xlrd
spacer = ' '

def generate_tv_dic():
    tv_dic = open('./tv_dic.txt', 'w', encoding='utf-8')
    urls = open('./url_tv_apks_education.txt')
    tv = ''
    for line in urls.readlines():
        line = line.split(" ")
        # apk name like: Tone it up, I cast
        if len(line) > 2:
            tv = " ".join(line[:-1])
        else:
            tv = line[0]

        tv = tv.replace('<b>', '')
        tv = tv.replace('</b>', '')
        tv = tv.strip()

        tv_dic.write(tv + '\n')

    tv_dic.close()
    urls.close()


def generate_tv_dic_from_list(list, dic_path):
    tv_dic = open(dic_path, 'w', encoding='utf-8')
    tv = ''
    for i in list:
        tv_dic.write(i + '\n')
    tv_dic.close()


def read_excel(excel_path, dic_path, urls_path):
    workbook = xlrd.open_workbook(excel_path)
    #print(workbook.sheet_names())
    sheet1 = workbook.sheet_by_name('Sheet1')
    #print(sheet1.name, sheet1.nrows, sheet1.ncols)
    android_dic = []
    tv_urls = open(urls_path, 'w', encoding='utf-8')
    for i in range(2, sheet1.nrows):
        try:
            android_name = str(sheet1.cell(i, 1).value)

            tv_name = str(sheet1.cell(i, 3).value).strip()
            tv_url = str(sheet1.cell(i, 4).value)
            name = tv_name + "_" + android_name
            tv_urls.write(name + spacer + str(tv_url) + '\n')

            android_dic.append(name)

        except FileNotFoundError:
            print('no file:')
        except ValueError:
            print('value error')

    generate_tv_dic_from_list(android_dic, dic_path)
    tv_urls.close()

if __name__ == '__main__':
    read_excel('..\preprocessed_data\selected_huawei\Phone TV apk list.xlsx',
               '..\preprocessed_data\selected_huawei\\android_dic.txt', '..\preprocessed_data\selected_huawei\\tv_urls.txt')
