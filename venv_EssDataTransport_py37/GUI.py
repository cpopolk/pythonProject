from tkinter import *
import TagName
from FunctionCode import *
import pandas as pd
#import schedule
import time
import sys
#import threading
#from btnAuto import *
#파일이름 넣어줘야 클래스 인스턴스됨

_root = Tk() # Tkinter Tool 사용을 root에 선언함

class Gui():
 def __init__(self,root): # _root 즉 tkinter의 인스턴스를 새로 만든 GUI Class 변수 root에 넣음
  self.root = root
  self.root.title("ESS 안전 정보 전송 시스템")
  self.root.geometry("760x500")
#  self.root.option_add("*Font","10")

 #이름 Lable
  l0= Label(root, text = " 구 분 ")
  l0.grid(row=0, column=1, sticky=N+E+W+S, ipadx=2, pady=2)
  l1= Label(root, text = " Database Host :")
  l1.grid(row=1, column=1, sticky=E, padx=2, pady=2)
  l2= Label(root, text = " Database Name :")
  l2.grid(row=2, column=1, sticky=E, padx=2, pady=2)
  l3= Label(root, text = " User :")
  l3.grid(row=3, column=1, sticky=E, padx=2, pady=2)
  l4= Label(root, text = " Password :")
  l4.grid(row=4, column=1, sticky=E, ipadx=2, pady=2)
  l5= Label(root, text = " ")
  l5.grid(row=5, column=1, sticky=E, ipadx=2)
  l6= Label(root, text = " URL주소 :")
  l6.grid(row=6, column=1, sticky=E, ipadx=2, pady=2)
  l7= Label(root, text = " ID(고유번호) :")
  l7.grid(row=7, column=1, sticky=E, ipadx=2, pady=2)
  l8= Label(root, text = " Password :")
  l8.grid(row=8, column=1, sticky=E, ipadx=2, pady=2)
  l9 = Label(root, text= "기 능")
  l9.grid(row=0, column=4, sticky=S+W, ipadx=2, pady=1)
  l10= Label(root, text = "서버 응답 결과 :")
  l10.grid(row=14, column=4, sticky=S+W, ipadx=2, pady=1)
  l11= Label(root, text = "반복 전송 실행 :")
  l11.grid(row=7, column=4, sticky=W)
  l12= Label(root, text = "반복 전송 주기 :\n  (단위:sec)")
  l12.grid(row=8, column=4, sticky=W)
  l13= Label(root, text = "    ")
  l13.grid(row=0, column=3)
  l14= Label(root, text = "    ")
  l14.grid(row=13, column=3)
  l15= Label(root, text = " 전송된 시간  :")
  l15.grid(row=14, column=1,sticky=E)

#l10= Label(root, text = "전송 데이터 Tag")
#l10.grid(row=9, column=1, sticky=N+E+W+S, ipadx=2, pady=2)

#Database Host
  hostInfor = StringVar()
  hostInfor.set("localhost")
  hostInfor = Entry(root, width=30, textvariable=hostInfor)
  hostInfor.grid(row=1, column=2, sticky=N+E+W+S, pady=0)

#Database Name
  nameInfor = StringVar()
  nameInfor.set("PlantController")
  nameInfor = Entry(root, width=30, textvariable=nameInfor)
  nameInfor.grid(row=2, column=2, sticky=N+E+W+S, pady=0)

#Database User Name
  userInfor=StringVar()
  userInfor.set("PlantControllerUser")
  userInfor = Entry(root, width=30, textvariable=userInfor)
  userInfor.grid(row=3, column=2, sticky=N+E+W+S, pady=0)

#Database password
  passwordInfor=StringVar()
  passwordInfor.set("pcUser")
  passwordInfor = Entry(root, width=30, textvariable=str(passwordInfor))
  passwordInfor.grid(row=4, column=2, sticky=N+E+W+S, pady=0)

#URL 주소입력
  urlInfor=StringVar()
  urlInfor.set('http://safe.kesco.or.kr/ess/datauploadtestV2.do')
  urlInfor = Entry(root, width=38, textvariable=urlInfor)
  urlInfor.grid(row=6, column=2, sticky=N+E+W+S, pady=0)

#ID 입력
  idInfor = StringVar()
#  idInfor.set("6505_016220_N_PV10R038864")# 삼척
#  idInfor.set("8100_028512_N_PV10S5477") #참새
#  idInfor.set("8100_028504_N_PV10S5478") #고니
#  idInfor.set("8100_028511_N_PV10S5476") #까치
  idInfor.set("3500_048428_N_PV15R033876") # 대한메탈본사 2Q4ZRFPCXTIE9AMR


  idInfor = Entry(root, width=30, textvariable=idInfor)
  idInfor.grid(row=7, column=2, sticky=N+E+W+S, pady=0)

