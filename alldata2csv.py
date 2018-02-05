# -*- coding:utf-8 -*-
# datas_get.py
'''
出席簿のデータ全件をCSV形式で取得する。
日付検索が前方一致検索が可能なように、「12/8\n全体Mtg」 -> 「12/8 全体Mtg」とする
*注 「12/11全体Mtg」とすると「12/11」or「12/1」となってしまう。
'''


import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def chenge_u3000(list,length):
	for w in range(length):
		if isinstance(list[w],str):
			list[w] = list[w].replace('\u3000',' ')
			list[w] = list[w].replace('\n',' ')

def del_u3000_for_list(list,length):				 # \u3000 を削除する　and 空のセルをlistから削除
	for w in range(length):
		if isinstance(list[w],str):
			list[w] = list[w].replace('\u3000','')
			list[w] = list[w].replace('\n','')
			list[w] = list[w].replace(' ','')

##### この関数、上手く機能していない...（泣）
def del_u3000_for_line(line):						 # \u3000 を削除する　and 空のセルをlistから削除
	print("start del line:{}".format(line))
	line = line.strip()

def insert_space_end_date(list,length):
	for x in range(length):
		# [12/1\naa][1/4 aa][1/12　aa]
		flag = 0
		idx_insert = 0
		#idx = [int(10),int(10),int(10)]
		print("[1] list[{}]:{}".format(x,list[x]))
		try:
			if not list[x][0].isdigit() : flag = 1
		except IndexError:
			print('IndexError:list[{}]'.format(x))
			flag = 1

		if flag == 0:						# lf,fullspcae,halfspcae is existing
			idx_tmp = list[x].find(' ')
			if idx_tmp > 2:
				idx_insert = idx_tmp		# search idx_harlfspace

			print("idx_insert")
			if idx_insert > 2:
				'''
				print("chack1:{}".format(list[x][idx_insert]))
				if list[x][idx_insert] == '\n':
					list[x].replace('\n',' ')
				else:
					list[x].replace('\n',' ')
				'''
				head_char = list[x][0]
				list[x].replace(head_char,' '+head_char,1)
				print("check2:{}".format(list[x]))
				list[x][idx_insert+1:].strip(' ')
				#del_u3000_for_line(list[x][idx_insert+1:])
			else:									#  Not lf,fullspcae,halfspcae is existing
				print("check3")
				if not list[x][3].isdigit(): 		# [1/4aa]
					list[x].replace(list[x][2],list[x][2]+' ')
					del_u3000_for_line(list[x][4:])			# [1/4 aa]
				elif not list[x][4].isdigit():		# [12/4aa]
					list[x].replace(list[x][3],list[x][3]+' ')
					del_u3000_for_line(list[x][5:])
				elif not list[x][5].isdigit():		# [11/14aa]
					list[x].replace(list[x][4],list[x][4]+' ')
					del_u3000_for_line(list[x][6:])
				else:
					print('insert Error!')
					print(list[x])
		print("[2] list[{}]:{}\n".format(x,list[x]))
		#break

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

def main():
	f = open('database.csv', 'w')

	wsheet  = worksheet_acquisition(0) # シートのindexを任意で入力
	records = wsheet.get_all_records() # head=1を指定すると便利らしい

	keys = list(records[0].keys())
	key_len = len(keys)
	
	chenge_u3000(keys,key_len)
	insert_space_end_date(keys,key_len)
	for i in range(len(keys)):
		#chenge_u3000(keys,key_len)
		#insert_space_end_date(keys,key_len)
		if i != (key_len-1): print('{},'.format(keys[i]),end='',file=f)
		if i == (key_len-1): print('{}'.format(keys[i]),file=f)

	for record in records:
		tmp = list(record.values())
		length = len(tmp)
		del_u3000_for_list(tmp,length)

		for i in range(length):
			if i != (length-1) and tmp[i] != 0: print('{},'.format(tmp[i]),end='',file=f)
			if i == (length-1) and tmp[i] != 0: print('{}'.format(tmp[i]),file=f)

if __name__ == '__main__':
	main()
