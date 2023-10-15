from InfinityTrainer import train_infinityModel_onSchedule
from HanshinTrainer import train_hanshinModel_onSchedule
from HanshinPredictor import predict_hanshinModel_onSchedule
from PdfMaker import make_pdfs_using3daysBeforeData
from datetime import datetime
from logger_AutoUpdater import logger
import sklearn.metrics._pairwise_distances_reduction._datasets_pair
import sklearn.metrics._pairwise_distances_reduction._middle_term_computer
import sklearn.ensemble._forest
import sklearn
import warnings
import schedule
from dateutil.relativedelta import relativedelta
warnings.filterwarnings("ignore")
days = 0
UPDATE_TIME = '01:00:00'

def update_daily():
    global days
    today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    if (today.month % 3 == 1 ) and (today.day == 4):
        train_hanshinModel_onSchedule()
        train_infinityModel_onSchedule()
    predict_hanshinModel_onSchedule()
    make_pdfs_using3daysBeforeData()
    logger.info(f'다음 업데이트 시각은 {UPDATE_TIME}입니다.')
    
# def test_update_daily():
#     global days
#     # today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
#     today = datetime(2023, 1, 4) + relativedelta(days=days)
#     # print('날짜 : ', today)
#     days += 1
#     if days==120:
#         print()
#     if (today.month % 3 == 1 ) and (today.day == 4):
#         train_hanshinModel_onSchedule(today)
#         train_infinityModel_onSchedule(today)
#     predict_hanshinModel_onSchedule(today)
#     make_pdfs_using3daysBeforeData(today)    

if __name__ == "__main__":
    logger.info(f'다음 업데이트 시각은 {UPDATE_TIME}입니다.')
    try:
        schedule.every().day.at(UPDATE_TIME).do(update_daily)
        # schedule.every(1).seconds.do(test_update_daily)
        while True:
            schedule.run_pending()
    except Exception as e:
        logger.exception(e)
    