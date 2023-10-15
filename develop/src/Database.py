import __main__
if 'main_AutoUpdater' in __main__.__file__: 
    from logger_AutoUpdater import logger
elif 'main_PDFMaker' in __main__.__file__: 
    from logger_PDFMaker import logger
elif 'main_Initiator' in __main__.__file__:
    from logger_Initiator import logger
import tqdm
import pymssql
from abc import *
import pandas as pd
from datetime import datetime

class Database(object):
    def __init__(self, today=None):
        # self._conn = pymssql.connect(server='localhost', user='sa', password='!hanshin22', database='AutocareHCB')
        self._conn = pymssql.connect(server='192.168.0.35', user='sa', password='shin#0313', database='AutocareHCB')
        self.today = today if today else datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        self._patient_info = {
            'RegistKey' : 'RegistKey, 검진자구별키',
            'CheckupDate' : 'per1_date, 검진일자',
            'PatientName' : 'per1_name, 성명',
            'PatientBirthday' : 'per1_birth_date, 생년월일',
            'PatientAge' : 'per1_age, 나이',
            'AgeGroup' : 'age_group, 연령그룹',
            'PatientSex' : 'per1_gender, 성별'
        }
        self._munjin_lifestyle = {
            'per1_life_code1' : 'per1_life_code1,생활습관(음주),음주',
            'per1_life_code2' : 'per1_life_code2,생활습관(흡연),흡연',
            'per1_life_code3' : 'per1_life_code3,생활습관(운동),신체활동',
            'per1_life_code4' : 'per1_life_code4,생활습관(체중),근력운동',
        }
        self._munjin_pastHistory = {
            'per1_kwa2' : 'per1_kwa2, 과거력(고혈압),고혈압',
            'per1_kwa3' : 'per1_kwa3, 과거력(뇌졸중),뇌졸중',
            'per1_kwa4' : 'per1_kwa4, 과거력(심장병),심장병',
            'per1_kwa5' : 'per1_kwa5, 과거력(당뇨병),당뇨',
            'per1_kwa6' : 'per1_kwa6, 과거력(암),암',
        }
        self._munjin_combined = {
            'N121115_2' : '생활습관 종합',
            'N121116_1' : '유질환 종합'
        }    
        self._munjin_paper = {
            'per1_spc_year' : 'per1_spc_year, 검진년도',
            'N1101011':'mj1_1_1, 뇌졸중 진단여부[현재/과거]',
            'N1101021':'mj1_1_2, 뇌졸중 약물치료여부[현재]',
            'N1101012':'mj1_2_1, 심근경색 진단여부[현재/과거]',
            'N1101022':'mj1_2_2, 심근경색 약물치료여부[현재]',
            'N1101013':'mj1_3_1, 고혈압 진단여부[현재/과거]',
            'N1101023':'mj1_3_2, 고혈압 약물치료여부[현재]',
            'N1101014':'mj1_4_1, 당뇨병 진단여부[현재/과거]',
            'N1101024':'mj1_4_2, 당뇨병 약물치료여부[현재]',
            'N1101015':'mj1_5_1, 이상지질혈증 진단여부[현재/과거]',
            'N1101025':'mj1_5_2, 이상지질혈증 약물치료여부[현재]',
            'N1101016':'mj1_6_1, 폐결핵 진단여부[현재/과거]',
            'N1101026':'mj1_6_2, 폐결핵 약물치료여부[현재]',
            'N1101017':'mj1_7_1, 기타 진단여부[현재/과거]',
            'N1101027':'mj1_7_2, 기타 약물치료여부[현재]',
            'N1102011':'mj2_1, 뇌졸중 가족력 (부모/형제자매 발병/사망여부)',
            'N1102012':'mj2_2, 심근경색 가족력 (부모/형제자매 발병/사망여부)',
            'N1102013':'mj2_3, 고혈압 가족력 (부모/형제자매 발병/사망여부)',
            'N1102014':'mj2_4, 당뇨병 가족력 (부모/형제자매 발병/사망여부)',
            'N1102015':'mj2_5, 기타 가족력 (부모/형제자매 발병/사망여부)',
            'N110301':'mj3, B형 바이러스',
            'N110401':'mj4, 흡연',
            'N110406':'mj5, 전자담배',
            'N110501':'mj6, 액상 전자담배',
            'N110601':'mj71, 음주 일주일',
            'N110602':'mj72, 음주 한달',
            'N110603':'mj73, 음주 1년',
            'N110604':'mj74, 음주 안함',
            'N110701':'mj8_1, 1주일 고강도 운동',
            'N110702':'mj8_2_1, 하루 고강도 운동 시간',
            'N110703':'mj8_2_2, 하루 고강도 운동 분',
            'N110801':'mj9_1, 1주일 중강도 운동',
            'N110802':'mj9_2_1, 하루 중강도 운동 시간',
            'N110803':'mj9_2_2, 하루 중강도 운동 분',
            'N110804':'mj10, 1주일 팔굽혀펴기',
        }
        self._blood_codes = {
            'TP01':'height, 신장', 
            'TP02':'weight, 체중', 
            'GP01':'wai_cir, 허리둘레', 
            'GP02':'bmi, 체질량지수', 
            'TP00':'obesity, 비만도', 
            'TP07':'blood_press_high, 혈압(최고)',
            'TP08':'blood_press_low, 혈압(최저)', 
            'C037':'total_col, 총 콜레스테롤', 
            'C039':'hdl_col, HDL-콜레스테롤', 
            'C904':'ldl_col_cal, LDL-콜레스테롤(계산)', 
            'C038':'tri_gly, TG-중성지방',
            'C026':'r_gtp, 감마-지티피(r-GTP)', 
            'C027':'liver_bilirubin, 총 빌리루빈', 
            'C029':'liver_protein, 총 단백', 
            'C030':'liver_albumin, 알부민',
            'C054':'liver_globulin, 글로부린', 
            'C022':'liver_ast, 간암지표_,유효혈액검사_AST(GOT)', 
            'C023':'liver_alt, 간암지표_유효혈액검사_ALT(GPT)', 
            'C024':'liver_alp, 간암지표_유효혈액검사_ALP', 
            'C018':'glucose, glucose(공복혈당)',
            'U008':'urine_protein, 요단백', 
            'C032':'creatinine, 크레아티닌', 
            'E001':'liver_b_antigen, 간암지표_B형간염표면항원(ECLIA)',
            'I521':'stomach_helico_bacter, 위암지표_헬리코박터', 
            'I105':'lung_cyfra21_1, 폐암지표_Cyfra 21-1(ECLIA)', 
            'I022':'lar_int_cea, 대장암지표_대장암표지자(CEA)',
            'I348':'lar_int_ca19, 대장암지표_대장암표지자(CA19-9)', 
            'I502':'thy_tsh, 갑상선암지표_갑상선자극호르몬(TSH)', 
            'I503':'thy_ft4, 갑상선암지표_FreeT4', 
            'I349':'breast_ca15_3, 유방암지표_CA15-3'
        }
        self._percents ={
            "percent_01":"간암 발병확률",
            "percent_02":"위암 발병확률",
            "percent_03":"폐암 발병확률",
            "percent_04":"대장암 발병확률",
            "percent_05":"갑상선암 발병확률",
            "percent_06":"유방암 발병확률",
            "percent_07":"뇌졸중 발병확률",
            "percent_08":"심근경색 발병확률",
            "percent_09":"당뇨병 발병확률",
            "percent_10":"폐결핵 발병확률",
            "percent_11":"고혈압 발병확률",
            "percent_12":"고지혈증 발병확률",
            "percent_13":"지방간 발병확률",
            "percent_14":"단백뇨 발병확률"
        }

