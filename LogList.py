#!/usr/local/bin/python3

import os
import requests
import subprocess

DownloadedListFile = "./log/downloaded_list.log"
TenhoLogURLBase = "https://tenhou.net/sc/raw/dat/"
TenhoLogListURL = "https://tenhou.net/sc/raw/list.cgi"

def getDownloadedLogList():
	if (not os.path.exists(DownloadedListFile)):
		return None

	logs = {}
	data = open(DownloadedListFile, "r")
	lines = data.readlines()
	for l in lines:
		tmp = l.split(",")
		logs[tmp[0]] = int(tmp[1])

	return logs

def parse(str):
	tmp = str.split(",")
	f_tmp = tmp[0].split(":")
	path = f_tmp[1].replace("'", "")
	if "/" in path:
		f_tmp = path.split("/")
		fname = f_tmp[1]
	else:
		fname = path
	sz_tmp = tmp[1].split(":")
	size = int(sz_tmp[1].replace("}", ""))
	return {"file": fname, "path": path, "size": size}

def getLogList(isOld):
	lists = []
	url = TenhoLogListURL + ("?old" if isOld == 1 else "")
	urlInfo = requests.get(url)
	
	tenholog_list = urlInfo.text.split("\n")
	for i in range(1, len(tenholog_list) - 2):
		if not "sca" in tenholog_list[i]:
			continue

		data = parse(tenholog_list[i])		
		lists.append(data)

	return lists

def downloadLog():
	dl_logs = [];
	log_list = getLogList(1)
	log_list.extend(getLogList(0))
	dled_list = getDownloadedLogList()
	if dled_list == None:
		dled_list = {}
	for d in log_list:
		if (not d["file"] in dled_list) or (d["size"] != dled_list[d["file"]]):
			url = TenhoLogURLBase + d["path"]
			path = "./tmp/" + d["file"]
			args = ["curl", url, "-o", path]
			subprocess.call(args)
			args = ["gzip", "-d", path]
			subprocess.call(args)
			dled_list[d["file"]] = d["size"]
			dl_logs.append(d["file"].replace(".gz", ""))
			continue

	with open(DownloadedListFile, mode="w") as log_file:
		for  f in dled_list:
			print("%s,%d" % (f, dled_list[f]), file=log_file)

	return dl_logs
