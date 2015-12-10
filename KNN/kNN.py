# -*- coding: cp936 -*-
# 1��Լ����վ
from numpy import *
import operator
from os import listdir

#�������ݼ�
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

#��һ��kNN������  inX-�������� dataSet-��������  labels-��ǩ k-�ڽ���k������
def classify0(inX,dataSet, labels, k):
    #�������
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1))- dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances **0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    #ѡ�������С��k����
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    #����
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]


# ���ı���¼��ת��numPy�Ľ�������
def file2matrix(filename):
    #���ļ����õ��ļ�����
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    #�������ص�numPy����
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index =0
    #�����ļ����ݵ��б�
    for line in arrayOLines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMat[index,:] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
        index += 1
    return returnMat, classLabelVector

#��һ������ֵ
def autoNorm(dataSet):
    minVals = dataSet.min(0);
    maxVals = dataSet.max(0);
    ranges = maxVals - minVals;
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals


#���Դ���
def datingClassTest():
    hoRatio = 0.10    #��������ռ�İٷֱ�
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print 'the classifier came back with: %d, the real answer is: %d' %(classifierResult, datingLabels[i])
        if(classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f " % (errorCount/float(numTestVecs))
    

#����ĳ�˵���Ϣ����ó��ԶԷ�ϲ���̶ȵ�Ԥ��ֵ
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals)/ranges, normMat, datingLabels,3)
    print 'You will probably like this person: ', resultList[classifierResult - 1]
    

# 2����дʶ��ϵͳ
#��һ��32*32�Ķ�����ͼ�����ת����1*1024������

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect


#��дʶ��ϵͳ���Դ���
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')   #��ȡĿ¼����
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]              #�ָ�õ���ǩ  ���ļ��������õ���������
        fileStr = fileNameStr.split('.')[0]
        classStr = int(fileStr.split('_')[0])
        hwLabels.append(classStr)                 #����������ǩ
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print 'the classifier came back with: %d, the real answer is: %d' % (classifierResult, classStr)
        if(classifierResult != classStr): errorCount += 1.0
    print "\nthe total numbers of errors is : %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))



datingClassTest();



