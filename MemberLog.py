#!/usr/local/bin/python3

import os

MemberListFile = "./log/member.log"

def getMemberList():
	if not os.path.exists(MemberListFile):
		return None
	
	members = {}
	fp = open(MemberListFile, "r")
	lines = fp.readlines()
	fp.close()
	for l in lines:
		tmp = l.replace("\r", "").replace("\n", "").split(",")
		members[tmp[0]] = {"file": tmp[1]}
	return members;
	
def addMember(members):
	with open(MemberListFile, mode="w") as f:
		for m in members:
			print("%s,%s" % (m, members[m]["file"]), file=f)

def readLog(f):
	logs = []
	fp = open("log/" + f, "r")
	lines = fp.readlines()
	fp.close()
	for l in lines:
		tmp = l.replace("\r", "").replace("\n", "").split(",")
		tp = int(tmp[0])
		od = int(tmp[1])
		sc = int(float(tmp[2]))
		date = int(tmp[3])
		time = tmp[4] if len(tmp) == 5 else 0
		logs.append({"type": tp, "order": od, "score": sc, "date": date, "time": time})
	
	return logs

def writeLog(fname, datas):
	with open("log/" + fname, mode="w") as f:
		for d in datas:
			print("%d,%d,%d,%d,%s" % (d["type"], d["order"], d["score"], d["date"], d["time"]), file=f)
