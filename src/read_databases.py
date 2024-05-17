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



def read_database1(time, h, w, subj, type, task, intensity, trial, exp, session):
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
        exp: None
        session: None
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

def read_database3(dado_orig, time, h, w, subj, type, task, intensity, trial, session, pathcwd=''):
    """_summary_

    Args:
        time (int):
        h (int):
        w (int):
        subj (int): from 1 to 25
        type: None
        task (int): from 1 to 13
        intensity: None
        trial (int): from 1 to 6
        exp (int): from 1 to ?
        session (int): from 1 to 3
    
    """

    emg = dado_orig['emg'][:126,:].T
    emg = emg[time,:].reshape(9,-1)
    resized = resize(emg, (h,w), anti_aliasing=True)

    return resized


def read_database4(dado_orig, time, h, w, subj, type, task, intensity, trial, session, pathcwd=''):
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
        exp: None
        session: None
    """   
    
    nrows_dict = {'biceps':8, 'forearm':6, 'torque':1, 'triceps':8}
    if type != 'torque':
        dado = dado_orig[time,:].reshape(nrows_dict[type],-1)
        resized = resize(dado, (h,w), anti_aliasing=True)
    else:
        resized = dado_orig[time]

    return resized

def get_database3(subj, type, task, intensity, trial, session,  pathcwd=''):
    
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    path = config['data_path']['dado3']
    fs = config['database_params']['dado3']['fs']        
    
    subj_string = 'subj'+str(subj).zfill(2)
    session_string = 'Sess'+str(session)

    dado = loadmat(pathcwd+path+subj_string+'/'+'detop_exp01_'+subj_string+'_'+session_string+'_'+str(task).zfill(2)+'_'+str(trial).zfill(2)+'.mat')
    length = len(dado['emg'].T)
    
    return length, dado

def get_database4(subj, type, task, intensity, trial,  session=None, pathcwd=''):

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
    dado = dado[:int(len(dado)//n_channels*n_channels)]
    file.close()
    if type != 'torque':
        dado = dado.reshape(n_channels,-1)
        dado = dado.T
        length = len(dado)
    else:
        length = len(dado)

    return length, dado

def include_metadata(dado, pathcwd, database_id, **kwargs):
    import os
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    
    path = config['data_path']['dado'+str(database_id)]
    subject = kwargs['subj']
    subj_string = 'subj'+str(kwargs['subj']).zfill(2)
    dado['database_id'] = database_id
    dado['database_id'] = dado['database_id'].astype('int8')
    dado['n_dim1'] = kwargs['h'] if 'h' in kwargs.keys() else np.nan
    dado['n_dim1'] = dado['n_dim1'].astype('category')
    dado['n_dim2'] = kwargs['w'] if 'w' in kwargs.keys() else np.nan
    dado['n_dim2'] = dado['n_dim2'].astype('category')
    dado['subject'] = kwargs['subj'] if 'subj' in kwargs.keys() else np.nan
    dado['subject'] = dado['subject'].astype('category')
    segment = kwargs['segment'] if 'segment' in kwargs.keys() else np.nan
    dado['segment'] = segment
    dado['segment'] = dado['segment'].astype('category')
    dado['trial'] = kwargs['trial'] if 'trial' in kwargs.keys() else np.nan
    dado['trial'] = dado['trial'].astype('int8')
    dado['task'] = kwargs['task'] if 'task' in kwargs.keys() else np.nan
    dado['task'] = dado['task'].astype('category')
    dado['intensity'] = kwargs['intensity'] if 'intensity' in kwargs.keys() else 0
    dado['intensity'] = dado['intensity'].astype('int8')
    dado['speed'] = kwargs['speed'] if 'speed' in kwargs.keys() else ''
    dado['speed'] = dado['speed'].astype('category')
    dado['session'] = kwargs['session'] if 'session' in kwargs.keys() else 0
    dado['session'] = dado['session'].astype('category')
    dado['date'] = kwargs['date'] if 'date' in kwargs.keys() else np.nan
    dado['date'] = dado['date'].astype('category')
    dado['frequency_sample (Hz)'] = kwargs['fs'] if 'fs' in kwargs.keys() else np.nan
    dado['frequency_sample (Hz)'] = dado['frequency_sample (Hz)'].astype('category')
    dado['original electrode distance (mm)'] = config['database_params']['dado'+str(database_id)]['elec_distance']
    dado['original electrode distance (mm)'] = dado['original electrode distance (mm)'].astype('int64')
    dado['original electrode diameter (mm)'] = config['database_params']['dado'+str(database_id)]['elec_diameter']
    dado['original electrode diameter (mm)'] = dado['original electrode diameter (mm)'].astype('category')
    orig_ndim1 = config['database_params'][f'dado{database_id}'][f'nrows_{kwargs["segment"]}']
    dado['original_n_dim1'] = orig_ndim1
    dado['original_n_dim1'] = dado['original_n_dim1'].astype('category')
    if f'ncolumns_{kwargs["segment"]}' in config['database_params'][f'dado{database_id}'].keys():
        orig_ndim2 = config['database_params'][f'dado{database_id}'][f'ncolumns_{kwargs["segment"]}']        
        dado['original_n_dim2'] = orig_ndim2
    else:
        nchannels_table = pd.read_csv(pathcwd+path+'nchannels.txt', sep='\s+')
        subs = 's'+str(subject)
        nchannels = nchannels_table.query(f'subject==@subs')[kwargs["segment"]].values[0]
        orig_ndim2 = int(nchannels//orig_ndim1)
        dado['original_n_dim2'] = orig_ndim2
    dado['original_n_dim2'] = dado['original_n_dim2'].astype('category')
    dado['electrode distance (mm)'] = config['database_params']['dado'+str(database_id)]['elec_distance']*(orig_ndim1/kwargs['h']+orig_ndim2/kwargs['w'])/2
    dado['electrode distance (mm)'] = dado['electrode distance (mm)'].astype('float64')
    dado['database URL'] = config['database_params']['dado'+str(database_id)]['database_url']
    dado['database URL'] = dado['database URL'].astype('category')
    if os.path.exists(pathcwd+path+'SubjectsDescription.txt'):
        meta_subjects = pd.read_csv(pathcwd+path+'SubjectsDescription.txt', sep='\t')        
        subs = 's'+str(subject)
        meta_subjects = meta_subjects.query('Subject==@subs')
        dado['gender'] = 'M'
        dado['gender'] = dado['gender'].astype('category')
        for column in list(meta_subjects.columns)[1:]:
            if column.find('circumference') < 0 and column.find('length') < 0 :
                dado[column.lower().strip()] = meta_subjects[column].values[0]
                dado[column.lower().strip()] = dado[column.lower().strip()].astype('category')
            elif column.find('circumference') >= 0 and column.find(segment.capitalize()) >=0:
                dado['circumference (cm)'] = meta_subjects[column].values[0]
                dado['circumference (cm)'] = dado['circumference (cm)'].astype('category')
            elif column.find('length (cm)') >= 0 and column.find(segment.capitalize())>=0:
                dado['length (cm)'] = meta_subjects[column].values[0]
                dado['length (cm)'] = dado['length (cm)'].astype('category')
        dado['dominant hand'] =   ''
        dado['dominant hand'] = dado['dominant hand'].astype('category')
    else:
        dado['age(years)'] = config['database_params']['dado'+str(database_id)][subj_string]['age']
        dado['age(years)'] = dado['age(years)'].astype('category')
        dado['gender'] = config['database_params']['dado'+str(database_id)][subj_string]['gender']
        dado['gender'] = dado['gender'].astype('category')
        dado['dominant hand'] =   config['database_params']['dado'+str(database_id)][subj_string]['dom_hand']
        dado['dominant hand'] = dado['dominant hand'].astype('category')
        dado['circumference (cm)'] = np.nan
        dado['length (cm)'] = np.nan
        dado['heigth(cm)'] = np.nan
        dado['weight(kg)'] = np.nan
    if os.path.exists(pathcwd+path+'ReferencePoints.txt'):
        subs = 's'+str(subject)
        header1 = pd.read_csv(pathcwd+path+'ReferencePoints.txt', sep='\t', index_col=0, nrows=0)        
        header1 = list(header1.columns)
        header = [h1 + '_' + h2 for h1 in header1[::2] for h2 in ['x', 'y']]        
        meta_reference = pd.read_csv(pathcwd+path+'ReferencePoints.txt', sep='\t', index_col=0, 
                                    skiprows=1, header=None, names=header) 
        meta_reference = meta_reference.loc[subs]
        if segment == 'biceps' or segment == 'triceps':
            dado['reference_x'] = meta_reference[segment.capitalize()+'_x']
            dado['reference_y'] = meta_reference[segment.capitalize()+'_y']
        if segment == 'forearm':
            for muscle in ['Brachio Radialis','Anconeus','Pronator Teres']:
                dado['reference_'+muscle+'_x'] = meta_reference[muscle+'_x']
                dado['reference_'+muscle+'_y'] = meta_reference[muscle+'_y']
    else:
        dado['reference_x'] = np.nan
        dado['reference_y'] = np.nan
        for muscle in ['Brachio Radialis','Anconeus','Pronator Teres']:
            dado['reference_'+muscle+'_x'] = np.nan
            dado['reference_'+muscle+'_y'] = np.nan
    return dado




def transform_database3(h, w, subj, type, task, intensity, trial, session, pathcwd=''):
    db_size, dado_orig = get_database3(subj, type, task, intensity, trial, session, pathcwd=pathcwd)
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    path = config['data_path']['dado3']
    fs = config['database_params']['dado3']['fs']
    subj_string = 'subj'+str(subj)
    column_names = np.arange(0, h*w)
    column_names = list(column_names)
    column_names = [str(d) for d in column_names]
    dado = pd.DataFrame(np.zeros((db_size,h*w)), columns=column_names)
    task = dado_orig['movement'][0]
    speed = dado_orig['speed'][0]
    date = dado_orig['date'][0]
    for t in range(db_size):
        dado.iloc[t, :] = read_database3(dado_orig, t, h, w, subj, type, task, intensity, trial, session=session, pathcwd=pathcwd).reshape(1,-1)
    dado = include_metadata(dado,  pathcwd, database_id=3, h=h, w=w, subj=subj, trial=trial, task=task, segment=type, speed=speed, session=session, date=date,fs=fs)
    return dado


def transform_database4(h, w, subj, type, task, intensity, trial, session=None,  pathcwd=''):
    db_size, dado_orig = get_database4(subj, type, task, intensity, trial, pathcwd=pathcwd)
    config = yaml.safe_load(open(pathcwd+'params.yaml'))
    path = config['data_path']['dado4']
    fs = config['database_params']['dado3']['fs']
    n_channels_file = pd.read_csv(pathcwd+path+'nchannels.txt', sep='\s+', index_col='subject')
    subj_string = 's'+str(subj)
    n_channels = n_channels_file.loc[subj_string, type]   
    dado_orig = dado_orig.reshape(n_channels,-1)
    dado_orig = dado_orig.T
    column_names = np.arange(0, h*w)
    column_names = list(column_names)
    column_names = [str(d) for d in column_names]
    dado = pd.DataFrame(np.zeros((db_size,h*w)), columns=column_names)
    for t in range(db_size):
        dado.iloc[t, :] = read_database4(dado_orig, t, h, w, subj, type, task, intensity, trial, session, pathcwd=pathcwd).reshape(1,-1)
    dado = include_metadata(dado, pathcwd, database_id=4, h=h, w=w, subj=subj, task=task, trial=trial, segment=type, intensity=intensity, fs=fs)
    return dado

