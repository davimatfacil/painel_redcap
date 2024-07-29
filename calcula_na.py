import streamlit as st
import redcap
import pandas as pd

def get_na_counts(redcap_uri, token, forms, event_name, columns):
    # Conectar ao projeto REDCap
    proj = redcap.Project(redcap_uri, token)

    # Exportar os registros do REDCap
    dados = proj.export_records(format_type='df', forms=forms, events=[event_name])

    # Filtrar o DataFrame pelo valor do índice 'redcap_event_name'
    filtro_evento = dados.loc[dados.index.get_level_values('redcap_event_name') == event_name]

    # Selecionar as colunas especificadas
    filtro_evento = filtro_evento[columns]

    # Contar os valores NaN em cada coluna
    na_counts = filtro_evento.isna().sum()

    # Criar um DataFrame com as contagens de NaN
    na_counts_df = pd.DataFrame({
        'Variavel Analisada': na_counts.index,
        'Qtde de Missing': na_counts.values
    })

    return na_counts_df 

# Interface do Streamlit
st.title('Análise de Dados Faltantes no Projeto LATAM') 

redcap_uri = st.text_input('REDCap URI', 'xxxxxxxxxxxxxxxx')
token = st.text_input('Token', 'xxxxxxxxxxxxxxxxxxx')
forms = st.text_input('Forms', 'sociodemografico')
event_name = st.text_input('Event Name', 'triagem1_arm_1')
columns = st.text_area('Columns (separadas por vírgula)', 'age_esp, sex_esp, race_esp, education_esp, tobacco_esp, salary_esp, job_esp, retirement_esp')

# Converter a lista de colunas de string para uma lista real
columns = [col.strip() for col in columns.split(',')]

if st.button('Exibir Contagem de Missing'):
    if redcap_uri and token and forms and event_name and columns:
        try:
            na_counts_df = get_na_counts(redcap_uri, token, forms, event_name, columns)
            st.write('Contagem de Valores Missing:')
            st.dataframe(na_counts_df)
        except Exception as e:
            st.error(f'Erro ao obter os dados: {e}')
    else:
        st.error('Por favor, preencha todos os campos!')
