import __main__
if 'main_AutoUpdater' in __main__.__file__: 
    from logger_AutoUpdater import logger
elif 'main_PDFMaker' in __main__.__file__: 
    from logger_PDFMaker import logger
elif 'main_Initiator' in __main__.__file__:
    from logger_Initiator import logger
import os
import glob
import tqdm
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, Normalizer
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
from Database import DBHandler, DBPreprocessor
from Preprocessor import preprocess_hanshinData
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HanshinModelPredictorDBHandler(DBHandler, DBPreprocessor):
    def __init__(self, today=None):
        super().__init__(today)

    def _deleteTB_allPeriod(self):
        sql = 'DELETE FROM AutocareHCB.dbo.Patient'
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()
    
    def _insertTB_allPeriod(self):
        now_updateDate = self.today - relativedelta(days=3)
        cursor = self._conn.cursor()
        sql = f"""DECLARE @patientInfo TABLE(
                    [RegistKey] [uniqueidentifier] NOT NULL,
                    [CheckupNo] [int] NOT NULL,
                    [PatientChartNo] [varchar](50) NULL,
                    [CheckupDate] [date] NULL,
                    [PatientName] [varchar](50) NULL,
                    [PatientBirthday] [varchar](50) NULL,
                    [PatientAge] [decimal](9, 3) NOT NULL,
                    [AgeGroup] [smallint] NULL,
                    [PatientSex] [varchar](50) NULL
                );

                INSERT INTO @patientInfo 
                    SELECT RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, 
                            (CASE 
                                WHEN cast(PatientAge as int) < 20 THEN 1  
                                WHEN cast(PatientAge as int) >= 20 AND cast(PatientAge as int) < 30 THEN 2 
                                WHEN cast(PatientAge as int) >= 30 AND cast(PatientAge as int) < 35 THEN 3 
                                WHEN cast(PatientAge as int) >= 35 AND cast(PatientAge as int) < 40 THEN 4 
                                WHEN cast(PatientAge as int) >= 40 AND cast(PatientAge as int) < 45 THEN 5 
                                WHEN cast(PatientAge as int) >= 45 AND cast(PatientAge as int) < 50 THEN 6 
                                WHEN cast(PatientAge as int) >= 50 AND cast(PatientAge as int) < 55 THEN 7 
                                WHEN cast(PatientAge as int) >= 55 AND cast(PatientAge as int) < 60 THEN 8 
                                WHEN cast(PatientAge as int) >= 60 AND cast(PatientAge as int) < 65 THEN 9 
                                WHEN cast(PatientAge as int) >= 65 AND cast(PatientAge as int) < 70 THEN 10 
                                WHEN cast(PatientAge as int) >= 70 AND cast(PatientAge as int) < 75 THEN 11 
                                WHEN cast(PatientAge as int) >= 75 AND cast(PatientAge as int) < 80 THEN 12 
                                WHEN cast(PatientAge as int) >= 80 AND cast(PatientAge as int) < 85 THEN 13 
                                WHEN cast(PatientAge as int) >= 85 THEN 14 
                            ELSE NULL END) as AgeGroup,
                            PatientSex
                    FROM HealthMIS.dbo.HmisRegistPatient
                    where RegistStatusType = 2 and CheckupDate>='2019-01-01' and CheckupDate<='{now_updateDate}';

                insert into AutocareHCB.dbo.Patient(RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex, per1_spc_year, N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014, N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013, N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701, N110702, N110703, N110801, N110802, N110803, N110804, TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027, C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022, I348, I502, I503, I349)
                    select info.RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex,
                            SUBSTRING(cast(CheckupDate as nvarchar), 1, 4),
                            N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014,
                            N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013,
                            N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701,
                            N110702, N110703, N110801, N110802, N110803, N110804,
                            TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027,
                            C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022,
                            I348, I502, I503, I349
                    from @patientInfo info
                        left outer join
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, MunjinValue 
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, CheckupDataCode as DataCode, ResultValue1 as MunjinValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistNational ON HmisRegistNational.RegistKey = info.RegistKey
                                            where CheckupDataCode in ('N121115_2', 'N121116_1', 'N1101011', 'N1101021', 'N1101012', 'N1101022', 'N1101013', 'N1101023', 'N1101014', 'N1101024', 'N1101015', 'N1101025', 'N1101016', 'N1101026', 'N1101017', 'N1101027', 'N1102011', 'N1102012', 'N1102013', 'N1102014', 'N1102015', 'N110301', 'N110401', 'N110406', 'N110501', 'N110601', 'N110602', 'N110603', 'N110604', 'N110701', 'N110702', 'N110703', 'N110801', 'N110802', 'N110803', 'N110804')
                                            group by info.RegistKey, CheckupDataCode, ResultValue1) as temp_munjin
                                    where info.registkey = temp_munjin.registkey) AS result
                            PIVOT (min(MunjinValue) FOR datacode IN ([N121115_2], [N121116_1], [N1101011], [N1101021], [N1101012], [N1101022], [N1101013], [N1101023], [N1101014],
                            [N1101024], [N1101015], [N1101025], [N1101016], [N1101026], [N1101017], [N1101027], [N1102011], [N1102012], [N1102013],
                            [N1102014], [N1102015], [N110301], [N110401], [N110406], [N110501], [N110601], [N110602], [N110603], [N110604], [N110701],
                            [N110702], [N110703], [N110801], [N110802], [N110803], [N110804])) as pivoted_munjin) as munjin on info.RegistKey = munjin.RegistKey
                        left outer join 
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, BloodValue
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, RegistDataCode as DataCode, ResultValue1 as BloodValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistResult ON HmisRegistResult.RegistKey = info.RegistKey
                                            where RegistDataCode in ('TP01', 'TP02', 'GP01', 'GP02', 'TP00', 'TP07', 'TP08', 'C037', 'C039', 'C904', 'C038', 'C026', 'C027', 'C029', 'C030', 'C054', 'C022', 'C023', 'C024', 'C018', 'U008', 'C032', 'E001', 'I521', 'I105', 'I022', 'I348', 'I502', 'I503', 'I349')
                                            group by info.RegistKey, RegistDataCode, ResultValue1) as temp_Blood
                                    where info.registkey = temp_Blood.registkey) AS result
                            PIVOT (min(BloodValue) FOR datacode IN 
                            ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904], [C038], [C026], [C027], 
                            [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], 
                            [I348], [I502], [I503], [I349])) as pivoted_blood) as blood on info.RegistKey = blood.RegistKey;
                """
        cursor.execute(sql)
        self._conn.commit()

    def reload_data(self):
        # self._deleteTB_allPeriod()
        # logger.info('한신메디피아 검진자 테이블(Patient) 데이터 삭제 완료')
        logger.info('')
        logger.info('한신메디피아 검진자 테이블(Patient) 데이터를 새로 불러옵니다..')
        self._insertTB_allPeriod()
        logger.info('완료')

    def _insertTB_onSchedule(self):
        pre = self.today - relativedelta(days=4)
        aft = self.today - relativedelta(days=2)
        cursor = self._conn.cursor()
        sql = f"""DECLARE @patientInfo TABLE(
                    [RegistKey] [uniqueidentifier] NOT NULL,
                    [CheckupNo] [int] NOT NULL,
                    [PatientChartNo] [varchar](50) NULL,
                    [CheckupDate] [date] NULL,
                    [PatientName] [varchar](50) NULL,
                    [PatientBirthday] [varchar](50) NULL,
                    [PatientAge] [decimal](9, 3) NOT NULL,
                    [AgeGroup] [smallint] NULL,
                    [PatientSex] [varchar](50) NULL
                );

                INSERT INTO @patientInfo 
                    SELECT RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, 
                            (CASE 
                                WHEN cast(PatientAge as int) < 20 THEN 1  
                                WHEN cast(PatientAge as int) >= 20 AND cast(PatientAge as int) < 30 THEN 2 
                                WHEN cast(PatientAge as int) >= 30 AND cast(PatientAge as int) < 35 THEN 3 
                                WHEN cast(PatientAge as int) >= 35 AND cast(PatientAge as int) < 40 THEN 4 
                                WHEN cast(PatientAge as int) >= 40 AND cast(PatientAge as int) < 45 THEN 5 
                                WHEN cast(PatientAge as int) >= 45 AND cast(PatientAge as int) < 50 THEN 6 
                                WHEN cast(PatientAge as int) >= 50 AND cast(PatientAge as int) < 55 THEN 7 
                                WHEN cast(PatientAge as int) >= 55 AND cast(PatientAge as int) < 60 THEN 8 
                                WHEN cast(PatientAge as int) >= 60 AND cast(PatientAge as int) < 65 THEN 9 
                                WHEN cast(PatientAge as int) >= 65 AND cast(PatientAge as int) < 70 THEN 10 
                                WHEN cast(PatientAge as int) >= 70 AND cast(PatientAge as int) < 75 THEN 11 
                                WHEN cast(PatientAge as int) >= 75 AND cast(PatientAge as int) < 80 THEN 12 
                                WHEN cast(PatientAge as int) >= 80 AND cast(PatientAge as int) < 85 THEN 13 
                                WHEN cast(PatientAge as int) >= 85 THEN 14 
                            ELSE NULL END) as AgeGroup,
                            PatientSex
                    FROM HealthMIS.dbo.HmisRegistPatient
                    where RegistStatusType = 2 and CheckupDate>'{pre}' and CheckupDate<'{aft}';

                insert into AutocareHCB.dbo.Patient(RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex, per1_spc_year, N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014, N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013, N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701, N110702, N110703, N110801, N110802, N110803, N110804, TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027, C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022, I348, I502, I503, I349)
                    select info.RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex,
                            SUBSTRING(cast(CheckupDate as nvarchar), 1, 4),
                            N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014,
                            N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013,
                            N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701,
                            N110702, N110703, N110801, N110802, N110803, N110804,
                            TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027,
                            C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022,
                            I348, I502, I503, I349
                    from @patientInfo info
                        left outer join
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, MunjinValue 
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, CheckupDataCode as DataCode, ResultValue1 as MunjinValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistNational ON HmisRegistNational.RegistKey = info.RegistKey
                                            where CheckupDataCode in ('N121115_2', 'N121116_1', 'N1101011', 'N1101021', 'N1101012', 'N1101022', 'N1101013', 'N1101023', 'N1101014', 'N1101024', 'N1101015', 'N1101025', 'N1101016', 'N1101026', 'N1101017', 'N1101027', 'N1102011', 'N1102012', 'N1102013', 'N1102014', 'N1102015', 'N110301', 'N110401', 'N110406', 'N110501', 'N110601', 'N110602', 'N110603', 'N110604', 'N110701', 'N110702', 'N110703', 'N110801', 'N110802', 'N110803', 'N110804')
                                            group by info.RegistKey, CheckupDataCode, ResultValue1) as temp_munjin
                                    where info.registkey = temp_munjin.registkey) AS result
                            PIVOT (min(MunjinValue) FOR datacode IN ([N121115_2], [N121116_1], [N1101011], [N1101021], [N1101012], [N1101022], [N1101013], [N1101023], [N1101014],
                            [N1101024], [N1101015], [N1101025], [N1101016], [N1101026], [N1101017], [N1101027], [N1102011], [N1102012], [N1102013],
                            [N1102014], [N1102015], [N110301], [N110401], [N110406], [N110501], [N110601], [N110602], [N110603], [N110604], [N110701],
                            [N110702], [N110703], [N110801], [N110802], [N110803], [N110804])) as pivoted_munjin) as munjin on info.RegistKey = munjin.RegistKey
                        left outer join 
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, BloodValue
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, RegistDataCode as DataCode, ResultValue1 as BloodValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistResult ON HmisRegistResult.RegistKey = info.RegistKey
                                            where RegistDataCode in ('TP01', 'TP02', 'GP01', 'GP02', 'TP00', 'TP07', 'TP08', 'C037', 'C039', 'C904', 'C038', 'C026', 'C027', 'C029', 'C030', 'C054', 'C022', 'C023', 'C024', 'C018', 'U008', 'C032', 'E001', 'I521', 'I105', 'I022', 'I348', 'I502', 'I503', 'I349')
                                            group by info.RegistKey, RegistDataCode, ResultValue1) as temp_Blood
                                    where info.registkey = temp_Blood.registkey) AS result
                            PIVOT (min(BloodValue) FOR datacode IN 
                            ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904], [C038], [C026], [C027], 
                            [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], 
                            [I348], [I502], [I503], [I349])) as pivoted_blood) as blood on info.RegistKey = blood.RegistKey;
                """
        cursor.execute(sql)
        self._conn.commit()

    def add_data(self):
        target_date = str(self.today-relativedelta(days=3))[:10]
        self._insertTB_onSchedule()
        logger.info(f'한신메디피아 검진자 테이블(Patient)에 {target_date}일자 데이터 추가 완료.')
    
    def _select_data(self):
        cursor = self._conn.cursor()
        columns = list(self._patient_info.keys())
        columns += ['cast('+i+' as int)' for i in self._munjin_lifestyle]
        columns += ['cast('+i+' as int)' for i in self._munjin_pastHistory]
        columns += ['cast('+i+' as int)' for i in self._munjin_paper]
        columns += ['cast('+i+' as float)' for i in self._blood_codes]
        columns = ', '.join(columns)
        columns = columns.replace('PatientSex, ', "(CASE WHEN PatientSex = '남' THEN 1 ELSE 2 END) AS PatientSex, ")
        sql = f"SELECT {columns} FROM AutocareHCB.dbo.Patient where percent_01 is null"
        cursor.execute(sql)
        data = cursor.fetchall()        
        self._conn.commit()
        return data    
    
    def get_data(self):
        data = self._select_data()
        df = self._convert2dataframe(data)
        return df

    def update_predictResult(self, result):
        cursor = self._conn.cursor()
        for i in tqdm.tqdm(range(len(result)), '발병 확률 예측 결과 업데이트 중..'):
            RegistKey = result.iloc[i]['RegistKey']
            percent_01, percent_02, percent_03, percent_04, percent_05, percent_06, percent_07, percent_08, percent_09, percent_10, percent_11, percent_12, percent_13, percent_14 = result.iloc[i]["percent_01"], result.iloc[i]["percent_02"], result.iloc[i]["percent_03"], result.iloc[i]["percent_04"], result.iloc[i]["percent_05"], result.iloc[i]["percent_06"], result.iloc[i]["percent_07"], result.iloc[i]["percent_08"], result.iloc[i]["percent_09"], result.iloc[i]["percent_10"], result.iloc[i]["percent_11"], result.iloc[i]["percent_12"], result.iloc[i]["percent_13"], result.iloc[i]["percent_14"]
            
            sql = f"UPDATE AutocareHCB.dbo.Patient \
                    SET percent_01 = {percent_01}, percent_02 = {percent_02}, percent_03 = {percent_03}, percent_04 = {percent_04}, percent_05 = {percent_05}, \
                        percent_06 = {percent_06}, percent_07 = {percent_07}, percent_08 = {percent_08}, percent_09 = {percent_09}, percent_10 = {percent_10}, \
                        percent_11 = {percent_11}, percent_12 = {percent_12}, percent_13 = {percent_13}, percent_14 = {percent_14} \
                    WHERE Registkey = '{RegistKey}'"
            cursor.execute(sql)        
            self._conn.commit()

