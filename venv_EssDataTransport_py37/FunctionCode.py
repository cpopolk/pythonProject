import os
import psycopg2, openpyxl
import pandas as pd
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad # 암호화 블럭사이즈 조정 역할
from base64 import b64encode
import requests
from tkinter import *
import sys
import datetime
import json
from threading import Timer
import threading
import math

class receiveIndex():

  def __init__(self, host, name, user, password, url, id, pw,
                   hostInfor, nameInfor, userInfor, passwordInfor, urlInfor, idInfor, pwInfor,
                   Common_list, BMS_List_1, EMS_List_1, BMS_List_2, EMS_List_2,ETC_List_1, ETC_List_2,
                   Converted_Roop_Time, Converted_AutoMode_Status,
                   Transfer_Time, Response_Result):
   self.host, self.name, self.user, self.password, self.url, self.id, self.pw = host, name, user, password, url, id, pw

   self.hostInfor = hostInfor
   self.nameInfor = nameInfor
   self.userInfor = userInfor
   self.passwordInfor = passwordInfor
   self.urlInfor = urlInfor
   self.idInfor = idInfor
   self.pwInfor = pwInfor

   self.Common_list= Common_list
   self.BMS_List_1= BMS_List_1
   self.EMS_List_1= EMS_List_1
   self.BMS_List_2= BMS_List_2
   self.EMS_List_2= EMS_List_2
   self.ETC_List_1= ETC_List_1
   self.ETC_List_2= ETC_List_2

   self.Converted_Roop_Time = Converted_Roop_Time
   self.Converted_AutoMode_Status = Converted_AutoMode_Status

   self.Transfer_Time = Transfer_Time
   self.Response_Result = Response_Result

  def ManualDataload(self):
      try:
          self.ConnectDatabase()
          self.GetDatabaseData()
          self.MakeDataList()
      except:
          print('failed to load data')


  def ManualDataWebExport(self):
      try:
          self.secretcode()
          self.ToWebTransport()
      except:
          print('failed to export data')

  def Auto(self):
      self.ManualDataload()
      self.ManualDataWebExport()
    #  roop.start()

  def AutoOperate(self):
      print(type(self.Converted_AutoMode_Status.get()))

      if  self.Converted_AutoMode_Status.get() == 1 :
          self.Auto()
          roop = threading.Timer(int(self.Converted_Roop_Time.get()), self.AutoOperate)
          roop.daemon = True # start 전에 true로 설정해 놓으면 메인뜨레드 종료시 서브뜨레드 종료
          roop.start()
     #     print(type(self.Converted_Roop_Time.get())) # get()함수로 가지고 오는 data는 string type 임

      else:
         raise threading.excepthook
         #os.kill()
         print("쓰레드가 해제되었습니다.")

  def insertNewCondition(self):


   self.host = self.hostInfor.get()
   self.name = self.nameInfor.get()
   self.user = self.userInfor.get()
   self.password = self.passwordInfor.get()
   self.url = self.urlInfor.get()
   self.id = self.idInfor.get()
   self.pw = self.pwInfor.get()

   print(self.url)

  def ConnectDatabase(self):
      try:
          global  con
          con = psycopg2.connect(host=self.host, database=self.name, user=self.user, password=self.password)
          global cur
          cur = con.cursor()

      except:
       print('failed to connection')

  def GetDatabaseData(self):
      try:
           cur.execute(""" SELECT "Name","CurrentValue" FROM "DataPoints" """)
           global rows
           rows = cur.fetchall()
#           print(rows)  #list임
           DGPC_Database_df= pd.DataFrame(rows, columns=['DB_TAG','Value'])
#           print(DGPC_Database_df)
           pd.set_option('display.max_row', None, 'display.max_columns', None)

