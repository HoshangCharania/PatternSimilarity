import json,urllib.request
import pandas as pd
from scipy.stats import zscore
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from scipy.fftpack import fft, ifft
from saxpy import sax
from saxpy.sax import sax_via_window
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity

def getStockClusters(stockSymbol):
    dF_Daily=runStockData(stockSymbol);
    combinedYearsDataFrame=getCombinedYearsDataFrame(dF_Daily)
    cosineMatrixDF=getCosineMatrixDF(combinedYearsDataFrame);
    #clusters=getClusters(cosineMatrixDF)
    #print(clusters)
    return cosineMatrixDF;


def runStockData(stockSymbol):
    data = urllib.request.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stockSymbol+"&outputsize=full&apikey=GZ78DWYK4UQOVQ83").read()
    output = json.loads(data)
    jsonOutput = output["Time Series (Daily)"]
    dF_Daily = pd.DataFrame.from_dict(jsonOutput, orient="index")
    dF_Daily.index = pd.to_datetime(dF_Daily.index)
    return dF_Daily;

def getCombinedYearsDataFrame(dF_Daily):
    dataframes = [];
    for x in range(1998, 2018):
        dataframes.append(dF_Daily[dF_Daily.index.year == x])
    min = 365;
    for x in range(0, len(dataframes)):
        if (len(dataframes[x]) < min):
            min = len(dataframes[x])
    combinedYearsDataFrame = pd.DataFrame();
    for x in range(0, len(dataframes)):
        dataframes[x] = dataframes[x][:min]
        # print(dataframes[x])
        dataframe = [float(x) for x in list(dataframes[x]["1. open"])]
        combinedYearsDataFrame[1998 + x] = dataframe
    for x in range(1998,2018):
        combinedYearsDataFrame[x]=zscore(combinedYearsDataFrame[x])
    return combinedYearsDataFrame

def getCosineMatrixDF(combinedYearsDataFrame):
    cosineMatrix=[]
    for x in range(1998,2018):
        cosineMatrix.append([]);
        for y in range(1998,2018):
            result = 1 - spatial.distance.cosine(combinedYearsDataFrame[x], combinedYearsDataFrame[y])
            cosineMatrix[x-1998].append(result);
    cosineMatrixDF = pd.DataFrame(cosineMatrix)
    for x in range(0, len(cosineMatrixDF)):
        cosineMatrixDF.rename(columns={x: 1998 + x},
                              inplace=True)
    tempList = list(cosineMatrixDF.columns)
    cosineMatrixDF["year"] = tempList
    cosineMatrixDF = cosineMatrixDF.set_index("year")
    return cosineMatrix;

def getClusters(cosineMatrixDF):
    cosineHashSet = set();
    threshold = 0.5;
    cosCluster = []
    for x in range(1998, 2018):
        cosCluster.append([]);
        currList = list(cosineMatrixDF[cosineMatrixDF[x] > 0.5].index)
        for i in range(0, len(currList)):
            if (currList[i] not in cosineHashSet):
                cosCluster[x - 1998].append(currList[i])
            cosineHashSet.add(x)
            cosineHashSet.add(currList[i])
    final_cosClusts = [x for x in cosCluster if x != []]
    data = []
    for x in range(0, len(final_cosClusts)):
        years = list(map(int, final_cosClusts[x]))
        currentData={'cluster': x ,'year': years};
        data.append(currentData);
    json_data = json.dumps(data)
    return json_data;

