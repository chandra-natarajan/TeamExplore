
# coding: utf-8

# ## This file contains some functions for data sampling

# In[4]:

import numpy as np


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


# In[6]:

def rolling_window(signal, segmentation_pos, annotation_sym, FDW_width, FW_width, gap_width, delay):
    
    '''
    Draw samples from data with a rolling window. Data are 1D arrays.
    
    signal, segmentation_pos, annotation_sym: signal array, segmentation position array, and annotation symbols array.
    FDW_width, FD_width, gap_width: widths(in number of beats) of the feature derivation window, forecast window, and the gap in between.
    delay: distance(in number of beats) between two consequential FDWs.    
    '''
    DataSet, LabelSet = {}, {}
    
    nsample = 1
    FDW_start = segmentation_pos[1]
    FDW_end = segmentation_pos[1 + FDW_width]
    FW_start = segmentation_pos[1 + FDW_width + gap_width]
    FW_end = segmentation_pos[1 + FDW_width + gap_width + FW_width]
    while FW_end <= segmentation_pos[-1]:
        DataSet[nsample] = SignalData[key][FDW_start:FDW_end]
        LabelSet[nsample] = AnnSym[key[:3]][FW_start:FW_end]
        FDW_start = FDW_start + delay
        FDW_end = FDW_end + delay
        FW_start = FW_start + delay
        FW_end = FW_end + delay
        nsample = nsample + 1
        
    return DataSet, LabelSet


# In[7]:

def build_training_testing_dataset(signal, segmentation_pos, annotation_sym, 
                                   split_pos, FDW_width, FW_width, gap_width, delay):
    
    '''
    Draw samples from the dataset for time series forecasting.
    The datasets are dictionaries that contain multiple subjects.
    
    signal, segmentation_pos, annotation_sym: dictionaries that contain all the signal arrays, segmentation position arrays, and annotation symbols arrays.
    split_pos: the position used for splitting training and testing dataset.
    FDW_width, FD_width, gap_width: widths(in number of beats) of the feature derivation window, forecast window, and the gap in between.
    delay: distance(in number of beats) between two consequential FDWs.    
    '''  
    
    for key in signal.keys():
        
        segmentation = segmentation_pos[key[:3]]
        # find splitting position in segmentation
        split = 0
        while segmentation[split] <= split_pos:
            split = split + 1
        
        # build training dataset
        TrainData, TrainLabel = rolling_window(signal[key], segmentation[0:split], annotation_sym,
                                               FDW_width, FW_width, gap_width, delay)
        
        # build testing dataset
        TestData, TestLabel = rolling_window(signal[key], segmentation[split:], annotation_sym,
                                               FDW_width, FW_width, gap_width, delay)
            
        return TrainData, TrainLabel, TestData, TestLabel


# In[ ]:



