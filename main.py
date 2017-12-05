# -*- coding:utf-8 -*-
# python main.py "<name>"
import gspread
import sys
from datas_get import sheet_get
from data_parse import datas_parse
from oauth2client.service_account import ServiceAccountCredentials

#debug flag
debug = 1

def main(argvs):

	wsheet = sheet_get.worksheet_acquisition(0)

	# Sheetから列情報をlistで取得
	name_col_record, name_col_len = sheet_get.get_col(wsheet,2)

	if debug == 1:
		print('[+] name_col_record:{}'.format(name_col_record))

	target_row_num = datas_parse.search_name(name_col_record,argvs[1],name_col_len) + 1

	if debug == 1:
		print('[+] target_row_num:{}'.format(target_row_num))

	# Sheetから行情報をlistで取得
	target_row_record, target_row_len = sheet_get.get_row(wsheet,target_row_num)
	head_row_record, head_row_len = sheet_get.get_row(wsheet,1)

	if debug == 1:
		print('[+] head_row_record:{}'.format(head_row_record))
		print('[+] target_row_record :{}'.format(target_row_record))

	# hiduke wo list ka?
	date = '11/29'
	st,en,rest = datas_parse.time_get(date, head_row_len, head_row_record, wsheet, target_row_num-1)

	if debug == 1:
		print('[+] st:{}'.format(st))
		print('[+] en:{}'.format(en))
		print('[+] rest:{}'.format(rest))





if __name__ == '__main__':
	argvs = sys.argv
	main(argvs)