class DBPreprocessor(Database):
    def __init__(self, today=None):
        super().__init__(today)

    def __fill_lifestyle(self):
        cursor = self._conn.cursor()
        for key in self._munjin_lifestyle.keys():
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {key} = 1 WHERE {key} IS NULL AND N121115_2 LIKE '%{self._munjin_lifestyle[key].split(',')[-1]}%'"
            cursor.execute(sql)
            self._conn.commit()
            
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {key} = 0 WHERE {key} IS NULL AND (N121115_2 LIKE '%해당사항%' or N121115_2 LIKE '%해당 사항%')"
            cursor.execute(sql)
            self._conn.commit()

    def __fill_pastHistory(self):
        cursor = self._conn.cursor()
        for key in self._munjin_pastHistory.keys():
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {key} = 1 WHERE {key} IS NULL AND N121116_1 LIKE '%{self._munjin_pastHistory[key].split(',')[-1]}%'"
            cursor.execute(sql)
            self._conn.commit()
            
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {key} = 0 WHERE {key} IS NULL AND (N121116_1 LIKE '%해당사항%' or N121116_1 LIKE '%해당 사항%')"
            cursor.execute(sql)
            self._conn.commit()

    def __fill_pastHistory_usingMunjinPaperCodes(self):
        # 'per1_kwa2' : 'per1_kwa2, 과거력(고혈압),고혈압',
        # 'per1_kwa3' : 'per1_kwa3, 과거력(뇌졸중),뇌졸중',
        # 'per1_kwa4' : 'per1_kwa4, 과거력(심장병),심장병',
        # 'per1_kwa5' : 'per1_kwa5, 과거력(당뇨병),당뇨',
        # 'per1_kwa6' : 'per1_kwa6, 과거력(암),암',
        
        # 'N1101011':'mj1_1_1, 뇌졸중 진단여부[현재/과거]',
        # 'N1101012':'mj1_2_1, 심근경색 진단여부[현재/과거]',
        # 'N1101013':'mj1_3_1, 고혈압 진단여부[현재/과거]',
        # 'N1101014':'mj1_4_1, 당뇨병 진단여부[현재/과거]',
        # 'N1101017':'mj1_7_1, 기타 진단여부[현재/과거]',
        cursor = self._conn.cursor()
        
        # 'N1101013':'mj1_3_1, 고혈압 진단여부[현재/과거]' -> per1_kwa2 = 1
        sql = f"UPDATE AutocareHCB.dbo.Patient SET per1_kwa2 = 1 WHERE per1_kwa2 IS NULL AND N1101013 = 1"
        cursor.execute(sql)
        self._conn.commit()
        
        # 'N1101011':'mj1_1_1, 뇌졸중 진단여부[현재/과거]', -> per1_kwa3 = 1
        sql = f"UPDATE AutocareHCB.dbo.Patient SET per1_kwa3 = 1 WHERE per1_kwa3 IS NULL AND N1101011 = 1"
        cursor.execute(sql)
        self._conn.commit()
        
        # 'N1101012':'mj1_2_1, 심근경색 진단여부[현재/과거]', -> per1_kwa4 = 1
        sql = f"UPDATE AutocareHCB.dbo.Patient SET per1_kwa4 = 1 WHERE per1_kwa4 IS NULL AND N1101012 = 1"
        cursor.execute(sql)
        self._conn.commit()
        
        # 'N1101014':'mj1_4_1, 당뇨병 진단여부[현재/과거]', -> per1_kwa5 = 1
        sql = f"UPDATE AutocareHCB.dbo.Patient SET per1_kwa5 = 1 WHERE per1_kwa5 IS NULL AND N1101014 = 1"
        cursor.execute(sql)
        self._conn.commit()
        
        # # 'N1101017':'mj1_7_1, 기타 진단여부[현재/과거]', 에 ~암있을 경우, -> per1_kwa6 = 1
        # sql = f"UPDATE AutocareHCB.dbo.Patient SET per1_kwa6 = 1 WHERE per1_kwa6 IS NULL AND N1101017 = 1 AND "
        # cursor.execute(sql)
        # self._conn.commit()
        
    def __remove_allWhiteSpace(self):
        cursor = self._conn.cursor()
        columns = list(self._munjin_paper)[1:]+list(self._blood_codes.keys())
        
        for c in tqdm.tqdm(columns, "공백 제거 중.."):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = TRIM({c}) WHERE {c} LIKE '% %'"
            cursor.execute(sql)
        self._conn.commit()    
 
    def __convert_vacantValue_as_null(self):
        cursor = self._conn.cursor()
        columns = list(self._munjin_combined.keys())+ list(self._munjin_paper.keys()) + list(self._blood_codes.keys())
        
        for c in tqdm.tqdm(columns, '빈값을 null로 변환'):
            sql=f"UPDATE AutocareHCB.dbo.Patient SET {c} = NULL WHERE ({c}) = ''"
            cursor.execute(sql)
        self._conn.commit()
    
    def __analysis_faminlyhistory_pasthistory(self):
        cursor = self._conn.cursor()
        target_columns = {'뇌졸중_과거력':'per1_kwa3', '뇌졸중_가족력':'N1102011',
                          '심근경색_과거력':'N1101012', '심근경색_가족력':'N1102012',
                          '당뇨병_과거력':'per1_kwa5', '당뇨병_가족력':'N1102014',
                          '폐결핵_과거력':'N1101016',# '폐결핵_가족력':'mj2_2',
                          '고혈압_과거력':'per1_kwa2', '고혈압_가족력':'N1102013',
                          '고지혈증_과거력':'N1101015'}
        
        for c in list(target_columns.keys()):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {target_columns[c]} = 5 WHERE {target_columns[c]} = 1"
            cursor.execute(sql)
            
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {target_columns[c]} = 0 WHERE {target_columns[c]} != 5 AND {target_columns[c]} != 0"
            cursor.execute(sql)
            
            sql = f"UPDATE AutocareHCB.dbo.Patient set {target_columns[c]} = 0 WHERE {target_columns[c]} IS NULL"
            cursor.execute(sql)
            
        self._conn.commit()
    
    def __fill_null_bloodcode_as_candidateData(self):
        cursor = self._conn.cursor()
        columns = list(self._blood_codes.keys())
            
        for c in tqdm.tqdm(columns, f"혈액검사 결측치 채우는 중..."):
            # check null data existance
            sql = f"SELECT RegistKey, AgeGroup, PatientSex, {c} \
                FROM AutocareHCB.dbo.Patient WHERE {c} IS NULL"
            cursor.execute(sql)
            datas = cursor.fetchall()
            
            if datas:
                # get candidate data
                candidate_value = {}
                sql = f"SELECT AgeGroup, PatientSex, candidate_value FROM AutocareHCB.dbo.Candidate WHERE analysis_index = '{c}'"
                cursor.execute(sql)
                datas = cursor.fetchall()
                
                for d in datas:
                    candidate_value[f'{d[0]}_{d[1]}'] = d[2]
                    
                # fill candidate
                for AgeGroup in range(1, 15):
                    for gender in ['남', '여']:
                        sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = '{candidate_value[f'{AgeGroup}_{gender}']}' WHERE {c} is  null AND AgeGroup = {AgeGroup} AND PatientSex='{gender}'"
                        cursor.execute(sql)
                        self._conn.commit()
        self._conn.commit()
    
    def __update_as_null(self, target_sql):
        cursor = self._conn.cursor()
        columns = list(self._blood_codes.keys())
            
        for c in tqdm.tqdm(columns, "혈액검사 컬럼 %.%.% -> Null 변환"):
            sql = target_sql.format(c = c)
            cursor.execute(sql)
            datas = cursor.fetchall()
            
            
            for d in datas:
                sql = f"UPDATE AutocareHCB.dbo.Patient SET {c}=Null WHERE RegistKey = '{d[0]}'"
                cursor.execute(sql)
            self._conn.commit()
        self._conn.commit()

    def __update_as_to(self, target, to):
        cursor = self._conn.cursor()
        columns = list(self._blood_codes.keys())
            
        for c in tqdm.tqdm(columns, f"혈액검사 컬럼 {target} -> {to} 변환"):
            sql = f"SELECT RegistKey, {c} FROM AutocareHCB.dbo.Patient WHERE {c} LIKE '%{target}%'"
            cursor.execute(sql)
            datas = cursor.fetchall()
            
            for d in datas:
                replace_to = d[1].replace(target, to)
                sql = f"UPDATE AutocareHCB.dbo.Patient SET {c}='{replace_to}' WHERE RegistKey = '{d[0]}'"
                cursor.execute(sql)
            self._conn.commit()
        self._conn.commit()
        
    def __clean_specialCharacters_in_bloodCodes(self):
        # , -> .
        self.__update_as_to(',', '.')
        # %..% -> %.%
        self.__update_as_to('..', '.')
        # %.%.% -> null
        sql = "SELECT RegistKey, {c} FROM AutocareHCB.dbo.Patient WHERE {c} LIKE '%.%.%'"
        self.__update_as_null(sql)
        # startswith(). -> null
        sql = "SELECT RegistKey, {c} FROM AutocareHCB.dbo.Patient WHERE substring({c}, 1, 1) = '.'"
        self.__update_as_null(sql)

    def __remove_outliers(self):
        # tp01 키가 500이상인 데이터 -> Null로 업데이트 
        # tp02 2몸무게가 500이상인 데이터 -> Null로 업데이트
        # gp01 허리둘레가 500이상인 데이터 -> Null로 업데이트
        cursor = self._conn.cursor()
        remove_column_target = ['TP01', 'TP02', 'GP01']
        for c in tqdm.tqdm(remove_column_target, '이상치 null로 변환'):
            sql = f"UPDATE Patient SET {c} = null FROM (SELECT {c} FROM AutocareHCB.dbo.Patient WHERE {c} IS NOT NULL AND ISNUMERIC({c}) = 1) Patient WHERE cast({c} as numeric) > (SELECT cast(500.0 AS FLOAT))"
            cursor.execute(sql)
            self._conn.commit()
        self._conn.commit()
    
    def __calculate_bmi(self):
        cursor = self._conn.cursor()
        sql = "UPDATE AutocareHCB.dbo.Patient SET gp02 = round(cast(tp02 AS FLOAT)/power(cast(tp01 AS FLOAT)/100, 2), 1) WHERE ISNUMERIC(tp01) = 1 And ISNUMERIC(tp02) = 1 And\
                tp01 IS NOT NULL And tp02 IS NOT NULL And gp02 IS NULL"
        cursor.execute(sql)
        logger.info('신장, 체중을 이용한 BMI 계산 완료')
        self._conn.commit()
        
    def __calculate_obesity(self):
        cursor = self._conn.cursor()
        sql = "UPDATE AutocareHCB.dbo.Patient \
                SET tp00 = (CASE \
                                WHEN gp02 < (SELECT cast(18.5 AS FLOAT)) THEN '1' \
                                WHEN gp02 >= (SELECT cast(18.5 AS FLOAT)) AND gp02 < (SELECT cast(25.0 AS FLOAT)) THEN '2' \
                                WHEN gp02 >= (SELECT cast(25.0 AS FLOAT)) AND gp02 < (SELECT cast(30.0 AS FLOAT)) THEN '3' \
                                WHEN gp02 >= (SELECT cast(30.0 AS FLOAT)) AND gp02 < (SELECT cast(35.0 AS FLOAT)) THEN '4' \
                                WHEN gp02 >= (SELECT cast(35.0 AS FLOAT)) THEN '5' \
                            END) \
                WHERE tp00 IS NULL AND gp02 IS NOT NULL AND ISNUMERIC(gp02) = 1"
        cursor.execute(sql)
        logger.info('BMI를 이용한 비만도 계산 완료')
        self._conn.commit()
    
    def __preprocess_korMixedColumns(self):
        cusror = self._conn.cursor()
        # tp00 비만도 한글값 치환
        sql = "UPDATE AutocareHCB.dbo.Patient \
                    SET tp00 = (CASE  \
                                    WHEN tp00 = '저체중' THEN '1'  \
                                    WHEN tp00 = '정상체중' THEN '2' \
                                    WHEN tp00 = '비만1단계' THEN '3' \
                                    WHEN tp00 = '비만2단계' THEN '4' \
                                    WHEN tp00 = '비만3단계' THEN '5' \
                                    else null \
                                END) \
                    WHERE ISNUMERIC(tp00) = 0"
        cusror.execute(sql)
        logger.info('비만도 한글 데이터 치환 완료')
        
        # u008 요단백 한글값 치환 -> numeric인 경우와 아닌경우 두번 sql 실행
        sql = "UPDATE AutocareHCB.dbo.Patient \
                SET u008 = (CASE \
                                WHEN u008 = '음성' THEN '0'\
                                WHEN u008 = '약양성' THEN '1'\
                                WHEN u008 = '양성' THEN '1'\
                END)\
                FROM AutocareHCB.dbo.Patient\
                WHERE u008 IS NOT NULL AND ISNUMERIC(u008)=0"
        cusror.execute(sql)

        # else null 있으면 안됨 -> 기존에 숫자로 맞춰진애들 전부 null됨
        sql = "UPDATE AutocareHCB.dbo.Patient \
                SET u008 = (CASE \
                                WHEN u008 = '+1' THEN '2'\
                                WHEN u008 = '+2' THEN '3'\
                                WHEN u008 = '+3' THEN '4'\
                                WHEN u008 = '+4' THEN '5'\
                                ELSE U008 \
                            END)\
                FROM AutocareHCB.dbo.Patient\
                WHERE u008 IS NOT NULL AND ISNUMERIC(u008)=1"
        cusror.execute(sql)
        logger.info('요단백 한글 데이터 치환 완료')
        
        # e001 B형간염표면항원 한글값 치환
        sql = "UPDATE AutocareHCB.dbo.Patient SET e001 = \
                (CASE\
                    WHEN e001 = '음성' THEN '0'\
                    WHEN e001 = '약양성' THEN '1'\
                    WHEN e001 = '양성' THEN '1'\
                    else null\
                END)\
                WHERE e001 IS NOT NULL AND ISNUMERIC(e001) = 0 "
        cusror.execute(sql)
        logger.info('B형간염표면항원 한글 데이터 치환 완료')
        
        # I521 헬리코박터균 한글값 치환 -> 오타는 null로 처리
        sql = "UPDATE AutocareHCB.dbo.Patient \
                SET I521 = (CASE \
                                WHEN I521 = '음성' THEN '0'\
                                WHEN I521 = '양성' THEN '1'\
                                else null\
                END)\
                FROM AutocareHCB.dbo.Patient\
                WHERE I521 IS NOT NULL AND ISNUMERIC(I521)=0"
        cusror.execute(sql)
        logger.info('헬리코박터균 한글 데이터 치환 완료')        
        self._conn.commit()
    
    def __double_check_errorData(self):
        cursor = self._conn.cursor()
        columns = list(self._blood_codes.keys())
        for c in tqdm.tqdm(columns, f"혈액검사 컬럼 오타 제거"):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = NULL WHERE isnumeric({c}) = 0"
            cursor.execute(sql)
            self._conn.commit()
        self._conn.commit()
        
    def __convert_errordata2null_from_munjin(self):
        cursor = self._conn.cursor()
        columns = list(self._munjin_lifestyle.keys())+list(self._munjin_pastHistory.keys())+list(self._munjin_paper.keys())
        for c in tqdm.tqdm(columns, f"문진 컬럼 오타 제거"):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = null WHERE ISNUMERIC({c}) = 0"
            cursor.execute(sql)
        self._conn.commit() 
    
    def __fill_null_munjin(self):
        cursor = self._conn.cursor()
        cols_fillas0 = list(self._munjin_lifestyle.keys())+list(self._munjin_pastHistory.keys())+['N110604', 'N110701', 'N110702', 'N110703', 'N110801', 'N110802', 'N110803', 'N110804']
        cols_fillas1 = ['N110401', 'N110406', 'N110501']
        cols_fillas2 = ['N1101011', 'N1101021', 'N1101012', 'N1101022', 'N1101013', 'N1101023', 'N1101014', 'N1101024', 'N1101015', 'N1101025', 'N1101016', 'N1101026', 'N1101017', 'N1101027', 'N1102011', 'N1102012', 'N1102013', 'N1102014', 'N1102015', 'N110301']
        
        # fill null as 0
        for c in tqdm.tqdm(cols_fillas0, '문진내역 0으로 채우는 중..'):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = '0' WHERE {c} IS NULL"
            cursor.execute(sql)
        self._conn.commit() 
        
        # fill null as 1
        for c in tqdm.tqdm(cols_fillas1, '문진내역 1으로 채우는 중..'):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = '1' WHERE {c} IS NULL"
            cursor.execute(sql)
        self._conn.commit() 
        
        # fill null as 2
        for c in tqdm.tqdm(cols_fillas2, '문진내역 2으로 채우는 중..'):
            sql = f"UPDATE AutocareHCB.dbo.Patient SET {c} = '2' WHERE {c} IS NULL"
            cursor.execute(sql)
        self._conn.commit()         
    
    def __remove_specialCharacters_in_munjin(self):
        cursor = self._conn.cursor()
        columns = list(self._munjin_lifestyle.keys())+list(self._munjin_pastHistory.keys())+list(self._munjin_paper.keys())
            
        for c in tqdm.tqdm(columns, f"문진 컬럼 '.' -> '' 변환"):
            sql = f"SELECT RegistKey, {c} FROM AutocareHCB.dbo.Patient WHERE {c} LIKE '%.%'"
            cursor.execute(sql)
            datas = cursor.fetchall()
            
            for d in datas:
                replace_to = d[1].replace('.', '')
                sql = f"UPDATE AutocareHCB.dbo.Patient SET {c}='{replace_to}' WHERE RegistKey = '{d[0]}'"
                cursor.execute(sql)
            self._conn.commit()
        self._conn.commit()     

    def __count_unPreprocessedData(self):
        sql = 'SELECT COUNT(*) FROM AutocareHCB.dbo.Patient WHERE percent_01 IS NULL'
        cursor = self._conn.cursor()
        cursor.execute(sql)
        counted = cursor.fetchall()
        self._conn.commit()
        return counted[0][0]

    def preprocessDB_ifNecessary(self):
        needPreprecessDB = self.__count_unPreprocessedData()
        if needPreprecessDB:
            logger.info('')
            logger.info('검진자 테이블 데이터 전처리가 필요합니다.')
            self.preprocess_DB()
        else:
            logger.info('')
            logger.info('검진자 테이블 데이터 전처리가 이미 완료되어 있습니다.')

    def preprocess_DB(self, fill_null=True):
        logger.info('검진자 테이블 데이터를 전처리 합니다.')
        self.__remove_allWhiteSpace()
        self.__fill_lifestyle()
        self.__fill_pastHistory()
        self.__fill_pastHistory_usingMunjinPaperCodes()
        self.__clean_specialCharacters_in_bloodCodes()
        self.__convert_vacantValue_as_null() # '' -> null
        self.__remove_outliers() # not
        self.__calculate_bmi()
        self.__calculate_obesity()
        self.__preprocess_korMixedColumns() # 비만도, 요단백, B형간염항원, 헬리코박터균
        self.__analysis_faminlyhistory_pasthistory() # 가족력, 과거력 채우기
        self.__double_check_errorData()
        self.__convert_errordata2null_from_munjin()
        self.__remove_specialCharacters_in_munjin() # not
        if fill_null:
            logger.info('검진자 테이블의 문진, 혈액검사 Null 데이터를 채우지 않습니다.')
            self.__fill_null_munjin()
            self.__fill_null_bloodcode_as_candidateData() # 혈액검사 결측치 채우기
        self._conn.commit()
        logger.info('검진자 테이블 데이터를 전처리 완료하였습니다.')
        logger.info('')

    def fill_null_data(self):
        logger.info('')
        logger.info('문진과 혈액검사 Null 데이터를 채웁니다.')
        self.__fill_null_munjin()
        self.__fill_null_bloodcode_as_candidateData() # 혈액검사 결측치 채우기
        self._conn.commit()

    def get_bloodCodeCriterion(self):
        cursor = self._conn.cursor()
        sql = f"SELECT analysis_index, male_min_value, male_max_value, female_min_value, female_max_value FROM AutocareHCB.dbo.BloodCodeInfo"
        cursor.execute(sql)
        return self.convert2criterionJson(cursor.fetchall())
     
    def convert2criterionJson(self, rawDB_data):
        result = {}
        for d in rawDB_data:
            result[f'{d[0]}'] = {'male_min_value':float(d[1]), 'male_max_value':float(d[2]), 'female_min_value':float(d[3]), 'female_max_value':float(d[4]),}
        return result

