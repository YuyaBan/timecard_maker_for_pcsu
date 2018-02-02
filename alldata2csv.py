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

def del_u3000(list,length):				 # \u3000 を削除する　and 空のセルをlistから削除
	for w in range(length):
		if isinstance(list[w],str):
			list[w] = list[w].replace('\u3000','')
			list[w] = list[w].replace('\n','')
			list[w] = list[w].replace(' ','')
'''
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
'''

def insert_space_end_date(list,length):
	for x in range(length):
		# [12/1aa]4[1/4aa]3[1/12aa]4[12/12aa]5->[12/12 aa]
		try:
			if not list[x][0].isdigit() : flag = 1
		except IndexError:
			print('try-catch!')
			flag = 1
		while flag == 0:
			if not list[x][3].isdigit():	#[1/4aa]
				list[x].replace(list[x][2],list[x][2]+' ')
			elif not list[x][4].isdigit():	#[1/4aa]
				list[x].replace(list[x][3],list[x][3]+' ')
			elif not list[x][5].isdigit():	#[1/4aa]
				list[x].replace(list[x][4],list[x][4]+' ')
			else:
				print('insert Error!')
				print(list[x])
				quit()
			break
		flag = 0

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

	for i in range(len(keys)):
		del_u3000(keys,key_len)
		insert_space_end_date(keys,key_len)
		if i != (key_len-1): print('{},'.format(keys[i]),end='',file=f)
		if i == (key_len-1): print('{}'.format(keys[i]),file=f)

	for record in records:
		tmp = list(record.values())
		length = len(tmp)
		del_u3000(tmp,length)

		for i in range(length):
			if i != (length-1) and tmp[i] != 0: print('{},'.format(tmp[i]),end='',file=f)
			if i == (length-1) and tmp[i] != 0: print('{}'.format(tmp[i]),file=f)

if __name__ == '__main__':
	main()
