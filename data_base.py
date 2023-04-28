import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit

def get_DB():
    path = r"C:\Users\oded\OneDrive\Desktop\לימודים\עבודות להגשה\סייבר\key_strokes_db"
    trainDF = pd.read_csv(path + r"\train.csv")
    testDF = pd.read_csv(path + r"\test.csv")
    trainDF.head()

    trainDF1 = trainDF
    for i in range(1, 13):
        trainDF1['PPD-' + str(i)] = trainDF1['press-' + str(i)] - trainDF1['press-' + str(i - 1)]
        trainDF1['RPD-' + str(i)] = trainDF1['release-' + str(i)] - trainDF1['press-' + str(i - 1)]

    for i in range(13):
        trainDF1['HD-' + str(i)] = trainDF1['release-' + str(i)] - trainDF1['press-' + str(i)]

    testDF1 = testDF
    for i in range(1, 13):
        testDF1['PPD-' + str(i)] = testDF1['press-' + str(i)] - testDF1['press-' + str(i - 1)]
        testDF1['RPD-' + str(i)] = testDF1['release-' + str(i)] - testDF1['press-' + str(i - 1)]

    for i in range(13):
        testDF1['HD-' + str(i)] = testDF1['release-' + str(i)] - testDF1['press-' + str(i)]

    noOfUsers = 5
    trainDF2 = trainDF1[:noOfUsers * 8]

    drop_cols_PPD_analysis = ['HD-' + str(i) for i in range(13)] + ['RPD-' + str(i) for i in range(1, 13)] + [
        'release-' + str(i) for i in range(13)] + ['press-0']

    trainDF_PPD_analysis = trainDF2.drop(columns=drop_cols_PPD_analysis)
    trainDF_PPD_analysis['id'] = trainDF_PPD_analysis.index
    trainDF_PPD_analysis = pd.wide_to_long(trainDF_PPD_analysis, ['press-', 'PPD-'], i='id', j='key_no').sort_values(
        by=['user', 'id', 'key_no'])

    # Training Data
    drop_cols_HD_analysis = ['PPD-' + str(i) for i in range(1, 13)] + ['RPD-' + str(i) for i in range(1, 13)] + [
        'release-' + str(i) for i in range(13)]

    trainDF_HD_analysis = trainDF1.drop(columns=drop_cols_HD_analysis)
    trainDF_HD_analysis['id'] = trainDF_HD_analysis.index
    trainDF_HD_analysis = pd.wide_to_long(trainDF_HD_analysis, ['press-', 'HD-'], i='id', j='key_no').sort_values(
        by=['user', 'id', 'key_no'])

    drop_cols_PPD_analysis = ['HD-' + str(i) for i in range(13)] + ['RPD-' + str(i) for i in range(1, 13)] + [
        'release-' + str(i) for i in range(13)] + ['press-0']

    trainDF_PPD_analysis = trainDF1.drop(columns=drop_cols_PPD_analysis)
    trainDF_PPD_analysis['id'] = trainDF_PPD_analysis.index
    trainDF_PPD_analysis = pd.wide_to_long(trainDF_PPD_analysis, ['press-', 'PPD-'], i='id', j='key_no').sort_values(
        by=['user', 'id', 'key_no'])

    drop_cols_RPD_analysis = ['HD-' + str(i) for i in range(13)] + ['PPD-' + str(i) for i in range(1, 13)] + [
        'release-' + str(i) for i in range(13)] + ['press-0']

    trainDF_RPD_analysis = trainDF1.drop(columns=drop_cols_RPD_analysis)
    trainDF_RPD_analysis['id'] = trainDF_RPD_analysis.index
    trainDF_RPD_analysis = pd.wide_to_long(trainDF_RPD_analysis, ['press-', 'RPD-'], i='id', j='key_no').sort_values(
        by=['user', 'id', 'key_no'])

    # Test Data
    testDF_HD_analysis = testDF1.drop(columns=drop_cols_HD_analysis)
    testDF_HD_analysis['id'] = testDF_HD_analysis.index
    testDF_HD_analysis = pd.wide_to_long(testDF_HD_analysis, ['press-', 'HD-'], i='id', j='key_no').sort_values(
        by=['id', 'key_no'])

    testDF_PPD_analysis = testDF1.drop(columns=drop_cols_PPD_analysis)
    testDF_PPD_analysis['id'] = testDF_PPD_analysis.index
    testDF_PPD_analysis = pd.wide_to_long(testDF_PPD_analysis, ['press-', 'PPD-'], i='id', j='key_no').sort_values(
        by=['id', 'key_no'])

    testDF_RPD_analysis = testDF1.drop(columns=drop_cols_RPD_analysis)
    testDF_RPD_analysis['id'] = testDF_RPD_analysis.index
    testDF_RPD_analysis = pd.wide_to_long(testDF_RPD_analysis, ['press-', 'RPD-'], i='id', j='key_no').sort_values(
        by=['id', 'key_no'])

    # Join these individual tables together
    testDFCombined = testDF_HD_analysis.join(testDF_RPD_analysis.drop(columns=['press-']), rsuffix='RPD_').join(
        testDF_PPD_analysis.drop(columns=['press-']), rsuffix='PPD_')

    trainDFCombined = trainDF_HD_analysis.join(trainDF_RPD_analysis.drop(columns=['user', 'press-']), rsuffix='RPD_').join(
        trainDF_PPD_analysis.drop(columns=['user', 'press-']), rsuffix='PPD_')

    noOfBins = 10

    # Training Data
    labels = [i for i in range(noOfBins)]

    trainDFCombined['HDEnc'], HDBins = pd.qcut(trainDFCombined['HD-'], retbins=True, labels=labels, q=noOfBins)
    trainDFCombined['PPDEnc'], RPDBins = pd.qcut(trainDFCombined['PPD-'], retbins=True, labels=labels, q=noOfBins)
    trainDFCombined['RPDEnc'], PPDBins = pd.qcut(trainDFCombined['RPD-'], retbins=True, labels=labels, q=noOfBins)

    trainDFCombined['HDEnc'] = trainDFCombined['HDEnc'].astype(str).replace('nan', -1).astype(int)
    trainDFCombined['PPDEnc'] = trainDFCombined['PPDEnc'].astype(str).replace('nan', -1).astype(float)
    trainDFCombined['RPDEnc'] = trainDFCombined['RPDEnc'].astype(str).replace('nan', -1).astype(float)

    # Test Data
    labels = [i for i in range(noOfBins)]

    testDFCombined['HDEnc'] = pd.cut(testDFCombined['HD-'], labels=labels, bins=HDBins)
    testDFCombined['PPDEnc'] = pd.cut(testDFCombined['PPD-'], labels=labels, bins=RPDBins)
    testDFCombined['RPDEnc'] = pd.cut(testDFCombined['RPD-'], labels=labels, bins=PPDBins)

    testDFCombined['HDEnc'] = testDFCombined['HDEnc'].astype(str).replace('nan', -1).astype(float)
    testDFCombined['PPDEnc'] = testDFCombined['PPDEnc'].astype(str).replace('nan', -1).astype(float)
    testDFCombined['RPDEnc'] = testDFCombined['RPDEnc'].astype(str).replace('nan', -1).astype(float)

    # Lower limit values of bins created
    HDBins, RPDBins, PPDBins, 'No. of buckets: ' + str(len(HDBins) - 1)

    trainDF_HDTemp = trainDFCombined.reset_index().groupby(['user', 'id'])['HDEnc'].apply(np.array)
    trainDF_PPDTemp = trainDFCombined.reset_index().groupby(['user', 'id'])['PPDEnc'].apply(np.array)
    trainDF_RPDTemp = trainDFCombined.reset_index().groupby(['user', 'id'])['RPDEnc'].apply(np.array)

    trainDF_User_AllSampleProps = pd.DataFrame({'HD': trainDF_HDTemp, 'PPD': trainDF_PPDTemp, 'RPD': trainDF_RPDTemp})

    trainDF_User_AllSampleProps = pd.DataFrame(trainDF_User_AllSampleProps.HD.tolist(),
                                               index=trainDF_User_AllSampleProps.index).add_prefix('HD_').join(
        pd.DataFrame(trainDF_User_AllSampleProps.PPD.tolist(), index=trainDF_User_AllSampleProps.index).add_prefix('PPD_')
    ).join(
        pd.DataFrame(trainDF_User_AllSampleProps.RPD.tolist(), index=trainDF_User_AllSampleProps.index).add_prefix('RPD_')
    ).reset_index().set_index('user').drop(columns=['id'])

    return trainDF_User_AllSampleProps
