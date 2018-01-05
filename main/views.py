# coding=UTF-8
from django.shortcuts import render
from django.http import HttpResponse
import MySQLdb
import json
import urllib2
import datetime
# Create your views here.
def here(request):
	db = MySQLdb.connect(host="localhost", user = "root", passwd = "ling0926", db = "small_class", use_unicode=True, charset="utf8")
	cursor = db.cursor()
	ids = [['s11','s12','s13','s14','s15','s16'],['s21','s22','s23','s24','s25','s26'],['s31','s32','s33','s34','s35','s36'],['s41','s42','s43','s44','s45','s46'],['s51','s52','s53','s54','s55','s56'],['s61','s62','s63','s64','s65','s66'],['s71','s72','s73','s74','s75','s76'],['s81','s82','s83','s84','s85','s86'],['s91','s92','s93','s94','s95','s96'],['s01','s02','s03','s04','s05','s06']]
	score = []
	i = 0
	weeks = request.GET.get("week")
	date = request.GET.get("day")
	sql = "INSERT INTO week_time(week_no, date) VALUES ('" + weeks + "','" + date + "')"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	sql = "SELECT * FROM student"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	for row in cursor.fetchall():
		ss = {}
		ss["no"] = row[0]
		ss["name"] = row[1]
		ss["t1"] = request.GET.get(ids[i][0],None)
		ss["t2"] = request.GET.get(ids[i][1],None)
		ss["t3"] = request.GET.get(ids[i][2],None)
		ss["t4"] = request.GET.get(ids[i][3],None)
		ss["t5"] = request.GET.get(ids[i][4],None)
		ss["t6"] = ""
		ss["t6"] += request.GET.get(ids[i][5],None)
		i += 1
		score.append(ss)
	sql = "INSERT INTO scoreboard(week_no, no, attend, score1, score2, score3, point) VALUES "
	sql2 = "INSERT INTO reason_board(week_no, no, reason) VALUES "
	for t in score:
		sql += "('" + weeks + "','" + str(t["no"]) + "','" + str(t["t5"]) + "'," + str(t["t1"]) + "," + str(t["t2"]) + "," + str(t["t3"]) + "," + str(t["t4"]) + "),"
		if len(t["t6"]) > 0:
			sql2 += "('" + weeks + "','" + str(t["no"]) + "','" + t["t6"] + "'),"
	sql = sql[0:-1]
	sql2 = sql2[0:-1]
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	try:
		cursor.execute(sql2)
		db.commit()
	except:
		db.rollback()
	db.close()
	return HttpResponse(sql)

def main(request):
	db = MySQLdb.connect(host="localhost", user = "root", passwd = "ling0926", db = "small_class", use_unicode=True, charset="utf8")
	cursor = db.cursor()
	sql = "SELECT * FROM student"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	data = []
	ids = [['s11','s12','s13','s14','s15','s16'],['s21','s22','s23','s24','s25','s26'],['s31','s32','s33','s34','s35','s36'],['s41','s42','s43','s44','s45','s46'],['s51','s52','s53','s54','s55','s56'],['s61','s62','s63','s64','s65','s66'],['s71','s72','s73','s74','s75','s76'],['s81','s82','s83','s84','s85','s86'],['s91','s92','s93','s94','s95','s96'],['s01','s02','s03','s04','s05','s06']]
	i = 0
	for row in cursor.fetchall():
		dic = {}
		dic["no"] = row[0]
		dic["name"] = row[1]
		dic['id1'] = ids[i][0]
		dic['id2'] = ids[i][1]
		dic['id3'] = ids[i][2]
		dic['id4'] = ids[i][3]
		dic['id5'] = ids[i][4]
		dic['id6'] = ids[i][5]
		i = i+1
		data.append(dic)
	db.close()
	return render(request, "main.html", locals())

