# 한신메디피아 AutocareHCB

한신메디피아의 검진자 정보를 이용하여 14개의 질병에 대하여 5년내에 발병할 확률을 예측하는 프로젝트입니다. <br><br>
14개의 질병 : 간암, 위암, 폐암, 대장암, 갑상선암, 유방암, 뇌졸중, 심근경색, 당뇨병, 폐결핵, 고혈압, 고지혈증, 지방간, 단백뇨

-----
### 요구사항

<img src="https://user-images.githubusercontent.com/116786798/231621857-9677c6db-0f10-450b-8fe5-61c07ce14af2.png" width="700" height="1000">

상세한 프로젝트 관련 서류는 `AI 전략사업 > 문서 > 사업개발팀 > Projects > 한신메디피아` 경로의 OneDrive에 있습니다.

-----
### Skills
- Python
- Javascript
- html & CSS
- pyqt5
- mssql
- BigData

-----
### Repository 구성
```plain text
hanshin-medipia/
├── 납품파일
│    ├── resources : AuotcareHCB 데이터 베이스 구축에 필요한 파일
│    │   ├── database_setup
│    │   │   ├── BloodCodeInfo.dat           데이터 파일
│    │   │   ├── Candidate.dat               데이터 파일
│    │   │   ├── DiseasePerBloodCodes.dat    데이터 파일
│    │   │   ├── Habit.dat                   데이터 파일
│    │   │   ├── Create_BloodCodeInfo.sql
│    │   │   ├── Create_Candidate.sql
│    │   │   ├── Create_DiseasePerBloodCodes.sql
│    │   │   ├── Create_Habit.sql
│    │   │   ├── Create_HanshinTrainData.sql
│    │   │   ├── Create_InfinityTrainData.sql
│    │   │   ├── Create_Patient.sql
│    │   │   ├── Create_FemalePDFView.sql
│    │   │   ├── Create_MalePDFView.sql
│    │   │   └── newPatientInsert.sql
│    │   └── src : PDF를 생성하기 위해 필요한 파일들
│    │       ├── css
│    │       │   ├── a4size.css
│    │       │   ├── allAnalysisComponents.css
│    │       │   ├── analysisIndexComponents.css
│    │       │   ├── coverComponents.css
│    │       │   └── layout.css
│    │       ├── img
│    │       │   ├── infinity_logo.png
│    │       │   ├── 경계.jpg
│    │       │   ├── 정상.jpg
│    │       │   ├── 주의.jpg
│    │       │   ├── 위험.jpg
│    │       │   ├── 관심.jpg
│    │       │   └── ok.png
│    │       ├── js
│    │       │   ├── AllAnalysisGraphs.js
│    │       │   ├── AnalysisIndexGraphs.js
│    │       │   ├── AnalysisIndexHTMLWriter.js
│    │       │   └── DataHandler.js
│    │       ├── result.html
│    │       └── ui
│    │           └── pdfGenerator.ui
│    └── src : 프로그램 관련 코드
│       ├── Database.py
│       ├── PdfMaker.py
│       ├── Preprocessor.py
│       ├── HanshinPredictor.py
│       ├── HanshinTrainer.py
│       ├── InfinityTrainer.py
│       ├── logger_AutoUpdater.py
│       ├── logger_Initiator.py
│       ├── logger_PDFMaker.py
│       ├── main_APIServer.py
│       ├── main_AutoUpdater.py
│       ├── main_Initiator.py
│       └── main_PDFMaker.py
├── develop
│   ├── create_AutocareHCB.sql
│   ├── create_AutocareHCBView.sql
│   ├── create_HealthMIS.sql
│   ├── percent분포.sql
│   ├── 이상치확인용.sql
│   └── 대체값계산.sql
├── README.md
└── requirements.txt
```

-----

### 한신메디피아 개발환경



-----

### Class Diagram


![image](https://user-images.githubusercontent.com/116786798/232376042-44b02efc-73c5-43bf-8022-082a47a54983.png)