# in  사용법 , series를 list화 : 'AI: BAT 2 Usable State of Charge' in DGPC_Database_df['DB_TAG'].to_list()


          # global Export_Dataframe # 데이터가 모이는 매개변수
           if 'AI: BAT 2 Usable State of Charge' in DGPC_Database_df['DB_TAG'].to_list():

               Common_list_df = pd.DataFrame(self.Common_list)
               BMS_List_1_df = pd.DataFrame(self.BMS_List_1)
               EMS_List_1_df = pd.DataFrame(self.EMS_List_1)
               BMS_List_2_df = pd.DataFrame(self.BMS_List_2)
               EMS_List_2_df = pd.DataFrame(self.EMS_List_2)
               ETC_List_1_df = pd.DataFrame(self.ETC_List_1)
               ETC_List_2_df = pd.DataFrame(self.ETC_List_2)

               BMS_MergredDataframe_1= pd.merge(BMS_List_1_df, DGPC_Database_df,how='left', on='DB_TAG')
               BMS_MergredDataframe_1.iloc[0,4] = 'BMS'
               BMS_MergredDataframe_1.iloc[1,4] = '01'
               BMS_MergredDataframe_1.iloc[22,4] = 'END'
 #              print(BMS_MergredDataframe_1)

               BMS_MergredDataframe_2= pd.merge(BMS_List_2_df, DGPC_Database_df,how='left', on='DB_TAG')
               BMS_MergredDataframe_2.iloc[0,4] = 'BMS'
               BMS_MergredDataframe_2.iloc[1,4] = '02'
               BMS_MergredDataframe_2.iloc[22,4] = 'END'
#               print(BMS_MergredDataframe_2)

               EMS_MergredDataframe_1= pd.merge(EMS_List_1_df, DGPC_Database_df,how='left', on='DB_TAG')

               EMS_MergredDataframe_1.iloc[0,4] = 'EMS'
               EMS_MergredDataframe_1.iloc[1,4] = '01'
               EMS_MergredDataframe_1.iloc[26,4] = 'END'
#               print(EMS_MergredDataframe_1)


               EMS_MergredDataframe_2= pd.merge(EMS_List_2_df, DGPC_Database_df,how='left', on='DB_TAG')

               EMS_MergredDataframe_2.iloc[0,4] = 'EMS'
               EMS_MergredDataframe_2.iloc[1,4] = '02'
               EMS_MergredDataframe_2.iloc[26,4] = 'END'
#               print(EMS_MergredDataframe_2)
# 화씨 섭씨로 변환
               def FtoC(x) :
                   a = (x - 32) / 1.8
                   return a

               BMS_MergredDataframe = [BMS_MergredDataframe_1, BMS_MergredDataframe_2]

               for Dataframe_Temp_Convert in BMS_MergredDataframe:
                   Module_Max_Temperature = float(Dataframe_Temp_Convert.iloc[14, 4])
                   Module_Max_Temperature = FtoC(Module_Max_Temperature)
                   Dataframe_Temp_Convert.iloc[14, 4] = round(Module_Max_Temperature, 1)

                   Module_Min_Temperature = float(Dataframe_Temp_Convert.iloc[15, 4])
                   Module_Min_Temperature = FtoC(Module_Min_Temperature)
                   Dataframe_Temp_Convert.iloc[15, 4] = round(Module_Min_Temperature, 1)

# 선간전압에서 상전압으로 변환
               def LineVtoPhaseV(x) :
                   a = x / math.sqrt(3)
                   return  a

               EMS_MergredDataframe = [EMS_MergredDataframe_1, EMS_MergredDataframe_2]

               for Dataframe_Voltage_Convert in EMS_MergredDataframe:
                 for i in range(7,10):
                    AC_LineVoltage = float(Dataframe_Voltage_Convert.iloc[i, 4])
#                    print(AC_LineVoltage)
                    AC_PhaseVoltage = LineVtoPhaseV(AC_LineVoltage)
                    Dataframe_Voltage_Convert.iloc[i, 4] = round(AC_PhaseVoltage ,5)
#                    print(AC_PhaseVoltage)

# Value 자릿수 변환

               BMS_EMS_DigitCorrection = [BMS_MergredDataframe_1, BMS_MergredDataframe_2, EMS_MergredDataframe_1, EMS_MergredDataframe_2]

               for datablock in BMS_EMS_DigitCorrection :
                   i=0
                   for row in datablock['TYPE']:

                     if  row == 'DECIMAL(4,1)':
                         beforeTypechanged = round(float(datablock.iloc[i, 4]), 1)
                         print(beforeTypechanged)
                         datablock.iloc[i,4] = beforeTypechanged
                         i =i +1

                     elif row =='DECIMAL(4,3)':
                         beforeTypechanged = float(datablock.iloc[i, 4])
                         datablock.loc[i,'Value']= round(beforeTypechanged, 3)
                         i =i +1

                     elif row == 'DECIMAL(3,1)':
                         beforeTypechanged = float(datablock.iloc[i, 4])
                         a = round(beforeTypechanged, 1)
                         datablock.loc[i,'Value'] = a
                         i =i +1

                     elif row == 'DECIMAL(3,2)':
                         beforeTypechanged = float(datablock.iloc[i, 4])
                         a = round(beforeTypechanged, 2)
                         datablock.loc[i,'Value'] = a
                         i = i + 1
                     elif row == 'DECIMAL(5,1)':
                         beforeTypechanged = float(datablock.iloc[i, 4])
                         a = round(beforeTypechanged, 1)
                         datablock.loc[i,'Value'] = a
                         i =i +1
                     elif row == 'DECIMAL(6,1)':
                         beforeTypechanged = float(datablock.iloc[i, 4])
                         a = round(beforeTypechanged, 1)
                         datablock.loc[i,'Value'] = a
                         i =i +1
                     else :
                         beforeTypechanged = datablock.iloc[i, 4]
                         datablock.loc[i,'Value'] = beforeTypechanged
                         i = i + 1