class CandidateDataCalculator(Database):
    def __init__(self, today=None):
        super().__init__(today)
    
    def __update_exceptedColumns(self):
        # update GP02:BMI, TP00:비만도 정상으로 채움
        cursor = self._conn.cursor()
        # BMI
        sql = f"UPDATE AutocareHCB.dbo.Candidate \
                SET candidate_value = '22' \
                WHERE analysis_index = 'GP02'"
        cursor.execute(sql)
        self._conn.commit()

        # 비만도
        sql = f"UPDATE AutocareHCB.dbo.Candidate \
                SET candidate_value = '2' \
                WHERE analysis_index = 'TP00'"
        cursor.execute(sql)
        self._conn.commit()

        # update U008:요단백, E001:B형간염항원, I521:헬리코박터  -> 모두 0으로 채움
        for index in ['U008', 'E001', 'I521']:
            sql = f"UPDATE AutocareHCB.dbo.Candidate \
                    SET candidate_value = '0' \
                    WHERE analysis_index = '{index}'"
            cursor.execute(sql)
            self._conn.commit()

    def __update_man_breast_ca15_3(self):
        cursor = self._conn.cursor()
        sql = "UPDATE AutocareHCB.dbo.Candidate \
                SET candidate_value = '0' \
                WHERE PatientSex = '남' AND analysis_index = 'I349'"
        cursor.execute(sql)
        self._conn.commit()

    def __calculate_candidateData(self):
        # print_info_msg("새로운 결측치 데이터를 계산합니다.")
        logger.info("새로운 결측치 대체값을 계산합니다.")
        cursor = self._conn.cursor()
        for c in tqdm.tqdm(self._blood_codes.keys(), '       업데이트 중 .. '):
            if c == 'GP02' or c == 'TP00' or c == 'U008' or c =='E001' or c == 'I521': # update at '__update_exceptedColumns', GP02:BMI, TP00:비만도, U008:요단백, E001:B형간염항원, I521:헬리코박터
                continue
            
            sql = f"SELECT AgeGroup, PatientSex, ROUND(AVG(CAST({c} AS FLOAT)), 1) FROM AutocareHCB.dbo.Patient  \
            WHERE ISNUMERIC({c}) = 1\
            GROUP BY AgeGroup, PatientSex ORDER BY AgeGroup"
            
            cursor.execute(sql)
            
            results = cursor.fetchall()
            for r in results:
                sql = f"UPDATE AutocareHCB.dbo.Candidate \
                        SET candidate_value = '{r[2]}' \
                        WHERE AgeGroup = {r[0]} AND PatientSex = '{r[1]}' AND analysis_index = '{c}'"
                cursor.execute(sql)
            self._conn.commit()
            
        # self.update_candidateData_of_ageGroup13n14() # 현재 데이터에 13, 14 연령대 그룹이 모두 있어서, 12그룹으로 대체하지 않고, 해당 값을 그대로 사용하기로 하였음.
        self.__update_exceptedColumns() # update GP02:BMI, TP00:비만도, U008:요단백, E001:B형간염항원, I521:헬리코박터
        self.__update_man_breast_ca15_3()
            
    def __delete_preCandidateData(self):
        logger.info('기존 결측치 대체 값 데이터를 삭제합니다.')
        sql = 'DELETE FROM AutocareHCB.dbo.Candidate'
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()

    def update_candidateData(self):
        # self.__delete_preCandidateData()
        self.__calculate_candidateData()
        self._conn.commit()

