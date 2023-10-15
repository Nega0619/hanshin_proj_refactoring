import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Database import PdfDatabase
from logger_AutoUpdater import logger

def make_pdfs_using3daysBeforeData(today=None):
    db = PdfDatabase(today)
    
    threeDays_before = db.today - relativedelta(days=3)
    
    threeDays_before = str(threeDays_before)[:10]
    patients = db.get_patients_threeDays_before(threeDays_before)
    if patients:
        for p in patients:
            data = db.get_patient_data(p)
            try:
                
                dir = f'/home/autocare/Autocare_Outputs/PDFs/{threeDays_before}'
                os.makedirs(dir, exist_ok=True)
                p = list(map(lambda x: str(x).replace(' ', '-'), p))
                # gender = '남' if int(p[6])==1 else '여'
                file_name = f"{p[0]}_{p[1]}_{p[2]}_{p[3]}_{p[4]}_{p[5]}_{p[6]}.pdf"
                save_file = os.path.join(dir, file_name)
                requests.post('http://localhost:9999/', json = data)
                # query = f'google-chrome --virtual-time-budget=50 --run-all-compositor-stages-before-draw --headless --print-to-pdf={save_file} file:///home/autocare/resources/src/result.html'
                query = f'google-chrome --virtual-time-budget=50 --headless --print-to-pdf={save_file} file:////home/autocare/resources/src/result.html'
                os.system(query)
                logger.info(f'{p[0]} {p[4]} pdf 생성 시도..')
            except Exception as e:
                logger.info(e)
    else :
        logger.info('\n', f'>> {str(threeDays_before)[:10]}일자 검진자가 없습니다. PDF를 생성하지 않습니다.', '\n', sep='')
  