#               print(BMS_MergredDataframe_1)
#               print(BMS_MergredDataframe_2)
#               print(EMS_MergredDataframe_1)
#               print(EMS_MergredDataframe_2)
#               print(ETC_List_1_df)
#               print(ETC_List_2_df)

               BMS_MergredDataframe_1['Value'].fillna('0', inplace=True)
               BMS_MergredDataframe_2['Value'].fillna('0', inplace=True)
               EMS_MergredDataframe_1['Value'].fillna('0', inplace=True)
               EMS_MergredDataframe_2['Value'].fillna('0', inplace=True)

               global Export_Dataframe
               Export_Dataframe = [BMS_MergredDataframe_1, BMS_MergredDataframe_2, EMS_MergredDataframe_1,EMS_MergredDataframe_2, ETC_List_1_df, ETC_List_2_df]

           else :
               Common_list_df = pd.DataFrame(self.Common_list)
               BMS_List_1_df = pd.DataFrame(self.BMS_List_1)
               EMS_List_1_df = pd.DataFrame(self.EMS_List_1)
               ETC_List_1_df = pd.DataFrame(self.ETC_List_1)

               BMS_MergredDataframe_1 = pd.merge(BMS_List_1_df, DGPC_Database_df, how='left', on='DB_TAG')
               BMS_MergredDataframe_1.iloc[0, 4] = 'BMS'
               BMS_MergredDataframe_1.iloc[1, 4] = '01'
               BMS_MergredDataframe_1.iloc[22, 4] = 'END'
               #               print(BMS_MergredDataframe_1)

               EMS_MergredDataframe_1 = pd.merge(EMS_List_1_df, DGPC_Database_df, how='left', on='DB_TAG')

               EMS_MergredDataframe_1.iloc[0, 4] = 'EMS'
               EMS_MergredDataframe_1.iloc[1, 4] = '01'
               EMS_MergredDataframe_1.iloc[26, 4] = 'END'
               #print(EMS_MergredDataframe_1)

# 화씨 섭씨로 변환
               def FtoC(x):
                   a = (x - 32) / 1.8
                   return a

               Module_Max_Temperature = float(BMS_MergredDataframe_1.iloc[14, 4])
               Module_Max_Temperature = FtoC(Module_Max_Temperature)
               BMS_MergredDataframe_1.iloc[14, 4] = round(Module_Max_Temperature, 5)

               Module_Min_Temperature = float(BMS_MergredDataframe_1.iloc[15, 4])
               Module_Min_Temperature = FtoC(Module_Min_Temperature)
               BMS_MergredDataframe_1.iloc[15, 4] = round(Module_Min_Temperature, 5)

# 선간전압에서 상전압으로 변환
               def LineVtoPhaseV(x):
                   a = x / math.sqrt(3)
                   return a

               for i in range(7, 10):
                   AC_LineVoltage = float(EMS_MergredDataframe_1.iloc[i, 4])
                   #print(AC_LineVoltage)
                   AC_PhaseVoltage = LineVtoPhaseV(AC_LineVoltage)
                   EMS_MergredDataframe_1.iloc[i, 4] = round(AC_PhaseVoltage, 5)
                   #print(AC_PhaseVoltage)