#PW 입력
  pwInfor = StringVar()
#  pwInfor.set("DRTB0X6QBAJURFKP") 삼척
#  pwInfor.set("GHYIC0B9VG1C5SEJ") #참새
#  pwInfor.set("G0K8OQE928EKGMZ8") #고니
#  pwInfor.set("FPF7O8NHRELDAZQ1") #까치
  pwInfor.set("2Q4ZRFPCXTIE9AMR")  # 대한메탈본사


  pwInfor = Entry(root, width=30, textvariable=pwInfor)
  pwInfor.grid(row=8, column=2, sticky=N+E+W+S, pady=0)

# 주기 시간 입력
  Roop_Time = IntVar()
  Roop_Time.set(10)
  Roop_Time = Entry(root, width=5, textvariable=Roop_Time)
  Roop_Time.place(x=510, y=200)
#  Roop_Time.grid(row=12, column=4, sticky=W, padx=7)
  #print(type(timeInfor))


#데이터를 받아서 Transter list에 넣어줌
  Common_list = TagName.TagList.Kesco_Common_list
#  print(Common_list)
  BMS_List_1 = TagName.TagList.Kesco_BMS_list_1
  EMS_List_1 = TagName.TagList.Kesco_EMS_list_1
  BMS_List_2 = TagName.TagList.Kesco_BMS_list_2
  EMS_List_2 = TagName.TagList.Kesco_EMS_list_2
  ETC_List_1 = TagName.TagList.Kesco_ETC_list_1
  ETC_List_2 = TagName.TagList.Kesco_ETC_list_2



#  print(EMS_List)
#  print(ETC_List)
#  for x, y in enumerate(orin):
#   transferDataList.insert(x+1, y)

  # Transfer Listbox 생성
  Transfer_Time = Listbox(root)  # selectmode ="extended", height=22)
  Transfer_Time.grid(row=15, column=2, sticky=N + E + W + S, rowspan=3)

# checkedData_list listbox 생성
  Response_Result = Listbox(root)  # selectmode ="extended", height=22)
  Response_Result.grid(row=15, column=4, sticky=N+E+W+S, rowspan=10, ipadx=100)

  host = hostInfor.get()
  name = nameInfor.get()
  user = userInfor.get()
  password = passwordInfor.get()
  url = urlInfor.get() # 처음부터 끝까지 입력값을 가져온다
  id = idInfor.get()
  pw = pwInfor.get()

  # 반복주기 값 입력
  Converted_Roop_Time = Roop_Time
  # 반복주기 적용 Check Box
  _on = IntVar()
  Converted_AutoMode_Status = _on

  # 사전에 class를 인스턴스화 시켜 변수를 넘겨 줌
  instance1 = receiveIndex(host, name, user, password, url, id, pw,
                           hostInfor, nameInfor, userInfor, passwordInfor, urlInfor, idInfor, pwInfor,
                           Common_list, BMS_List_1, EMS_List_1, BMS_List_2, EMS_List_2, ETC_List_1, ETC_List_2,
                           Converted_Roop_Time, Converted_AutoMode_Status, Transfer_Time, Response_Result)

 # btn_Term_change = Button(root, text='연결정보변경', command = lambda : insertNewCondition(hostInfor,nameInfor,userInfor,passwordInfor,urlInfor,idInfor,pwInfor))
  btn_Term_change = Button(root, text='연결정보변경',command=instance1.insertNewCondition)
  btn_Term_change.place(x=290, y=237)
#  btn_Term_change.grid(row=2, column=5, sticky=N+W, ipadx=6)

  btn1 = Button(root, text ='     Data load     ', command=instance1.ManualDataload)
  btn1.place(x=470, y=50)
#  btn1.grid(row=5, column=5, sticky= W, ipadx=6)
#btn1 = Button(root, text ='입력', command=lambda: basicInfor(uA))
# inputInfor() 가로 치면 한번 수행, ()없으면 버튼 누를때마다

  btn2 = Button(root, text ='Data Web Export', command=instance1.ManualDataWebExport)
  btn2.place(x=470, y=100)
#  btn2.grid(row=7, column=5, sticky= W, ipadx=6)

  btn_AutoFC= Checkbutton(root, var=_on, command=instance1.AutoOperate)
  btn_AutoFC.place(x=510, y=170)
  '''
  btn_AutoFC= Checkbutton(root, var=_on, command=instance1.AutoMode)
  btn_AutoFC.grid(row=9, column=5, sticky= W)'''

  root.mainloop()

mygui = Gui(_root)  # Tkinter Tool의 세부 모양을 기존 Class에서 불러옴

