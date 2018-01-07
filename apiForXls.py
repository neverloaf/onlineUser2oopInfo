#-*- coding:utf-8 -*-
import sys
import site
#引入电子表格插件
import  xlrd
import xlwt

#根据label name 查询索引集 mode ROW , COLUMN
def getValuesByName(dataSheet,indexLine,mode,needLabels):

    columIndexTuple = getIndexByName(dataSheet, indexLine,"ROW", needLabels)
    columIndex = columIndexTuple.get(OPERATOR_ID[0])
    # 获取行列个数
    if mode == "ROW":
        dataValue = dataSheet.row_values(columIndex)
    elif mode == "COLUMN":
        dataValue = dataSheet.col_values(columIndex)
    return dataValue[1:]

#根据label name 查询索引集 mode ROW , COLUMN
def getIndexByName(dataSheet,indexLine,mode,needLabels):
    numIndex = 0
    labelIndexArray = {}

    #获取行列个数
    if mode == "ROW":
        numIndex = dataSheet.nrows
        dataValue = dataSheet.row_values(indexLine)
    elif mode == "COLUMN":
        numIndex = dataSheet.ncols
        dataValue = dataSheet.col_values(indexLine)

    for needLable in needLabels:
        for index in range(0,numIndex):
            if dataValue[index] == needLable:
                    break
        labelIndexArray[needLable]=index

    print(needLabels)
    print(labelIndexArray)
    return labelIndexArray

#获取表格的sheet内容
def getSheetContent(fileName):
    data = xlrd.open_workbook(fileName)
    sheet_data = data.sheet_by_index(0)
    nrows = sheet_data.nrows
    ncols = sheet_data.ncols

    print("*******************基本信息*****************")
    print("数据总行数%d"%(nrows))
    print("数据总列数%d"%(ncols))
    print("********************************************")
    return sheet_data


#获取表格的指定字段
def getAssignedColumn(sheet_data,itemName):

    indexOfLabel = getIndexByName(sheet_data,0,"ROW",itemName)
    #获取改了内容
    columValue=sheet_data.col_values(indexOfLabel[0],1)
    return columValue;

#获取指定虚拟ID对应的行号
def getRowIndexByColumValue(sheet_data,indexOfColum,valueOfColum):
    dataValue = sheet_data.col_values(indexOfColum)
    maxIndex = sheet_data.nrows
    for i in range(0,maxIndex):
        if valueOfColum == dataValue[i]:
            break
    if (i != maxIndex):
        return i
    else:
        return -1

#根据指定行号，获取所需属性值
def getAssigedRowValueByIndex(sheet_data,rowIndex, mapOfNeedLabel):
    rowValues = mapOfNeedLabel.copy()
    dataValue = sheet_data.row_values(rowIndex)

    for itemName,itemRowIndex in mapOfNeedLabel.items():
        rowValues[itemName]=dataValue[itemRowIndex]
    print("获取的行值%s"%(str(rowValues)))
    return rowValues

#根据提供的所有虚拟ID所属列号，获取这些列的所有属性值
def getAssignedColumn(sheet_data,assignedIndexOfColum,valueOfAssigedColum,mapOfNeedLabel):
    mapOfQueryValue = {}
    count = 0
    #遍历所有的虚拟ID
    for operatorId in valueOfAssigedColum:
        count=count+1
        rowIndex = getRowIndexByColumValue(sheet_data,assignedIndexOfColum,operatorId)
        rowValues = getAssigedRowValueByIndex(sheet_data,rowIndex,mapOfNeedLabel)
        #进行写操作，待开发
        print(rowValues)
    print("共处理虚拟ID%d个"%(count))
    #return columValue;

if __name__ == "__main__":
    ON_LINE_INFO = "C:\\Users\\neverloaf\\PycharmProjects\\onlineUser2oopInfo\\resource\\onlineUser.xlsx"
    RAW_OOP_INFO = "C:\\Users\\neverloaf\\PycharmProjects\\onlineUser2oopInfo\\resource\\raw_oop_info.xls"
    BASIC_OOP_INFO = "C:\\Users\\neverloaf\\PycharmProjects\\onlineUser2oopInfo\\resource\\whole_oop_info.xlsx"
    NEEDED_ROW_VALUE = ["省分","本地网","主要行业","重点产品","细分产品（新）","客户分级","客户名称","客户编号","虚拟ID"]
    OPERATOR_ID = ["虚拟ID"]
    OPERATOR_ID_WORD = "虚拟ID"
    #获取已上线虚拟ID字段
    sheet_data = getSheetContent(ON_LINE_INFO)
    operatorID = getValuesByName(sheet_data,0,"COLUMN",OPERATOR_ID)
    print(operatorID)

    # 获取已整理商机的所需字段行索引
    sheet_data = getSheetContent(BASIC_OOP_INFO)
    mapOfNeedLabel = getIndexByName(sheet_data,0,"ROW",NEEDED_ROW_VALUE)
    # 获取对应字段索引
    indexOfOperatorId = mapOfNeedLabel[OPERATOR_ID_WORD]
    getAssignedColumn(sheet_data,indexOfOperatorId,operatorID,mapOfNeedLabel)
    #




