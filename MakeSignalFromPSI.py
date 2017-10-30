# -*- coding: cp1251 -*-
import csv
import sys

# if __name__ == '__main__':

version = "0.0.1"

############################################### global variable declaration #########################################
SignalParameters = ""
#position in csv
SignalDescript = dict()


Uind = 2
Iind = 14
StartUhInd = 30
HarmonicsCnt = 49
StartIhInd = StartUhInd + HarmonicsCnt
StartPhiUhInd = StartIhInd + HarmonicsCnt
StartPhiIhInd = StartPhiUhInd + HarmonicsCnt
StartUihInd = StartPhiIhInd + HarmonicsCnt
StartIihInd = StartUihInd + HarmonicsCnt

VoltageNominal = 57.735
LineVoltageNominal = 100

CurrentNominal = 5


############################################## functions declaration ##################################################
def InitVoltageCsvInd(signalParam):
	'''
	InitVoltageCsvInd - automate initialization indexes in csv
	:param signalParam:
	:return:
	'''
	paramNames = ("�������","U���� �","U���� �","U���� �","U����� ���� �","U����� ���� �")
	startInd = Uind
	for name in paramNames:
		signalParam[name] = startInd
		startInd+=1

def InitCurrentCsvInd(signalParam):
	paramNames = ("I���� �","I���� �","I���� �","I����� ���� �","I����� ���� �","I����� ���� �")
	startInd = Iind
	for name in paramNames:
		signalParam[name] = startInd
		startInd+=1
	
		
def InitHarmonicsTemplate(signalParam,startInd,prefixName,startHarmNum,endHarmNum):
    for num in range(startHarmNum, endHarmNum + 1):
        partName = prefixName + str(num)
        signalParam[partName] = startInd
        startInd+=1


def InitUaUbUcHarmonicsCsvInd(signalParam):
    '''
    InitUaUbUcHarmonicsCsvInd - automate init indexes of Uh on phase A,B,C
    :param signalParam:
    :return:
    '''
    InitHarmonicsTemplate(signalParam, StartUhInd, "Uh", 2, 50)

def InitIaIbIcHarmonicsCsvInd(signalParam):
    '''
    InitIaIbIcHarmonicsCsvInd - automate init indexes of Ih on phase A,B,C
    :param signalParam:
    :return:
    '''
    InitHarmonicsTemplate(signalParam, StartIhInd, "Ih", 2, 50)

def InitPhiUaUbUcHarmonicsCsvInd(signalParam):
    InitHarmonicsTemplate(signalParam, StartPhiUhInd, "PhiUh", 2, 50)

def InitPhiIaIbIcHarmonicsCsvInd(signalParam):
    InitHarmonicsTemplate(signalParam, StartPhiIhInd, "PhiIh", 2, 50)

def InitUaUbUcInterHarmonicsCsvInd(signalParam):
    InitHarmonicsTemplate(signalParam, StartUihInd, "Uih", 1, 49)

def InitIaIbIcInterHarmonicsCsvInd(signalParam):
    InitHarmonicsTemplate(signalParam, StartIihInd, "Iih", 1, 49)

def InitSignalParamIndexes():
	global SignalDescript
	InitVoltageCsvInd(SignalDescript)
	InitCurrentCsvInd(SignalDescript)
	InitUaUbUcHarmonicsCsvInd(SignalDescript)
	InitIaIbIcHarmonicsCsvInd(SignalDescript)
	InitPhiUaUbUcHarmonicsCsvInd(SignalDescript)
	InitPhiIaIbIcHarmonicsCsvInd(SignalDescript)
	InitUaUbUcInterHarmonicsCsvInd(SignalDescript)
	InitIaIbIcInterHarmonicsCsvInd(SignalDescript)
	
######################################### part write to file ######################################
#maybe create template
#startSymb - ������� ����� ����������!!!
def WriteDataTemplate(fileToWrite,DefaultValue,WriteValue = True,startSymb=0,*args):
    '''
    args - list of strings with key names
    fileToWrite - open file descriptor
    :param args:
    :param fileToWrite:
    :return:
    '''
    global SignalDescript
    global SignalParameters
    for item in args:
        if item in SignalDescript.keys():
            val = SignalParameters[SignalDescript[item]]
            print(item[startSymb:]+'='+val,file = fileToWrite)
        else:
            print(item[startSymb:]+'='+str(DefaultValue) if WriteValue else item,file = fileToWrite)

