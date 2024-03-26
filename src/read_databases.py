import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean

import scipy.io
import mat73

from scipy.io import loadmat

import yaml
import sys
import os




def read_database1(time,h, w, subj, type, task, intensity, trial,  pathcwd=''):
    """_summary_

    Args:
        time (_type_): _description_
        h (_type_): _description_
        w (_type_): _description_
        subj (int): _description_
        type (string): can be hdEMG or fwEMG
        task (string): can be baseline, DFMVC, ISOK, ISOT, PFMVC, RAH, SINE
        intensity (int):  can be 30, 90 300, 25, 50, None. Note that  these intensities are not available for all tasks.
        trial (int): can be 1, 2, 3, None
    """
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    path = config['data_path']['seeds']
    subj_string = 'S'+str(subj).zfill(2)
    if intensity != None:
        intnsity_string = str(intensity)
    else:
        intensity_string = ''
    if trial != None:
        trial_string = '_'+str(trial)
    else:
        trial_string = ''
    db = pd.read_csv(pathcwd+path+'/'+type+'/'+subj_string+'/'+subj_string+'_'+task+intensity_string+trial_string+'.csv')
    img = db.loc[time,'MA1':'MN9'].values.reshape(9,14)
    resized = resize(img, (h,w), anti_aliasing=True)

    return resized

def database3(time,h, w, subj, type, task, intensity, trial, pathcwd=''):
    """_summary_

    Args:
        time (_type_): _description_
        h (_type_): _description_
        w (_type_): _description_
        subj (_type_): _description_
        type (_type_): _description_
        task (_type_): _description_
        intensity (_type_): _description_
        trial (_type_): _description_
        pathcwd (str, optional): _description_. Defaults to ''.

    Returns:
        _type_: _description_
    """    
    
    plt.imshow(db2['emg_extensors'][t])


    return resized


def read_database4(time, h, w, subj, type, task, intensity, trial,  pathcwd=''):
    """_summary_

    Args:
        time (int): _description_
        h (int): _description_
        w (int): _description_
        subj (int): from 1 to 12
        type (string): can be biceps, forearm, torque, triceps
        task (string): can be e, f, p, s
        intensity (int): can be 10, 30, 50
        trial (_type_): None
    """   
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    path = config['data_path']['dado4']
    fs = config['database_params']['dado4']['fs']
    n_channels_file = pd.read_csv(pathcwd+path+'nchannels.txt', sep='\s+', index_col='subject')
    
    type_dict = {'biceps':'bb', 'forearm':'fa', 'torque':'torque', 'triceps':'tb'}
    nrows_dict = {'biceps':8, 'forearm':8, 'torque':1, 'triceps':6}
    subj_string = 's'+str(subj)
    intensity_string = str(intensity)

    n_channels = n_channels_file.loc[subj_string, type]

    file = open(pathcwd+path+subj_string+'/'+type+'/'+subj_string+'_'+task+intensity_string+'_'+type_dict[type]+'.bin',"rb")
    dado = np.fromfile(file, dtype='<d')
    if type != 'torque':
        dado = dado.reshape(n_channels,-1)
        dado = dado.T
        dado = dado[time,:].reshape(nrows_dict[type],-1)
        resized = resize(dado, (h,w), anti_aliasing=True)
    else:
        resized = dado[time]

    return resized

    
