import tqdm
import numpy as np
# from Database import DBPreprocessor
import warnings
warnings.filterwarnings( 'ignore' )

# def preprocess_DB():
#     print('검진자 테이블(AutocareHCB.dbo.CheckupPatients) 전처리를 시작합니다.')

def preprocess_munjin(data):
    ## 1년 기준 음주량 컬럼 생성
    print("1년기준 음주량 컬럼 추가 : mj70(1년 중 음주 일수)")

    # mj74 : 음주여부 null -> 0으로 대체 (0: 음주 안함)
    data['mj74'] = data['mj74'].replace(np.nan, 0)
    data['mj74'] = data['mj74'].astype('int')

    # mj71 : 일주일 음주량 * 52 = 1년 음주량으로 환산
    data['mj71'].fillna(-2, inplace=True)
    data['mj71'] = data['mj71'].astype('int')

    for i in tqdm.tqdm(range(0,len(data)), '일주일 음주량 환산중..'):
        if data['mj71'].iloc[i] !=-2:
            data['mj71'].iloc[i] = data['mj71'].iloc[i]*52

    # mj72 :  한달 음주량 * 12 = 1년 음주량 환산
    data['mj72'].fillna(-2, inplace=True)
    data['mj72'] = data['mj72'].astype('int')

    for i in tqdm.tqdm(range(0,len(data)), '한달 음주량 환산중..'):
        if data['mj72'].iloc[i]!=-2:
            data['mj72'].iloc[i] = data['mj72'].iloc[i]*12
            
    # mj73 : 1년 음주량 계산
    data['mj73'] = data['mj73'].replace(np.nan, 0)
    data['mj73'] = data['mj73'].astype('int')

    ## 음주_ 1년 음주 횟수 컬럼 생성 : mj70------
    # mj70(1년 음주 횟수) 0으로 생성 후 변환
    data['mj70'] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['mj71'].iloc[i]==-2:
            if data['mj72'].iloc[i]==-2:
                data['mj70'].iloc[i] = data['mj73'].iloc[i]
            else :
                data['mj70'].iloc[i] = data['mj72'].iloc[i]
        else:
            data['mj70'].iloc[i] = data['mj71'].iloc[i]

    ## 일반문진내역 컬럼 정수화
    # mj_columns : 일반검진 문진 컬럼 리스트
    mj_columns = ['mj1_1_1', 'mj1_1_2', 'mj1_2_1', 'mj1_2_2', 'mj1_3_1',
        'mj1_3_2', 'mj1_4_1', 'mj1_4_2', 'mj1_5_1', 'mj1_5_2', 'mj1_6_1',
        'mj1_6_2', 'mj1_7_1', 'mj1_7_2', 'mj2_1', 'mj2_2', 'mj2_3', 'mj2_4',
        'mj2_5', 'mj3', 'mj4', 'mj5', 'mj6',
        'mj8_1', 'mj8_2_1', 'mj8_2_2', 'mj9_1', 'mj9_2_1', 'mj9_2_2', 'mj10']

    for i in range(0, len(mj_columns)):
        data[mj_columns[i]].fillna(0, inplace=True)
                
    for i in range(0, len(mj_columns)):
        data[mj_columns[i]]=data[mj_columns[i]].astype('int')
    # data.info()

    ## 일반문진내역 확률 계산용 컬럼(20% 기준)
    # 1) 음주
    print('1) 음주량으로 인한 발병 위험 확률 계산(20% 기준)')
    data["drinking_danger_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['mj70'].iloc[i]>=324:
            data["drinking_danger_per"].iloc[i] = 20
        elif data['mj70'].iloc[i]<324 and data['mj70'].iloc[i]>=288:
            data["drinking_danger_per"].iloc[i] = 18
        elif data['mj70'].iloc[i]<288 and data['mj70'].iloc[i]>=252:
            data["drinking_danger_per"].iloc[i] = 16
        elif data['mj70'].iloc[i]<252 and data['mj70'].iloc[i]>=216:
            data["drinking_danger_per"].iloc[i] = 14
        elif data['mj70'].iloc[i]<216 and data['mj70'].iloc[i]>=180:
            data["drinking_danger_per"].iloc[i] = 12
        elif data['mj70'].iloc[i]<180 and data['mj70'].iloc[i]>=144:
            data["drinking_danger_per"].iloc[i] = 10
        elif data['mj70'].iloc[i]<144 and data['mj70'].iloc[i]>=108:
            data["drinking_danger_per"].iloc[i] = 8
        elif data['mj70'].iloc[i]<108 and data['mj70'].iloc[i]>=72:
            data["drinking_danger_per"].iloc[i] = 6
        elif data['mj70'].iloc[i]<72 and data['mj70'].iloc[i]>=36:
            data["drinking_danger_per"].iloc[i] = 4
        elif data['mj70'].iloc[i]<36 and data['mj70'].iloc[i]>=12:
            data["drinking_danger_per"].iloc[i] = 2
    # print(data["drinking_danger_per"].value_counts())

    # 2) 흡연
    print('2) 흡연으로 인한 발병 위험 확률 계산(20% 기준)')
    data["smoking_danger_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['mj4'].iloc[i]==2 or data['mj5'].iloc[i]==2 or data['mj6'].iloc[i]==2:
            data["smoking_danger_per"].iloc[i] = 20
    # print(data["smoking_danger_per"].value_counts())

    # 3) 운동량
    print('3-1) 중강도 운동량으로 인한 발병 위험 확률 계산(20% 기준)')
    data["middle_exercise_danger_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['mj8_1'].iloc[i]==7:
            data["middle_exercise_danger_per"].iloc[i] = 0
        elif data['mj8_1'].iloc[i]==6:
            data["middle_exercise_danger_per"].iloc[i] = 1
        elif data['mj8_1'].iloc[i]==5:
            data["middle_exercise_danger_per"].iloc[i] = 2
        elif data['mj8_1'].iloc[i]==4:
            data["middle_exercise_danger_per"].iloc[i] = 4
        elif data['mj8_1'].iloc[i]==3:
            data["middle_exercise_danger_per"].iloc[i] = 6
        elif data['mj8_1'].iloc[i]==2:
            data["middle_exercise_danger_per"].iloc[i] = 8
        elif data['mj8_1'].iloc[i]==1:
            data["middle_exercise_danger_per"].iloc[i] = 9
        elif data['mj8_1'].iloc[i]==0:
            data["middle_exercise_danger_per"].iloc[i] = 10
    # print(data["middle_exercise_danger_per"].value_counts())

    print('3-2) 고강도 운동량으로 인한 발병 위험 확률 계산(20% 기준)')
    data["high_exercise_danger_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['mj9_1'].iloc[i]==7:
            data["high_exercise_danger_per"].iloc[i] = 0
        elif data['mj9_1'].iloc[i]==6:
            data["high_exercise_danger_per"].iloc[i] = 1
        elif data['mj9_1'].iloc[i]==5:
            data["high_exercise_danger_per"].iloc[i] = 2
        elif data['mj9_1'].iloc[i]==4:
            data["high_exercise_danger_per"].iloc[i] = 4
        elif data['mj9_1'].iloc[i]==3:
            data["high_exercise_danger_per"].iloc[i] = 6
        elif data['mj9_1'].iloc[i]==2:
            data["high_exercise_danger_per"].iloc[i] = 8
        elif data['mj9_1'].iloc[i]==1:
            data["high_exercise_danger_per"].iloc[i] = 9
        elif data['mj9_1'].iloc[i]==0:
            data["high_exercise_danger_per"].iloc[i] = 10
    # print(data["high_exercise_danger_per"].value_counts())
    
    return data

def preprocess_bloodcodes(data, bloodcodes_criterion):
    keys = bloodcodes_criterion.keys()
    # 1) AST
    print('1) AST 확률 계산(20% 기준)')
    data["liver_ast_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'AST' in keys:
                ast_min=bloodcodes_criterion['AST']['male_min_value']
                ast_max=bloodcodes_criterion['AST']['male_max_value']
            else:
                ast_min=4
                ast_max=40
            if data['liver_ast'].iloc[i]>=(ast_max*0.6) and data['liver_ast'].iloc[i]<(ast_max*0.8):
                data['liver_ast_per'].iloc[i]+=4
            elif data['liver_ast'].iloc[i]>=(ast_max*0.8) and data['liver_ast'].iloc[i]<ast_max:
                data['liver_ast_per'].iloc[i]+=8
            elif data['liver_ast'].iloc[i]>=ast_max and data['liver_ast'].iloc[i]<(ast_max*1.2):
                data['liver_ast_per'].iloc[i]+=12 
            elif data['liver_ast'].iloc[i]>=(ast_max*1.2) and data['liver_ast'].iloc[i]<(ast_max*1.4):
                data['liver_ast_per'].iloc[i]+=16
            elif data['liver_ast'].iloc[i]<=ast_min:
                data['liver_ast_per'].iloc[i]+=16 
            elif data['liver_ast'].iloc[i]>=(ast_max*1.4):
                data['liver_ast_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'AST' in keys:
                ast_min=bloodcodes_criterion['AST']['female_min_value']
                ast_max=bloodcodes_criterion['AST']['female_max_value']
            else:
                ast_min=4
                ast_max=40
            if data['liver_ast'].iloc[i]>=(ast_max*0.6) and data['liver_ast'].iloc[i]<(ast_max*0.8):
                data['liver_ast_per'].iloc[i]+=4
            elif data['liver_ast'].iloc[i]>=(ast_max*0.8) and data['liver_ast'].iloc[i]<ast_max:
                data['liver_ast_per'].iloc[i]+=8
            elif data['liver_ast'].iloc[i]>=ast_max and data['liver_ast'].iloc[i]<(ast_max*1.2):
                data['liver_ast_per'].iloc[i]+=12 
            elif data['liver_ast'].iloc[i]>=(ast_max*1.2) and data['liver_ast'].iloc[i]<(ast_max*1.4):
                data['liver_ast_per'].iloc[i]+=16
            elif data['liver_ast'].iloc[i]<=ast_min:
                data['liver_ast_per'].iloc[i]+=16 
            elif data['liver_ast'].iloc[i]>=(ast_max*1.4):
                data['liver_ast_per'].iloc[i]+=20
    # print(data['liver_ast_per'].value_counts())

    # 2) ALT
    print('2) ALT 확률 계산(20% 기준)')
    data["liver_alt_per"] = 0          
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'ALT' in keys:
                alt_min=bloodcodes_criterion['ALT']['male_min_value']
                alt_max=bloodcodes_criterion['ALT']['male_max_value']
            else:
                alt_min=4
                alt_max=40
            if data['liver_alt'].iloc[i]>=(alt_max*0.6) and data['liver_alt'].iloc[i]<(alt_max*0.8):
                data['liver_alt_per'].iloc[i]+=4
            elif data['liver_alt'].iloc[i]>=(alt_max*0.8) and data['liver_alt'].iloc[i]<alt_max:
                data['liver_alt_per'].iloc[i]+=8
            elif data['liver_alt'].iloc[i]>=alt_max and data['liver_alt'].iloc[i]<(alt_max*1.2):
                data['liver_alt_per'].iloc[i]+=12 
            elif data['liver_alt'].iloc[i]>=(alt_max*1.2) and data['liver_alt'].iloc[i]<(alt_max*1.4):
                data['liver_alt_per'].iloc[i]+=16
            elif data['liver_alt'].iloc[i]<=alt_min:
                data['liver_alt_per'].iloc[i]+=16 
            elif data['liver_alt'].iloc[i]>=(alt_max*1.4):
                data['liver_alt_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'ALT' in keys:
                alt_min=bloodcodes_criterion['ALT']['female_min_value']
                alt_max=bloodcodes_criterion['ALT']['female_max_value']
            else:
                alt_min=4
                alt_max=40
            if data['liver_alt'].iloc[i]>=(alt_max*0.6) and data['liver_alt'].iloc[i]<(alt_max*0.8):
                data['liver_alt_per'].iloc[i]+=4
            elif data['liver_alt'].iloc[i]>=(alt_max*0.8) and data['liver_alt'].iloc[i]<alt_max:
                data['liver_alt_per'].iloc[i]+=8
            elif data['liver_alt'].iloc[i]>=alt_max and data['liver_alt'].iloc[i]<(alt_max*1.2):
                data['liver_alt_per'].iloc[i]+=12 
            elif data['liver_alt'].iloc[i]>=(alt_max*1.2) and data['liver_alt'].iloc[i]<(alt_max*1.4):
                data['liver_alt_per'].iloc[i]+=16
            elif data['liver_alt'].iloc[i]<=alt_min:
                data['liver_alt_per'].iloc[i]+=16 
            elif data['liver_alt'].iloc[i]>=(alt_max*1.4):
                data['liver_alt_per'].iloc[i]+=20
    # print(data['liver_alt_per'].value_counts())

    # 3) ALP
    print('3) ALP 확률 계산(20% 기준)')
    data["liver_alp_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'ALP' in keys:
                alp_min=bloodcodes_criterion['ALP']['male_min_value']
                alp_max=bloodcodes_criterion['ALP']['male_max_value']
            else:
                alp_min=35
                alp_max=130
            if data['liver_alp'].iloc[i]<=(alp_min*0.8):
                data['liver_alp_per'].iloc[i]+=12
            elif data['liver_alp'].iloc[i]>(alp_min*0.8) and data['liver_alp'].iloc[i]<=alp_min:
                data['liver_alp_per'].iloc[i]+=8
            elif data['liver_alp'].iloc[i]>alp_min and data['liver_alp'].iloc[i]<=(alp_min*1.3):
                data['liver_alp_per'].iloc[i]+=4
            elif data['liver_alp'].iloc[i]>(alp_min*1.3) and data['liver_alp'].iloc[i]<(alp_max*0.8):
                data['liver_alp_per'].iloc[i]+=0
            elif data['liver_alp'].iloc[i]>=(alp_max*0.8) and data['liver_alp'].iloc[i]<(alp_max*0.9):
                data['liver_alp_per'].iloc[i]+=4
            elif data['liver_alp'].iloc[i]>=(alp_max*0.9) and data['liver_alp'].iloc[i]<alp_max:
                data['liver_alp_per'].iloc[i]+=8
            elif data['liver_alp'].iloc[i]>=alp_max and data['liver_alp'].iloc[i]<(alp_max*1.1):
                data['liver_alp_per'].iloc[i]+=12
            elif data['liver_alp'].iloc[i]>=(alp_max*1.1) and data['liver_alp'].iloc[i]<(alp_max*1.3):
                data['liver_alp_per'].iloc[i]+=16
            elif data['liver_alp'].iloc[i]>=(alp_max*1.3):
                data['liver_alp_per'].iloc[i]+=20
        if data['per1_gender'].iloc[i]==2:
            if 'ALP' in keys:
                alp_min=bloodcodes_criterion['ALP']['female_min_value']
                alp_max=bloodcodes_criterion['ALP']['female_max_value']
            else:
                alp_min=35
                alp_max=130
            if data['liver_alp'].iloc[i]<=(alp_min*0.8):
                data['liver_alp_per'].iloc[i]+=12
            elif data['liver_alp'].iloc[i]>(alp_min*0.8) and data['liver_alp'].iloc[i]<=alp_min:
                data['liver_alp_per'].iloc[i]+=8
            elif data['liver_alp'].iloc[i]>alp_min and data['liver_alp'].iloc[i]<=(alp_min*1.3):
                data['liver_alp_per'].iloc[i]+=4
            elif data['liver_alp'].iloc[i]>(alp_min*1.3) and data['liver_alp'].iloc[i]<(alp_max*0.8):
                data['liver_alp_per'].iloc[i]+=0
            elif data['liver_alp'].iloc[i]>=(alp_max*0.8) and data['liver_alp'].iloc[i]<(alp_max*0.9):
                data['liver_alp_per'].iloc[i]+=4
            elif data['liver_alp'].iloc[i]>=(alp_max*0.9) and data['liver_alp'].iloc[i]<alp_max:
                data['liver_alp_per'].iloc[i]+=8
            elif data['liver_alp'].iloc[i]>=alp_max and data['liver_alp'].iloc[i]<(alp_max*1.1):
                data['liver_alp_per'].iloc[i]+=12
            elif data['liver_alp'].iloc[i]>=(alp_max*1.1) and data['liver_alp'].iloc[i]<(alp_max*1.3):
                data['liver_alp_per'].iloc[i]+=16
            elif data['liver_alp'].iloc[i]>=(alp_max*1.3):
                data['liver_alp_per'].iloc[i]+=20
    # print(data['liver_alp_per'].value_counts())

    # 4) r-GTP
    print('4) r-GTP 확률 계산(20% 기준)')
    data["r_gtp_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'γ-GTP' in keys:
                r_gtp_m_min=bloodcodes_criterion['γ-GTP']['male_min_value']
                r_gtp_m_max=bloodcodes_criterion['γ-GTP']['male_max_value']
            else:
                r_gtp_m_min=11
                r_gtp_m_max=63
            if data['r_gtp'].iloc[i]<=(r_gtp_m_min*0.5):
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>(r_gtp_m_min*0.5) and data['r_gtp'].iloc[i]<=r_gtp_m_min:
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>r_gtp_m_min and data['r_gtp'].iloc[i]<(r_gtp_m_max*0.6):
                data['r_gtp_per'].iloc[i]+=0
            elif data['r_gtp'].iloc[i]>=(r_gtp_m_max*0.6) and data['r_gtp'].iloc[i]<(r_gtp_m_max*0.7):
                data['r_gtp_per'].iloc[i]+=4
            elif data['r_gtp'].iloc[i]>=(r_gtp_m_max*0.7) and data['r_gtp'].iloc[i]<(r_gtp_m_max*0.8):
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>=(r_gtp_m_max*0.8) and data['r_gtp'].iloc[i]<r_gtp_m_max:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>=r_gtp_m_max and data['r_gtp'].iloc[i]<(r_gtp_m_max*1.2):
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>=(r_gtp_m_max*1.2):
                data['r_gtp_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'γ-GTP' in keys:
                r_gtp_f_min=bloodcodes_criterion['γ-GTP']['female_min_value']
                r_gtp_f_max=bloodcodes_criterion['γ-GTP']['female_max_value']
            else:
                r_gtp_f_min=11
                r_gtp_f_max=63
            if data['r_gtp'].iloc[i]<=(r_gtp_f_min*0.5):
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>(r_gtp_f_min*0.5) and data['r_gtp'].iloc[i]<=r_gtp_f_min:
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>r_gtp_f_min and data['r_gtp'].iloc[i]<(r_gtp_f_max*0.6):
                data['r_gtp_per'].iloc[i]+=0
            elif data['r_gtp'].iloc[i]>=(r_gtp_f_max*0.6) and data['r_gtp'].iloc[i]<(r_gtp_f_max*0.7):
                data['r_gtp_per'].iloc[i]+=4
            elif data['r_gtp'].iloc[i]>=(r_gtp_f_max*0.7) and data['r_gtp'].iloc[i]<(r_gtp_f_max*0.8):
                data['r_gtp_per'].iloc[i]+=8
            elif data['r_gtp'].iloc[i]>=(r_gtp_f_max*0.8) and data['r_gtp'].iloc[i]<r_gtp_f_max:
                data['r_gtp_per'].iloc[i]+=12
            elif data['r_gtp'].iloc[i]>=r_gtp_f_max and data['r_gtp'].iloc[i]<(r_gtp_f_max*1.2):
                data['r_gtp_per'].iloc[i]+=16
            elif data['r_gtp'].iloc[i]>=(r_gtp_f_max*1.2):
                data['r_gtp_per'].iloc[i]+=20
    # print(data['r_gtp_per'].value_counts())

    # 5) HDL
    print('5) HDL 확률 계산(20% 기준)')
    data["hdl_col_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'HDL' in keys:
                hdl_min=bloodcodes_criterion['HDL']['male_min_value']
                hdl_max=bloodcodes_criterion['HDL']['male_max_value']
            else:
                hdl_min=60
                hdl_max=999
            if data['hdl_col'].iloc[i]<=(hdl_min*0.8):
                data['hdl_col_per'].iloc[i]+=20
            elif data['hdl_col'].iloc[i]<=(hdl_min*0.9) and data['hdl_col'].iloc[i]>(hdl_min*0.8):
                data['hdl_col_per'].iloc[i]+=16
            elif data['hdl_col'].iloc[i]<=hdl_min and data['hdl_col'].iloc[i]>(hdl_min*0.9):
                data['hdl_col_per'].iloc[i]+=12 
            elif data['hdl_col'].iloc[i]<=(hdl_min*1.1) and data['hdl_col'].iloc[i]>hdl_min:
                data['hdl_col_per'].iloc[i]+=8
            elif data['hdl_col'].iloc[i]<=(hdl_min*1.2) and data['hdl_col'].iloc[i]>(hdl_min*1.1):
                data['hdl_col_per'].iloc[i]+=4
        elif data['per1_gender'].iloc[i]==2:
            if 'HDL' in keys:
                hdl_min=bloodcodes_criterion['HDL']['female_min_value']
            else:
                hdl_min=60
            if data['hdl_col'].iloc[i]<=(hdl_min*0.8):
                data['hdl_col_per'].iloc[i]+=20
            elif data['hdl_col'].iloc[i]<=(hdl_min*0.9) and data['hdl_col'].iloc[i]>(hdl_min*0.8):
                data['hdl_col_per'].iloc[i]+=16
            elif data['hdl_col'].iloc[i]<=hdl_min and data['hdl_col'].iloc[i]>(hdl_min*0.9):
                data['hdl_col_per'].iloc[i]+=12 
            elif data['hdl_col'].iloc[i]<=(hdl_min*1.1) and data['hdl_col'].iloc[i]>hdl_min:
                data['hdl_col_per'].iloc[i]+=8
            elif data['hdl_col'].iloc[i]<=(hdl_min*1.2) and data['hdl_col'].iloc[i]>(hdl_min*1.1):
                data['hdl_col_per'].iloc[i]+=4
    # print(data['hdl_col_per'].value_counts())

    # 6) CEA
    print('6) CEA 확률 계산(20% 기준)')
    data["cea_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'CEA' in keys:
                cea_min=bloodcodes_criterion['CEA']['male_min_value']
                cea_max=bloodcodes_criterion['CEA']['male_max_value']
            else:
                cea_min=0
                cea_max=4.7
            if data['lar_int_cea'].iloc[i]>=(cea_max*0.25) and data['lar_int_cea'].iloc[i]<(cea_max*0.5):
                data['cea_per'].iloc[i]+=4
            elif data['lar_int_cea'].iloc[i]>=(cea_max*0.5) and data['lar_int_cea'].iloc[i]<(cea_max*0.75):
                data['cea_per'].iloc[i]+=8
            elif data['lar_int_cea'].iloc[i]>=(cea_max*0.75) and data['lar_int_cea'].iloc[i]<cea_max:
                data['cea_per'].iloc[i]+=12 
            elif data['lar_int_cea'].iloc[i]>=cea_max and data['lar_int_cea'].iloc[i]<(cea_max*1.25):
                data['cea_per'].iloc[i]+=16
            elif data['lar_int_cea'].iloc[i]>=(cea_max*1.25):
                data['cea_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'CEA' in keys:
                cea_min=bloodcodes_criterion['CEA']['female_min_value']
                cea_max=bloodcodes_criterion['CEA']['female_max_value']
            else:
                cea_min=0
                cea_max=4.7
            if data['lar_int_cea'].iloc[i]>=(cea_max*0.25) and data['lar_int_cea'].iloc[i]<(cea_max*0.5):
                data['cea_per'].iloc[i]+=4
            elif data['lar_int_cea'].iloc[i]>=(cea_max*0.5) and data['lar_int_cea'].iloc[i]<(cea_max*0.75):
                data['cea_per'].iloc[i]+=8
            elif data['lar_int_cea'].iloc[i]>=(cea_max*0.75) and data['lar_int_cea'].iloc[i]<cea_max:
                data['cea_per'].iloc[i]+=12 
            elif data['lar_int_cea'].iloc[i]>=cea_max and data['lar_int_cea'].iloc[i]<(cea_max*1.25):
                data['cea_per'].iloc[i]+=16
            elif data['lar_int_cea'].iloc[i]>=(cea_max*1.25):
                data['cea_per'].iloc[i]+=20
    # print(data['cea_per'].value_counts())

    # 7) CA19 
    print('7) CA19 확률 계산(20% 기준)')
    data["ca19_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'CA19' in keys:
                ca19_min=bloodcodes_criterion['CA19']['male_min_value']
                ca19_max=bloodcodes_criterion['CA19']['male_max_value']
            else:
                ca19_min=0
                ca19_max=34
            if data['lar_int_ca19'].iloc[i]>=(ca19_max*0.25) and data['lar_int_ca19'].iloc[i]<(ca19_max*0.5):
                data['ca19_per'].iloc[i]+=4
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*0.5) and data['lar_int_ca19'].iloc[i]<(ca19_max*0.75):
                data['ca19_per'].iloc[i]+=8
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*0.75) and data['lar_int_ca19'].iloc[i]<ca19_max:
                data['ca19_per'].iloc[i]+=12 
            elif data['lar_int_ca19'].iloc[i]>=ca19_max and data['lar_int_ca19'].iloc[i]<(ca19_max*1.25):
                data['ca19_per'].iloc[i]+=16
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*1.25):
                data['ca19_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'CA19' in keys:
                ca19_min=bloodcodes_criterion['CA19']['female_min_value']
                ca19_max=bloodcodes_criterion['CA19']['female_max_value']
            else:
                ca19_min=0
                ca19_max=34
            if data['lar_int_ca19'].iloc[i]>=(ca19_max*0.25) and data['lar_int_ca19'].iloc[i]<(ca19_max*0.5):
                data['ca19_per'].iloc[i]+=4
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*0.5) and data['lar_int_ca19'].iloc[i]<(ca19_max*0.75):
                data['ca19_per'].iloc[i]+=8
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*0.75) and data['lar_int_ca19'].iloc[i]<ca19_max:
                data['ca19_per'].iloc[i]+=12 
            elif data['lar_int_ca19'].iloc[i]>=ca19_max and data['lar_int_ca19'].iloc[i]<(ca19_max*1.25):
                data['ca19_per'].iloc[i]+=16
            elif data['lar_int_ca19'].iloc[i]>=(ca19_max*1.25):
                data['ca19_per'].iloc[i]+=20
    # print(data['ca19_per'].value_counts())

    # 8) Cyfra21-1 
    print('8) Cyfra21-1 확률 계산(20% 기준)')
    data["cyfra21_1_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'Cyfra21-1' in keys:
                cyfra21_min=bloodcodes_criterion['Cyfra21-1']['male_min_value']
                cyfra21_max=bloodcodes_criterion['Cyfra21-1']['male_max_value']
            else:
                cyfra21_min=0
                cyfra21_max=3.3
            if data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*0.6) and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*0.8):
                data['cyfra21_1_per'].iloc[i]+=4
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*0.8)and data['lung_cyfra21_1'].iloc[i]<cyfra21_max:
                data['cyfra21_1_per'].iloc[i]+=8
            elif data['lung_cyfra21_1'].iloc[i]>=cyfra21_max and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*1.2):
                data['cyfra21_1_per'].iloc[i]+=12 
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*1.2) and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*1.4):
                data['cyfra21_1_per'].iloc[i]+=16
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*1.4):
                data['cyfra21_1_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'Cyfra21-1' in keys:
                cyfra21_min=bloodcodes_criterion['Cyfra21-1']['female_min_value']
                cyfra21_max=bloodcodes_criterion['Cyfra21-1']['female_max_value']
            else:
                cyfra21_min=0
                cyfra21_max=3.3
            if data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*0.6) and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*0.8):
                data['cyfra21_1_per'].iloc[i]+=4
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*0.8)and data['lung_cyfra21_1'].iloc[i]<cyfra21_max:
                data['cyfra21_1_per'].iloc[i]+=8
            elif data['lung_cyfra21_1'].iloc[i]>=cyfra21_max and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*1.2):
                data['cyfra21_1_per'].iloc[i]+=12 
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*1.2) and data['lung_cyfra21_1'].iloc[i]<(cyfra21_max*1.4):
                data['cyfra21_1_per'].iloc[i]+=16
            elif data['lung_cyfra21_1'].iloc[i]>=(cyfra21_max*1.4):
                data['cyfra21_1_per'].iloc[i]+=20
    # print(data['cyfra21_1_per'].value_counts())

    # 9) FreeT4
    print('9) FreeT4 확률 계산(20% 기준)')
    data["ft4_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'Free T4' in keys:
                ft4_min=bloodcodes_criterion['Free T4']['male_min_value']
                ft4_max=bloodcodes_criterion['Free T4']['male_max_value']
            else:
                ft4_min=0.90
                ft4_max=1.70
            if data['thy_ft4'].iloc[i]<(0.8*ft4_min):
                data['ft4_per'].iloc[i]+=8
            elif data['thy_ft4'].iloc[i]>=(0.8*ft4_min) and data['thy_ft4'].iloc[i]<ft4_min:
                data['ft4_per'].iloc[i]+=6 
            elif data['thy_ft4'].iloc[i]>=ft4_min and data['thy_ft4'].iloc[i]<(0.8*ft4_max):
                data['ft4_per'].iloc[i]+=0
            elif data['thy_ft4'].iloc[i]>=(0.8*ft4_max) and data['thy_ft4'].iloc[i]<(0.9*ft4_max):
                data['ft4_per'].iloc[i]+=4
            elif data['thy_ft4'].iloc[i]>=(0.9*ft4_max) and data['thy_ft4'].iloc[i]<ft4_max:
                data['ft4_per'].iloc[i]+=8
            elif data['thy_ft4'].iloc[i]>=ft4_max and data['thy_ft4'].iloc[i]<(1.1*ft4_max):
                data['ft4_per'].iloc[i]+=12
            elif data['thy_ft4'].iloc[i]>=(1.1*ft4_max) and data['thy_ft4'].iloc[i]<(1.2*ft4_max):
                data['ft4_per'].iloc[i]+=16
            elif data['thy_ft4'].iloc[i]>=(1.2*ft4_max):
                data['ft4_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'Free T4' in keys:
                ft4_min=bloodcodes_criterion['Free T4']['female_min_value']
                ft4_max=bloodcodes_criterion['Free T4']['female_max_value']
            else:
                ft4_min=0.90
                ft4_max=1.70
            if data['thy_ft4'].iloc[i]<(0.8*ft4_min):
                data['ft4_per'].iloc[i]+=8
            elif data['thy_ft4'].iloc[i]>=(0.8*ft4_min) and data['thy_ft4'].iloc[i]<ft4_min:
                data['ft4_per'].iloc[i]+=6 
            elif data['thy_ft4'].iloc[i]>=ft4_min and data['thy_ft4'].iloc[i]<(0.8*ft4_max):
                data['ft4_per'].iloc[i]+=0
            elif data['thy_ft4'].iloc[i]>=(0.8*ft4_max) and data['thy_ft4'].iloc[i]<(0.9*ft4_max):
                data['ft4_per'].iloc[i]+=4
            elif data['thy_ft4'].iloc[i]>=(0.9*ft4_max) and data['thy_ft4'].iloc[i]<ft4_max:
                data['ft4_per'].iloc[i]+=8
            elif data['thy_ft4'].iloc[i]>=ft4_max and data['thy_ft4'].iloc[i]<(1.1*ft4_max):
                data['ft4_per'].iloc[i]+=12
            elif data['thy_ft4'].iloc[i]>=(1.1*ft4_max) and data['thy_ft4'].iloc[i]<(1.2*ft4_max):
                data['ft4_per'].iloc[i]+=16
            elif data['thy_ft4'].iloc[i]>=(1.2*ft4_max):
                data['ft4_per'].iloc[i]+=20
    # print(data['ft4_per'].value_counts())

    # 10) TSH 
    print('10) TSH 확률 계산(20% 기준)')
    data["tsh_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'TSH' in keys:
                tsh_min=bloodcodes_criterion['TSH']['male_min_value']
                tsh_max=bloodcodes_criterion['TSH']['male_max_value']
            else:
                tsh_min=0.3
                tsh_max=5.0
            if data['thy_tsh'].iloc[i]>=(0.8*tsh_max) and data['thy_tsh'].iloc[i]<(0.9*tsh_max):
                data['tsh_per'].iloc[i]+=4
            elif data['thy_tsh'].iloc[i]>=(0.9*tsh_max) and data['thy_tsh'].iloc[i]<tsh_max:
                data['tsh_per'].iloc[i]+=8
            elif data['thy_tsh'].iloc[i]>=tsh_max and data['thy_tsh'].iloc[i]<(1.1*tsh_max):
                data['tsh_per'].iloc[i]+=12 
            elif data['thy_tsh'].iloc[i]>=(1.1*tsh_max) and data['thy_tsh'].iloc[i]<(1.2*tsh_max):
                data['tsh_per'].iloc[i]+=16
            elif data['thy_tsh'].iloc[i]>=(1.2*tsh_max):
                data['tsh_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'TSH' in keys:
                tsh_min=bloodcodes_criterion['TSH']['female_min_value']
                tsh_max=bloodcodes_criterion['TSH']['female_max_value']
            else:
                tsh_min=0.3
                tsh_max=5.0
            if data['thy_tsh'].iloc[i]>=(0.8*tsh_max) and data['thy_tsh'].iloc[i]<(0.9*tsh_max):
                data['tsh_per'].iloc[i]+=4
            elif data['thy_tsh'].iloc[i]>=(0.9*tsh_max) and data['thy_tsh'].iloc[i]<tsh_max:
                data['tsh_per'].iloc[i]+=8
            elif data['thy_tsh'].iloc[i]>=tsh_max and data['thy_tsh'].iloc[i]<(1.1*tsh_max):
                data['tsh_per'].iloc[i]+=12 
            elif data['thy_tsh'].iloc[i]>=(1.1*tsh_max) and data['thy_tsh'].iloc[i]<(1.2*tsh_max):
                data['tsh_per'].iloc[i]+=16
            elif data['thy_tsh'].iloc[i]>=(1.2*tsh_max):
                data['tsh_per'].iloc[i]+=20
    # print(data['tsh_per'].value_counts())
            
    # 11) CA15-3
    print('11) CA15-3 확률 계산(20% 기준)')
    data["ca15_3_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'CA15-3' in keys:
                ca15_3_min=bloodcodes_criterion['CA15-3']['male_min_value']
                ca15_3_max=bloodcodes_criterion['CA15-3']['male_max_value']
            else:
                ca15_3_min=0
                ca15_3_max=30
            if data['breast_ca15_3'].iloc[i]>=(0.1*ca15_3_max) and data['breast_ca15_3'].iloc[i]<(0.4*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=4
            elif data['breast_ca15_3'].iloc[i]>=(0.4*ca15_3_max) and data['breast_ca15_3'].iloc[i]<(0.7*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=8
            elif data['breast_ca15_3'].iloc[i]>=(0.7*ca15_3_max) and data['breast_ca15_3'].iloc[i]<ca15_3_max:
                data['ca15_3_per'].iloc[i]+=12 
            elif data['breast_ca15_3'].iloc[i]>=ca15_3_max and data['breast_ca15_3'].iloc[i]<(1.3*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=16
            elif data['breast_ca15_3'].iloc[i]>=(1.3*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'CA15-3' in keys:
                ca15_3_min=bloodcodes_criterion['CA15-3']['female_min_value']
                ca15_3_max=bloodcodes_criterion['CA15-3']['female_max_value']
            else:
                ca15_3_min=0
                ca15_3_max=30
            if data['breast_ca15_3'].iloc[i]>=(0.1*ca15_3_max) and data['breast_ca15_3'].iloc[i]<(0.4*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=4
            elif data['breast_ca15_3'].iloc[i]>=(0.4*ca15_3_max) and data['breast_ca15_3'].iloc[i]<(0.7*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=8
            elif data['breast_ca15_3'].iloc[i]>=(0.7*ca15_3_max) and data['breast_ca15_3'].iloc[i]<ca15_3_max:
                data['ca15_3_per'].iloc[i]+=12 
            elif data['breast_ca15_3'].iloc[i]>=ca15_3_max and data['breast_ca15_3'].iloc[i]<(1.3*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=16
            elif data['breast_ca15_3'].iloc[i]>=(1.3*ca15_3_max):
                data['ca15_3_per'].iloc[i]+=20
    # print(data['ca15_3_per'].value_counts())

    # 12) BMI 
    print('12) BMI 확률 계산(20% 기준)')
    data["bmi_per"] = 0
    # BMI는 최저/최고 수치 반영 이후 구간화해서 진행(저체중 ~ 고도비만까지)
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'BMI' in keys:
                bmi_min=bloodcodes_criterion['BMI']['male_min_value']
                bmi_max=bloodcodes_criterion['BMI']['male_max_value']
            else:
                bmi_min=18.5
                bmi_max=22.9
            if data['bmi'].iloc[i]<=bmi_min:
                data['bmi_per'].iloc[i]+=10
            elif data['bmi'].iloc[i]>=22.5 and data['bmi'].iloc[i]<=bmi_max:
                data['bmi_per'].iloc[i]+=5
            elif data['bmi'].iloc[i]>bmi_max and data['bmi'].iloc[i]<=23.9:
                data['bmi_per'].iloc[i]+=10
            elif data['bmi'].iloc[i]>=24.0 and data['bmi'].iloc[i]<=24.9:
                data['bmi_per'].iloc[i]+=15
            elif data['bmi'].iloc[i]>=25.0:
                data['bmi_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'BMI' in keys:
                bmi_min=bloodcodes_criterion['BMI']['female_min_value']
                bmi_max=bloodcodes_criterion['BMI']['female_max_value']
            else:
                bmi_min=18.5
                bmi_max=22.9
            if data['bmi'].iloc[i]<=bmi_min:
                data['bmi_per'].iloc[i]+=10
            elif data['bmi'].iloc[i]>=22.5 and data['bmi'].iloc[i]<=bmi_max:
                data['bmi_per'].iloc[i]+=5
            elif data['bmi'].iloc[i]>bmi_max and data['bmi'].iloc[i]<=23.9:
                data['bmi_per'].iloc[i]+=10
            elif data['bmi'].iloc[i]>=24.0 and data['bmi'].iloc[i]<=24.9:
                data['bmi_per'].iloc[i]+=15
            elif data['bmi'].iloc[i]>=25.0:
                data['bmi_per'].iloc[i]+=20
    # print(data['bmi_per'].value_counts())

    # 13) 총 콜레스테롤
    print('13) 총 콜레스테롤 확률 계산(20% 기준)')
    data["total_col_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '총 콜레스테롤' in keys:
                total_col_min=bloodcodes_criterion['총 콜레스테롤']['male_min_value']
                total_col_max=bloodcodes_criterion['총 콜레스테롤']['male_max_value']
            else:
                total_col_min=130
                total_col_max=199
            if data['total_col'].iloc[i]<(0.75*total_col_min):
                data['total_col_per'].iloc[i]+=8
            elif data['total_col'].iloc[i]>=(0.75*total_col_min) and data['total_col'].iloc[i]<total_col_min:
                data['total_col_per'].iloc[i]+=4
            elif data['total_col'].iloc[i]>=total_col_min and data['total_col'].iloc[i]<(0.85*total_col_max):
                data['total_col_per'].iloc[i]+=0
            elif data['total_col'].iloc[i]>=(0.85*total_col_max) and data['total_col'].iloc[i]<(0.9*total_col_max):
                data['total_col_per'].iloc[i]+=4
            elif data['total_col'].iloc[i]>=(0.9*total_col_max) and data['total_col'].iloc[i]<total_col_max:
                data['total_col_per'].iloc[i]+=8
            elif data['total_col'].iloc[i]>=total_col_max and data['total_col'].iloc[i]<(1.1*total_col_max):
                data['total_col_per'].iloc[i]+=12
            elif data['total_col'].iloc[i]>=(1.1*total_col_max) and data['total_col'].iloc[i]<(1.2*total_col_max):
                data['total_col_per'].iloc[i]+=16
            elif data['total_col'].iloc[i]>=(1.2*total_col_max):
                data['total_col_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '총 콜레스테롤' in keys:
                total_col_min=bloodcodes_criterion['총 콜레스테롤']['female_min_value']
                total_col_max=bloodcodes_criterion['총 콜레스테롤']['female_max_value']
            else:
                total_col_min=130
                total_col_max=199
            if data['total_col'].iloc[i]<(0.75*total_col_min):
                data['total_col_per'].iloc[i]+=8
            elif data['total_col'].iloc[i]>=(0.75*total_col_min) and data['total_col'].iloc[i]<total_col_min:
                data['total_col_per'].iloc[i]+=4
            elif data['total_col'].iloc[i]>=total_col_min and data['total_col'].iloc[i]<(0.85*total_col_max):
                data['total_col_per'].iloc[i]+=0
            elif data['total_col'].iloc[i]>=(0.85*total_col_max) and data['total_col'].iloc[i]<(0.9*total_col_max):
                data['total_col_per'].iloc[i]+=4
            elif data['total_col'].iloc[i]>=(0.9*total_col_max) and data['total_col'].iloc[i]<total_col_max:
                data['total_col_per'].iloc[i]+=8
            elif data['total_col'].iloc[i]>=total_col_max and data['total_col'].iloc[i]<(1.1*total_col_max):
                data['total_col_per'].iloc[i]+=12
            elif data['total_col'].iloc[i]>=(1.1*total_col_max) and data['total_col'].iloc[i]<(1.2*total_col_max):
                data['total_col_per'].iloc[i]+=16
            elif data['total_col'].iloc[i]>=(1.2*total_col_max):
                data['total_col_per'].iloc[i]+=20
    # print(data['total_col_per'].value_counts())
            
    # 14) LDL 
    print('14) LDL 확률 계산(20% 기준)')
    data["ldl_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if 'LDL' in keys:
                ldl_col_min=bloodcodes_criterion['LDL']['male_min_value']
                ldl_col_max=bloodcodes_criterion['LDL']['male_max_value']
            else:
                ldl_col_min=0
                ldl_col_max=129
            if data['ldl_col_cal'].iloc[i]>=(0.8*ldl_col_max) and data['ldl_col_cal'].iloc[i]<(0.9*ldl_col_max):
                data['ldl_per'].iloc[i]+=4
            elif data['ldl_col_cal'].iloc[i]>=(0.9*ldl_col_max) and data['ldl_col_cal'].iloc[i]<ldl_col_max:
                data['ldl_per'].iloc[i]+=8
            elif data['ldl_col_cal'].iloc[i]>=ldl_col_max and data['ldl_col_cal'].iloc[i]<(1.1*ldl_col_max):
                data['ldl_per'].iloc[i]+=12 
            elif data['ldl_col_cal'].iloc[i]>=(1.1*ldl_col_max) and data['ldl_col_cal'].iloc[i]<(1.2*ldl_col_max):
                data['ldl_per'].iloc[i]+=16
            elif data['ldl_col_cal'].iloc[i]>=(1.2*ldl_col_max):
                data['ldl_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if 'LDL' in keys:
                ldl_col_min=bloodcodes_criterion['LDL']['female_min_value']
                ldl_col_max=bloodcodes_criterion['LDL']['female_max_value']
            else:
                ldl_col_min=0
                ldl_col_max=129
            if data['ldl_col_cal'].iloc[i]>=(0.8*ldl_col_max) and data['ldl_col_cal'].iloc[i]<(0.9*ldl_col_max):
                data['ldl_per'].iloc[i]+=4
            elif data['ldl_col_cal'].iloc[i]>=(0.9*ldl_col_max) and data['ldl_col_cal'].iloc[i]<ldl_col_max:
                data['ldl_per'].iloc[i]+=8
            elif data['ldl_col_cal'].iloc[i]>=ldl_col_max and data['ldl_col_cal'].iloc[i]<(1.1*ldl_col_max):
                data['ldl_per'].iloc[i]+=12 
            elif data['ldl_col_cal'].iloc[i]>=(1.1*ldl_col_max) and data['ldl_col_cal'].iloc[i]<(1.2*ldl_col_max):
                data['ldl_per'].iloc[i]+=16
            elif data['ldl_col_cal'].iloc[i]>=(1.2*ldl_col_max):
                data['ldl_per'].iloc[i]+=20
    # print(data['ldl_per'].value_counts())
            
    # 15) 공복혈당
    print('15) 공복혈당 확률 계산(20% 기준)')
    data["glucose_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '공복혈당' in keys:
                glucose_min=bloodcodes_criterion['공복혈당']['male_min_value']
                glucose_max=bloodcodes_criterion['공복혈당']['male_max_value']
            else:
                glucose_min=70
                glucose_max=99
            if data['glucose'].iloc[i]<(0.85*glucose_min):
                data['glucose_per'].iloc[i]+=20
            elif data['glucose'].iloc[i]>=(0.85*glucose_min) and data['glucose'].iloc[i]<(0.9*glucose_min):
                data['glucose_per'].iloc[i]+=16    
            elif data['glucose'].iloc[i]>=(0.9*glucose_min) and data['glucose'].iloc[i]<glucose_min:
                data['glucose_per'].iloc[i]+=12
            elif data['glucose'].iloc[i]>=glucose_min and data['glucose'].iloc[i]<(0.75*glucose_max):
                data['glucose_per'].iloc[i]+=8 
            elif data['glucose'].iloc[i]>=(0.75*glucose_max) and data['glucose'].iloc[i]<(0.80*glucose_max):
                data['glucose_per'].iloc[i]+=4
            elif data['glucose'].iloc[i]>=(0.80*glucose_max) and data['glucose'].iloc[i]<glucose_max:
                data['glucose_per'].iloc[i]+=0
            elif data['glucose'].iloc[i]>=glucose_max and data['glucose'].iloc[i]<(1.1*glucose_max):
                data['glucose_per'].iloc[i]+=4
            elif data['glucose'].iloc[i]>=(1.1*glucose_max) and data['glucose'].iloc[i]<(1.2*glucose_max):
                data['glucose_per'].iloc[i]+=8
            elif data['glucose'].iloc[i]>=(1.2*glucose_max) and data['glucose'].iloc[i]<(1.3*glucose_max):
                data['glucose_per'].iloc[i]+=12
            elif data['glucose'].iloc[i]>=(1.3*glucose_max) and data['glucose'].iloc[i]<(1.4*glucose_max):
                data['glucose_per'].iloc[i]+=16
            elif data['glucose'].iloc[i]>=(1.4*glucose_max):
                data['glucose_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '공복혈당' in keys:
                glucose_min=bloodcodes_criterion['공복혈당']['female_min_value']
                glucose_max=bloodcodes_criterion['공복혈당']['female_max_value']
            else:
                glucose_min=70
                glucose_max=99
            if data['glucose'].iloc[i]<(0.85*glucose_min):
                data['glucose_per'].iloc[i]+=20
            elif data['glucose'].iloc[i]>=(0.85*glucose_min) and data['glucose'].iloc[i]<(0.9*glucose_min):
                data['glucose_per'].iloc[i]+=16    
            elif data['glucose'].iloc[i]>=(0.9*glucose_min) and data['glucose'].iloc[i]<glucose_min:
                data['glucose_per'].iloc[i]+=12
            elif data['glucose'].iloc[i]>=glucose_min and data['glucose'].iloc[i]<(0.75*glucose_max):
                data['glucose_per'].iloc[i]+=8 
            elif data['glucose'].iloc[i]>=(0.75*glucose_max) and data['glucose'].iloc[i]<(0.80*glucose_max):
                data['glucose_per'].iloc[i]+=4
            elif data['glucose'].iloc[i]>=(0.80*glucose_max) and data['glucose'].iloc[i]<glucose_max:
                data['glucose_per'].iloc[i]+=0
            elif data['glucose'].iloc[i]>=glucose_max and data['glucose'].iloc[i]<(1.1*glucose_max):
                data['glucose_per'].iloc[i]+=4
            elif data['glucose'].iloc[i]>=(1.1*glucose_max) and data['glucose'].iloc[i]<(1.2*glucose_max):
                data['glucose_per'].iloc[i]+=8
            elif data['glucose'].iloc[i]>=(1.2*glucose_max) and data['glucose'].iloc[i]<(1.3*glucose_max):
                data['glucose_per'].iloc[i]+=12
            elif data['glucose'].iloc[i]>=(1.3*glucose_max) and data['glucose'].iloc[i]<(1.4*glucose_max):
                data['glucose_per'].iloc[i]+=16
            elif data['glucose'].iloc[i]>=(1.4*glucose_max):
                data['glucose_per'].iloc[i]+=20
    # print(data['glucose_per'].value_counts())
        
    # 16) 중성지방 
    print('16) 중성지방 확률 계산(20% 기준)')
    data["tri_gly_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '중성지방' in keys:
                tri_gly_min=bloodcodes_criterion['중성지방']['male_min_value']
                tri_gly_max=bloodcodes_criterion['중성지방']['male_max_value']
            else:
                tri_gly_min=0
                tri_gly_max=149
            if data['tri_gly'].iloc[i]>=(0.9*tri_gly_max) and data['tri_gly'].iloc[i]<tri_gly_max:
                data['tri_gly_per'].iloc[i]+=4
            elif data['tri_gly'].iloc[i]>=tri_gly_max and data['tri_gly'].iloc[i]<(1.1*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=8
            elif data['tri_gly'].iloc[i]>=(1.1*tri_gly_max) and data['tri_gly'].iloc[i]<(1.2*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=12 
            elif data['tri_gly'].iloc[i]>=(1.2*tri_gly_max) and data['tri_gly'].iloc[i]<(1.3*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=16
            elif data['tri_gly'].iloc[i]>=(1.3*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '중성지방' in keys:
                tri_gly_min=bloodcodes_criterion['중성지방']['female_min_value']
                tri_gly_max=bloodcodes_criterion['중성지방']['female_max_value']
            else:
                tri_gly_min=0
                tri_gly_max=149
            if data['tri_gly'].iloc[i]>=(0.9*tri_gly_max) and data['tri_gly'].iloc[i]<tri_gly_max:
                data['tri_gly_per'].iloc[i]+=4
            elif data['tri_gly'].iloc[i]>=tri_gly_max and data['tri_gly'].iloc[i]<(1.1*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=8
            elif data['tri_gly'].iloc[i]>=(1.1*tri_gly_max) and data['tri_gly'].iloc[i]<(1.2*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=12 
            elif data['tri_gly'].iloc[i]>=(1.2*tri_gly_max) and data['tri_gly'].iloc[i]<(1.3*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=16
            elif data['tri_gly'].iloc[i]>=(1.3*tri_gly_max):
                data['tri_gly_per'].iloc[i]+=20
    # print(data['tri_gly_per'].value_counts())

    # 17) 수축기 혈압
    print('17) 수축기 혈압 확률 계산(20% 기준)')
    data["blood_press_high_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '수축기 혈압' in keys:
                bp_high_min=bloodcodes_criterion['수축기 혈압']['male_min_value']
                bp_high_max=bloodcodes_criterion['수축기 혈압']['male_max_value']
            else:
                bp_high_min=0
                bp_high_max=90
            if data['blood_press_high'].iloc[i]>=(bp_high_max+5) and data['blood_press_high'].iloc[i]<(bp_high_max+10):
                data['blood_press_high_per'].iloc[i]+=4
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+10) and data['blood_press_high'].iloc[i]<(bp_high_max+15):
                data['blood_press_high_per'].iloc[i]+=8
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+15) and data['blood_press_high'].iloc[i]<(bp_high_max+20):
                data['blood_press_high_per'].iloc[i]+=12 
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+20) and data['blood_press_high'].iloc[i]<(bp_high_max+25):
                data['blood_press_high_per'].iloc[i]+=16
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+25):
                data['blood_press_high_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '수축기 혈압' in keys:
                bp_high_min=bloodcodes_criterion['수축기 혈압']['female_min_value']
                bp_high_max=bloodcodes_criterion['수축기 혈압']['female_max_value']
            else:
                bp_high_min=0
                bp_high_max=119
            if data['blood_press_high'].iloc[i]>=(bp_high_max+5) and data['blood_press_high'].iloc[i]<(bp_high_max+10):
                data['blood_press_high_per'].iloc[i]+=4
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+10) and data['blood_press_high'].iloc[i]<(bp_high_max+15):
                data['blood_press_high_per'].iloc[i]+=8
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+15) and data['blood_press_high'].iloc[i]<(bp_high_max+20):
                data['blood_press_high_per'].iloc[i]+=12 
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+20) and data['blood_press_high'].iloc[i]<(bp_high_max+25):
                data['blood_press_high_per'].iloc[i]+=16
            elif data['blood_press_high'].iloc[i]>=(bp_high_max+25):
                data['blood_press_high_per'].iloc[i]+=20
    # print(data['blood_press_high_per'].value_counts())

    # 18) 이완기 혈압
    print('18) 이완기 혈압 확률 계산(20% 기준)')
    data["blood_press_low_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '이완기 혈압' in keys:
                bp_low_min=bloodcodes_criterion['이완기 혈압']['male_min_value']
                bp_low_max=bloodcodes_criterion['이완기 혈압']['male_max_value']
            else:
                bp_low_min=0
                bp_low_max=79
            if data['blood_press_low'].iloc[i]>=(bp_low_max-10) and data['blood_press_low'].iloc[i]<(bp_low_max-5):
                data['blood_press_low_per'].iloc[i]+=4
            elif data['blood_press_low'].iloc[i]>=(bp_low_max-5) and data['blood_press_low'].iloc[i]<bp_low_max:
                data['blood_press_low_per'].iloc[i]+=8
            elif data['blood_press_low'].iloc[i]>=bp_low_max and data['blood_press_low'].iloc[i]<(bp_low_max+10):
                data['blood_press_low_per'].iloc[i]+=12 
            elif data['blood_press_low'].iloc[i]>=(bp_low_max+10) and data['blood_press_low'].iloc[i]<(bp_low_max+20):
                data['blood_press_low_per'].iloc[i]+=16
            elif data['blood_press_low'].iloc[i]>=(bp_low_max+20):
                data['blood_press_low_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '이완기 혈압' in keys:
                bp_low_min=bloodcodes_criterion['이완기 혈압']['female_min_value']
                bp_low_max=bloodcodes_criterion['이완기 혈압']['female_max_value']
            else:
                bp_low_min=0
                bp_low_max=79
            if data['blood_press_low'].iloc[i]>=(bp_low_max-10) and data['blood_press_low'].iloc[i]<(bp_low_max-5):
                data['blood_press_low_per'].iloc[i]+=4
            elif data['blood_press_low'].iloc[i]>=(bp_low_max-5) and data['blood_press_low'].iloc[i]<bp_low_max:
                data['blood_press_low_per'].iloc[i]+=8
            elif data['blood_press_low'].iloc[i]>=bp_low_max and data['blood_press_low'].iloc[i]<(bp_low_max+10):
                data['blood_press_low_per'].iloc[i]+=12 
            elif data['blood_press_low'].iloc[i]>=(bp_low_max+10) and data['blood_press_low'].iloc[i]<(bp_low_max+20):
                data['blood_press_low_per'].iloc[i]+=16
            elif data['blood_press_low'].iloc[i]>=(bp_low_max+20):
                data['blood_press_low_per'].iloc[i]+=20
    # print(data['blood_press_low_per'].value_counts())

    # 19) 총 단백질
    print('19) 총 단백질 확률 계산(20% 기준)')
    data["liver_protein_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '총 단백질' in keys:
                total_protein_min=bloodcodes_criterion['총 단백질']['male_min_value']
                total_protein_max=bloodcodes_criterion['총 단백질']['male_max_value']
            else:
                total_protein_min=6.5
                total_protein_max=8.3
            if data['liver_protein'].iloc[i]<(total_protein_min-1.0):
                data['liver_protein_per'].iloc[i]+=20
            elif data['liver_protein'].iloc[i]>=(total_protein_min-1.0) and data['liver_protein'].iloc[i]<(total_protein_min-0.5):
                data['liver_protein_per'].iloc[i]+=16
            elif data['liver_protein'].iloc[i]>=(total_protein_min-0.5) and data['liver_protein'].iloc[i]<total_protein_min:
                data['liver_protein_per'].iloc[i]+=12
            elif data['liver_protein'].iloc[i]>=total_protein_min and data['liver_protein'].iloc[i]<(total_protein_min+0.5):
                data['liver_protein_per'].iloc[i]+=8
            elif data['liver_protein'].iloc[i]>=(total_protein_min+0.5) and data['liver_protein'].iloc[i]<(total_protein_max-1.0):
                data['liver_protein_per'].iloc[i]+=4
            elif data['liver_protein'].iloc[i]>=(total_protein_max-1.0) and data['liver_protein'].iloc[i]<(total_protein_min+1.0):
                data['liver_protein_per'].iloc[i]+=0
            elif data['liver_protein'].iloc[i]>=(total_protein_min+1.0) and data['liver_protein'].iloc[i]<(total_protein_max-0.5):
                data['liver_protein_per'].iloc[i]+=4
            elif data['liver_protein'].iloc[i]>=(total_protein_max-0.5) and data['liver_protein'].iloc[i]<total_protein_max:
                data['liver_protein_per'].iloc[i]+=8
            elif data['liver_protein'].iloc[i]>=total_protein_max and data['liver_protein'].iloc[i]<(total_protein_max+0.5):
                data['liver_protein_per'].iloc[i]+=12
            elif data['liver_protein'].iloc[i]>=(total_protein_max+0.5) and data['liver_protein'].iloc[i]<(total_protein_max+1.0):
                data['liver_protein_per'].iloc[i]+=16
            elif data['liver_protein'].iloc[i]>=(total_protein_max+1.0):
                data['liver_protein_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '총 단백질' in keys:
                total_protein_min=bloodcodes_criterion['총 단백질']['female_min_value']
                total_protein_max=bloodcodes_criterion['총 단백질']['female_max_value']
            else:
                total_protein_min=6.5
                total_protein_max=8.3
            if data['liver_protein'].iloc[i]<(total_protein_min-1.0):
                data['liver_protein_per'].iloc[i]+=20
            elif data['liver_protein'].iloc[i]>=(total_protein_min-1.0) and data['liver_protein'].iloc[i]<(total_protein_min-0.5):
                data['liver_protein_per'].iloc[i]+=16
            elif data['liver_protein'].iloc[i]>=(total_protein_min-0.5) and data['liver_protein'].iloc[i]<total_protein_min:
                data['liver_protein_per'].iloc[i]+=12
            elif data['liver_protein'].iloc[i]>=total_protein_min and data['liver_protein'].iloc[i]<(total_protein_min+0.5):
                data['liver_protein_per'].iloc[i]+=8
            elif data['liver_protein'].iloc[i]>=(total_protein_min+0.5) and data['liver_protein'].iloc[i]<(total_protein_max-1.0):
                data['liver_protein_per'].iloc[i]+=4
            elif data['liver_protein'].iloc[i]>=(total_protein_max-1.0) and data['liver_protein'].iloc[i]<(total_protein_min+1.0):
                data['liver_protein_per'].iloc[i]+=0
            elif data['liver_protein'].iloc[i]>=(total_protein_min+1.0) and data['liver_protein'].iloc[i]<(total_protein_max-0.5):
                data['liver_protein_per'].iloc[i]+=4
            elif data['liver_protein'].iloc[i]>=(total_protein_max-0.5) and data['liver_protein'].iloc[i]<total_protein_max:
                data['liver_protein_per'].iloc[i]+=8
            elif data['liver_protein'].iloc[i]>=total_protein_max and data['liver_protein'].iloc[i]<(total_protein_max+0.5):
                data['liver_protein_per'].iloc[i]+=12
            elif data['liver_protein'].iloc[i]>=(total_protein_max+0.5) and data['liver_protein'].iloc[i]<(total_protein_max+1.0):
                data['liver_protein_per'].iloc[i]+=16
            elif data['liver_protein'].iloc[i]>=(total_protein_max+1.0):
                data['liver_protein_per'].iloc[i]+=20
    # print(data['liver_protein_per'].value_counts())

    # 20) 알부민
    print('20) 알부민 확률 계산(20% 기준)')
    data["albumin_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '알부민' in keys:
                albumin_min=bloodcodes_criterion['알부민']['male_min_value']
                albumin_max=bloodcodes_criterion['알부민']['male_max_value']
            else:
                albumin_min=3.5
                albumin_max=5.3
            if data['liver_albumin'].iloc[i]<(albumin_min-1.0):
                data['albumin_per'].iloc[i]+=20
            elif data['liver_albumin'].iloc[i]>=(albumin_min-1.0) and data['liver_albumin'].iloc[i]<(albumin_min-0.5):
                data['albumin_per'].iloc[i]+=16
            elif data['liver_albumin'].iloc[i]>=(albumin_min-0.5) and data['liver_albumin'].iloc[i]<albumin_min:
                data['albumin_per'].iloc[i]+=12 
            elif data['liver_albumin'].iloc[i]>=albumin_min and data['liver_albumin'].iloc[i]<(albumin_min+0.5):
                data['albumin_per'].iloc[i]+=8
            elif data['liver_albumin'].iloc[i]>=(albumin_min+0.5) and data['liver_albumin'].iloc[i]<(albumin_max-1.0):
                data['albumin_per'].iloc[i]+=4
            elif data['liver_albumin'].iloc[i]>=(albumin_max-1.0) and data['liver_albumin'].iloc[i]<(albumin_min+1.0):
                data['albumin_per'].iloc[i]+=0
            elif data['liver_albumin'].iloc[i]>=(albumin_min+1.0) and data['liver_albumin'].iloc[i]<(albumin_max-0.5):
                data['albumin_per'].iloc[i]+=4
            elif data['liver_albumin'].iloc[i]>=(albumin_max-0.5) and data['liver_albumin'].iloc[i]<albumin_max:
                data['albumin_per'].iloc[i]+=8
            elif data['liver_albumin'].iloc[i]>=albumin_max and data['liver_albumin'].iloc[i]<(albumin_max+0.5):
                data['albumin_per'].iloc[i]+=12
            elif data['liver_albumin'].iloc[i]>=(albumin_max+0.5) and data['liver_albumin'].iloc[i]<(albumin_max+1.0):
                data['albumin_per'].iloc[i]+=16
            elif data['liver_albumin'].iloc[i]>=(albumin_max+1.0):
                data['albumin_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '알부민' in keys:
                albumin_min=bloodcodes_criterion['알부민']['female_min_value']
                albumin_max=bloodcodes_criterion['알부민']['female_max_value']
            else:
                albumin_min=3.5
                albumin_max=5.3
            if data['liver_albumin'].iloc[i]<(albumin_min-1.0):
                data['albumin_per'].iloc[i]+=20
            elif data['liver_albumin'].iloc[i]>=(albumin_min-1.0) and data['liver_albumin'].iloc[i]<(albumin_min-0.5):
                data['albumin_per'].iloc[i]+=16
            elif data['liver_albumin'].iloc[i]>=(albumin_min-0.5) and data['liver_albumin'].iloc[i]<albumin_min:
                data['albumin_per'].iloc[i]+=12 
            elif data['liver_albumin'].iloc[i]>=albumin_min and data['liver_albumin'].iloc[i]<(albumin_min+0.5):
                data['albumin_per'].iloc[i]+=8
            elif data['liver_albumin'].iloc[i]>=(albumin_min+0.5) and data['liver_albumin'].iloc[i]<(albumin_max-1.0):
                data['albumin_per'].iloc[i]+=4
            elif data['liver_albumin'].iloc[i]>=(albumin_max-1.0) and data['liver_albumin'].iloc[i]<(albumin_min+1.0):
                data['albumin_per'].iloc[i]+=0
            elif data['liver_albumin'].iloc[i]>=(albumin_min+1.0) and data['liver_albumin'].iloc[i]<(albumin_max-0.5):
                data['albumin_per'].iloc[i]+=4
            elif data['liver_albumin'].iloc[i]>=(albumin_max-0.5) and data['liver_albumin'].iloc[i]<albumin_max:
                data['albumin_per'].iloc[i]+=8
            elif data['liver_albumin'].iloc[i]>=albumin_max and data['liver_albumin'].iloc[i]<(albumin_max+0.5):
                data['albumin_per'].iloc[i]+=12
            elif data['liver_albumin'].iloc[i]>=(albumin_max+0.5) and data['liver_albumin'].iloc[i]<(albumin_max+1.0):
                data['albumin_per'].iloc[i]+=16
            elif data['liver_albumin'].iloc[i]>=(albumin_max+1.0):
                data['albumin_per'].iloc[i]+=20
    # print(data['albumin_per'].value_counts())
        
    # 21) 요단백
    print('21) 요단백 확률 계산(20% 기준)')
    data["urine_protein_per"] = 0
    # 요단백 = 음성 = 정상
    # 그 외 1+ ~ 5+ 존재 -> 각각 1구간씩 계산 -> %부여
    for i in tqdm.tqdm(range(0,len(data))):
        if data['urine_protein'].iloc[i]==1:
            data['urine_protein_per'].iloc[i]+=4
        elif data['urine_protein'].iloc[i]==2:
            data['urine_protein_per'].iloc[i]+=8
        elif data['urine_protein'].iloc[i]==3:
            data['urine_protein_per'].iloc[i]+=12 
        elif data['urine_protein'].iloc[i]==4:
            data['urine_protein_per'].iloc[i]+=16
        elif data['urine_protein'].iloc[i]==5:        
            data['urine_protein_per'].iloc[i]+=20
    # print(data['urine_protein_per'].value_counts())

    # 22) 혈청 크레아티닌 
    print('22) 혈청 크레아티닌 확률 계산(20% 기준)')
    data["creatinine_per"] = 0
    for i in tqdm.tqdm(range(0,len(data))):
        if data['per1_gender'].iloc[i]==1:
            if '혈청크레아티닌' in keys:
                creatinine_min=bloodcodes_criterion['혈청크레아티닌']['male_min_value']
                creatinine_max=bloodcodes_criterion['혈청크레아티닌']['male_max_value']
            else:
                creatinine_min=0.6
                creatinine_max=1.5
            if data['creatinine'].iloc[i]<(creatinine_min-0.2):
                data['creatinine_per'].iloc[i]+=20
            elif data['creatinine'].iloc[i]>=(creatinine_min-0.2) and data['creatinine'].iloc[i]<(creatinine_min-0.1):
                data['creatinine_per'].iloc[i]+=16
            elif data['creatinine'].iloc[i]>=(creatinine_min-0.1) and data['creatinine'].iloc[i]<creatinine_min:
                data['creatinine_per'].iloc[i]+=12 
            elif data['creatinine'].iloc[i]>=creatinine_min and data['creatinine'].iloc[i]<(creatinine_min+0.1):
                data['creatinine_per'].iloc[i]+=8
            elif data['creatinine'].iloc[i]>=(creatinine_min+0.1) and data['creatinine'].iloc[i]<(creatinine_min+0.2):
                data['creatinine_per'].iloc[i]+=4
            elif data['creatinine'].iloc[i]>=(creatinine_min+0.2) and data['creatinine'].iloc[i]<(creatinine_max-0.2):
                data['creatinine_per'].iloc[i]+=0
            elif data['creatinine'].iloc[i]>=(creatinine_max-0.2) and data['creatinine'].iloc[i]<(creatinine_max-0.1):
                data['creatinine_per'].iloc[i]+=4
            elif data['creatinine'].iloc[i]>=(creatinine_max-0.1) and data['creatinine'].iloc[i]<creatinine_max:
                data['creatinine_per'].iloc[i]+=8
            elif data['creatinine'].iloc[i]>=creatinine_max and data['creatinine'].iloc[i]<(creatinine_max+0.1):
                data['creatinine_per'].iloc[i]+=12
            elif data['creatinine'].iloc[i]>=(creatinine_max+0.1) and data['creatinine'].iloc[i]<(creatinine_max+0.2):
                data['creatinine_per'].iloc[i]+=16
            elif data['creatinine'].iloc[i]>=(creatinine_max+0.2):
                data['creatinine_per'].iloc[i]+=20
        elif data['per1_gender'].iloc[i]==2:
            if '혈청크레아티닌' in keys:
                creatinine_min=bloodcodes_criterion['혈청크레아티닌']['female_min_value']
                creatinine_max=bloodcodes_criterion['혈청크레아티닌']['female_max_value']
            else:
                creatinine_min=0.6
                creatinine_max=1.5
            if data['creatinine'].iloc[i]<(creatinine_min-0.2):
                data['creatinine_per'].iloc[i]+=20
            elif data['creatinine'].iloc[i]>=(creatinine_min-0.2) and data['creatinine'].iloc[i]<(creatinine_min-0.1):
                data['creatinine_per'].iloc[i]+=16
            elif data['creatinine'].iloc[i]>=(creatinine_min-0.1) and data['creatinine'].iloc[i]<creatinine_min:
                data['creatinine_per'].iloc[i]+=12 
            elif data['creatinine'].iloc[i]>=creatinine_min and data['creatinine'].iloc[i]<(creatinine_min+0.1):
                data['creatinine_per'].iloc[i]+=8
            elif data['creatinine'].iloc[i]>=(creatinine_min+0.1) and data['creatinine'].iloc[i]<(creatinine_min+0.2):
                data['creatinine_per'].iloc[i]+=4
            elif data['creatinine'].iloc[i]>=(creatinine_min+0.2) and data['creatinine'].iloc[i]<(creatinine_max-0.2):
                data['creatinine_per'].iloc[i]+=0
            elif data['creatinine'].iloc[i]>=(creatinine_max-0.2) and data['creatinine'].iloc[i]<(creatinine_max-0.1):
                data['creatinine_per'].iloc[i]+=4
            elif data['creatinine'].iloc[i]>=(creatinine_max-0.1) and data['creatinine'].iloc[i]<creatinine_max:
                data['creatinine_per'].iloc[i]+=8
            elif data['creatinine'].iloc[i]>=creatinine_max and data['creatinine'].iloc[i]<(creatinine_max+0.1):
                data['creatinine_per'].iloc[i]+=12
            elif data['creatinine'].iloc[i]>=(creatinine_max+0.1) and data['creatinine'].iloc[i]<(creatinine_max+0.2):
                data['creatinine_per'].iloc[i]+=16
            elif data['creatinine'].iloc[i]>=(creatinine_max+0.2):
                data['creatinine_per'].iloc[i]+=20
    # print(data['creatinine_per'].value_counts())
    return data
    
def preprocess_hanshinData(data, bloodcodes_criterion):
    print('로드된 데이터 전처리를 시작합니다.')
    data = preprocess_munjin(data)
    data = preprocess_bloodcodes(data, bloodcodes_criterion)
    return data    

def preprocess_infinityData(data, bloodcodes_criterion):
    print('로드된 데이터 전처리를 시작합니다.')
    data = preprocess_bloodcodes(data, bloodcodes_criterion)
    return data    
