def MSE(N, actual, predicted, j):
        tong = 0
        for i in range(j, N):
            tong += (actual[i] - predicted[i])**2
        
        result = tong / N
        return result

def RMSE(N, actual, predicted, j):
        tong = 0
        for i in range(j, N):
            tong += (actual[i] - predicted[i])**2
        
        result = (tong / N) ** (1/2)
        return result

def R2(N, actual, predicted, mean, j):
        tong1 = 0
        tong2 = 0

        for i in range(j, N):
            tong1 += (actual[i] - predicted[i])**2

        for i in range(j, N):
            tong2 += (actual[i] - mean[i])**2

        result = 1 - (tong1 / tong2)
        return result
       
def AdjustR2(R, n, k):
        return 1-(1-R) * ((n-1)/(n-k-1))

def MAE(N, actual, predict, j):
    tong = 0
    for i in range(j, N):
        tong += abs(actual[i] - predict[i]) 

    result = tong / N
    return result

def Precision(tp, fp):
    return tp/(tp+fp)

def Recall(tp, fn):
    return tp/(tp+fn)

def F1Score(P, R):
    return 2 * ((P*R) / (P+R))

def Accuracy(N, dung):  
    if N == 0:
        return 0
    return dung / N