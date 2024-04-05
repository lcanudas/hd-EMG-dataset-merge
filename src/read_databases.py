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

print(sys.path)
print(os.environ.get('PYTHONPATH'))
print(os.environ.items)
config = yaml.safe_load(open('params.yaml'))

def read_database1(time,h, w, subj, type, task, intensity, trial):
    """_summary_

    Args:
        time (_type_): _description_
        h (_type_): _description_
        w (_type_): _description_
        subj (int): from 1 to 7
        type (string): can be hdEMG or fwEMG
        task (string): can be baseline, DFMVC, ISOK, ISOT, PFMVC, RAH, SINE
        intensity (int):  can be 30, 90, 300, 25, 50, None, 10. Note that  these intensities are not available for all tasks.
        trial (int): can be 1, 2, 3, None
    """

    path = config['data_path']['seeds']
    subj_string = 'S'+str(subj).zfill(2)
    if intensity != None:
        intensity_string = str(intensity)
    else:
        intensity_string = ''
    if trial != None:
        trial_string = '_'+str(trial)
    else:
        trial_string = ''
    db = pd.read_csv(path+'/'+type+'/'+subj_string+'/'+subj_string+'_'+task+intensity_string+trial_string+'.csv')
    img = db.loc[time,'MA1':'MN9'].values.reshape(9,14)
    resized = resize(img, (h,w), anti_aliasing=True)

    return resized

def read_database4(time,h, w, subj, type, task, intensity, trial):
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
    path = config['data_path']['dado4']
    fs = config['database_params']['dado4']['fs']
    n_channels = pd.read_csv(path+'nchannels.txt')
    
    type_dict = {'biceps':'bb', 'forearm':'fa', 'torque':'torque', 'triceps':'tb'}
    subj_string = 's'+str(subj)
    intensity_string = str(intensity)
    return n_channels

def read_database3(time, h, w, subj, exp, session, X, Y)
    """_summary_

    Args:
        time (int):
        h (int):
        w (int):
        subj (int): from 1 to 25
        exp (int): from 1 to ?
        session (int): from 1 to 3
        X (int): from 1 to 13
        Y (int): from 1 to 6
    """

    path = config['data_path']['seeds']

    subj_string = 'subj'+str(subj).zfill(2)
    exp = str(exp).zfill(2)
    session = 'Sess'+str(session)
    X = str(X).zfill(2)
    Y = str(Y).zfill(2)


    seeds = loadmat(path+'\ '+subj_string+'\ '+'detop_exp'+exp+'_'+subj_string+'_'+session+'_'+X+'_'+Y+'.mat')
    # as aspas em relação a: \

    emg = seeds[emg][:126,:]
    resized = plt.imshow(emg[:,time].reshape(h,w))
    # função tirada do 'funções_imagem.ipynb'
    # não sei se o 'time' está bem localizado

    return resized