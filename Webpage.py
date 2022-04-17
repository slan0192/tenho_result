#!/usr/local/bin/python3

import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Hiragino Sans'

def createHeader():
	now = datetime.datetime.now()
	html = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja-JP">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="main.css" type="text/css" />
  <script src="result_data.js"></script>
  <script src="result_img.js"></script>
  <script src="result.js"></script>
  <title>Void</title>
</head>
<body>
  <div class="contents">
    <div class="head">
      <h1 class="title">Void</h1>
      <h2 class="subtitle">天鳳の結果</h2>
      <div class="updated_date">Updated {year}/{mon}/{day}</div>
    </div>
""".format(year=now.year, mon=now.month, day=now.day).strip() + "\n"
	return html

def createFooter():
	html = "  </div>\n</body>\n</html>\n"
	return html

def createMenu(logs, all):
	min_y = all["min_year"]
	max_y = all["max_year"] + 1
	html = "    <div class=\"menu\">\n"
	for y in reversed(range(min_y, max_y)):
		html += "      <div><a href=\"javascript:void(0);\" onclick=\"showDetail('top5', '{year}');\">{year}年</a></div>\n".format(year=y)
	html += "	  <div>個人成績</div>\n	  <ul>\n"
	for m in sorted(logs.items(), key=lambda x:x[1]["update"], reverse=True):
		html += "        <li><a href='javascript:void(0);' onclick='showDetail(\"personal\", {id});'>{name}</a></li>\n".format(id=m[1]["id"], name=m[0])
	html += "      </ul>\n    </div>\n"
	return html

def createMain():
	html = "    <div id=\"result\" class=\"main\">\n    </div>\n"
	return html

def createDataForJS_Top5(datas, item):
	js = "      " + item + ": [\n"
	n = 0
	for d in datas[item]:
		js += "        {name: \"" + d["name"] + "\", value: " + str(d["value"]) + "},\n"
		n += 1
		if n >= 5:
			break
	js += "      ],\n"
	return js

def createDataForJS(logs, all):
	min_y = all["min_year"]
	max_y = all["max_year"] + 1
	js = "var top5_data = {\n"
	for y in range(min_y, max_y):
		js += "  " + str(y) + ": {\n"
		for tp in range(3, 5):
			tp = str(tp)
			js += "    " + tp + ": {\n"
			js += createDataForJS_Top5(all["top5"][y][tp], "score")
			js += createDataForJS_Top5(all["top5"][y][tp], "top_rate")
			js += createDataForJS_Top5(all["top5"][y][tp], "top_count")
			js += createDataForJS_Top5(all["top5"][y][tp], "bestscore")
			js += createDataForJS_Top5(all["top5"][y][tp], "avoidlast")
			js += "    },\n"
		js += "  },\n"
	js += "};\n"
	js += "\nvar personal_data = [\n"
	for m in logs:
		js += "  {\n"
		js += "    name: '" + m + "',\n"
		js += "    id: " + str(logs[m]["id"]) + ",\n"
		js += "    lastupdate: " + str(logs[m]["update"]) + ",\n"
		for y in range(min_y, max_y):
			if logs[m][y]["3"]["n"] == 0 and logs[m][y]["4"]["n"] == 0:
				continue
			js += "    " + str(y) + ": {\n"
			for tp in range(3, 5):
				tp = str(tp)
				if logs[m][y][tp]["n"] == 0:
					continue
				js += "      " + tp + ": {\n"
				js += "        count: {n},\n".format(n=logs[m][y][tp]["n"])
				js += "        score: {sc},\n".format(sc=logs[m][y][tp]["score"])
				js += "        order: [\n          "
				for od in logs[m][y][tp]["order"]:
					js += "{od},".format(od=od)
				js += "\n        ],\n"
				js += "        bestscore: {sc},\n".format(sc=logs[m][y][tp]["bestscore"])
				if "avoidlast" in logs[m][y][tp]:
					js += "        avoidlast: {val},\n".format(val=logs[m][y][tp]["avoidlast"])
				js += "      },\n"
			js += "    },\n"
		js += "  },\n"
	js += "]"
	return js

def plot(mem_data):
	datas = mem_data["data"]
	tsc = {}
	sc = {}
	min_year = 9999
	max_year = 0
	for d in sorted(datas, key=lambda x: x["date"], reverse=True):
		y = d["date"] // 10000
		tp = d["type"]
		if not y in sc:
			sc[y] = {3: [], 4: []}
			tsc[y] = {3: 0, 4: 0}
		tsc[y][tp] += d["score"]
		sc[y][tp].append(tsc[y][tp])
		min_year = y if min_year > y else min_year
		max_year = y if max_year < y else max_year
	js = ""
	for y in range(min_year, max_year + 1):
		if not y in sc:
			continue
		sz = max(len(sc[y][3]), len(sc[y][4]))
		if sz < 5:
			continue
		div = 10 * (sz // 100) if sz >= 100 else (5 if sz > 20 else 1)
		xm = [i * div for i in range(1, sz // div + 1)]
		if div != 1:
			xm.insert(0, 1)
		plt.xticks(xm)
		plt.clf()		
		for tp in range(3, 5):
			sz = len(sc[y][tp])
			x = [i for i in range(1, sz + 1)]
			plt.plot(x, sc[y][tp], label="{tp}麻".format(tp=tp))
		plt.legend()
		fname = "img/%04d-%d.png" % (mem_data["id"], y)
		plt.savefig(fname)
		js += "    '{y}': '{fname}',\n".format(y=y, fname=fname)
	return js

def create(logs):
	all = logs.pop("___all___")
	html = createHeader()
	html += createMenu(logs, all)
	html += createMain()
	html += createFooter()
	js = createDataForJS(logs, all)

	with open("result.html", mode="w") as f:
		print(html, file=f)
	with open("result_data.js", mode="w") as f:
		print(js, file=f)

	js = "var img_list = {\n"
	for m in logs:
		img_js = plot(logs[m])
		if img_js != "":
			js += "  '{m}': ".format(m=m) + "{\n"
			js += img_js
			js += "  },\n"
	js += "};"
	with open("result_img.js", mode="w") as f:
		print(js, file=f)