# Value 자릿수 변환
               BMS_EMS_DigitCorrection = [BMS_MergredDataframe_1,  EMS_MergredDataframe_1]

               for datablock in BMS_EMS_DigitCorrection:
                   i = 0
                   for row in datablock['TYPE']:

                       if row == 'DECIMAL(4,1)':
                           beforeTypechanged = datablock.iloc[i][4].astype(float)
                           a = round(beforeTypechanged, 1)
                           print(a)
                           datablock.iloc[i][4] = a
                           i = i + 1
                       elif row == 'DECIMAL(4,3)':
                           beforeTypechanged = datablock.iloc[i][4].astype(float)
                           a = round(beforeTypechanged, 3)
                           datablock.iloc[i][4] = a
                           i = i + 1

                       elif row == 'DECIMAL(3,1)':
                           beforeTypechanged = float(datablock.iloc[i][4])
                           a = round(beforeTypechanged, 1)
                           datablock.iloc[i][4] = a
                           i = i + 1

                       elif row == 'DECIMAL(3,2)':
                           beforeTypechanged = float(datablock.iloc[i][4])
                           a = round(beforeTypechanged, 2)
                           datablock.iloc[i][4] = a
                           i = i + 1
                       elif row == 'DECIMAL(5,1)':
                           beforeTypechanged = float(datablock.iloc[i][4])
                           a = round(beforeTypechanged, 1)
                           datablock.iloc[i][4] = a
                           i = i + 1
                       elif row == 'DECIMAL(6,1)':
                           beforeTypechanged = float(datablock.iloc[i][4])
                           a = round(beforeTypechanged, 1)
                           datablock.iloc[i][4] = a
                           i = i + 1
                       else:
                           beforeTypechanged = datablock.iloc[i][4]
                           datablock.iloc[i][4] = beforeTypechanged
                           i = i + 1

               BMS_MergredDataframe_1['Value'].fillna('0', inplace=True)
               EMS_MergredDataframe_1['Value'].fillna('0', inplace=True)
#               print(BMS_MergredDataframe_1)
#               print(EMS_MergredDataframe_1)
#               print(ETC_List_1_df)


               Export_Dataframe = [BMS_MergredDataframe_1, EMS_MergredDataframe_1, ETC_List_1_df]

           #           calibrated_DataType = pd.DataFrame(self.D_data_type.items(), columns=['k_tag', 'Datatype'])
           #           print(calibrated_DataType) 딕션어리를 데이터 프레임으로 만드는 방법
           cur.close()
           con.close()

      except:
          print('failed to get Data in database')

  def MakeDataList(self):
    try:
        _Now = str(datetime.datetime.now())
 #       print(_Now)
        #essTime = [now.year, now.month, now.day, now.hour, now.minute] 이렇게도 정보를 받을 수있만 0이 생략된 형태(참고)
        Day = _Now[0:10]
        Time = _Now[11:19]

        inputDay = "CAA=" + Day + "\n"
        inputTime = "CAB=" + Time +"\n"
        protocol = "CAC=" + "2" + "\n"
        conCount = "CAD=" + "0" + "\n"
        conSerial = "CAE=" + "0" + "\n"

        global  outputData
        outputData =  inputDay + inputTime + protocol + conCount + conSerial

        for Data_frame in Export_Dataframe:
           for Data_Frame_Index in range(len(Data_frame['KESCO_TAG'])) :
              outputData_Line = "{}={}".format(Data_frame.iloc[Data_Frame_Index,1],Data_frame.iloc[Data_Frame_Index,4])
              outputData = outputData + outputData_Line + '\n'

#        print(outputData)

    except:
        print('No DataList be created')

  def secretcode(self):
    try:
      data = bytes(outputData, encoding="utf-8")
#      print(type(data))
#      print(data)
      key = bytes(self.pw, encoding="utf-8")
#      print(key)
      cipher = AES.new(key, AES.MODE_CBC, key)
      ct_bytes = cipher.encrypt(pad(data, AES.block_size))
      ID = self.id
      ChangedId = bytes(ID, encoding="utf-8")
      #ID = b64encode(ChangedId).decode('utf-8')
      key = b64encode(key).decode('utf-8')
#      print(key)
      ct_bytes = b64encode(ct_bytes).decode('utf-8')
      global result
      result = {"id": ID, "data":ct_bytes}

#      print(result)
#      print(self.url)
    except:
        print('failed to AES' )

  def ToWebTransport(self):
    try:
      stored = outputData.replace("\n","")
      response = requests.post(url=self.url, data= result, timeout=(3,10))

      filePath = os.getcwd() #파일설치 폴더 경로만(파일명 제외)
#      print(type(filePath))

      if not os.path.exists("Data Log"):
       os.mkdir("Data Log")

      filename = str(datetime.date.today())
      Log_stored_path = "{}/Data Log/{}.txt".format (filePath, filename)
#      print(stored_path)

      with open(Log_stored_path, 'a') as file:
       file.write(response.text)
       file.write(stored)

# HMI에 표시
      self.Transfer_Time.insert(0,str(datetime.datetime.now()))
      self.Response_Result.insert(0, response.text)

    except:
      print('failed to Transport data' )






