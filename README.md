# hd-EMG-dataset-merge
Nicole Moura
Renato Watanabe

### Notebook exemplo

Existe um Jupyter notebook com exemplo básico de como utilizar os dados:

[notebooks/exemplo_uso_dataset.ipynb](notebooks/exemplo_uso_dataset.ipynb)


---
### Instalar miniconda:

(https://docs.anaconda.com/free/miniconda/index.html)

---
### Vscode 

(https://code.visualstudio.com/)

---
### Dentro do Vscode executar em um terminal [https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/]:



1-`git clone https://github.com/nicbmoura/hd-EMG-dataset-merge.git`

2- `cd hd-EMG-dataset-merge`


3- `python3 -m venv hdemg`



4- No Linux

`echo "export PYTHONPATH=$PWD" >> hdemg/bin/activate`

`source hdemg/bin/activate`

No Windows

`hdemg\Scripts\activate`

5 - `pip install -r requirements.txt`

Passar os dados pro Github

---

### Após cada adição de dado na pasta data, entrar com os seguintes comandos:

- `dvc add data`

- `dvc push`

- `git commit -m "mensagem"`

- `git push`


--- 

### Para pegar os dados, usar os comandos:

- `git pull`

- `dvc pull`


---

### Tarefas

Puxar arquivo sujeito 1 do database 2.

Ler o arquivo .mat
Como ler arquivos .mat: https://www.askpython.com/python/examples/mat-files-in-python

Pegar emg_flexors e emg_extensors

Fazer um gráfico de um instante dos dados de EMG
