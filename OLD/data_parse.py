# -*- coding:utf-8 -*-
# data_parse.py
# record:1 or 0 or 遅刻、早退
# time_record: 全体Mtgの時間


from datas_get import sheet_get

debug = 0

class datas_parse:

	def search_name(list,name,length):   # 名前がある行数を取得
		if name.count(' '):
			print('[-] include space in serching name')
			quit()
		for n in range(length):
			if list[n] == name:
				return n

	def time_get(date, length, head, sheet, row_num):   # Mtg時間を取得
		time=[0,0,0]
		for col_num in range(length):
			if head[col_num].count(date):
				time = datas_parse.parse_time(col_num+1,sheet,row_num)
				return [time[0],time[1],time[2]]
		return [0,0,0]

	def parse_time(col_num, sheet, row_num):
		record, record_len = sheet_get.get_col(sheet,col_num)
		time = [0,0,0]
		if debug == 1:
			print('[*] record:{}'.format(record[row_num]))
	
		if record_len < row_num:
			print('[-] record_len:{} is smaller than row_num:{}'.format(record_len,row_num))
			print(record)
			return ['3:33','4:44','1.0']

		if record[row_num] == '':												# 欠席
			return [0,0,0]
		elif record[row_num] == '1':
			time = datas_parse.time_extraction(record[record_len-1])		# 最初から最後まで出席
			return [time[0],time[1],time[2]]
		else:
			time = datas_parse.attendance_and_rest_time(record[row_num],record[record_len-1])	# 遅刻、早退有り
			return [time[0],time[1],time[2]]

	def time_extraction(time_record):
		time=[0,0,0]
		if debug == 1:
			print('[*] time_record:{}'.format(time_record))
		
		index_kyu = time_record.find('休')
		if index_kyu == -1:
			print('[-] not include 休')
			quit()
		time[0] = time_record[0:index_kyu-6]
		time[1] = time_record[index_kyu-5:index_kyu]
		index_h = time_record.find('h')
		if index_h == -1 or index_h < index_kyu:
			print('[-] not include h or reverse')
			quit()
		time[2] = time_record[index_kyu+2:index_h]
		return [time[0],time[1],time[2]]

	def attendance_and_rest_time(record,time_record):
		time = [0,0,0]
		index_wave = record.find('~')
		if index_wave == -1:
			index_wave = record.find('～')
		print(index_wave)
		index_kyu = record.find('休')
		index_h = record.find('h')

		time = datas_parse.time_extraction(time_record)

		if record.count('早'):					# 早退パターン
			time[1] = record[index_wave+1:index_wave+6]
			if index_kyu > 0:
				time[2] = record[index_kyu+2:index_h]
		elif 5 < index_kyu-index_wave:			# oo:oo~oo:ooパターン
			time[0] = record[index_wave-5:index_wave]
			time[1] = record[index_wave+1:index_wave+6]
			time[2] = record[index_kyu+2:index_h]
		elif index_wave < index_kyu:			# 遅刻パターン
			time[0] = record[index_wave-5:index_wave]
			if index_kyu > 0:
				time[2] = record[index_kyu+2:index_h]
		elif index_wave > 0 and index_kyu == -1:# 遅刻 and 休憩不記載パターン
			time[0] = record[index_wave-5:index_wave]
		else:									# 不明パターン
			time[0] = '3:33'
			time[1] = '4:44'
			time[2] = '1'
		return [time[0],time[1],time[2]]






