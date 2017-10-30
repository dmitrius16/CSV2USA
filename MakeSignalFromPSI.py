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
	paramNames = ("Частота","UФаза А","UФаза В","UФаза С","UСдвиг фазы В","UСдвиг фазы С")
	startInd = Uind
	for name in paramNames:
		signalParam[name] = startInd
		startInd+=1

def InitCurrentCsvInd(signalParam):
	paramNames = ("IФаза А","IФаза В","IФаза С","IСдвиг фазы А","IСдвиг фазы В","IСдвиг фазы С")
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
#startSymb - костыль нужно переделать!!!
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
		print(str(num)+'-я'+'='+str(val),file = fileToWrite)
	
			
def WriteSignalVltgHeader(fileToWrite):
    '''
    :param file:
    :return:
    '''
    global VoltageNominal
    global LineVoltageNominal
    Items = ("[Уникальный идентификатор]", "Тип файла=Все параметры", "[Напряжение]")
    WriteDataTemplate(fileToWrite,0,False,0,*Items)
    #"Наминал", "Фазный номинал", "Междуфазный номинал"
    print("Наминал="+str(VoltageNominal),file = fileToWrite)
    print("Фазный номинал=" + str(VoltageNominal), file=fileToWrite)
    print("Междуфазный номинал=" + str(LineVoltageNominal), file=fileToWrite)

def WriteThreePhaseVltgParam(fileToWrite):
    Items = ("UФаза А","UФаза В","UФаза С","UСдвиг фазы А","UСдвиг фазы В","UСдвиг фазы С")
    WriteDataTemplate(fileToWrite,0,True,1,*Items)

def WriteFrequencyParam(fileToWrite):
    Items = ("Номинал частоты","Частота")
    WriteDataTemplate(fileToWrite, 50,True,0, *Items)
	
def WriteVltgHarmonics(fileToWrite):
	Items = ("[Гармоники напряжения по фазе А]","[Гармоники напряжения по фазе B]","[Гармоники напряжения по фазе C]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Uh",2,50)# по гармоникам все фазы одинаковые
	Items = ("[Угол сдвига гармоник напряжения по фазе А]","[Угол сдвига гармоник напряжения по фазе В]","[Угол сдвига гармоник напряжения по фазе С]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"PhiUh",2,50)
	Items = ("[Интергармоники напряжения по фазе А]","[Интергармоники напряжения по фазе В]","[Интергармоники напряжения по фазе С]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Uih",1,49)

def WriteThreePhaseCurrentParam(fileToWrite):
	print("[Ток]",file=fileToWrite)
	print("Наминал="+str(CurrentNominal),file=fileToWrite)
	Items=("IФаза А","IФаза В","IФаза С","IСдвиг фазы А","IСдвиг фазы В","IСдвиг фазы С")
	WriteDataTemplate(fileToWrite,0,True,1,*Items)
	
def WriteCurrentHarmonics(fileToWrite):
	Items = ("[Гармоники тока по фазе А]","[Гармоники тока по фазе B]","[Гармоники тока по фазе C]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"Ih",2,50)# по гармоникам все фазы одинаковые
	Items = ("[Угол сдвига гармоник тока по фазе А]","[Угол сдвига гармоник тока по фазе В]","[Угол сдвига гармоник тока по фазе С]")
	for item in Items:
		WriteHarmonicsTemplate(fileToWrite,item,"PhiIh",2,50)
	Items = ("[Интергармоники тока по фазе А]","[Интергармоники тока по фазе В]","[Интергармоники тока по фазе С]")
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
