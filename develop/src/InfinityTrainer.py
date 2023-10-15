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
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, Normalizer
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
from Database import DBHandler, DBPreprocessor
from Preprocessor import preprocess_infinityData
from datetime import datetime
from dateutil.relativedelta import relativedelta

class InfinityModelTrainerDBHandler(DBHandler, DBPreprocessor):
    def __init__(self, today=None):
        super().__init__(today)
        
        self.tasks = {"01":"간암", "02":"위암", "03":"폐암", "04":"대장암", "05":"갑상선암",
                      "06":"유방암", "07":"뇌졸중", "08":"심근경색", "09":"당뇨병", "10":"폐결핵", 
                      "11":"고혈압", "12":"고지혈증", "13":"지방간", "14":"단백뇨"}
        self.train_cols = {
                "common":["per1_age", "per1_gender", "per1_spc_year",
                            "height", "weight", "wai_cir",
                            "bmi", "obesity", "blood_press_high", "blood_press_low", "total_col",
                            "hdl_col", "ldl_col_cal", "tri_gly", "r_gtp", "liver_bilirubin",
                            "liver_protein", "liver_albumin", "liver_globulin", "liver_ast", "liver_alt",
                            "liver_alp", "glucose", "urine_protein", "creatinine"],
                "01": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "liver_ast_per", "liver_alt_per", "liver_alp_per", "r_gtp_per", "hdl_col_per"],
                "02": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "stomach_helico_bacter", "cea_per", "ca19_per", "hdl_col_per", "tri_gly_per", "glucose_per"],
                "03": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "lung_cyfra21_1", "thy_tsh", "cyfra21_1_per", "cea_per", "liver_ast_per", "liver_alp_per", "glucose_per", "ca19_per"],
                "04": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "cea_per", "ca19_per", "glucose_per", "tri_gly_per", "bmi_per", "r_gtp_per"],
                "05": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "thy_ft4", "thy_tsh", "ft4_per", "tsh_per", "tri_gly_per", "bmi_per", "ldl_per", "liver_alp_per"],
                "06": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "breast_ca15_3", "ca15_3_per", "ldl_per", "total_col_per", "bmi_per", "hdl_col_per"],
                "07": ["blood_press_high_per","blood_press_low_per","ldl_per","total_col_per"],
                "08": ["total_col_per","ldl_per","bmi_per","blood_press_high_per","blood_press_low_per","glucose_per"],
                "09": ["glucose_per","tri_gly_per","r_gtp_per","total_col_per","ldl_per"],
                "10": ["total_col_per","albumin_per","ldl_per","hdl_col_per","tri_gly_per"],
                "11": ["blood_press_low_per","blood_press_high_per","bmi_per","glucose_per","tri_gly_per"],
                "12": ["total_col_per","tri_gly_per","ldl_per","hdl_col_per"],
                "13": ["liver_ast_per","liver_alt_per","r_gtp_per","liver_alp_per","tri_gly_per","bmi_per"],
                "14": ["urine_protein_per","albumin_per","creatinine_per","liver_protein_per"]
            }

    def _select_data(self):
        cursor = self._conn.cursor()
        columns = list(self._patient_info.keys())+['per1_spc_year']
        columns += ['cast('+i+' as float)' for i in self._blood_codes]
        columns = ', '.join(columns)
        columns = columns.replace('PatientSex, ', "(CASE WHEN PatientSex = '남' THEN 1 ELSE 2 END) AS PatientSex, ")
        sql = f"SELECT {columns} FROM AutocareHCB.dbo.InfinityTrainData"
        cursor.execute(sql)
        data = cursor.fetchall()        
        self._conn.commit()
        return data
    
    def get_data(self):
        data = self._select_data()
        df = self._convert2dataframe(data)
        return df
        
    def _deleteTB_allPeriod(self):
        sql = 'DELETE FROM AutocareHCB.dbo.InfinityTrainData'
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()

    # TODO : sql문 수정해야함.    
    def _insertTB_allPeriod(self):
        m = self.today.month
        nowUpdated_month = (m//3-1)*3+1 if m%3 == 0 else (m//3)*3+1
        nowUpdated_date = datetime(self.today.year, nowUpdated_month, 1)
        nowUpdated_date = str(nowUpdated_date)[:10]
        columns = ', '.join(list(self._patient_info.keys())+['per1_spc_year']+\
                            list(self._blood_codes.keys()))
        sql = f"INSERT INTO AutocareHCB.dbo.InfinityTrainData \
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
        logger.info('인피니티케어 학습 테이블(InfinityTrainData) 데이터 삭제 완료')
        self._insertTB_allPeriod()
        logger.info('인피니티케어 학습 테이블(InfinityTrainData) 새로운 데이터 추가 완료')

    def _insertTB_onSchedule(self):
        m = self.today.month
        nowUpdated_month = (m//3-1)*3+1 if m%3 == 0 else (m//3)*3+1
        nowUpdated_date = datetime(self.today.year, nowUpdated_month, 1)
        preUpdate_date = nowUpdated_date - relativedelta(months=3)
        nowUpdated_date = str(nowUpdated_date)[:10]
        preUpdate_date = str(preUpdate_date)[:10]
        columns = ', '.join(list(self._patient_info.keys())+['per1_spc_year']+\
                            list(self._blood_codes.keys()))
        sql = f"INSERT INTO AutocareHCB.dbo.InfinityTrainData \
                SELECT {columns} \
                    FROM AutocareHCB.dbo.Patient \
                    WHERE CheckupDate >= '{preUpdate_date}' AND CheckupDate < '{nowUpdated_date}' AND (PatientChartNo) IN ( \
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
  

class InfinityModelTrainer:
    def __init__(self):
        self.tasks = {"01":"간암", "02":"위암", "03":"폐암", "04":"대장암", "05":"갑상선암",
                      "06":"유방암", "07":"뇌졸중", "08":"심근경색", "09":"당뇨병", "10":"폐결핵", 
                      "11":"고혈압", "12":"고지혈증", "13":"지방간", "14":"단백뇨"}
        self.train_cols = {
                "common":["per1_age", "per1_gender", "per1_spc_year",
                            "height", "weight", "wai_cir",
                            "bmi", "obesity", "blood_press_high", "blood_press_low", "total_col",
                            "hdl_col", "ldl_col_cal", "tri_gly", "r_gtp", "liver_bilirubin",
                            "liver_protein", "liver_albumin", "liver_globulin", "liver_ast", "liver_alt",
                            "liver_alp", "glucose", "urine_protein", "creatinine"],
                "01": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "liver_ast_per", "liver_alt_per", "liver_alp_per", "r_gtp_per", "hdl_col_per"],
                "02": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "stomach_helico_bacter", "cea_per", "ca19_per", "hdl_col_per", "tri_gly_per", "glucose_per"],
                "03": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "lung_cyfra21_1", "thy_tsh", "cyfra21_1_per", "cea_per", "liver_ast_per", "liver_alp_per", "glucose_per", "ca19_per"],
                "04": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "cea_per", "ca19_per", "glucose_per", "tri_gly_per", "bmi_per", "r_gtp_per"],
                "05": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "thy_ft4", "thy_tsh", "ft4_per", "tsh_per", "tri_gly_per", "bmi_per", "ldl_per", "liver_alp_per"],
                "06": ["liver_b_antigen", "lar_int_ca19", "lar_int_cea", "breast_ca15_3", "ca15_3_per", "ldl_per", "total_col_per", "bmi_per", "hdl_col_per"],
                "07": ["blood_press_high_per","blood_press_low_per","ldl_per","total_col_per"],
                "08": ["total_col_per","ldl_per","bmi_per","blood_press_high_per","blood_press_low_per","glucose_per"],
                "09": ["glucose_per","tri_gly_per","r_gtp_per","total_col_per","ldl_per"],
                "10": ["total_col_per","albumin_per","ldl_per","hdl_col_per","tri_gly_per"],
                "11": ["blood_press_low_per","blood_press_high_per","bmi_per","glucose_per","tri_gly_per"],
                "12": ["total_col_per","tri_gly_per","ldl_per","hdl_col_per"],
                "13": ["liver_ast_per","liver_alt_per","r_gtp_per","liver_alp_per","tri_gly_per","bmi_per"],
                "14": ["urine_protein_per","albumin_per","creatinine_per","liver_protein_per"]
            }
        
        self.output_dir = "/home/autocare/Autocare_Outputs/infinity_output/"
    
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
        if task == '01': #간암                
            data['percent_01'] = 0
            logger.info('간암 발병 확률 컬럼 생성')
            for i in tqdm.tqdm(range(0, len(data))):
                if data['liver_b_antigen'].iloc[i]==1:
                    data['percent_01'].iloc[i] = 50 + (0.5*(data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + data['r_gtp_per'].iloc[i] +data['hdl_col_per'].iloc[i]))
                else:
                    data['percent_01'].iloc[i] = data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['liver_alp_per'].iloc[i] + data['r_gtp_per'].iloc[i] +data['hdl_col_per'].iloc[i]
            # logger.info(data['percent_01'].value_counts())
            
        elif task == '02': #위암
            data['percent_02'] = 0
            logger.info('위암 발병 확률 컬럼 생성')
            for i in tqdm.tqdm(range(0, len(data))):
                if data['stomach_helico_bacter'].iloc[i]==1:
                    data['percent_02'].iloc[i] = 50 + (0.5*((1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i] + (0.5*data['glucose_per'].iloc[i])))
                else:
                    data['percent_02'].iloc[i] = (1.5*data['cea_per'].iloc[i]) + data['ca19_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i] + (0.5*data['glucose_per'].iloc[i])
            # logger.info(data['percent_02'].value_counts())
            
        elif task == '03': #폐암
            data['percent_03'] = 0
            logger.info("폐암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_03'].iloc[i]=(1.5*data['cyfra21_1_per'].iloc[i]) + data['cea_per'].iloc[i] + (0.5*data['liver_ast_per'].iloc[i]) + (0.5*data['liver_alp_per'].iloc[i]) + data['glucose_per'].iloc[i] + (0.5*data['ca19_per'].iloc[i])

        elif task == '04': #대장암
            data['percent_04'] = 0
            logger.info("대장암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_04'].iloc[i]=(1.5*data['cea_per'].iloc[i]) + (1.5*data['ca19_per'].iloc[i]) + (0.5*data['glucose_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i]) + (0.5*data['r_gtp_per'].iloc[i])
            # logger.info(data['percent_04'].value_counts())
        
        elif task == '05': #갑상선암
            data['percent_05'] = 0
            logger.info("갑상선암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_05'].iloc[i]=(1.5*data['ft4_per'].iloc[i]) + (1.5*data['tsh_per'].iloc[i]) + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['liver_alp_per'].iloc[i])
            # logger.info(data['percent_05'].value_counts())
            
        elif task == '06': #유방암
            data['percent_06'] = 0
            logger.info("유방암 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_06'].iloc[i]=(1.5*data['ca15_3_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + data['total_col_per'].iloc[i] + (1.5*data['bmi_per'].iloc[i]) + (0.5*data['hdl_col_per'].iloc[i])
            # logger.info(data['percent_06'].value_counts())
            
        elif task == '07': #뇌졸중
            data['percent_07'] = 0
            logger.info("뇌졸중 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_07'].iloc[i]=(2.5*data['blood_press_high_per'].iloc[i]) + (1.5*data['blood_press_low_per'].iloc[i]) + (0.5*data['ldl_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i])
            # logger.info(data['percent_07'].value_counts())
            
        elif task == '08': #심근경색
            data['percent_08'] = 0
            logger.info("심근경색 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_08'].iloc[i]=(1.5*data['total_col_per'].iloc[i]) + data['ldl_per'].iloc[i] + data['bmi_per'].iloc[i] + (0.5*data['blood_press_high_per'].iloc[i]) + (0.5*data['blood_press_low_per'].iloc[i]) + (0.5*data['glucose_per'].iloc[i])
            # logger.info(data['percent_08'].value_counts())

        elif task == '09': #당뇨병
            data['percent_09'] = 0
            logger.info("당뇨병 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_09'].iloc[i]=(2*data['glucose_per'].iloc[i]) + data['tri_gly_per'].iloc[i] + (0.5*data['r_gtp_per'].iloc[i]) + (0.5*data['total_col_per'].iloc[i]) + data['ldl_per'].iloc[i]
            # logger.info(data['percent_09'].value_counts())
            
        elif task == '10': #폐결핵
            data['percent_10'] = 0
            logger.info("폐결핵 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_10'].iloc[i] = data['total_col_per'].iloc[i] + data['albumin_per'].iloc[i] + data['ldl_per'].iloc[i] + data['hdl_col_per'].iloc[i] + data['tri_gly_per'].iloc[i]
            # logger.info(data['percent_10'].value_counts())
                    
        elif task == '11': #고혈압
            data['percent_11'] = 0
            logger.info("고혈압 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_11'].iloc[i] = (1.5*data['blood_press_low_per'].iloc[i]) + (1.5*data['blood_press_high_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])  + data['glucose_per'].iloc[i] + (0.5*data['tri_gly_per'].iloc[i])
            # logger.info(data['percent_11'].value_counts())
            
        elif task == '12': #고지혈증
            data['percent_12'] = 0
            logger.info("고지혈증 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_12'].iloc[i] = (1.5*data['total_col_per'].iloc[i]) + (1.5*data['tri_gly_per'].iloc[i]) + data['ldl_per'].iloc[i] + data['hdl_col_per'].iloc[i]
            # logger.info(data['percent_12'].value_counts())

        elif task == '13': #지방간
            data['percent_13'] = 2
            logger.info("지방간 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_13'].iloc[i] = data['liver_ast_per'].iloc[i] + data['liver_alt_per'].iloc[i] + data['r_gtp_per'].iloc[i] + data['liver_alp_per'].iloc[i] + (0.5*data['tri_gly_per'].iloc[i]) + (0.5*data['bmi_per'].iloc[i])
            # logger.info(data['percent_13'].value_counts())
                        
        elif task == '14': #단백뇨
            data['percent_14'] = 2
            logger.info("단백뇨 발병 확률 컬럼 생성")
            for i in tqdm.tqdm(range(0, len(data))):
                data['percent_14'].iloc[i]=(2*data['urine_protein_per'].iloc[i]) + data['albumin_per'].iloc[i] + data['creatinine_per'].iloc[i] + data['liver_protein_per'].iloc[i]
            # logger.info(data['percent_14'].value_counts())

        X = data.drop(['percent_'+task], axis=1)
        y = data[['percent_'+task]].astype('float')
        # # row 생략 없이 출력
        # pd.set_option('display.max_rows', None)
        # # col 생략 없이 출력
        # pd.set_option('display.max_columns', None)
        # logger.info(X.isna().sum())
        # logger.info(y.isna().sum())
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
    
    def remove_infinityModels(self):
        if os.path.exists(os.path.join(self.output_dir, "train")):
            shutil.rmtree(os.path.join(self.output_dir, "train"))
            logger.info('인피니티케어 기존 모델이 존재하여 삭제합니다.')
            logger.info('')
            
    def remove_infinityModelsZipFile(self):
        if os.path.exists(os.path.join(self.output_dir, "infinityModels.zip")):
            logger.info(f"기존 인피니티케어 모델 압축 파일을 삭제합니다.")
            os.remove(os.path.join(self.output_dir, "infinityModels.zip"))
    
    def train_infinityModel(self, data):
        random_state = 1234
        n_estimators = 5
        
        logger.info('')
        logger.info("-------------------------------------------------------")
        logger.info('인피니티케어 모델 학습을 시작합니다.')
        logger.info('모델 저장경로', self.output_dir)
        logger.info('학습 hyperparameter')
        logger.info(f"random_state: {random_state}")
        logger.info(f"n_estimators: {n_estimators}")

        self.remove_infinityModels()
            
        for task in list(self.tasks.keys()):
            logger.info(f"{self.tasks[task]} 학습을 위한 데이터 전처리를 시작합니다.")
            (X_train, X_test, y_train, y_test), scaler, noramlizer = self.__preprocess_per_task(data, task)
            
            logger.info(f"{self.tasks[task]}에 대해 학습을 시작합니다.")
            rf_run = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
            rf_run.fit(X_train, y_train)
            
            pred = rf_run.predict(X_test)
            logger.info('인피니티케어 모델 훈련 세트 정확도 : {:.3f}'.format(rf_run.score(X_train, y_train)))
            logger.info('인피니티케어 모델 테스트 세트 정확도 : {:.3f}'.format(rf_run.score(X_test, y_test)))
            
            os.makedirs(os.path.join(self.output_dir, "train"), exist_ok=True)
            file_name = f"인피니티케어_{task}_{self.tasks[task]}_발병확률_예측모델_{rf_run.score(X_test, y_test):.3f}.pkl"
            weights = (rf_run, scaler, noramlizer)
            with open(file=os.path.join(self.output_dir, "train", file_name), mode='wb') as f:
                pickle.dump(weights, f)
            
            logger.info(f"{self.tasks[task]}에 대해 인피니티케어 모델 학습이 완료되었습니다.")
            logger.info("-------------------------------------------------------")
            logger.info('')   
        
        self.remove_infinityModelsZipFile()
        
        shutil.make_archive(self.output_dir+'infinityModels', 'zip', os.path.join(self.output_dir, 'train'))
        logger.info(f"인피니티케어 모델 압축 파일을 생성하였습니다.")
        logger.info('')   

def remove_infinityModels():
    tr = InfinityModelTrainer()
    tr.remove_infinityModels()
    tr.remove_infinityModelsZipFile()

def train_new_infinityModel(need_reloadTrainTB=True):
    trainer = InfinityModelTrainer()
    db = InfinityModelTrainerDBHandler()
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("인피니티케어 모델을 새로 만듭니다.")
    
    if need_reloadTrainTB:
        logger.info("인피니티케어 학습 테이블(InfinityTrainData)을 새로 생성합니다.")
        db.reload_data()
    
    logger.info('')
    logger.info("인피니티케어 학습 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()
    data = db.get_data()
    
    logger.info("인피니티케어 학습 데이터를 전처리를 진행합니다.")
    data = preprocess_infinityData(data, criterion)
    logger.info('인피니티케어 학습 전처리를 완료하였습니다.')
    
    trainer.train_infinityModel(data)
    logger.info("인피니티케어 모델을 새로 만들었습니다.")
    logger.info("-------------------------------------------------------")
    logger.info('')
    
def train_infinityModel_onSchedule(today=None):
    trainer = InfinityModelTrainer()
    db = InfinityModelTrainerDBHandler(today)
    
    logger.info('')
    logger.info("-------------------------------------------------------")
    logger.info("인피니티케어 모델을 업데이트 합니다.")
    
    db.preprocessDB_ifNecessary()
    db.add_data()

    logger.info('')
    logger.info("인피니티케어 학습 데이터를 가지고 옵니다.")
    criterion = db.get_bloodCodeCriterion()
    data = db.get_data()
    
    logger.info("인피니티케어 학습 데이터를 전처리를 진행합니다.")
    data = preprocess_infinityData(data, criterion)
    logger.info('인피니티케어 학습 전처리를 완료하였습니다.')
    
    trainer.train_infinityModel(data)
    logger.info("인피니티케어 모델을 업데이트 했습니다.")
    logger.info("-------------------------------------------------------")    
    logger.info("")    