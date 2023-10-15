var cancers = {};
var chronics = {};
var my_json;
//여기서 데이터를 받아오면 됩니다.
function setData() {
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:9999/req");
    request.send();
    request.onload = function () {
        my_json = JSON.parse(request.response);
        writeFirstHTML();
        getUserName();
        getGender();
        getBirthDate();
        getInspcDate();
        if (my_json.gender == 2) {
            getCancerContent();
        }
        getDiseases(my_json);
        writeSecondHTML();
        writeThridHTML();
    };
}

function writeFirstHTML(){
    document.write('<html lang="kr">')
    document.write('<head>')
        document.write('<meta charset="UTF-8" />')
        document.write('<title>OK AI CHECK</title>')
        document.write('<link rel="stylesheet" href="css/a4size.css" />')
        document.write('<link rel="stylesheet" href="css/layout.css" />')
        document.write('<link rel="stylesheet" href="css/coverComponents.css" />')
        // document.write('<a class="disableClick" href="src/">')
        //     document.write('<script src="js/DataHandler.js"></script>')
        //     document.write('<script>')
        //         document.write('setData();')
        //     document.write('</script>')
        // document.write('</a>')
    document.write('</head>')
    document.write('<body>')
        document.write('<div class="page">')
            document.write('<header>')
                document.write('<div class="coverBase">')
                    document.write('<div class="inner">')
                        document.write('<section id="coverHeadSpace">')
                            document.write('<div id="coverHeadLogo">')
                                document.write('<a class="disableClick" href="src/">')
                                    document.write('<img src="img/ok.png" />')
                                document.write('</a>')
                                document.write('<p>AI CHECK</p>')
                            document.write('</div>')
                            document.write('<div id="coverHeadTitle">OK AI CHECK</div>')
                            document.write('서울대 기술지주회사와 서울대 AI전공 교수들이')
                            document.write('참여하여 함께 설계한 AI질병예측 지표')
                        document.write('</section>')
                        document.write('<section id="userInfoSpace">')
                            document.write('<div class="userInfoItem">')
                                document.write('<div class="userIndex">이름</div>')
                                document.write('<div class="userValue" id="userName"></div>')
                            document.write('</div>')
                            document.write('<div class="userInfoItem">')
                                document.write('<div class="userIndex">성별</div>')
                                document.write('<div class="userValue" id="userGender"></div>')
                            document.write('</div>')
                            document.write('<div class="userInfoItem">')
                                document.write('<div class="userIndex">생년월일</div>')
                                document.write('<div class="userValue" id="userBirthDate"></div>')
                            document.write('</div>')
                            document.write('<div class="userInfoItem">')
                                document.write('<div class="userIndex">검진일자</div>')
                                document.write('<div class="userValue" id="userInspcDate"></div>')
                            document.write('</div>')
                        document.write('</section>')
                    document.write('</div>')
                document.write('</div>')
            document.write('</header>')
            document.write('<main>')
                document.write('<div class="inner">')
                    document.write('<section id="mainSpace">')
                        document.write('<div id="mainTitle">content</div>')
                        document.write('<div class="miniTitle">- 분석내용 종합</div>')
                        document.write('<div class="miniTitle">- 암 위험도 분석</div>')
                        document.write('<div class="content" id="cancerContent">')
                            document.write('· 간암 위험도 분석 <br />')
                            document.write('· 위암 위험도 분석 <br />')
                            document.write('· 폐암 위험도 분석 <br />')
                            document.write('· 대장암 위험도 분석 <br />')
                            document.write('· 갑상선암 위험도 분석 <br />')
                        document.write('</div>')
                        document.write('<div class="miniTitle">- 만성질환 위험도 분석</div>')
                        document.write('<div class="content">')
                            document.write('· 뇌졸중 위험도 분석<br />')
                            document.write('· 심근경색 위험도 분석<br />')
                            document.write('· 당뇨병 위험도 분석<br />')
                            document.write('· 폐결핵 위험도 분석<br />')
                            document.write('· 고혈압 위험도 분석<br />')
                            document.write('· 고지혈증 위험도 분석<br />')
                            document.write('· 지방간 위험도 분석<br />')
                            document.write('· 단백뇨 위험도 분석')
                        document.write('</div>')
                    document.write('</section>')
                document.write('</div>')
            document.write('</main>')
            document.write('<footer>')
                document.write('<div class="inner">')
                    document.write('<section id="mainDesc">')
                        document.write('본 분석은 서울대학교 AI개발 공식 자회사인 SNUAiLAB 과')
                        document.write('공동 연구 설계한 AI질병예측 프로그램입니다. 방대한')
                        document.write('데이터를 학습한 인공지능이 고객님의 건강검진 결과를')
                        document.write('기반으로 암질환과 만성질환에 대한 발병 위험도를 분석하여')
                        document.write('예측하게 됩니다. 다만 실제 위험도는 고객님의 생활습관,')
                        document.write('식습관, 환경요인 등 데이터에 잡히지 않는 다양한 요인에')
                        document.write('따라 달라질 수 있습니다. OK AI CHECK는 의료행위가')
                        document.write('아니므로, 자세한 사항은 반드시 의사 선생님과 상담이')
                        document.write('필요합니다.')
                    document.write('</section>')
                document.write('</div>')
                document.write('<div class="coverBase">')
                    document.write('<div class="inner"></div>')
                document.write('</div>')
            document.write('</footer>')
        document.write('</div>')
    document.write('</body>')
document.write('</html>')
}