def WriteHarmonicsTemplate(fileToWrite,HarmonicHeader,NameParam,startHarmNum,endHarmNum):
	global SignalDescript
	global SignalParameters
	print(HarmonicHeader,file = fileToWrite)
	for num in range(startHarmNum,endHarmNum+1):
		harmName = NameParam+str(num)
		val = SignalParameters[SignalDescript[harmName]]
		print(str(num)+'-�'+'='+str(val),file = fileToWrite)
	
			
def WriteSignalVltgHeader(fileToWrite):
    '''
    :param file:
    :return:
    '''
    global VoltageNominal
    global LineVoltageNominal
    Items = ("[���������� �������������]", "��� �����=��� ���������", "[����������]")
    WriteDataTemplate(fileToWrite,0,False,0,*Items)
    #"�������", "������ �������", "����������� �������"
    print("�������="+str(VoltageNominal),file = fileToWrite)
    print("������ �������=" + str(VoltageNominal), file=fileToWrite)
    print("����������� �������=" + str(LineVoltageNominal), file=fileToWrite)

def WriteThreePhaseVltgParam(fileToWrite):
    Items = ("U���� �","U���� �","U���� �","U����� ���� �","U����� ���� �","U����� ���� �")
    WriteDataTemplate(fileToWrite,0,True,1,*Items)

def WriteFrequencyParam(fileToWrite):
    Items = ("������� �������","�������")
    WriteDataTemplate(fileToWrite, 50,True,0, *Items)
	
def WriteVltgHarmonics(fileToWrite):
	Items = ("[��������� ���������� �� ���� �]","[��������� ���������� �� ���� B]","[��������� ���������� �� ���� C]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Uh",2,50)# �� ���������� ��� ���� ����������
	Items = ("[���� ������ �������� ���������� �� ���� �]","[���� ������ �������� ���������� �� ���� �]","[���� ������ �������� ���������� �� ���� �]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"PhiUh",2,50)
	Items = ("[�������������� ���������� �� ���� �]","[�������������� ���������� �� ���� �]","[�������������� ���������� �� ���� �]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Uih",1,49)

def WriteThreePhaseCurrentParam(fileToWrite):
	print("[���]",file=fileToWrite)
	print("�������="+str(CurrentNominal),file=fileToWrite)
	Items=("I���� �","I���� �","I���� �","I����� ���� �","I����� ���� �","I����� ���� �")
	WriteDataTemplate(fileToWrite,0,True,1,*Items)
	
def WriteCurrentHarmonics(fileToWrite):
	Items = ("[��������� ���� �� ���� �]","[��������� ���� �� ���� B]","[��������� ���� �� ���� C]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Ih",2,50)# �� ���������� ��� ���� ����������
	Items = ("[���� ������ �������� ���� �� ���� �]","[���� ������ �������� ���� �� ���� �]","[���� ������ �������� ���� �� ���� �]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"PhiIh",2,50)
	Items = ("[�������������� ���� �� ���� �]","[�������������� ���� �� ���� �]","[�������������� ���� �� ���� �]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Iih",1,49)


################################################## Programm body ####################################



#read csv file
with open(sys.argv[1], "r") as f:
    csvLines = csv.reader(f, delimiter=';')
    for line in csvLines:
        if line[0] == sys.argv[2]:
            SignalParameters = line

#init indexes
InitSignalParamIndexes()
for ind in range(0,len(SignalParameters)):
	SignalParameters[ind] = SignalParameters[ind].replace(",",".")

#Write File usa
with open(sys.argv[2] + '.usa', 'w') as outFile:
	WriteSignalVltgHeader(outFile)
	WriteThreePhaseVltgParam(outFile)
	WriteFrequencyParam(outFile)
	WriteVltgHarmonics(outFile)
	WriteThreePhaseCurrentParam(outFile)
	WriteCurrentHarmonics(outFile)
#print(SignalDescript)

#print(signalParameters)
