import pandas as pd
from util import get_completion

data = pd.read_csv('car_dataset_unprocessed.csv', index_col=0)
selected_cols = ['Anunciante', 'Marca', 'Modelo', 'Versão', 'Combustível', 'Ano',
             'Quilómetros', 'Cilindrada', 'Potência', 'Segmento', 'Cor',
             'Tipo de Caixa', 'Nº de portas', 'Garantia de Stand (incl. no preço)',
             'Condição', 'Foto', 'Preço', 'Link', 'PreçoComparado', 'Morada', 'Consumo Urbano']
data = data[selected_cols]

data['Consumo Urbano'] = pd.to_numeric(data['Consumo Urbano'].map(lambda x: x.split(" ")[0] if isinstance(x, str) else pd.NA).str.replace(',', '.'), errors='coerce')
data.rename({'Consumo Urbano': 'Consumo Urbano (l/100 km)'}, axis=1, inplace=True)
data['Nº de portas'] = data['Nº de portas'].astype('Int32')
data['Quilómetros'] = data['Quilómetros'].str.replace('[^0-9]', '', regex=True).astype('Int32')
data['Cilindrada'] = data['Cilindrada'].str.replace('[^0-9]', '', regex=True).str[:-1].astype('Int32')
data.rename({'Cilindrada': 'Cilindrada (cm3)'}, axis=1, inplace=True)
data['Potência'] = data['Potência'].str.replace('[^0-9]', '', regex=True).astype('Int32')
data.rename({'Potência': 'Potência (cv)'}, axis=1, inplace=True)
data['Garantia de Stand (incl. no preço)'] = data['Garantia de Stand (incl. no preço)'].str.replace('[^0-9]', '', regex=True).astype('Int32')
data.rename({'Garantia de Stand (incl. no preço)': 'Garantia de Stand (incl. no preço) (meses)'}, axis=1, inplace=True)
data['Preço'] = data['Preço'].str.replace(' ', '').astype('Int32')
data.rename({'Preço': 'Preço (€)'}, axis=1, inplace=True)
data['Ano'] = data['Ano'].astype('Int32')


prompt1 = f"You are a translator bot. You are translating car specifications from Portuguese to English.\
 You will receive, inside triple brackets, a list of the values to translate and you should output in the same format as input(a list). Only output the translated list.\
 '''{data.columns}'''"

response1 = get_completion(prompt=prompt1)

cols_to_translate = ['Anunciante', 'Combustível', 'Segmento', 'Cor', 'Tipo de Caixa', 'Condição', 'PreçoComparado']
unique_values = {col: data[col].unique().tolist() for col in cols_to_translate}

prompt2 = (f"You are a translator bot. You are translating car specifications from Portuguese to English.\
 You will receive, inside triple brackets, a dictionary where key is column name and value is that column's unique values.\
 You will return a dictionary where keys are the column names and the values are lists of the column unique values translated to English, IGNORE nan values, please don't output them.\
 Output in the same format as input. Only output the dictionary with translated values.\
 '''{unique_values}'''")

response2 = get_completion(prompt=prompt2)


# Apply transformations
replace_dict = {col: dict(zip(unique_values[col], eval(response2)[col])) for col in unique_values}
data = data.replace(replace_dict)
data.columns = eval(response1)

data.to_csv('car_dataset.csv')
