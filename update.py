#!/usr/local/bin/python3

import sys
import LogList
import MemberLog
import TenhoLog
import Webpage

def updateLog():
	logs = LogList.downloadLog()
	if len(logs) == 0:
		print("Don't need to update!")
		return None

	tenhoLogs = TenhoLog.readAllData()
	members = MemberLog.getMemberList()
	id = 0
	for nam in members:
		members[nam]["data"] = MemberLog.readLog(members[nam]["file"])
		id += 1

	add_member_flag = 0
	for nam in tenhoLogs:
		if not nam in members:
			add_member_flag = 1
			id += 1
			members[nam] = {"file": "%02d.log" % (id)}
		if not "data" in members[nam]:
			members[nam]["data"] = []
		for td in tenhoLogs[nam]:
			add_flg = 1
			for md in members[nam]["data"]:
				if md["date"] == td["date"] and md["time"] == td["time"]:
					add_flg = 0
					break
			if add_flg == 1:
				members[nam]["data"].append(td)
		MemberLog.writeLog(members[nam]["file"], members[nam]["data"])
		print("Update " + nam + " (" + members[nam]["file"] + ")")

	if add_member_flag == 1:
		MemberLog.addMember(members)
	TenhoLog.deleteLogFiles()
	return members

def calc(logs):
	min_year = 9999
	max_year = 0
	id = 0
	for m in logs:
		logs[m]["id"] = id
		id += 1
		logs[m]["update"] = 0
		for d in logs[m]["data"]:
			if logs[m]["update"] < d["date"]:
				logs[m]["update"] = d["date"]
			year = d["date"] // 10000
			if min_year > year:
				min_year = year
			if max_year < year:
				max_year = year
			if not year in logs[m]:
				logs[m][year] = {}
			tp = str(d["type"])
			if not tp in logs[m][year]:
				logs[m][year][tp] = {"n": 0, "score": 0, "order": [0, 0, 0, 0], "bestscore": -9999}
			logs[m][year][tp]["score"] += d["score"]
			logs[m][year][tp]["n"] += 1
			logs[m][year][tp]["order"][d["order"]] += 1
			if logs[m][year][tp]["bestscore"] < d["score"]:
				logs[m][year][tp]["bestscore"] = d["score"]

	top5 = {}
	for y in range(min_year, max_year + 1):
		for m in logs:
			if not y in logs[m]:
				logs[m][y] = {"3": {"n": 0, "score": 0, "order": [0, 0, 0, 0], "bestscore": -9999}, "4":	 {"n": 0, "score": 0, "order": [0, 0, 0, 0], "bestscore": -9999}}
			elif not "3" in logs[m][y]:
				logs[m][y]["3"] = {"n": 0, "score": 0, "order": [0, 0, 0, 0], "bestscore": -9999}
			elif not "4" in logs[m][y]:
				logs[m][y]["4"] = {"n": 0, "score": 0, "order": [0, 0, 0, 0], "bestscore": -9999}
	
		top5[y] = {}
		top5[y]["3"] = {"score": [], "top_rate": [], "top_count": [], "bestscore": [], "avoidlast": []}
		top5[y]["4"] = {"score": [], "top_rate": [], "top_count": [], "bestscore": [], "avoidlast": []}
		for tp in range(3, 5):
			tp = str(tp)
			datas = sorted(logs.items(), key=lambda x:x[1][y][tp]["score"], reverse=True)
			n = 0
			for d in datas:
				if d[1][y][tp]["n"] > 5:
					n += 1
					top5[y][tp]["score"].append({"name": d[0], "value": d[1][y][tp]["score"]})
				if n >= 5:
					break
			datas = sorted(logs.items(), key=lambda x:x[1][y][tp]["order"][0], reverse=True)
			n = 0
			for d in datas:
				if d[1][y][tp]["n"] > 5:
					n += 1
					top5[y][tp]["top_count"].append({"name": d[0], "value": d[1][y][tp]["order"][0]})
				if n >= 5 or d[1][y][tp]["n"] == 0:
					break
			datas = sorted(logs.items(), key=lambda x:x[1][y][tp]["order"][0]*100/x[1][y][tp]["n"] if x[1][y][tp]["n"] > 0 else 0, reverse=True)
			n = 0
			for d in datas:
				if d[1][y][tp]["n"] > 5:
					n += 1
					top5[y][tp]["top_rate"].append({"name": d[0], "value": d[1][y][tp]["order"][0]*10000//d[1][y][tp]["n"]/100})
				if n >= 5 or d[1][y][tp]["n"] == 0:
					break
			datas = sorted(logs.items(), key=lambda x:x[1][y][tp]["bestscore"], reverse=True)
			n = 0
			for d in datas:
				if d[1][y][tp]["n"] > 5:
					n += 1
					top5[y][tp]["bestscore"].append({"name": d[0], "value": d[1][y][tp]["bestscore"]})
				if n >= 5 or d[1][y][tp]["n"] == 0:
					break
			datas = sorted(logs.items(), key=lambda x:100-x[1][y][tp]["order"][int(tp)-1]*100/x[1][y][tp]["n"] if x[1][y][tp]["n"] > 0 else 0, reverse=True)
			n = 0
			for d in datas:
				if d[1][y][tp]["n"] > 5:
					n += 1
					logs[d[0]][y][tp]["avoidlast"] = n
					if n <= 5:
						top5[y][tp]["avoidlast"].append({"name": d[0], "value": (1-d[1][y][tp]["order"][int(tp)-1]/d[1][y][tp]["n"])*10000//1/100})
	logs["___all___"] = {"min_year": min_year, "max_year": max_year, "top5":  top5}

def updateWebpage(logs):
	Webpage.create(logs)

#main
logs = updateLog()
if logs == None:
	sys.exit()

calc(logs)
updateWebpage(logs)
