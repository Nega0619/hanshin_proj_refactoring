from HanshinTrainer import HanshinModelTrainerDBHandler, train_new_hanshinModel, remove_hanshinModels
from InfinityTrainer import train_new_infinityModel, remove_infinityModels
from HanshinPredictor import HanshinModelPredictorDBHandler, predict_new_hanshinModel
from datetime import datetime
from Database import reset_tabel
from logger_Initiator import logger
import sklearn.metrics._pairwise_distances_reduction._datasets_pair
import sklearn.metrics._pairwise_distances_reduction._middle_term_computer
import sklearn.ensemble._forest
import sklearn
import schedule
import warnings
warnings.filterwarnings("ignore")

def remove_all_modelfile():
    remove_hanshinModels()
    remove_infinityModels()
    
def reset():
    global inited
    inited = True

    logger.info('AutocareHCB 시스템을 초기화합니다.')
    remove_all_modelfile()
    
    reset_tabel()
    db = HanshinModelPredictorDBHandler(datetime(2022, 12, 31))
    db.reload_data()
    db.preprocess_DB(fill_null=False)
    
    db = HanshinModelTrainerDBHandler()
    
    logger.info("")
    logger.info("한신메디피아 결측치 대체값을 업데이트합니다.")
    db.update_candidateData()
    
    db.fill_null_data()
    
    train_new_hanshinModel()
    train_new_infinityModel()
    predict_new_hanshinModel()
    

if __name__=="__main__":
    global inited
    inited = False
    try:
        logger.info('19:00에 AutocareHCB 시스템을 초기화 합니다.')
        schedule.every().day.at('19:00').do(reset)
        while not inited:
            schedule.run_pending()
    except Exception as e:
        logger.exception(e)