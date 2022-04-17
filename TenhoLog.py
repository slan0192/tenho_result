#!/usr/local/bin/python3

import os
import shutil
import glob

ROOM_NAME = "L1000"

def readLog(f, logs):
	date = int(f.replace("tmp/", "").replace(".log", "").replace("sca", ""))
	fp = open(f, "r")
	lines = fp.readlines()
	for l in lines:
		if not ROOM_NAME in l:
			continue;
		tmp = l.replace("\n", "").split("|")
		tp = 3 if "三" in tmp[2] else (4 if "四" in tmp[2] else 0)
		od = 0;
		for mem in tmp[3].replace("+","").replace(")","").strip().split(" "):
			nam, sc = mem.split("(")
			if not nam in logs:
				logs[nam] = []
			logs[nam].append({"type": tp, "order": od, "score": int(float(sc)), "date": int(date), "time": tmp[1].strip()})
			od += 1
	fp.close()

def readAllData():
	logs = {}
	for f in glob.glob("tmp/*"):
		readLog(f, logs)
	
	return logs;

def deleteLogFiles():
	shutil.rmtree("tmp/")
	os.mkdir("tmp/")