class DBHandler(metaclass=ABCMeta):
    def _convert2dataframe(self, data):
        cols = list(self._patient_info.values())
        if 'Hanshin' in str(type(self)):
            cols += list(self._munjin_lifestyle.values())+list(self._munjin_pastHistory.values())+list(self._munjin_paper.values())
        elif 'Infinity' in str(type(self)):
            cols += ['per1_spc_year']
        cols += list(self._blood_codes.values())
        cols = [i.split(',')[0] for i in cols]
        df = pd.DataFrame(data, columns= cols)
        return df
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def _select_data(self):
        pass

    @abstractmethod
    def reload_data (self):
        pass
    
    @abstractmethod
    def _deleteTB_allPeriod(self):
        pass
    
    @abstractmethod
    def _insertTB_allPeriod(self):
        pass
    
    @abstractmethod
    def add_data(self):
        pass

    @abstractmethod
    def _insertTB_onSchedule(self):
        pass

class PdfDatabase(Database):
    def __init__(self, today=None):
        super().__init__(today)
        self.patient_indexName = ['RegistKey', '검진일자', '차트번호', '검체번호', '이름', '생년월일', '성별']
        self.patient_column = 'RegistKey, CheckupDate, PatientChartNo, CheckupNo, PatientName, PatientBirthday, PatientSex'
        
        self.analysis_indexName = ['분석지표', '분석지표 한글명', '남성 최저치', '남성 최고치', '여성 최저치' '여성 최고치', '단위', '검사코드']
        self.analysis_column = 'analysis_index_kor, male_min_value, male_max_value, female_min_value, female_max_value, unit, gum_code'
        
        self.percents ={
            "percent_01":"간암",
            "percent_02":"위암",
            "percent_03":"폐암",
            "percent_04":"대장암",
            "percent_05":"갑상선암",
            "percent_06":"유방암",
            "percent_07":"뇌졸중",
            "percent_08":"심근경색",
            "percent_09":"당뇨병",
            "percent_10":"폐결핵",
            "percent_11":"고혈압",
            "percent_12":"고지혈증",
            "percent_13":"지방간",
            "percent_14":"단백뇨"
        }

    def __get_patient_searchingSQL(self, registKey, cht_no, bun_no, inspc_date, name):
        # TODO delete TOP
        sql = 'SELECT '+ self.patient_column + ' FROM AutocareHCB.dbo.Patient WHERE '
        
        temp = []
        if registKey:
            temp.append(f"RegistKey = '{registKey}'")
        if cht_no:
            temp.append(f"PatientChartNo = '{cht_no}'")
        if bun_no:
            temp.append(f"CheckupNo = '{bun_no}'")
        if inspc_date:
            temp.append(f"CheckupDate = '{inspc_date}'")
        if name:
            temp.append(f"PatientName = '{name}'")
            
        sql += ' and '.join(temp)
        sql += ' and percent_01 is not null'
        sql += ' ORDER BY CheckupDate'
        return sql

    def search_patients(self, registKey, cht_no, bun_no, inspc_date, name):
        if not (registKey or cht_no or bun_no or inspc_date or name):
            return None, None
        
        cursor = self._conn.cursor()
        
        # TODO add try except
        sql = self.__get_patient_searchingSQL(registKey, cht_no, bun_no, inspc_date, name)
        try:
            cursor.execute(sql)
            patients = cursor.fetchall()
            return self.patient_indexName, patients
        except Exception as e:
            logger.info("__get_patient_searchingSQL Error sql: "+sql)
            logger.info(e)
            return None, None
        
    def get_patients_threeDays_before(self, threeDays_before):
        cursor = self._conn.cursor()
        sql = f"SELECT RegistKey, CheckupDate, PatientChartNo, CheckupNo, PatientName, PatientBirthday, PatientSex\
            FROM AutocareHCB.dbo.Patient WHERE CheckupDate = '{threeDays_before}' AND PERCENT_01 IS NOT NULL"
        cursor.execute(sql)
        patients = cursor.fetchall()
        self._conn.commit()
        return patients    

    def __search_patient_info(self, RegistKey, PatientSex):
        try:
            cursor = self._conn.cursor()
            if PatientSex == 1:
                sql = f"SELECT pdf.[index], pdf.disease, pdf.analysis_index_kor, pdf.male_min_value, pdf.male_max_value, real_data.VALUE\
                        FROM MalePDFView AS pdf,\
                             (SELECT value, CONVERT(NVARCHAR(10), code) AS gum_code\
                                FROM\
                                    (SELECT *\
                                        FROM AutocareHCB.dbo.Patient\
                                            WHERE registkey = '{RegistKey}') A\
                                            UNPIVOT(value FOR code IN (C024,C023,C022,GP02,I349,I348,I022,I105,I502,C039,C904,I503,C026,C018,TP07,C030,U008,TP08,C038,C029,C037,C032)) AS UNPVT) \
                                            as real_data\
                        WHERE pdf.gum_code = real_data.gum_code"
                cursor.execute(sql)
                p_info = cursor.fetchall()
                self._conn.commit()
                return p_info
            else :
                sql = f"SELECT pdf.[index], pdf.disease, pdf.analysis_index_kor, pdf.female_min_value, pdf.female_max_value, real_data.VALUE\
                        FROM FemalePDFView AS pdf,\
                             (SELECT value, CONVERT(NVARCHAR(10), code) AS gum_code\
                                FROM\
                                    (SELECT *\
                                        FROM AutocareHCB.dbo.Patient\
                                            WHERE registkey = '{RegistKey}') A\
                                            UNPIVOT(value FOR code IN (C024,C023,C022,GP02,I349,I348,I022,I105,I502,C039,C904,I503,C026,C018,TP07,C030,U008,TP08,C038,C029,C037,C032)) AS UNPVT) \
                                            as real_data\
                        WHERE pdf.gum_code = real_data.gum_code"
                cursor.execute(sql)
                p_info = cursor.fetchall()
                self._conn.commit()
                return p_info
        except Exception as e:
            logger.info("__search_patient_info sql Error :" + sql.replace('    ', ''))
            logger.info(e)

    def __search_patient_percent(self, RegistKey, PatientSex):
        cursor = self._conn.cursor()
        try:
            if PatientSex == 1:
                cols = list(self._percents.keys())
                cols.remove('percent_06')
                cols = ', '.join(cols)
                sql = f"SELECT {cols} FROM AutocareHCB.dbo.Patient \
                        WHERE RegistKey='{RegistKey}'"
                cursor.execute(sql)
                percents = cursor.fetchall()
                self._conn.commit()
                return percents
            else:
                cols = ', '.join(list(self._percents.keys()))
                sql = f"SELECT {cols} FROM AutocareHCB.dbo.Patient \
                        WHERE RegistKey='{RegistKey}'"
                cursor.execute(sql)
                percents = cursor.fetchall()
                self._conn.commit()
                return percents
        except Exception as e:
            logger.info("__search_patient_percent sql Error :"+sql.replace('                        ', ' '))
            logger.info(e)

    def __convert2json_Female(cls, db_result):
        result = {'간암':{}, '위암':{}, '폐암':{}, '대장암':{}, '갑상선암':{}, '유방암':{}, '뇌졸중':{}, '심근경색':{}, '당뇨병':{}, '폐결핵':{}, '고혈압':{}, '고지혈증':{}, '지방간':{}, '단백뇨':{}}
        if db_result:
            for row in db_result:
                result[row[1]][str(row[0]%6)] = {'name':row[2], 'min':float(row[3]), 'max':float(row[4]), 'value':float(row[5])}
        return result
        
    def __convert2json_Male(cls, db_result):
        result = {'간암':{}, '위암':{}, '폐암':{}, '대장암':{}, '갑상선암':{}, '뇌졸중':{}, '심근경색':{}, '당뇨병':{}, '폐결핵':{}, '고혈압':{}, '고지혈증':{}, '지방간':{}, '단백뇨':{}}
        if db_result:
            for row in db_result:
                if row[1] =='유방암':
                    continue
                result[row[1]][str(row[0]%6)] = {'name':row[2], 'min':float(row[3]), 'max':float(row[4]), 'value':float(row[5])}
        return result 

    def __search_habits(self):
        try:
            cursor = self._conn.cursor()
            sql = 'SELECT disease, habit_guide FROM AutocareHCB.dbo.Habit'
            cursor.execute(sql)
            habits = cursor.fetchall()
            self._conn.commit()
            return habits
        except Exception as e:
            logger.info('Error! __search_habits :'+sql)
            logger.info(e)

    def __get_habit(self, disease, habits):
        for h in habits:
            if h[0] == disease:
                return h[1]

    def get_patient_data(self, patient_info):
        RegistKey, CheckupDate, PatientName, PatientBirthday, PatientSex = str(patient_info[0]), str(patient_info[1]), patient_info[4], patient_info[5], patient_info[6]
        PatientSex = 1 if PatientSex == '남' else 2
        result = {'name': PatientName, 'gender':PatientSex, 'birth_date':PatientBirthday, 'inspc_date':CheckupDate, 'diseases':{}}
        info = self.__search_patient_info(RegistKey, PatientSex)
        if PatientSex==1:
            result['diseases'].update(self.__convert2json_Male(info))
        elif PatientSex==2:
            result['diseases'].update(self.__convert2json_Female(info))
            
        percents = self.__search_patient_percent(RegistKey, PatientSex)
        habits = self.__search_habits()
        for idx, disease in enumerate(list(result['diseases'].keys())):
            result['diseases'][disease]['percent'] = percents[0][idx]
            result['diseases'][disease]['habit'] = self.__get_habit(disease, habits)
        return result
    
def reset_tabel():
    db = Database()
    cursor = db._conn.cursor()
    target_table = ['AutocareHCB.dbo.HanshinTrainData', 'AutocareHCB.dbo.Patient', 'AutocareHCB.dbo.InfinityTrainData']
    logger.info('')
    logger.info('다음 테이블 데이터를 삭제합니다. '+str(target_table))
    for tb in target_table:
        sql = f'DELETE FROM {tb}'
        cursor.execute(sql)
        db._conn.commit()
    logger.info('결측치 대체값 테이블(AutocareHCB.dbo.Candidate) 데이터를 초기화 합니다.')
    sql = 'UPDATE AutocareHCB.dbo.Candidate SET candidate_value = 0'