function writeSecondHTML(){
    document.write('<!DOCTYPE html>')
    document.write('<html lang="kr">')
    document.write('<head>')
        document.write('<meta charset="UTF-8" />')
        document.write('<title>OK AI CHECK</title>')
        document.write('<link rel="stylesheet" href="css/allAnalysisComponents.css" />')
        document.write('<'+'sc'+'ri'+'pt'+' s'+'r'+'c'+'="ht'+'tps://cdn.jsdelivr.net/npm/chart.js"></'+'sc'+'ri'+'pt'+'>')
        document.write('<a class="disableClick" href="src/">')
            document.write('<'+'sc'+'ri'+'pt'+' src="js/AllAnalysisGraphs.js"></'+'sc'+'ri'+'pt'+'>')
        document.write('</a>')
    document.write('</head>')
    document.write('<body>')
        document.write('<div class="page">')
            document.write('<header>')
                document.write('<div class="base">')
                    document.write('<div class="inner">')
                        document.write('<div id="headline">OK AI CHECK</div>')
                    document.write('</div>')
                document.write('</div>')
            document.write('</header>')
            document.write('<main>')
                document.write('<div class="inner">')
                    document.write('<div id="analysisTitle">')
                        document.write('<h1>분석내용 종합</h1>')
                        document.write('OK AI CHECK의 위험도는 향후 5년 이내에 해당 질병의 발병')
                        document.write('가능성을 의미합니다.')
                    document.write('</div>')
                    document.write('<h2>암 위험도 분석</h2>')
                    document.write('<section class="analysisBlock">')
                        document.write('<div class="graphWrapper">')
                            document.write('<div class="analysisGraph">')
                                document.write('<canvas id="allCancers"></canvas>')
                            document.write('</div>')
                        document.write('</div>')
                    document.write('</section>')
                    document.write('<section class="analysisBlock">')
                        document.write('<h2>만성 질환 위험도 분석</h2>')
                        document.write('<div class="graphWrapper">')
                            document.write('<div class="analysisGraph">')
                                document.write('<canvas id="allChronics"></canvas>')
                            document.write('</div>')
                        document.write('</div>')
                    document.write('</section>')
                    document.write('<'+'sc'+'ri'+'pt'+'>')
                        document.write('drawAllAnalysisGraphs();')
                    document.write('</'+'sc'+'ri'+'pt'+'>')
                document.write('</div>')
            document.write('</main>')
            document.write('<footer>')
                document.write('<div class="base">')
                    document.write('<div class="inner">')
                        document.write('<div id="footline">')
                            document.write('<p class="desc">')
                                document.write('서울대 공식 자회사 SNUAiLAB과 INFINITYCARE 공동')
                                document.write('연구 개발&nbsp')
                            document.write('</p>')
                            document.write('<a class="disableClick" href="src/">')
                                document.write('<img id="logo" src="img/infinity_logo.png" />')
                            document.write('</a>')
                            document.write('<div id="logoDesc">')
                                document.write('인피니티케어<br />R&D 연구센터')
                            document.write('</div>')
                        document.write('</div>')
                    document.write('</div>')
                document.write('</div>')
            document.write('</footer>')
        document.write('</div>')
    document.write('</body>')
document.write('</html>')
}