class HanshinPredictor:
    def __init__(self):
        self.inference_cols = {
            "common":["per1_age", "per1_gender", "per1_life_code1", "per1_life_code2","per1_life_code3", 
                        # "per1_life_code4", "per1_life_code5", "per1_ilban", "per1_kwa1", "per1_kwa2",  
                        "per1_life_code4", "per1_kwa2",  
                        "per1_kwa3", "per1_kwa4", "per1_kwa5", "per1_kwa6", "per1_spc_year",
                        "mj1_1_1", "mj1_1_2", "mj1_2_1", "mj1_2_2", "mj1_3_1",
                        "mj1_3_2", "mj1_4_1", "mj1_4_2", "mj1_5_1", "mj1_5_2",
                        "mj1_6_1", "mj1_6_2", "mj1_7_1", "mj1_7_2", "mj2_1",
                        "mj2_2", "mj2_3", "mj2_4",  "mj2_5", "mj3", 
                        "mj4", "mj5", "mj6", "mj70", "mj74", 
                        "mj8_1", "mj8_2_1", "mj8_2_2", "mj9_1", "mj9_2_1",
                        "mj9_2_2", "mj10", "height", "weight", "wai_cir",
                        "bmi", "obesity", "blood_press_high", "blood_press_low", "total_col",
                        "hdl_col", "ldl_col_cal", "tri_gly", "r_gtp", "liver_bilirubin",
                        "liver_protein", "liver_albumin", "liver_globulin", "liver_ast", "liver_alt",
                        "liver_alp", "glucose", "urine_protein", "creatinine"],
            "01": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "drinking_danger_per", "liver_ast_per", "liver_alt_per", "liver_alp_per", "r_gtp_per", "hdl_col_per"],
            "02": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "stomach_helico_bacter", "smoking_danger_per", "middle_exercise_danger_per", "high_exercise_danger_per", "cea_per", "ca19_per", "hdl_col_per", "tri_gly_per"],
            "03": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "lung_cyfra21_1", "thy_tsh", "smoking_danger_per", "middle_exercise_danger_per", "high_exercise_danger_per", "cyfra21_1_per", "cea_per", "liver_ast_per", "liver_alp_per", "glucose_per", "ca19_per"],
            "04": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "drinking_danger_per", "middle_exercise_danger_per", "high_exercise_danger_per", "cea_per", "ca19_per", "glucose_per", "tri_gly_per", "bmi_per"],
            "05": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "thy_ft4", "thy_tsh", "drinking_danger_per", "smoking_danger_per", "ft4_per", "tsh_per", "ldl_per", "tri_gly_per", "bmi_per"],
            "06": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "breast_ca15_3", "middle_exercise_danger_per", "high_exercise_danger_per", "drinking_danger_per", "ca15_3_per", "ldl_per", "total_col_per", "bmi_per", "hdl_col_per"],
            "07": ["smoking_danger_per", "drinking_danger_per", "middle_exercise_danger_per", "high_exercise_danger_per", "blood_press_high_per","blood_press_low_per","ldl_per","total_col_per"],
            "08": ["smoking_danger_per","middle_exercise_danger_per", "high_exercise_danger_per", "total_col_per","ldl_per","bmi_per","blood_press_high_per","blood_press_low_per","glucose_per"],
            "09": ["smoking_danger_per", "drinking_danger_per", "glucose_per","tri_gly_per","r_gtp_per","total_col_per","ldl_per"],
            "10": ["smoking_danger_per", "total_col_per","albumin_per","ldl_per","hdl_col_per","tri_gly_per"],
            "11": ["drinking_danger_per", "smoking_danger_per", "blood_press_low_per","blood_press_high_per","bmi_per","glucose_per","tri_gly_per"],
            "12": ["drinking_danger_per", "total_col_per","tri_gly_per","ldl_per","hdl_col_per"],
            "13": ["drinking_danger_per", "liver_ast_per","liver_alt_per","r_gtp_per","liver_alp_per","tri_gly_per","bmi_per"],
            "14": ["smoking_danger_per", "drinking_danger_per", "middle_exercise_danger_per", "high_exercise_danger_per","urine_protein_per","albumin_per","creatinine_per","liver_protein_per"]
        }
    
    def predict(self, data):
        random_state = 1234
        n_estimators = 5
        output_dir = "/home/autocare/Autocare_Outputs/hanshin_output/train"
        
        logger.info('')
        logger.info("-------------------------------------------------------")
        logger.info('한신메디피아 모델 예측을 시작합니다.')
        logger.info('모델 저장경로', output_dir)
        logger.info('학습 hyperparameter')
        logger.info(f"random_state: {random_state}")
        logger.info(f"n_estimators: {n_estimators}")
                
        if len(os.listdir(output_dir)) != 14:
            raise ('((ERROR)) 모델이 부족합니다! 저장경로=', output_dir)
            
        for joblib_path in tqdm.tqdm(glob.glob(os.path.join(output_dir, "*.joblib"))):
            rf, scaler, normalizer = joblib.load(joblib_path)
            joblib_name = os.path.split(joblib_path)[-1]
            task = joblib_name.split("_")[0]

            # filter data customized for disease
            cols = self.inference_cols['common'] + self.inference_cols[task]
            x = data[cols]
            
            # scaler & normalizer
            
            x = pd.DataFrame(scaler.transform(x), columns=cols)
            x = pd.DataFrame(normalizer.transform(x), columns=cols)
            
            # predict
            data[f'percent_{task}'] = pd.DataFrame(rf.predict(x))
            data[f'percent_{task}'] = round(data[f'percent_{task}'],1)
        
        return data

