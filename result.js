var now_year;
window.onload = function() {
	var date = new Date();
	now_year = date.getFullYear();
    showTop5(now_year);
};

function showTop5(year) {
    var result = document.getElementById("result");
    var html = "<h3>" + year + "年の TOP5 </h3>";
    var order = ["１", "２", "３", "４", "５"];
    for (var tp = 3; tp <= 4; tp++) {
        if (top5_data[year][tp]["score"].length > 0) {
            html += '<div class="blk">';
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + '麻：得点</div>';
            html += "    <table class=\"result\">";
            for (var i = 0; i < top5_data[year][tp]["score"].length; i++) {
                if (top5_data[year][tp]["score"][i]["name"] != undefined)
                    html += "<tr><td>" + order[i] + ".</td><td>" + top5_data[year][tp]["score"][i]["name"] + "</td><td>" + top5_data[year][tp]["score"][i]["value"] + "</td></tr>";
            }
            html += "    </table>";
            html += "  </div>";
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + '麻：１位率</div>';
            html += "    <table class=\"result\">";
            for (var i = 0; i < top5_data[year][tp]["top_rate"].length; i++) {
                if (top5_data[year][tp]["top_rate"][i]["name"] != undefined)
                    html += "<tr><td>" + order[i] + ".</td><td>" + top5_data[year][tp]["top_rate"][i]["name"] + "</td><td>" + top5_data[year][tp]["top_rate"][i]["value"] + "%</td></tr>";
            }
            html += "    </table>";
            html += "  </div>";
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + '麻：１位回数</div>';
            html += "    <table class=\"result\">";
            for (var i = 0; i < top5_data[year][tp]["top_count"].length; i++) {
                if (top5_data[year][tp]["top_count"][i]["name"] != undefined)
                    html += "<tr><td>" + order[i] + ".</td><td>" + top5_data[year][tp]["top_count"][i]["name"] + "</td><td>" + top5_data[year][tp]["top_count"][i]["value"] + "回</td></tr>";
            }
            html += "    </table>";
            html += "  </div>";
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + '麻：ゲーム最高スコア</div>';
            html += "    <table class=\"result\">";
            for (var i = 0; i < top5_data[year][tp]["bestscore"].length; i++) {
                if (top5_data[year][tp]["bestscore"][i]["name"] != undefined)
                    html += "<tr><td>" + order[i] + ".</td><td>" + top5_data[year][tp]["bestscore"][i]["name"] + "</td><td>" + top5_data[year][tp]["bestscore"][i]["value"] + "</td></tr>";
            }
            html += "    </table>";
            html += "  </div>";
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + '麻：ラス回避率</div>';
            html += "    <table class=\"result\">";
            for (var i = 0; i < top5_data[year][tp]["avoidlast"].length; i++) {
                if (top5_data[year][tp]["avoidlast"][i]["name"] != undefined)
                    html += "<tr><td>" + order[i] + ".</td><td>" + top5_data[year][tp]["avoidlast"][i]["name"] + "</td><td>" + top5_data[year][tp]["avoidlast"][i]["value"] + "%</td></tr>";
            }
            html += "    </table>";
            html += "  </div>";
            html += "</div>";
        }
    }
    result.innerHTML = html;
}

function showPersonal(id) {
    var result = document.getElementById("result");
    var html = "<h3>" + personal_data[id]["name"] + "の結果</h3>";
    for (var y = now_year; y >= 2017; y--) {
        if (personal_data[id][y] == undefined)
            continue;
        html += '<h4>' + y + "年</h4>";
        html += '<div class="blk">';
        for (var tp = 3; tp <= 4; tp++) {
            if (personal_data[id][y][tp] == undefined)
                continue;
            var count = personal_data[id][y][tp]["count"];
            var score = personal_data[id][y][tp]["score"];
            var bestscore = personal_data[id][y][tp]["bestscore"];
            var avoidlast = personal_data[id][y][tp]["avoidlast"];
            var od = 0;
            html += '  <div class="blk_contents">';
            html += '    <div class="blk_contents_title">' + tp + "麻：" + count + "回</div>";
            html += '      <table class="result">';
            for (var k = 0; k < tp; k++) {
                var v = personal_data[id][y][tp]["order"][k];
                html += "<tr><td>" + (k+1) + "位率</td><td>" + (v / count * 100).toFixed(2) +  "%</td></tr>";
                od += (k + 1) * v;
            }
            html += "<tr><td>合計得点</td><td>" + score + "</td></tr>";
            html += "<tr><td>平均得点</td><td>" + (score / count).toFixed(2) + "</td></tr>";
            html += "<tr><td>平均順位</td><td>" + (od / count).toFixed(2) + "</td></tr>";
            html += "<tr><td>最高スコア</td><td>" + bestscore + "</td></tr>";
            if (avoidlast != undefined)
                html += "<tr><td>ラス回避率</td><td>" + avoidlast + "位</td></tr>";
            html += "    </table>";
            html += "  </div>";
        }
        var nam = personal_data[id]["name"];
        if (img_list[nam] != undefined && img_list[nam][y] != undefined) {
            html += '  <img src="' + img_list[nam][y] + '" width="50%" />';
        }
        html += "</div>";
    }
    result.innerHTML = html;
}

function showDetail(tp, val) {
    switch (tp) {
        case "top5":
            showTop5(val);
            break;
        case "personal":
            showPersonal(val);
            break;
    }
}
