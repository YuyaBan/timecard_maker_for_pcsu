# -*- coding:utf-8 -*-
# python main.py "<name>"
import os
import json
import re
import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials

#debug flag
debug = 1

def search_name(list,name,length):
    if name.count(' '):
        print('[-] include space in serching name')
        quit()
    for n in range(length):
        if list[n] == name:
            return n

def del_u3000(list,length):                 # \u3000 を削除する　and 空のセルをlistから削除
    for w in range(length):     
        list[w] = list[w].replace('\u3000','')
        list[w] = list[w].replace('\n','')
        list[w] = list[w].replace(' ','')

def del_nancell(list,length):
    for w in range(length):
        if list[w] == '':
            cnt = cnt + 1
        else:
            cnt = 0

        if cnt == 6:
            st = w - 3
            del list[st:length]
            break

def get_col(sheet,num):
    record = sheet.col_values(num)
    record_len = len(record)
    del_u3000(record,record_len)
    del_nancell(record,record_len)
    record_len = len(record)

    return (record,record_len)

def get_row(sheet,num):
    record = sheet.row_values(num)
    del record[23:]
    record_len = len(record)
    del_u3000(record,record_len)
    record_len = len(record)

    return (record,record_len)

def worksheet_acquisition(sheet_index):
     # JSONをロード
    json_path = "PCSU-timecard.json"
    scope = ["https://spreadsheets.google.com/feeds"]
    path = os.path.expanduser(json_path)
    f = open('doc_id.txt')
    doc_id = f.readline()

    # credentialsを取得 and Sheetの情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    gclient = gspread.authorize(credentials)
    gfile = gclient.open_by_key(doc_id)
    wsheet  = gfile.get_worksheet(0) # シートのindexを任意で入力
    return wsheet

def main(name):

    wsheet = worksheet_acquisition(0)

    # Sheetから列情報をlistで取得
    name_col_record, name_col_len = get_col(wsheet,2)

    if debug == 1:
        print('[+] name_col_record:{}'.format(name_col_record))

    target_row_num = search_name(name_col_record,name[1],name_col_len) + 1

    if debug == 1:
        print('[+] target_row_num:{}'.format(target_row_num))

    # Sheetから行情報をlistで取得
    target_row_record, target_row_len = get_row(wsheet,target_row_num)
    head_row_record, head_row_len = get_row(wsheet,1)

    if debug == 1:
        print('[+] head_row_record:{}'.format(head_row_record))
        print('[+] target_row_record :{}'.format(target_row_record))

    


if __name__ == '__main__':
    argvs = sys.argv
    main(argvs)