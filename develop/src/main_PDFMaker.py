from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import json
from multiprocessing import Process
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import pandas as pd
from Database import PdfDatabase
import datetime
import requests
from logger_PDFMaker import logger

default_save_dir = '/home/autocare/Autocare_Outputs/PDFs'

ui_generatePDF = uic.loadUiType(r"/home/autocare/resources/src/ui/pdfGenerator.ui")[0]
html_file = 'file:////home/autocare/resources/src/result.html'

class WindowClass(QMainWindow, ui_generatePDF) :
    def __init__(self) :
        super().__init__()
        self.today = datetime.date.today()
        self.setupUi(self)
        self.database = PdfDatabase()
        self.btn_search.clicked.connect(self.search)
        self.btn_generatePDF.clicked.connect(self.generatePDF)
        self.btn_reset.clicked.connect(self.reset_edits)
        self.line_save_path.setText(os.path.join(default_save_dir, str(self.today)))
        self.patients=None
        self.progressBar.setValue(0) 
        self.generate_cnt = 0
        self.index_name = []
        self.reset_save_path = True
        
    def reset_edits(self,):
        if self.reset_save_path:
            self.line_save_path.setText(os.path.join(default_save_dir, str(self.today)))
        self.line_registkey.setText('')
        self.line_chatNo.setText('')
        self.line_bunNo.setText('')
        self.line_checkupDate.setText('')
        self.line_name.setText('')
        if self.index_name:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(len(self.index_name))
            self.tableWidget.setHorizontalHeaderLabels(self.index_name)
        self.progressBar.setValue(0) 
        self.patients = None
        
    def search(self):
        try:
            self.generate_cnt = 0
            self.progressBar.setValue(0) 
            self.index_name, self.patients = self.database.search_patients(registKey=self.line_registkey.text(), cht_no=self.line_chatNo.text(), bun_no=self.line_bunNo.text(), inspc_date=self.line_checkupDate.text(), name=self.line_name.text())
            if self.patients:
                self.draw_patientsTableWidget()
            else:
                logger.info('PDF를 만들 검진자가 없습니다. 검색한 요소의 데이터가 실제 DB에 존재하는지, 있다면 발병확률 예측이 되어있는지 확인하시길 바랍니다.')
                self.reset_save_path = False
                self.reset_edits()
                self.reset_save_path = True
        except Exception as e:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(len(self.index_name))
            self.tableWidget.setHorizontalHeaderLabels(self.index_name)
            logger.info("Error! ", e)
        
    def draw_patientsTableWidget(self,):
        logger.info(len(self.patients))
        start = datetime.datetime.now()
        
        # setting Table Widget
        self.tableWidget.setRowCount(len(self.patients))
        self.tableWidget.setColumnCount(len(self.index_name))
        self.tableWidget.setHorizontalHeaderLabels(self.index_name)
        
        # insert Data in Table Widget
        for row, p in enumerate(self.patients):
            for col in range(len(self.index_name)):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.patients[row][col])))
        end = datetime.datetime.now()
        logger.info(end-start)        
    
    def generatePDF(self):
        try:
            self.generate_cnt += 1
            if self.generate_cnt == 1:
                save_path = self.line_save_path.text()
                if not save_path.startswith('/home/autocare'):
                    self.generate_cnt = 0
                    QMessageBox.warning(self, 'warning', '폴더경로는 "/home/autocare"로 시작해야 합니다.')
                else:
                    os.makedirs(self.line_save_path.text(), exist_ok=True)
                    if self.patients:
                        for idx, p in enumerate(self.patients):
                            result = self.database.get_patient_data(p)
                            dir = self.line_save_path.text()
                            p = list(map(lambda x: str(x).replace(' ', '-'), p))
                            # name = p[4].replace(' ', '-')
                            file_name = f"{p[0]}_{p[1]}_{p[2]}_{p[3]}_{p[4]}_{p[5]}_{p[6]}.pdf"
                            save_file = os.path.join(dir, file_name)
                            requests.post('http://localhost:9999/', json = result)
                            # query = f'google-chrome --virtual-time-budget=50 --run-all-compositor-stages-before-draw --headless --logger.info-to-pdf={save_file} {html_file}'
                            query = f'google-chrome --virtual-time-budget=50 --headless --print-to-pdf={save_file} {html_file}'
                            os.system(query)
                            logger.info(f'{p[0]} {p[4]} pdf 생성 시도..')
                            self.progressBar.setValue(int((idx+1)/len(self.patients)*100))
                        self.progressBar.setValue(100)
                
        except FileNotFoundError:
            QMessageBox.warning(self, 'warning', '초기화 버튼을 클릭하거나, 저장경로를 입력하세요!')
        except Exception as e:
            QMessageBox.warning(self,'Error', '아래 에러 메시지에 Port가 보인다면, API서버가 켜져있는지 확인하세요.\n\n'+str(e))
            logger.info(e)    
    
if __name__ == "__main__" :
    try:
        gui = QApplication(sys.argv) 
        myWindow = WindowClass() 
        myWindow.show()
        gui.exec_()
    except Exception as e:
        logger.exception(e)