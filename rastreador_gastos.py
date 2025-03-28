import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

# Configuração da página
st.set_page_config(page_title="Rastreador de Gastos", layout="wide", initial_sidebar_state="expanded")

# Ler o arquivo CSV
df = pd.read_csv('gastos.csv')

# Converter a coluna 'data' para o tipo datetime e depois para date
df['data'] = pd.to_datetime(df['data']).dt.date

# Criar filtros na barra lateral
with st.sidebar.expander('Filtros'):
    st.subheader('Categorias')
    categorias = st.multiselect(
        'Selecione as categorias',
        options=sorted(df['categoria'].unique()),
        default=sorted(df['categoria'].unique())
    )

    st.subheader('Período')
    meses = ['Jan', 'Fev', 'Mar', 'Abr']
    periodo_numeros = st.select_slider('Selecione o período', options=meses, value=('Jan', 'Abr'))
    meses_numeros = {mes: i + 1 for i, mes in enumerate(meses)}
    periodo_numeros_ajustado = (meses_numeros[periodo_numeros[0]], meses_numeros[periodo_numeros[1]])

# Filtrar o dataframe
df_filtrado = df[df['categoria'].isin(categorias)].copy()
df_filtrado['data'] = pd.to_datetime(df_filtrado['data'])
df_filtrado = df_filtrado[(df_filtrado['data'].dt.month >= periodo_numeros_ajustado[0]) & (df_filtrado['data'].dt.month <= periodo_numeros_ajustado[1])]

# Converter a coluna 'data' para o tipo date após a filtragem
df_filtrado['data'] = df_filtrado['data'].dt.date

# Calcular métricas
gasto_total = df_filtrado['valor'].sum()
gasto_medio = df_filtrado['valor'].mean()

# Criar o painel Streamlit
colored_header(
    label="Rastreador de Gastos (Jan-Abr 2025)",
    description="Acompanhe seus gastos e visualize seus padrões de consumo.",
    color_name="blue-70",
)

# Estilo personalizado para a tabela
with stylable_container(
    key="gastos_container",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
        }
        """,
):
    # Formatação da tabela
    df_filtrado_exibir = df_filtrado.copy()
    df_filtrado_exibir['data'] = pd.to_datetime(df_filtrado_exibir['data']).dt.strftime('%d/%m/%Y')
    df_filtrado_exibir['valor'] = df_filtrado_exibir['valor'].apply(lambda x: f'R$ {x:.2f}')

    # Exibir o dataframe filtrado
    st.dataframe(df_filtrado_exibir,
                 column_config={
                     'data': st.column_config.Column('Data'),
                     'descricao': st.column_config.Column('Descrição'),
                     'valor': st.column_config.Column('Valor'),
                     'categoria': st.column_config.Column('Categoria')
                 },
                 height=300,
                 use_container_width=True)

# Exibir métricas em colunas
col1, col2 = st.columns(2)
col1.metric('Gasto Total', value=f'R$ {gasto_total:.2f}')
col2.metric('Gasto Médio', value=f'R$ {gasto_medio:.2f}')
style_metric_cards(background_color="#f0f2f6", border_left_color="#90EE90")

# Exibir gráfico de barras
st.subheader('Gastos por Categoria')
gastos_por_categoria = df_filtrado.groupby('categoria')['valor'].sum()
fig_bar = px.bar(gastos_por_categoria, x=gastos_por_categoria.index, y='valor', labels={'valor': 'Gasto (R$)'})
st.plotly_chart(fig_bar, use_container_width=True)

# Exibir gráfico de linhas
st.subheader('Gastos ao Longo do Tempo')
fig_line, ax_line = plt.subplots()
sns.lineplot(x='data', y='valor', data=df_filtrado, ax=ax_line, color='darkblue', marker='o', linewidth=2)
ax_line.set_xlabel('Data', fontsize=12)
ax_line.set_ylabel('Gasto (R$)', fontsize=12)
ax_line.set_title('Gastos ao Longo do Tempo', fontsize=14)
ax_line.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
fig_line.autofmt_xdate(rotation=45)
st.pyplot(fig_line)

# Gráfico de pizza
st.subheader('Proporção de Gastos por Categoria')
st.plotly_chart(px.pie(df.groupby('categoria')['valor'].sum().reset_index(), names='categoria', values='valor'), use_container_width=True)

# Adicionar interatividade com um widget de entrada de texto
nome = st.text_input('Digite seu nome')
st.write(f'Olá, {nome}!')

# Adicionar alertas
limite_gasto = 500
if gasto_total > limite_gasto:
    st.warning(f'Seu gasto total ultrapassou o limite de R${limite_gasto}!')

# Exportar dados
add_vertical_space(2)
if st.download_button('Exportar dados para CSV', df_filtrado.to_csv(index=False).encode('utf-8'), 'gastos.csv', 'text/csv'):
    st.success('Arquivo CSV gerado com sucesso!')
