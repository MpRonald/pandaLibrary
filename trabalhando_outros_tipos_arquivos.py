# -*- coding: utf-8 -*-
"""
PANDAS -> ENTRADAS E SAÍDAS EM DIFERENTES FORMATOS
"""

import pandas as pd
"""CRIANDO NOMES"""

# lendo arquivo json;
nomes_m = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=m")
nomes_f = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=f")

print(f'Quantidade de nomes: {str(len(nomes_m)+ len(nomes_f))}')


# juntando os dois frames;
frames = [nomes_m, nomes_f]
nomes = pd.concat(frames)['nome'].to_frame()

"""INCLUINDO ID DOS ALUNOS"""
import numpy as np
np.random.seed(123)

total_alunos = len(nomes)

# criando nova coluna e criando id dos alunos;
nomes['id_aluno'] = np.random.permutation(total_alunos) + 1
nomes.sample(10)

# criando dominios de email
dominios = ['@dominiodoemail.com.br', '@servicodoemail.com']
nomes['dominio'] = np.random.choice(dominios, total_alunos)

nomes['email'] = nomes.nome.str.cat(nomes.dominio).str.lower()

"""CRIANDO A TABELAS CURSOS"""
import html5lib
url = 'http://tabela-cursos.herokuapp.com/index.html'
cursos = pd.read_html(url)
cursos = cursos[0]

"""ALTERANDO NOME DO INDEX"""
cursos = cursos.rename(columns={'Nome do curso' : 'nome_do_curso'})
cursos['id'] = cursos.index + 1

cursos = cursos.set_index('id')
cursos

"""MATRICULANDO OS ALUNOS NOS CURSOS"""
nomes['matriculas'] = np.ceil(np.random.exponential(size=total_alunos)*1.5).astype(int)
nomes.matriculas.describe()


import seaborn as sns
sns.distplot(nomes.matriculas)

# verificando quantos alunos estão escritos em nº de cursos;
nomes.matriculas.value_counts()

"""SELECIONANDO CURSOS"""

todas_matriculas = []
x = np.random.rand(20)
prob = x / sum(x)

# atribuindo curso de maneira aleatoria;
for index, row in nomes.iterrows():
    id = row.id_aluno
    matriculas = row.matriculas
    for i in range(matriculas):
        mat = [id, np.random.choice(cursos.index, p = prob)]
        todas_matriculas.append(mat)

matriculas = pd.DataFrame(todas_matriculas, columns = ['id_aluno', 'id_curso'])

matriculas.head()
matriculas.groupby('id_curso').count().join(cursos['nome_do_curso']).rename(columns={'id_aluno':'quantidade_de_alunos'})
matriculas_por_curso = matriculas.groupby('id_curso').count().join(cursos['nome_do_curso']).rename(columns={'id_aluno':'quantidade_de_alunos'})

"""EXPORTANDO DATAFRAME"""

matriculas_por_curso.to_csv('matriculas_por_curso.csv', index=False)
matriculas_json = matriculas_por_curso.to_json()
matriculas_json

matriculas_html = matriculas_por_curso.to_html()

"""CRIANDO BANCO SQL"""
from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///:memory:')
engine

matriculas_por_curso.to_sql('matriculas', engine)
print(engine.table_names())

"""BUSCANDO DO BANCO SQL"""
query = 'select * from matriculas where quantidade_de_alunos < 20'

pd.read_sql(query, engine)

pd.read_sql_table('matriculas', engine, columns=['nome_do_curso',
                                                 'quantidade_de_alunos'])

muitas_matriculas = pd.read_sql_table('matriculas',
                                      engine, columns=['nome_do_curso',
                                                       'quantidade_de_alunos'])
muitas_matriculas = muitas_matriculas.query('quantidade_de_alunos > 70')
muitas_matriculas

"""ESCREVENDO NO BANCO"""
muitas_matriculas.to_sql('muitas_matriculas', con=engine)
print(engine.table_names())

id_curso = 16

proxima_turma = matriculas.query("id_curso == {}".format(id_curso))
proxima_turma

proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))['nome'].to_frame()

nome_curso = cursos.loc[id_curso]
nome_curso

nome_curso = nome_curso.nome_do_curso
nome_curso

proxima_turma = proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))['nome'].to_frame()
proxima_turma

proxima_turma = proxima_turma.rename(columns = {'nome' : 'Alunos do curso de {}'.format(nome_curso)})

proxima_turma

"""Excel"""
proxima_turma.to_excel('proxima_turma.xlsx', index=False)

pd.read_excel('proxima_turma.xlsx')







































































































