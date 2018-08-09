
# coding: utf-8

# ## This file contains some functions for data sampling

# In[1]:

import numpy as np
from sklearn.utils import shuffle


# In[5]:

def segmentation(annotation_pos):
    
    '''annotation_pos is a dictionary that contains all the annotation positions for all subjects.
    Return the starting positions of every beats, i.e. the middle point between the beat and the former beat.'''
    
    segmentation = {}
    
    for key in annotation_pos.keys():
        ann_pos = annotation_pos[key]
        # compute middle value between two neighboring annotation positions.
        segmentation[key] = ((np.append(ann_pos, 0) + np.insert(ann_pos, 0, 0)) / 2.0)[:-1].astype(np.int64)
        segmentation[key][0] = 0

    return segmentation


# In[3]:

def train_test_split(signal, test_ratio):
    '''
    Split training and testing dataset according to the test_train ratio.
    '''
    SignalTrain, SignalTest = {}, {}
    n_test = int(len(signal) * test_ratio)
    keys = shuffle(list(signal.keys()))
    for n in range(n_test):
        SignalTest[keys[n]] = signal[keys[n]]
    for n in range(n_test, len(signal)):
        SignalTrain[keys[n]] = signal[keys[n]]
    return SignalTrain, SignalTest       


# In[5]:

def rolling_window(signal, segmentation_pos, annotation_sym, FDW_width, FW_width, gap_width, delay):
    
    '''
    Draw samples from the dataset for time series forecasting.
    The datasets are dictionaries that contain multiple subjects.
    
    signal, segmentation_pos, annotation_sym: dictionaries that contain all the signal arrays, 
    segmentation position arrays, and annotation symbols arrays.
    FDW_width, FD_width, gap_width: widths(in number of beats) of the feature derivation window, 
    forecast window, and the gap in between.
    delay: distance(in number of beats) between two consequential FDWs.    
    '''  
    
    Dataset, Labelset=  {}, {}
     
    nsample = 0
    for key in signal.keys():
        
        segmentation = segmentation_pos[key[:3]]
            
        # build dataset 
            # initialize window positions  
        FDW_start = 1
        FDW_end = FDW_start + FDW_width
        FW_start = FDW_start + FDW_width + gap_width
        FW_end = FDW_start + FDW_width + gap_width + FW_width
            # draw samples while moving windows
        while FW_end < len(segmentation):
            data = np.append(signal[key][segmentation[FDW_start]:segmentation[FDW_end]], 
                             int(key[:3])) # add patient information to the array
            label = AnnSym[key[:3]][FW_start:FW_end]          
            # add sample to dataset
            Dataset[nsample], Labelset[nsample] = data, label
            # move the window
            FDW_start = FDW_start + delay
            FDW_end = FDW_end + delay
            FW_start = FW_start + delay
            FW_end = FW_end + delay  
            nsample = nsample + 1
    
    return Dataset, Labelset


# In[ ]:

def split_dataset_by_patient(X, y, ratio):
    '''
    Split X and y to parts by patients. The last column of X is patient information.
    ratio is a list contains the ratio of each part. sum(ratio) <= 1.
    '''
    patients = shuffle(list(set(X[:, -1])), random_state = 0)
    k = len(ratio) # split to k part
    patients = shuffle(list(set(X[:, -1])), random_state = 0)
        
    # create splitted patients and count sample numbers in each splitted  parts.
    patient_split, count_part = {}, []
    start = 0
    for part in range(k):
        if part == k - 1:
            end = len(patients)
        else:
            end = start + int(len(patients) * ratio[part])
        patient_split[part] = patients[start : end]
        start = end
        # count numbers of samples in each part
        count = 0
        for sample in range(X.shape[0]):
            if X[sample, -1] in patient_split[part]:
                count = count + 1
        count_part = count_part + [count]

         
    # split samples according to patient_split
    X_split, y_split = {}, {}
    for part in range(k):
        X_split[part] = np.zeros((count_part[part], X.shape[1]))
        y_split[part] = np.zeros(count_part[part])
        
    count = np.zeros((k,), dtype = int)
    for sample in range(X.shape[0]):
        for part in range(k):
            if X[sample, -1] in patient_split[part]:
                X_split[part][count[part], :] = X[sample, :]
                y_split[part][count[part]] = y[sample]
                count[part] = count[part] + 1
                break
                    
    return X_split, y_split