def final(request):
	def sqls(str):
		datas = 0
		try:
			cursor.execute(str)
			db.commit()
		except:
			db.rollback()
		for row in cursor.fetchall():
			if row[0] is None:
				datas = 0
			else:
				datas = row[0]
		return datas
	def result(tt, id):
		if id == 0:
			if tt >= 98:
				return '特優'
			elif tt >= 94:
				return '優'
			elif tt >= 90:
				return '甲'
			elif tt >= 86:
				return '乙'
			else :
				return '丙'
		elif id == 1:
			if tt >= 95:
				return '特優'
			elif tt >= 90:
				return '優'
			elif tt >= 85:
				return '甲'
			elif tt >= 80:
				return '乙'
			else :
				return '丙'
		elif id == 2:
			if tt >= 500:
				return '特優'
			elif tt >= 300:
				return '優'
			elif tt >= 150:
				return '甲'
			elif tt >= 100:
				return '乙'
			else :
				return '丙'
		else:
			if tt >= 100:
				return '特優'
			elif tt >= 90:
				return '優'
			elif tt >= 80:
				return '甲'
			elif tt >= 70:
				return '乙'
			else :
				return '丙'
	student_no = request.GET.get("st",0)
	db = MySQLdb.connect(host="localhost", user = "root", passwd = "ling0926", db = "small_class", use_unicode=True, charset="utf8")
	cursor = db.cursor()
	sql = "SELECT * FROM student"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	data = []
	for row in cursor.fetchall():
		dic = {}
		dic["no"] = row[0]
		dic["name"] = row[1]
		data.append(dic)
	sql = "SELECT a.date, b.reason FROM week_time a, reason_board b WHERE a.week_no = b.week_no AND b.no = " + str(student_no)
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	leave = []
	for row in cursor.fetchall():
		dic = {}
		dic["date"] = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d').strftime('%m/%d')
		dic["reason"] = row[1]
		leave.append(dic)
	sql = "SELECT name FROM student WHERE no = " + str(student_no)
	names = sqls(sql)
	sql = "SELECT COUNT(*) FROM scoreboard WHERE no = " + str(student_no) + " AND (attend='attend' OR attend='late')"
	attends = sqls(sql)
	sql = "SELECT COUNT(*) FROM scoreboard WHERE no = " + str(student_no) + " AND attend='late'"
	lates = sqls(sql)
	sql = "SELECT COUNT(*) FROM scoreboard WHERE no = " + str(student_no) + " AND attend='leave'"
	leaves = sqls(sql)
	sql = "SELECT COUNT(*) FROM scoreboard WHERE no = " + str(student_no) + " AND attend='sick'"
	sicks = sqls(sql)
	sql = "SELECT COUNT(*) FROM scoreboard WHERE no = " + str(student_no) + " AND attend='absent'"
	absents = sqls(sql)
	sql = "SELECT COUNT(*) AS a FROM `week_time` WHERE 1"
	classes = sqls(sql)
	sql = "SELECT SUM(score1) FROM scoreboard WHERE no = " + str(student_no)
	score1 = sqls(sql)
	sql = "SELECT SUM(score2) FROM scoreboard WHERE no = " + str(student_no)
	score2 = sqls(sql)
	sql = "SELECT SUM(score3) FROM scoreboard WHERE no = " + str(student_no)
	score3 = sqls(sql)
	sql = "SELECT SUM(point) FROM scoreboard WHERE no = " + str(student_no)
	points = sqls(sql)
	sql = "SELECT SUM(score1)/COUNT(score1) FROM scoreboard WHERE no = " + str(student_no) 
	score1_avg = sqls(sql)
	sql = "SELECT SUM(score2)/COUNT(score2) FROM scoreboard WHERE no = " + str(student_no) 
	score2_avg = sqls(sql)
	sql = "SELECT SUM(score3)/COUNT(score3) FROM scoreboard WHERE no = " + str(student_no) 
	score3_avg = sqls(sql)
	final_total = score1_avg + score2_avg + score3_avg + points
	total = score1 + score2 + score3 + points
	sql = "SELECT SUM(score1)/COUNT(score1) FROM scoreboard GROUP BY no ORDER BY SUM(score1)/COUNT(score1) ASC"
	ss = ['score1','score2','score3']
	ss_2 = [score1_avg,score2_avg,score3_avg]
	ss_3 = {}
	score4 = ['740','0','0','0','0','140','0','0','0']
	ss_4 = ['優','0','0','0','0','甲','0','0','0','0']
	realscore4 = score4[int(student_no)-1]
	realss_4 = ss_4[int(student_no)-1]
	kk = 0
	for dd in ss:
		k = 0
		sql = "SELECT SUM("+dd+")/COUNT("+dd+") FROM scoreboard GROUP BY no ORDER BY SUM("+dd+")/COUNT("+dd+") ASC"
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
		for row in cursor.fetchall():
			if ss_2[kk] >= row[0]:
				k+=1
		ss_3[ss[kk]] = result(ss_2[kk],kk)
		kk+=1
	sql = "SELECT SUM(point) FROM scoreboard GROUP BY no ORDER BY SUM(point) ASC"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	k = 0
	for row in cursor.fetchall():
		if points >= row[0]:
			k+=1
	ss_3['point'] = result(points, 3)
	return render(request, "final.html", locals())
def example(request):
	return render(request, "example.html", locals())
def data(request):
	db = MySQLdb.connect(host="localhost", user = "root", passwd = "ling0926", db = "small_class", use_unicode=True, charset="utf8")
	cursor = db.cursor()
	sql = "SELECT b.no, b.name, SUM(a.score1), SUM(a.score2), SUM(a.score3), SUM(a.point) ,SUM(a.score1)/COUNT(a.score1)+SUM(a.score2)/COUNT(a.score2)+SUM(a.score3)/COUNT(a.score3)+SUM(a.point) AS total FROM scoreboard a, student b WHERE a.no = b.no GROUP BY b.no ORDER BY total DESC, SUM(a.score1)+SUM(a.score2)+SUM(a.score3)+SUM(a.point) DESC"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	data = []
	for row in cursor.fetchall():
		dic = {}
		dic["no"] = row[0]
		dic["name"] = row[1]
		dic["sum1"] = row[2]
		dic["sum2"] = row[3]
		dic["sum3"] = row[4]
		dic["sum4"] = row[5]
		dic["sum5"] = row[6]
		data.append(dic)
	return render(request, "data.html", locals())
