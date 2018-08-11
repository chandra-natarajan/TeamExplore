import numpy as np
import random
import wfdb as wf
import pywt
from model import WindowPair

# This code is a terrible mess and will definitely need to be fixed later!

def main(train_records, test_records, wavelet_family = 'db1'):
    
    train_wps, test_wps = [], []
    ls = []
    for t in train_records:
        for wp in t.wps:
            train_wps.append(wp)
            ls.append(wp.length)
    for t in test_records:
        for wp in t.wps:
            test_wps.append(wp)
            ls.append(wp.length)
    lmin = np.min(ls)

    train_wps_new, test_wps_new = [], []
    for wp in train_wps:
        signal = np.empty((lmin, 2))
        signal[:,0] = random.sample(list(wp.signal[:,0]), lmin)
        signal[:,1] = random.sample(list(wp.signal[:,1]), lmin)
        #cA1, cD1 = pywt.dwt(signal[:,0], wavelet_family)
        #cA2, cD2 = pywt.dwt(signal[:,1], wavelet_family)
        #wp.dwt =  np.concatenate((cA1, cA2, cD1, cD2))
        #wp.dwt =  np.concatenate((cA1, cD1))
        cA2, cD2, cD1 = pywt.wavedec(signal[:,0], wavelet_family, level=2) 
        wp.dwt = np.concatenate((cA2, cD2, cD1))
        wp.signal = signal
        train_wps_new.append(wp)
    for wp in test_wps:
        signal = np.empty((lmin, 2))
        signal[:,0] = random.sample(list(wp.signal[:,0]), lmin)
        signal[:,1] = random.sample(list(wp.signal[:,1]), lmin)
        #cA1, cD1 = pywt.dwt(signal[:,0], wavelet_family)
        #cA2, cD2 = pywt.dwt(signal[:,1], wavelet_family)
        #wp.dwt =  np.concatenate((cA1, cA2, cD1, cD2))
        #wp.dwt =  np.concatenate((cA1, cD1))
        cA2, cD2, cD1 = pywt.wavedec(signal[:,0], wavelet_family, level=2) 
        wp.dwt = np.concatenate((cA2, cD2, cD1))
        wp.signal = signal
        test_wps_new.append(wp)
        
    return train_wps_new, test_wps_new

if __name__ == "__main__":
    main()