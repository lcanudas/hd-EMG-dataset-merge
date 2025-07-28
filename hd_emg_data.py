import os
import yaml
import numpy as np
import pandas as pd
import h5py
from pathlib import Path

def get_database2(mat_file, signal_type):
    file_path = Path(mat_file)
    file_size = file_path.stat().st_size
    with h5py.File(mat_file, 'r') as mat_data:
        data = np.array(mat_data[signal_type])
        length = data.shape[2]
        fs = mat_data['Fs'][0]
        labels = np.array(mat_data['label']).flatten()
        repetitions = np.array(mat_data['repetition']).flatten()
        force = np.array(mat_data['force'])
    return file_size, length, data, fs, labels, repetitions, force

def include_metadata(dado, pathcwd, database_id, **kwargs):
    with open(os.path.join(pathcwd, 'params.yaml'), 'r') as f:
        config = yaml.safe_load(f)

    path = config.get('data_path', {}).get(f'dado{database_id}', '')
    subject = kwargs.get('subj', np.nan)
    subj_string = 's' + str(subject)
    dado['database_id'] = database_id
    dado['database_id'] = dado['database_id'].astype('int8')
    dado['n_dim1'] = kwargs['h'] if 'h' in kwargs else np.nan
    dado['n_dim1'] = dado['n_dim1'].astype('category')
    dado['n_dim2'] = kwargs['w'] if 'w' in kwargs else np.nan
    dado['n_dim2'] = dado['n_dim2'].astype('category')
    dado['subject'] = subject
    dado['subject'] = dado['subject'].astype('category')
    segment = kwargs.get('segment', np.nan)
    dado['segment'] = segment
    dado['segment'] = dado['segment'].astype('category')
    dado['trial'] = kwargs.get('trial', np.nan)
    dado['trial'] = dado['trial'].astype('Int64')
    dado['task'] = kwargs.get('task', np.nan)
    dado['task'] = dado['task'].astype('category')
    dado['intensity'] = kwargs.get('intensity', 0)
    dado['intensity'] = dado['intensity'].astype('int8')
    dado['speed'] = kwargs.get('speed', '')
    dado['speed'] = dado['speed'].astype('category')
    dado['session'] = kwargs.get('session', 0)
    dado['session'] = dado['session'].astype('category')
    dado['signal_length'] = kwargs.get('length', np.nan)
    dado['signal_length'] = dado['signal_length'].astype('int32')
    signal_matrix = kwargs.get('data', np.nan)
    flat_signal = signal_matrix.flatten(order='F')
    for i in range(64):
        dado[f'electrode{i+1}'] = flat_signal[i]
    force_array = kwargs.get('force', np.full(9, np.nan))
    force_colnames = [
        "D2 flex/ext",
        "D3 flex/ext",
        "D4 flex/ext",
        "D5 flex/ext",
        "thumb flex/ext",
        "thumb abd/add",
        "wrist flex/ext",
        "wrist pro/sup",
        "wrist rad/uln"
    ]
    for j, col_name in enumerate(force_colnames):
        dado[col_name] = force_array[j] if j < len(force_array) else np.nan
    dado['date'] = kwargs.get('date', np.nan)
    dado['date'] = dado['date'].astype('category')
    dado['frequency_sample (Hz)'] = kwargs.get('fs', np.nan)
    dado['frequency_sample (Hz)'] = dado['frequency_sample (Hz)'].astype('category')
    dado['original electrode distance (mm)'] = config['database_params']['dado'+str(database_id)]['elec_distance']
    dado['original electrode distance (mm)'] = dado['original electrode distance (mm)'].astype('int64')
    dado['original electrode diameter (mm)'] = config['database_params']['dado'+str(database_id)]['elec_diameter']
    dado['original electrode diameter (mm)'] = dado['original electrode diameter (mm)'].astype('category')
    orig_ndim1 = config.get('database_params', {}).get(f'dado{database_id}', {}).get(f'nrows_{segment}', np.nan)
    dado['original_n_dim1'] = orig_ndim1
    dado['original_n_dim1'] = dado['original_n_dim1'].astype('category')
    if f'ncolumns_{segment}' in config['database_params'][f'dado{database_id}']:
        dado['original_n_dim2'] = config['database_params'][f'dado{database_id}'][f'ncolumns_{segment}']
    else:
        dado['original_n_dim2'] = np.nan
    dado['original_n_dim2'] = dado['original_n_dim2'].astype('category')
    try:
        elec_dist = dado['original electrode distance (mm)'].iloc[0]
        h_val = kwargs.get('h', np.nan)
        w_val = kwargs.get('w', np.nan)
        dado['electrode distance (mm)'] = elec_dist * ((orig_ndim1 / h_val) + (dado['original_n_dim2'].iloc[0] / w_val)) / 2
    except:
        dado['electrode distance (mm)'] = np.nan
    dado['electrode distance (mm)'] = dado['electrode distance (mm)'].astype('float64')
    dado['database URL'] = config.get('database_params', {}).get(f'dado{database_id}', {}).get('database_url', '')
    dado['database URL'] = dado['database URL'].astype('category')
    subj_info = config.get('database_params', {}).get(f'dado{database_id}', {}).get(subj_string, {})
    dado['age(years)'] = subj_info.get('age', np.nan)
    dado['age(years)'] = dado['age(years)'].astype('category')
    dado['gender'] = subj_info.get('gender', np.nan)
    dado['gender'] = dado['gender'].astype('category')
    dado['dominant hand'] = subj_info.get('laterality', np.nan)
    dado['dominant hand'] = dado['dominant hand'].astype('category')
    dado['circumference (cm)'] = subj_info.get('forearm_circumference_cm', np.nan)
    dado['length (cm)'] = np.nan
    dado['height(cm)'] = subj_info.get('height_cm', np.nan)
    dado['weight(kg)'] = subj_info.get('weight_kg', np.nan)
    dado['palm width(cm)'] = subj_info.get('palm_width_cm', np.nan)
    dado['palm circumference(cm)'] = subj_info.get('palm_circumference_cm', np.nan)
    ref_path = os.path.join(pathcwd, path, 'ReferencePoints.txt')
    if os.path.exists(ref_path):
        subs = 's' + str(subject)
        header1 = pd.read_csv(ref_path, sep='\t', index_col=0, nrows=0)
        header1 = list(header1.columns)
        header = [h1 + '_' + h2 for h1 in header1[::2] for h2 in ['x', 'y']]
        meta_reference = pd.read_csv(ref_path, sep='\t', index_col=0, skiprows=1, header=None, names=header)
        meta_reference = meta_reference.loc[subs]
        if segment == 'biceps' or segment == 'triceps':
            dado['reference_x'] = meta_reference[segment.capitalize() + '_x']
            dado['reference_y'] = meta_reference[segment.capitalize() + '_y']
        if segment == 'forearm':
            for muscle in ['Brachio Radialis', 'Anconeus', 'Pronator Teres']:
                dado['reference_' + muscle + '_x'] = meta_reference[muscle + '_x']
                dado['reference_' + muscle + '_y'] = meta_reference[muscle + '_y']
    else:
        dado['reference_x'] = np.nan
        dado['reference_y'] = np.nan
        for muscle in ['Brachio Radialis', 'Anconeus', 'Pronator Teres']:
            dado['reference_' + muscle + '_x'] = np.nan
            dado['reference_' + muscle + '_y'] = np.nan

    return dado

