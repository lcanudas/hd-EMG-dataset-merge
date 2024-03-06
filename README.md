# hd-EMG-dataset-merge
Nicole Moura
Renato Watanabe

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