def predict_new_hanshinModel(need_reloadPredictTB = True):
    predictor = HanshinPredictor()
    db = HanshinModelPredictorDBHandler()
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("한신메디피아 발병확률 예측을 시작합니다.")
    
    logger.info('')
    logger.info("한신메디피아 검진자(CheckupPatients) 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()

    # db.let_chkupPatientTB_needUpdate()
    data = db.get_data()
    
    logger.info("한신메디피아 학습 데이터를 전처리를 진행합니다.")
    data = preprocess_hanshinData(data, criterion)
    logger.info('한신메디피아 학습 전처리를 완료하였습니다.')
    
    result = predictor.predict(data)
    logger.info("한신메디피아 발병확률 예측결과를 DB에 저장합니다.")
    db.update_predictResult(result)
    logger.info("한신메디피아 발병확률 예측을 완료하였습니다.")
    logger.info("-------------------------------------------------------")
    logger.info('')

def predict_hanshinModel_onSchedule(today=None):
    predictor = HanshinPredictor()
    db = HanshinModelPredictorDBHandler(today)
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("한신메디피아 발병확률 예측을 시작합니다.")
    
    db.add_data()    
    db.preprocessDB_ifNecessary()
    
    logger.info('')
    logger.info("한신메디피아 검진자(CheckupPatients) 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()
    data = db.get_data()
    
    if data.empty:
        target_date = str(db.today-relativedelta(days=3))[:10]
        logger.info("")
        logger.info(f"{target_date}일자 한신메디피아 발병확률 예측할 데이터가 없습니다.")
        logger.info("-------------------------------------------------------")
        logger.info('')
    else:
        logger.info("한신메디피아 학습 데이터를 전처리를 진행합니다.")
        data = preprocess_hanshinData(data, criterion)
        logger.info('한신메디피아 학습 전처리를 완료하였습니다.')
        
        result = predictor.predict(data)
        logger.info("한신메디피아 발병확률 예측결과를 DB에 저장합니다.")
        db.update_predictResult(result)
        logger.info("한신메디피아 발병확률 예측을 완료하였습니다.")
        logger.info("-------------------------------------------------------")
        logger.info('')