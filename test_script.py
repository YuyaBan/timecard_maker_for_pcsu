# -*- coding:utf-8 -*-
import os
import json
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def del_u3000(list,length):                 # \u3000 を削除する　and 空のセルをlistから削除
    for w in range(length):     
        list[w] = list[w].replace('\u3000',' ')
        if list[w] == '':
            cnt = cnt + 1
        else:
            cnt = 0

        if cnt == 6:
            st = w - 3
            del list[st:length]
            length = st
            break

def main():
    doc_id = "1uMqr-5UMNCC5bZ09pTs0OTQnKRPqUz3_8XNXFmYQHfs"

    # 先ほどDLしたJSONをロード
    json_path = "PCSU-3ec02f8e9df1.json"
    scope = ["https://spreadsheets.google.com/feeds"]
    path = os.path.expanduser(json_path)

    # credentialsを取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)

    gclient = gspread.authorize(credentials)
    gfile = gclient.open_by_key(doc_id)
    wsheet  = gfile.get_worksheet(0) # シートのindexを任意で入力

    #records = wsheet.get_all_records(empty2zero=False,head=1)
    #record2 = wsheet.range('A1:B20')
    row = wsheet.row_values(2)
    col = wsheet.col_values(2)

    del row[23:]
    print(row)

    row_len = len(row)
    col_len = len(col)

    del_u3000(col,col_len)
    del_u3000(row,row_len)
    print(col)
    print(row)

if __name__ == '__main__':
    main()