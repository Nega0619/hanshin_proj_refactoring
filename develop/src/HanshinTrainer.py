import __main__
if 'main_AutoUpdater' in __main__.__file__: 
    from logger_AutoUpdater import logger
elif 'main_PDFMaker' in __main__.__file__: 
    from logger_PDFMaker import logger
elif 'main_Initiator' in __main__.__file__:
    from logger_Initiator import logger
import os
import tqdm
import shutil
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, Normalizer
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
from Database import DBHandler, DBPreprocessor, CandidateDataCalculator
from Preprocessor import preprocess_hanshinData
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HanshinModelTrainerDBHandler(DBHandler, DBPreprocessor, CandidateDataCalculator):
    def __init__(self, today=None):
        super().__init__(today)
              
    def _deleteTB_allPeriod(self):
        sql = 'DELETE FROM AutocareHCB.dbo.HanshinTrainData'
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()

    def _insertTB_allPeriod(self):
        m = self.today.month
        nowUpdated_month = (m//3-1)*3+1 if m%3 == 0 else (m//3)*3+1
        nowUpdated_date = datetime(self.today.year, nowUpdated_month, 1)
        nowUpdated_date = str(nowUpdated_date)[:10]
        columns = ', '.join(list(self._patient_info.keys())+\
                            list(self._munjin_lifestyle.keys())+\
                            list(self._munjin_pastHistory.keys())+\
                            list(self._munjin_paper.keys())+\
                            list(self._blood_codes.keys()))
        sql = f"INSERT INTO AutocareHCB.dbo.HanshinTrainData \
                SELECT {columns} \
                    FROM AutocareHCB.dbo.Patient \
                    WHERE CheckupDate >= '2019-01-01' AND CheckupDate < '{nowUpdated_date}' AND (PatientChartNo) IN ( \
                        SELECT PatientChartNo \
                        FROM AutocareHCB.dbo.Patient \
                        GROUP BY PatientChartNo, PatientBirthday, PatientName \
                        HAVING  COUNT(PatientChartNo) >= 3) \
                ORDER BY PatientBirthday, PatientName, CheckupDate ASC"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()
    
    def reload_data(self):
        self._deleteTB_allPeriod()
        logger.info('한신메디피아 학습 테이블(HanshinTrainData) 데이터 삭제 완료')
        self._insertTB_allPeriod()
        logger.info('한신메디피아 학습 테이블(HanshinTrainData) 새로운 데이터 추가 완료')

    def _insertTB_onSchedule(self):
        m = self.today.month
        nowUpdated_month = (m//3-1)*3+1 if m%3 == 0 else (m//3)*3+1
        nowUpdated_date = datetime(self.today.year, nowUpdated_month, 1)
        preUpdated_date = nowUpdated_date - relativedelta(months=3)
        nowUpdated_date = str(nowUpdated_date)[:10]
        preUpdated_date = str(preUpdated_date)[:10]
        columns = ', '.join(list(self._patient_info.keys())+\
                            list(self._munjin_lifestyle.keys())+\
                            list(self._munjin_pastHistory.keys())+\
                            list(self._munjin_paper.keys())+\
                            list(self._blood_codes.keys()))
        sql = f"INSERT INTO AutocareHCB.dbo.HanshinTrainData \
                SELECT {columns} \
                    FROM AutocareHCB.dbo.Patient \
                    WHERE CheckupDate >= '{preUpdated_date}' AND CheckupDate < '{nowUpdated_date}' AND (PatientChartNo) IN ( \
                        SELECT PatientChartNo \
                        FROM AutocareHCB.dbo.Patient \
                        GROUP BY PatientChartNo, PatientBirthday, PatientName \
                        HAVING  COUNT(PatientChartNo) >= 3) \
                ORDER BY PatientBirthday, PatientName, CheckupDate ASC"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()
                
    def add_data(self):
        self._insertTB_onSchedule()
        logger.info('한신메디피아 학습 테이블(HanshinTrainData)에 데이터 추가 완료.')
    
    def _select_data(self):
        cursor = self._conn.cursor()
        columns = list(self._patient_info.keys())
        columns += ['cast('+i+' as int)' for i in self._munjin_lifestyle]
        columns += ['cast('+i+' as int)' for i in self._munjin_pastHistory]
        columns += ['cast('+i+' as int)' for i in self._munjin_paper]
        columns += ['cast('+i+' as float)' for i in self._blood_codes]
        columns = ', '.join(columns)
        columns = columns.replace('PatientSex, ', "(CASE WHEN PatientSex = '남' THEN 1 ELSE 2 END) AS PatientSex, ")
        sql = f"SELECT {columns} FROM AutocareHCB.dbo.HanshinTrainData"
        cursor.execute(sql)
        data = cursor.fetchall()        
        self._conn.commit()
        return data
    
    def get_data(self):
        data = self._select_data()
        df = self._convert2dataframe(data)
        return df
  

class HanshinModelTrainer:
    def __init__(self):
        self.tasks = {"01":"간암", "02":"위암", "03":"폐암", "04":"대장암", "05":"갑상선암",
                      "06":"유방암", "07":"뇌졸중", "08":"심근경색", "09":"당뇨병", "10":"폐결핵", 
                      "11":"고혈압", "12":"고지혈증", "13":"지방간", "14":"단백뇨"}
    
        self.train_cols = {
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
        
        self.output_dir = "/home/autocare/Autocare_Outputs/hanshin_output/"

    
    def __noramlize_data(self, data):
        normal_scaler = Normalizer()
        X_train, X_test, y_train, y_test = data
        normal_scaler.fit(X_train)
        X_train = normal_scaler.transform(X_train)
        X_test = normal_scaler.transform(X_test)
        return (X_train, X_test, y_train, y_test), normal_scaler

    def __scale_robust(self, data):
        scaler = RobustScaler()
        X_train, X_test, y_train, y_test = data
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        return (X_train, X_test, y_train, y_test), scaler
        
    def __make_x_y_dataset(self, data, task):
        # 새로운 기준이 있는경우 컬럼 생성
        if task == "01": #간암                
            data['percent_01'] = 0
            logger.info('간암 발병 확률 컬럼 생성')
            for i in tqdm.tqdm(range(0, len(data))):
                if data['liver_b_antigen'].iloc[i]==1:
                    data['percent_01'].iloc[i] = 50 + (0.5*(data['drinking_danger_per'].iloc[i] + data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + 0.5*(data['r_gtp_per'].iloc[i]) + 0.5*(data['hdl_col_per'].iloc[i])))
                else:
                    data['percent_01'].iloc[i] = data['drinking_danger_per'].iloc[i] + data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + 0.5*(data['r_gtp_per'].iloc[i]) + 0.5*(data['hdl_col_per'].iloc[i])
            data['percent_01'] = round(data['percent_01'],1)
            

            # data = data.drop(['alp_yn'], axis=1)  #안 쓸 컬럼 drop 
            # data[col] = data[col].replace(0,2)

        elif task == "02": #위암
            data['percent_02'] = 0
            logger.info('위암 발병 확률 컬럼 생성')
            for i in tqdm.tqdm(range(0, len(data))):
                if data['stomach_helico_bacter'].iloc[i]==1:
                    data['percent_02'].iloc[i] = 50 + (0.5*((0.75*data['smoking_danger_per'].iloc[i]) + (0.75*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + (0.5*(data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i]))))
                else:
                    data['percent_02'].iloc[i] = (0.75*data['smoking_danger_per'].iloc[i]) + (0.75*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + (0.5*(data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i]))
            #data[col] = data[col].replace(0,2)
            data['percent_02'] = round(data['percent_02'],1)
            

        elif task == "03": #폐암
            data['percent_03'] = 0
            logger.info("폐암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_03'].iloc[i] = (1.5*data['smoking_danger_per'].iloc[i]) + (0.5*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + data['cyfra21_1_per'].iloc[i] + data['cea_per'].iloc[i] + (0.5*data['glucose_per'].iloc[i]) + (0.5*data['ca19_per'].iloc[i])
            data['percent_03'] = round(data['percent_03'],1)
            

        elif task == "04": #대장암
            data['percent_04'] = 0
            logger.info("대장암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_04'].iloc[i]=(0.25*data['drinking_danger_per'].iloc[i]) + (0.75*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (1.5*data['cea_per'].iloc[i]) + (1.5*data['ca19_per'].iloc[i]) + (0.5*data['glucose_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])
            data['percent_04'] = round(data['percent_04'],1)
            

        elif task == "05": #갑상선암
            data['percent_05'] = 0
            logger.info("갑상선암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_05'].iloc[i]=(0.25*data['drinking_danger_per'].iloc[i]) + (0.25*data['smoking_danger_per'].iloc[i]) + (1.5*data['ft4_per'].iloc[i]) + (1.5*data['tsh_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])
            data['percent_05'] = round(data['percent_05'],1)
            

        elif task == "06": #유방암
            data['percent_06'] = 0
            logger.info("유방암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_06'].iloc[i]=(0.75*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (0.75*data['drinking_danger_per'].iloc[i]) + (0.75*data['ca15_3_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + data['total_col_per'].iloc[i] + data['bmi_per'].iloc[i] + (0.25*data['hdl_col_per'].iloc[i])
            data['percent_06'] = round(data['percent_06'],1)
            

        elif task == "07": #뇌졸중
            data['percent_07'] = 0
            logger.info("뇌졸중 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_07'].iloc[i]=data['per1_kwa3'].iloc[i] + data['mj2_1'].iloc[i] + (0.5*data['smoking_danger_per'].iloc[i]) + (0.5*data['drinking_danger_per'].iloc[i]) + (0.25*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (1.5*data['blood_press_high_per'].iloc[i]) + (0.75*data['blood_press_low_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i])
            data['percent_07'] = round(data['percent_07'],1)
            

        elif task == "08": #심근경색
            data['percent_08'] = 0
            logger.info("심근경색 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_08'].iloc[i]=data['mj1_2_1'].iloc[i] + data['mj2_2'].iloc[i] + (0.25*data['smoking_danger_per'].iloc[i]) + (0.25*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) + (1.25*data['total_col_per'].iloc[i]) + (0.75*data['ldl_per'].iloc[i]) + (0.75*data['bmi_per'].iloc[i]) + (0.5*data['blood_press_high_per'].iloc[i]) + (0.5*data['blood_press_low_per'].iloc[i]) + (0.25*data['glucose_per'].iloc[i])
            data['percent_08'] = round(data['percent_08'],1)
            

        elif task == "09": #당뇨병
            data['percent_09'] = 0
            logger.info("당뇨병 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_09'].iloc[i]=data['per1_kwa5'].iloc[i] + data['mj2_4'].iloc[i] + (0.5*data['drinking_danger_per'].iloc[i]) + (0.25*data['smoking_danger_per'].iloc[i]) + (1.5*data['glucose_per'].iloc[i]) + 0.75*(data['tri_gly_per'].iloc[i]) + (0.5*data['r_gtp_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i])
            data['percent_09'] = round(data['percent_09'],1)
            

        elif task == "10": #폐결핵
            data['percent_10'] = 0
            logger.info("폐결핵 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_10'].iloc[i] = data['mj1_6_1'].iloc[i] + (0.75*data['smoking_danger_per'].iloc[i]) + data['total_col_per'].iloc[i] + data['albumin_per'].iloc[i] + data['ldl_per'].iloc[i] + (0.5*(data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i]))
            data['percent_10'] = round(data['percent_10'],1)
            

        elif task == "11": #고혈압
            data['percent_11'] = 0
            logger.info("고혈압 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_11'].iloc[i] = data['per1_kwa2'].iloc[i] + data['mj2_3'].iloc[i] + (0.25*data['drinking_danger_per'].iloc[i]) + (0.25*data['smoking_danger_per'].iloc[i]) + (1.25*data['blood_press_low_per'].iloc[i]) + data['blood_press_high_per'].iloc[i] + (0.5*data['bmi_per'].iloc[i]) + (0.75*data['glucose_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i])
            data['percent_11'] = round(data['percent_11'],1)
            

        elif task == "12": #고지혈증
            data['percent_12'] = 0
            logger.info("고지혈증 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_12'].iloc[i] = data['mj1_5_1'].iloc[i] + (0.25*data['drinking_danger_per'].iloc[i]) + (1.5*data['total_col_per'].iloc[i]) + (1.25*data['tri_gly_per'].iloc[i]) + data['ldl_per'].iloc[i] + (0.75*data['hdl_col_per'].iloc[i])
            data['percent_12'] = round(data['percent_12'],1)
            

        elif task == "13": #지방간
            data['percent_13'] = 0
            logger.info("지방간 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_13'].iloc[i] = (0.5*data['drinking_danger_per'].iloc[i]) + data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['r_gtp_per'].iloc[i] + (0.5*data['liver_alp_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])
            data['percent_13'] = round(data['percent_13'],1)    
            

        elif task == "14": #단백뇨
            data['percent_14'] = 0
            logger.info("단백뇨 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_14'].iloc[i]=(0.25*data['smoking_danger_per'].iloc[i]) + (0.25*data['drinking_danger_per'].iloc[i]) + (0.25*(data['middle_exercise_danger_per'].iloc[i]+data['high_exercise_danger_per'].iloc[i])) +(2*data['urine_protein_per'].iloc[i]) + data['albumin_per'].iloc[i] + (0.75*data['creatinine_per'].iloc[i]) + (0.5*data['liver_protein_per'].iloc[i])
            data['percent_14'] = round(data['percent_14'],1)

        X = data.drop(['percent_'+task], axis=1)
        y = data[['percent_'+task]].astype('float')
        return X, y

    def __preprocess_per_task(self, data, task):
        # filter data customized for disease
        cols = self.train_cols['common'] + self.train_cols[task]
        x = pd.DataFrame()
        for c in cols:
            x[c] = data[c]
        
        x, y = self.__make_x_y_dataset(x, task)
        data = train_test_split(x, y, train_size=0.7, test_size=0.3)
        data, scaler = self.__scale_robust(data)
        data, noramlizer = self.__noramlize_data(data)
        return data, scaler, noramlizer

    def remove_models(self):
        if os.path.exists(os.path.join(self.output_dir, "train")):
            shutil.rmtree(os.path.join(self.output_dir, "train"))
            logger.info('한신메디피아 기존 모델이 존재하여 삭제합니다.')
            logger.info('')
    
    def train_hanshinModel(self, data):
        random_state = 1234
        n_estimators = 5
        
        logger.info('')
        logger.info("-------------------------------------------------------")
        logger.info('한신메디피아 모델 학습을 시작합니다.')
        logger.info('모델 저장경로', self.output_dir)
        logger.info('학습 hyperparameter')
        logger.info(f"random_state: {random_state}")
        logger.info(f"n_estimators: {n_estimators}")
        
        self.remove_models()
                
        for task in list(self.tasks.keys()):
            logger.info(f"{self.tasks[task]} 학습을 위한 데이터 전처리를 시작합니다.")
            (X_train, X_test, y_train, y_test), scaler, noramlizer = self.__preprocess_per_task(data, task)
            
            logger.info(f"{self.tasks[task]}에 대해 학습을 시작합니다.")
            rf_run = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
            rf_run.fit(X_train, y_train)
            
            pred = rf_run.predict(X_test)
            logger.info('한신메디피아 모델 훈련 세트 정확도 : {:.3f}'.format(rf_run.score(X_train, y_train)))
            logger.info('한신메디피아 모델 테스트 세트 정확도 : {:.3f}'.format(rf_run.score(X_test, y_test)))
            
            os.makedirs(os.path.join(self.output_dir, "train"), exist_ok=True)
            file_name = f"{task}_{self.tasks[task]}_발병확률_예측모델_{rf_run.score(X_test, y_test):.3f}.joblib"
            
            weights = (rf_run, scaler, noramlizer)
            joblib.dump(weights, os.path.join(self.output_dir, "train", file_name))
            logger.info(f"{self.tasks[task]}에 대해 한신메디피아 모델 학습이 완료되었습니다.")
            logger.info("-------------------------------------------------------")
            logger.info('')

def remove_hanshinModels():
    tr = HanshinModelTrainer()
    tr.remove_models()

def train_new_hanshinModel(need_reloadTrainTB=True, isTest=True):
    trainer = HanshinModelTrainer()
    db = HanshinModelTrainerDBHandler()
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("한신메디피아 모델을 새로 만듭니다.")
    
    if need_reloadTrainTB:
        logger.info("한신메디피아 학습 테이블(HanshinTrainData)을 새로 생성합니다.")
        db.reload_data()
    
    logger.info('')
    logger.info("한신메디피아 학습 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()
    data = db.get_data()
    
    logger.info('')
    logger.info("한신메디피아 학습 데이터를 전처리를 진행합니다.")
    data = preprocess_hanshinData(data, criterion)
    logger.info('한신메디피아 학습 전처리를 완료하였습니다.')
    
    trainer.train_hanshinModel(data)
    logger.info("한신메디피아 모델을 새로 만들었습니다.")
    logger.info("-------------------------------------------------------")
    logger.info('')
    
def train_hanshinModel_onSchedule(today=None):
    trainer = HanshinModelTrainer()
    db = HanshinModelTrainerDBHandler(today)
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("한신메디피아 모델을 업데이트 합니다.")
    
    db.preprocessDB_ifNecessary()
    
    logger.info("결측치 테이블을 업데이트 합니다.")
    db.update_candidateData()
    
    db.add_data()
    
    logger.info('')
    logger.info("한신메디피아 학습 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()
    data = db.get_data()
    
    logger.info("한신메디피아 학습 데이터를 전처리를 진행합니다.")
    data = preprocess_hanshinData(data, criterion)
    logger.info('한신메디피아 학습 전처리를 완료하였습니다.')
    
    trainer.train_hanshinModel(data)
    logger.info("한신메디피아 모델을 업데이트 했습니다.")
    logger.info("-------------------------------------------------------")
    logger.info('')