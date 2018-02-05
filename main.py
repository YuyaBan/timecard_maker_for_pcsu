# -*- coding:utf-8 -*-
# python main.py <name> <date>
# date = %Y/%M/16
import sys
import csv, datetime
from dateutil.relativedelta import relativedelta

#debug flag
debug = 1

def get_time_row(reader):
	for r in range(len(reader)):
		if reader[r][2].count("時間"):
			return r

def get_weekday(date):		# 曜日の計算
	#weekday = ["月","火","水","木","金","土","日"]
	d = datetime.datetime.strptime(date, "%Y/%m/%d")
	return d.weekday()

def get_date_list(date):
	tmp = get_weekday(date)
	day = datetime.datetime.strptime(date, "%Y/%m/%d")
	next_mounth = datetime.datetime.strptime(date, "%Y/%m/%d") + relativedelta(months=1)
	# 水曜日との日数差を計算
	if tmp < 2:
		diff = 2 - tmp
	elif tmp == 2:
		diff = 0
	else:
		diff = 7 - tmp + 2

	# dateから次の最初の水曜日(Mtgの日)を計算
	Mtg = []
	Mtg.append(datetime.datetime.strptime(date, "%Y/%m/%d") + datetime.timedelta(days=diff))
	Mtg.append(Mtg[0] + datetime.timedelta(days=7))
	Mtg.append(Mtg[1] + datetime.timedelta(days=7))

	nextMtg = Mtg[2] + datetime.timedelta(days=7)
	if nextMtg <= next_mounth:
		Mtg.append(nextMtg)
	else:
		return Mtg

	nextMtg = Mtg[3] + datetime.timedelta(days=7)
	if nextMtg <= next_mounth:
		Mtg.append(nextMtg)
	else:
		return Mtg

	nextMtg = Mtg[4] + datetime.timedelta(days=7)
	if nextMtg <= next_mounth:
		Mtg.append(nextMtg)

	return Mtg

def search_date_col(header,date):
	date_list = get_date_list(date)
	#if debug == 1: print('[*] date_list:{}'.format(date_list))
	date_col =[]
	for d in date_list:
		tmp = d.strftime('%-m/%-d') + ' '
		for h in range(len(header)):
			if header[h].count(tmp):
				date_col.append(h)
	return date_col

def search_name_row(reader,name):
	i = 0
	if name.count(' '):
		print('[-] include space in serching name')
		quit()
	for row in reader:
		if row[1] == name:
			return i
		i += 1

def time_get(reader,name_row,time_row,date_col):   # Mtg時間を取得
	time_tmp=[]
	time =[]
	for t in date_col:
		if reader[name_row][t] == '1':	#
			print("start normal:{},user:{}".format(reader[time_row][t],reader[name_row][t]))
			time.append(parse_time_normal(reader[time_row][t]))
		elif reader[name_row][t] == '0':
			print("kesseki:{},user:{}".format(reader[time_row][t],reader[name_row][t]))
			time.append(['0:00','0:00','0'])
		else:
			print("late_or_early:{},user:{}".format(reader[time_row][t],reader[name_row][t]))
			time.append(parse_time_late_or_early(reader[time_row][t],reader[name_row][t]))
		print("t:{},time:{}".format(t,time))
		#time.append(time_tmp)
	return time

def parse_time_normal(data):	# 通常出席（1）の場合
	time = []
	index_kyu =  data.find('休')
	print(data)
	if index_kyu == -1:
		print('[-] not include 休')
		quit()
	time.append(data[0:index_kyu-6])
	time.append(data[index_kyu-5:index_kyu])
	index_h = data.find('h')
	if index_h == -1 or index_h < index_kyu:
		print('[-] not include h or reverse')
		quit()
	time.append(str(data[index_kyu+2:index_h]))
	print(time[2])
	return time

def parse_time_late_or_early(data,user_data):		# 遅刻or出席の場合
	index_colon = user_data.find(':')
	index_wave = user_data.find('~')
	if index_wave < 0:
		index_wave = user_data.find('〜')
	if index_wave < 0:
		index_wave = user_data.find('～')
	index_kyu = user_data.find('休')
	index_h = user_data.find('h')
	time = parse_time_normal(data)
	print("kyu:{},col:{},wave:{}".format(index_kyu,index_colon,index_wave))
	if user_data.count(':') > 1 : # oo:oo~oo:ooパターン[oo:oo~oo:oo(休oh)]
		print(111)
		time[0] = user_data[index_colon-2:index_wave]
		time[1] = user_data[index_wave+2:index_wave+6]
		time[2] = str(user_data[index_kyu+2:index_h])
	elif index_colon < index_wave : # 遅刻パターン[oo:oo~ (休oh)]
		print(222)
		time[0] = user_data[index_colon-2:index_wave]
		if index_kyu > 0:
			time[2] = str(user_data[index_kyu+2:index_h])
	elif index_wave < index_colon : # 早退パターン[~oo:oo (休oh)]
		print(333)
		time[1] = user_data[index_wave+2:index_wave+6]
		if index_kyu > 0:
			time[2] = str(user_data[index_kyu+2:index_h])
	else: # 不明パターン[]
		print(4445)
		time[0] = 'error'
		time[1] = 'error'
		time[2] = '0'
	return time

def main(argvs):

	'''
	0.databaseからデータをlistにして取得
	1.人の名前(name)を探す(行番号) => name_row = 24
	2.日付を探す(timecardの範囲)(列番号) => date_col = [1,2,3,4]
		変数dateは、timecardの初日(2/17,3/17.5/17など)
	3.各日の開始時間、終了時間、休憩時間を取得 => list = [[18:00,21:00,0.25],[18:00,....}
	4.ページとして出力　= > HTML?
	EX
	5.エクセルシートに出力（DL）
	'''

# name(名前),date(日付)
	name = argvs[1]
	date = argvs[2]
	reader = []
	header = []

#### 0.databaseからデータをlistにして取得
	f = open('database.csv', 'r')

	read = csv.reader(f)			# reader is list(csv_data)
	head = next(read)				# header is list(header)

	for row in read:
		reader.append(row)

	for row in head:
		header.append(row)

#### 1.人の名前(name)を探す(行番号)
	name_row = search_name_row(reader,name)   # 名前がある行番号を取得
	if debug == 1:
		print('[*] name_row:{}'.format(name_row))

#### 2.日付を探す(timecardの範囲)(列番号)
	date_col = search_date_col(header,date)
	if debug == 1:
		print('[*] Mtg:{}'.format(date_col))
		print('{},{},{},{}'.format(header[date_col[0]],header[date_col[1]],header[date_col[2]],header[date_col[3]]))

#### 3.各日の開始時間、終了時間、休憩時間を取得
## 時間の列を取得
	time_row = get_time_row(reader[name_row:]) + name_row
	if debug == 2:
		print('[*] time_row:{}'.format(reader[time_row]))
	time = time_get(reader,name_row,time_row,date_col)

	if debug == 1:
		print('[*] st:{}'.format(time))

if __name__ == '__main__':
	argvs = sys.argv
	main(argvs)