if __name__ == '__main__':
    pathcwd = r"C:\Program Files (x86)\files\hd-EMG-dataset-merge\\"
    database_id = 2
    segmento = 'emg_extensors'
    lista_dados = []

    for subj in range(1, 21):
        mat_path = rf"C:\Users\Luana\Downloads\s{subj}.mat"
        try:
            file_size, length, data, fs, labels, repetitions, force = get_database2(mat_path, segmento)
            h, w = data.shape[0], data.shape[1]
        except Exception as e:
            print(f"[ERRO] Falha ao processar sujeito {subj}: {e}")
            continue
        for i in range(length):
            signal_i = data[:, :, i]
            label_i = labels[i] if i < len(labels) else np.nan
            repetition_i = repetitions[i] if i < len(repetitions) else np.nan
            force_i = force[:, i] if i < force.shape[1] else np.full(force.shape[0], np.nan)

            dado_base = pd.DataFrame([{}])
            dado_completo = include_metadata(
                dado_base,
                pathcwd,
                database_id=database_id,
                subj=subj,
                h=h,
                w=w,
                segment='forearm',
                trial=np.nan,
                task=np.nan,
                intensity=0,
                speed='',
                session=0,
                date=np.nan,
                fs=fs,
                length=length,
                data=signal_i,
                label=label_i,
                repetition=repetition_i,
                force=force_i
            )

            lista_dados.append(dado_completo)

    df_todos = pd.concat(lista_dados, ignore_index=True)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    print(df_todos)


