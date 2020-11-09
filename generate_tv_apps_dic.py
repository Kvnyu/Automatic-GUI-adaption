#coding: utf-8
tv_dic = open('./tv_dic.txt', 'w', encoding='gbk')

urls = open('./url_tv_apks_education.txt')

tv = ''
for line in urls.readlines():
    line = line.split(" ")
    #apk name like: Tone it up, I cast
    if len(line) > 2:
        tv = " ".join(line[:-1])
    else:
        tv = line[0]

    tv = tv.replace('<b>', '')
    tv = tv.replace('</b>', '')
    tv = tv.strip()

    tv_dic.write(tv+'\n')

tv_dic.close()
urls.close()

# import difflib
#
#
# def string_similar(s1, s2):
#     return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
#
#
# print(string_similar('西瓜视频', '西瓜视频TV版'))