function writeThridHTML(){
    document.write('<!DOCTYPE html>')
    document.write('<html lang="kr">')
        document.write('<head>')
            document.write('<meta charset="UTF-8" />')
            document.write('<title>OK AI CHECK</title>')
            document.write('<link rel="stylesheet" href="css/a4size.css" />')
            document.write('<link rel="stylesheet" href="css/layout.css" />')
            document.write('<link rel="stylesheet" href="css/analysisIndexComponents.css" />')
            document.write('<'+'sc'+'ri'+'pt'+' s'+'r'+'c'+'="ht'+'tps://cdn.jsdelivr.net/npm/chart.js"></'+'sc'+'ri'+'pt'+'>')
            document.write('<'+'sc'+'ri'+'pt'+' s'+'r'+'c'+'="ht'+'tps://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.min.js"></'+'sc'+'ri'+'pt'+'>')
            document.write('<'+'sc'+'ri'+'pt'+' s'+'r'+'c'+'="ht'+'tps://cdn.rawgit.com/chartjs/Chart.LinearGauge.js/master/Chart.LinearGauge.js"></'+'sc'+'ri'+'pt'+'>')
            document.write('<a class="disableClick" href="src/">')
                document.write('<'+'sc'+'ri'+'pt'+' src="js/AnalysisIndexGraphs.js"></'+'sc'+'ri'+'pt'+'>')
                document.write('<'+'sc'+'ri'+'pt'+' src="js/AnalysisIndexHTMLWriter.js"></'+'sc'+'ri'+'pt'+'>')
            document.write('</a>')
        document.write('</head>')
        document.write('<'+'sc'+'ri'+'pt'+' src="json/AnalysisIndex.json" type="text/javascript"></'+'sc'+'ri'+'pt'+'>')
        document.write('<'+'sc'+'ri'+'pt'+'>')
            document.write('writeHTMLs();')
        document.write('</'+'sc'+'ri'+'pt'+'>')
        document.write('</html>')
}

function getUserName() {
    document.getElementById("userName").innerText = my_json.name;
}
function getGender() {
    if (my_json.gender == 1) {
        document.getElementById("userGender").innerText = "남성";
    } else {
        document.getElementById("userGender").innerText = "여성";
    }
}
function getBirthDate() {
    document.getElementById("userBirthDate").innerText = my_json.birth_date;
}
function getInspcDate() {
    document.getElementById("userInspcDate").innerText = my_json.inspc_date;
}

function getCancerContent() {
    document.getElementById("cancerContent").innerText +=
        "· 유방암 위험도 분석";
}

function getDiseases(data) {
    for (const key in data["diseases"]) {
        if (key.endsWith("암")) {
            cancers[key] = data["diseases"][key];
            cancers[key]["dangerRange"] = setDangerRange(cancers[key]);
        } else {
            chronics[key] = data["diseases"][key];
            chronics[key]["dangerRange"] = setDangerRange(chronics[key]);
        }
    }
    cancers = resort_cancers(cancers);
    chronics = resort_chronics(chronics);

    return cancers, chronics;
}

function resort_cancers(cancers) {
    var temp = {};
    var seq = ["간암", "위암", "폐암", "대장암", "갑상선암"];
    if (Object.keys(cancers).length != seq.length) {
        seq.push("유방암");
    }
    for (const s of seq) {
        temp[s] = cancers[s];
    }
    return temp;
}

function resort_chronics(chronics) {
    var temp = {};
    var seq = [
        "뇌졸중",
        "심근경색",
        "당뇨병",
        "폐결핵",
        "고혈압",
        "고지혈증",
        "지방간",
        "단백뇨",
    ];
    for (const s of seq) {
        temp[s] = chronics[s];
    }
    return temp;
}

function setDangerRange(data) {
    const percent = data["percent"];
    if (percent >= 0 && percent <= 20) {
        return "정상";
    } else if (percent > 20 && percent <= 40) {
        return "관심";
    } else if (percent > 40 && percent <= 60) {
        return "주의";
    } else if (percent > 60 && percent <= 80) {
        return "경계";
    } else if (percent > 80 && percent <= 100) {
        return "위험";
    } else {
        console.error("Invalid percent");
    }
}
