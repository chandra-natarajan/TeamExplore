
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import wfdb

def  get_channels_ann(file_name, 
                     rec_array = ['p_signal'], 
                     rec_columns = [],
                     ann_array = ['sample', 'symbol']):
    
    record = wfdb.io.rdrecord(file_name)

    record_df = pd.DataFrame()    
    for item in rec_array: 
        record_df = pd.concat([record_df, pd.DataFrame(record.__dict__[item])])
    if rec_columns:
        record_df.columns = rec_columns
    else:
        record_df.columns = record.__dict__['sig_name']
    
    ann = wfdb.io.rdann(file_name, 'atr')
    
    ann_df = pd.DataFrame()
    for item in ann_array: 
        ann_df[item] = ann.__dict__[item]

    return record_df, ann_df

def download_db(db_name = 'mitdb'):
    wfdb.dl_database(db_name, '../'+db_name)    