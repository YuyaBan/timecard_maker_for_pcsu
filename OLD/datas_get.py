# -*- coding:utf-8 -*-
# datas_get.py
import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class sheet_get:

	def del_u3000(list,length):				 # \u3000 を削除する　and 空のセルをlistから削除
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
				st = w - 5
				del list[st:length]
				break

	def get_col(sheet,num):
		record = sheet.col_values(num)
		record_len = len(record)
		sheet_get.del_u3000(record,record_len)
		sheet_get.del_nancell(record,record_len)
		record_len = len(record)

		return (record,record_len)

	def get_row(sheet,num):
		record = sheet.row_values(num)
		#del record[23:]
		record_len = len(record)
		sheet_get.del_u3000(record,record_len)
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


