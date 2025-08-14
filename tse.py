#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px 
import sqlalchemy
import seaborn as sn
import requests
import os


if not os.path.exists('data'):
    os.makedirs('data')

DB_PATH = 'data/database.db'
DB_URL = 'https://www.dropbox.com/scl/fi/ku1yc1gppsg6ktuzwz28q/database.db?rlkey=g8m844s4q7h33mc4hwpf4sb8a&st=z3nu188x&dl=1'

def baixar_db(url, path):
    st.info("Preparando ambiente / Baixando o banco de dados.")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    st.success("Ambiente pronto!")

@st.cache_data
def carregar_dados(): #função para abrir o arquivo sql com a query
    if not os.path.exists(DB_PATH):
        baixar_db(DB_URL, DB_PATH)
    try:
        with open("query1.sql", "r", encoding='utf-8') as open_file:
            query = open_file.read()
        engine = sqlalchemy.create_engine("sqlite:///data/database.db")
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame() # retorna df vazio se der erro

df = carregar_dados()

df = df.rename(columns={   #renomeia as colunas
    'SQ_CANDIDATO':'NUM_CANDIDATO',
    'SG_UF' : 'ESTADO',
    'DS_CARGO': 'CARGO',
    'SG_PARTIDO' : 'SIGLA_PARTIDO',
    'NM_PARTIDO' : 'PARTIDO',
    'DT_NASCIMENTO':'NASCIMENTO',
    'DS_GENERO': 'GENERO',
    'DS_GRAU_INSTRUCAO': 'GRAU_INSTRUCAO',
    'DS_ESTADO_CIVIL': 'ESTADO_CIVIL',
    'DS_COR_RACA': 'COR',
    'NR_TURNO': 'TURNO',
    'DS_OCUPACAO':'OCUPACAO',
    'DS_SIT_TOT_TURNO': 'RESULTADO_ELEICAO',
    'totalBens': 'BENS_TOTAIS',
    'IDEOLOGIA': 'ESPECTRO_POLITICO',
    'Status_Cassacao': 'CASSADO?'
})

PALETA_ESPECTRO = {
    'ESQUERDA': '#d62728', 'EXTREMA-ESQUERDA': '#8c564b', 'CENTRO-ESQUERDA': '#ff7f0e',
    'CENTRO': '#7f7f7f', 'CENTRO-DIREITA': '#17becf', 'DIREITA': '#1f77b4'
}
PALETA_GENERO = {'tx_feminino': '#FFA6C9', 'tx_masculino': '#99CCFF'}



# CRIAÇÃO DOS DFS PERSONALIZADOS:

df_genero_partido = df.groupby('PARTIDO').agg(
    tx_feminino=('GENERO', lambda x: (x=='FEMININO').mean()*100),
    tx_masculino = ('GENERO', lambda x: (x=='MASCULINO').mean()*100)
).reset_index()

df_genero_espectro = df.groupby('ESPECTRO_POLITICO').agg(
    tx_feminino=('GENERO', lambda x: (x=='FEMININO').mean()*100),
    tx_masculino = ('GENERO', lambda x: (x=='MASCULINO').mean()*100)
).reset_index()

df_escolaridade_partido = df.groupby('PARTIDO').agg(
    tx_baixa_escolaridade = ('GRAU_INSTRUCAO', lambda x: x.isin([
        'LÊ E ESCREVE',
        'ENSINO FUNDAMENTAL INCOMPLETO',
        'ENSINO MÉDIO INCOMPLETO',
        'ANALFABETO',
        'ENSINO FUNDAMENTAL COMPLETO']).mean()*100),

    tx_escolarizados = ('GRAU_INSTRUCAO', lambda x: x.isin([
        'SUPERIOR INCOMPLETO',
        'ENSINO MÉDIO COMPLETO']).mean()*100),

    tx_graduados = ('GRAU_INSTRUCAO', lambda x: (x=='SUPERIOR COMPLETO').mean()*100)
)

df_escolaridade_espectro = df.groupby('ESPECTRO_POLITICO').agg(
    tx_baixa_escolaridade = ('GRAU_INSTRUCAO', lambda x: x.isin([
        'LÊ E ESCREVE',
        'ENSINO FUNDAMENTAL INCOMPLETO',
        'ENSINO MÉDIO INCOMPLETO',
        'ANALFABETO',
        'ENSINO FUNDAMENTAL COMPLETO']).mean()*100),

    tx_escolarizados = ('GRAU_INSTRUCAO', lambda x: x.isin([
        'SUPERIOR INCOMPLETO',
        'ENSINO MÉDIO COMPLETO']).mean()*100),

    tx_graduados = ('GRAU_INSTRUCAO', lambda x: (x=='SUPERIOR COMPLETO').mean()*100)
).reset_index()

df_cor_partido = df.groupby('PARTIDO').agg(
    tx_pretos_pardos=('COR', lambda x: x.isin(['PRETA','PARDA']).mean()*100),
    tx_brancos = ('COR', lambda x: (x=='BRANCA').mean()*100),
    tx_indigenas = ('COR', lambda x: (x=='INDÍGENA').mean()*100),
    tx_amarelos= ('COR', lambda x: (x=='AMARELA').mean()*100),
).reset_index()

df_cor_espectro= df.groupby('ESPECTRO_POLITICO').agg(
    tx_pretos_pardos=('COR', lambda x: x.isin(['PRETA','PARDA']).mean()*100),
    tx_brancos = ('COR', lambda x: (x=='BRANCA').mean()*100),
    tx_indigenas = ('COR', lambda x: (x=='INDÍGENA').mean()*100),
    tx_amarelos= ('COR', lambda x: (x=='AMARELA').mean()*100),
).reset_index()

df_bens_partido = df.groupby('PARTIDO').agg(
    mediana_bens=('BENS_TOTAIS', 'median')
).reset_index()

df_bens_espectro = df.groupby('ESPECTRO_POLITICO').agg(
    media_bens=('BENS_TOTAIS', 'median')
).reset_index()

df_eleitos_partido = df.groupby('PARTIDO').agg(
    tx_eleitos=('RESULTADO_ELEICAO', lambda x: x.isin(['ELEITO','ELEITO POR MÉDIA', 'ELEITO POR QP']).mean()*100)
).reset_index()


status_de_eleito = ['ELEITO', 'ELEITO POR MÉDIA', 'ELEITO POR QP']
df_eleitos_total = df[df['RESULTADO_ELEICAO'].isin(status_de_eleito)]
df_eleitos_espectro = df_eleitos_total['ESPECTRO_POLITICO'].value_counts(normalize=True).reset_index()
df_eleitos_espectro.columns = ['ESPECTRO_POLITICO','PERCENTUAL_DO_TOTAL']
df_eleitos_espectro['PERCENTUAL_DO_TOTAL'] *= 100

top_10_partidos_series = df_eleitos_total['PARTIDO'].value_counts().head(10)
df_top_10_partidos = top_10_partidos_series.reset_index()
df_top_10_partidos.columns = ['PARTIDO', 'numero_de_eleitos']

st.set_page_config(layout="wide") # Usa a largura total da tela
st.title("Dashboard de Análises das Eleições 2024 🗳️")

#GRAFICOS E VISUALIZAÇAO

st.header("📊 Análise de Gênero")
col1, col2 = st.columns((2,1))

with col1:
    df_melted_genero = df_genero_partido.melt(
        id_vars='PARTIDO', 
        value_vars=['tx_feminino', 'tx_masculino'],
        var_name='Gênero', value_name='Percentual'
    )

    fig_genero_partido = px.bar (
        df_melted_genero, 
        x='PARTIDO', y='Percentual', color='Gênero',
        title="Distribuição de genero por partidos políticos",
        barmode='group',
        color_discrete_map={'tx_feminino': PALETA_GENERO['tx_feminino'], 'tx_masculino': PALETA_GENERO['tx_masculino']},
        labels={'PARTIDO': 'Partido', 'Percentual':'%'}
    )
    st.plotly_chart(fig_genero_partido, use_container_width=True)
    st.markdown("""
    Pode-se notar que homens ainda são a grande maioria na política, com uma média global de quase 65% do total. o PCB é que possui a maior % de homens.
    """)
    

with col2:
        df_genero_partido_filtrado = df_genero_partido.sort_values(by='tx_feminino', ascending=False)
        df_genero_partido_filtrado2 = df_genero_partido.sort_values(by='tx_masculino', ascending=False)
        st.subheader("Métricas Principais")
        media_feminina = df_genero_partido['tx_feminino'].mean()
        partido_max_feminino = df_genero_partido_filtrado.iloc[0]
        media_masculina = df_genero_partido['tx_masculino'].mean()
        partido_max_masculino = df_genero_partido_filtrado2.iloc[0]

        st.metric(
             label = "Média geral de representação feminina:",
             value= f"{media_feminina:.1f}%"
        )
        st.metric(
             label = "Partido com maior representação feminina: ",
             value= partido_max_feminino['PARTIDO'],
             delta = f"{partido_max_feminino['tx_feminino']:.1f}%",
             delta_color="normal"
        )
        st.metric(
             label = "Média geral de representação masculina:",
             value= f"{media_masculina:.1f}%"
        )
        st.metric(
             label = "Partido com maior representação masculina: ",
             value= partido_max_masculino['PARTIDO'],
             delta = f"{partido_max_masculino['tx_masculino']:.1f}%",
             delta_color="normal"
        )
        
st.divider()    

col3, col4 = st.columns((2,1))    

with col3:
     df_melted_genero_espectro = df_genero_espectro.melt(
          id_vars= 'ESPECTRO_POLITICO',
          value_vars= ['tx_feminino', 'tx_masculino'],
          var_name= 'Gênero', value_name='Percentual'
     )

     fig_genero_espectro = px.bar (
          df_melted_genero_espectro,
          x='ESPECTRO_POLITICO', y='Percentual', color='Gênero',
          title="⚖️ Distribuição de genero por espectro político",
          barmode='group',
          color_discrete_map={'tx_feminino': PALETA_GENERO['tx_feminino'], 'tx_masculino': PALETA_GENERO['tx_masculino']},
          labels = {'ESPECTRO_POLITICO': 'Espectro Político','Percentual':'%' }
     )
     st.plotly_chart(fig_genero_espectro, use_container_width=True)

     st.markdown("""
    Partidos de todos os espectros políticos possuem a distribuição de genero bem semelhante, próximo a média, com exceção de partidos de Extrema esquerda.
    """)

with col4:
     df_genero_espectro_filtrado = df_genero_espectro.sort_values(by='tx_feminino', ascending=False)    
     df_genero_espectro_filtrado2 = df_genero_espectro.sort_values(by='tx_masculino', ascending=False)     
     media_masculina_espectro = df_genero_espectro['tx_masculino'].mean()
     espectro_max_masculino = df_genero_espectro_filtrado2.iloc[0]
     media_feminina_espectro = df_genero_espectro['tx_feminino'].mean()
     espectro_max_feminina = df_genero_espectro_filtrado.iloc[0]

     st.metric(
          label="Espectro político com maior representação feminina: ",
          value= espectro_max_feminina['ESPECTRO_POLITICO'],
          delta= f"{espectro_max_feminina['tx_feminino']:.1f}%"
     )
     st.metric(
          label="Espectro político com maior representação masculina: ",
          value= espectro_max_masculino['ESPECTRO_POLITICO'],
          delta= f"{espectro_max_masculino['tx_masculino']:.1f}%"
     )

st.divider()

df_interseccional = df.groupby(['PARTIDO', 'ESPECTRO_POLITICO']).agg(
     tx_pretos_pardos=('COR', lambda x : x.isin(['PRETA', 'PARDA']).mean()*100),
     tx_mulheres=('GENERO', lambda x: (x =='FEMININO').mean()*100),
     tx_eleitos= ('RESULTADO_ELEICAO', lambda x : x.isin(['ELEITO', 'ELEITO POR MÉDIA', 'ELEITO POR QP']).mean()*100),
     total_candidatos = ('NUM_CANDIDATO', 'count') 
).reset_index()

df_interseccional = df_interseccional[df_interseccional['total_candidatos'] > 50]


st.header("🧬 Análise Interseccional: Gênero e Raça")
media_mulheres = df_interseccional['tx_mulheres'].mean()
media_pretos_pardos = df_interseccional['tx_pretos_pardos'].mean()

fig_interseccional = px.scatter(
     df_interseccional,
     x='tx_mulheres',
     y='tx_pretos_pardos',
     size='total_candidatos',
     color='ESPECTRO_POLITICO',
     hover_name='PARTIDO',
     title='Relação entre Representatividade de Gênero e Raça por Partido',
     labels={'tx_mulheres': 'Percentual de Candidatas Mulheres (%)',
        'tx_pretos_pardos': 'Percentual de Candidatos Pretos e Pardos (%)',
        'ESPECTRO_POLITICO': 'Espectro Político'},
    size_max=50    
)

fig_interseccional.add_vline(x=media_mulheres, line_dash="dash", line_color="gray", 
                            annotation_text=f"Média Mulheres ({media_mulheres:.1f}%)", 
                            annotation_position="bottom right")

fig_interseccional.add_hline(y=media_pretos_pardos, line_dash="dash", line_color="gray", 
                            annotation_text=f"Média Pretos/Pardos ({media_pretos_pardos:.1f}%)", 
                            annotation_position="top left")

fig_interseccional.add_annotation(x=95, y=95, text="<b>Acima da média em ambos</b>", showarrow=False, bgcolor="rgba(0,255,0,0.1)")
fig_interseccional.add_annotation(x=5, y=5, text="<b>Abaixo da média em ambos</b>", showarrow=False, bgcolor="rgba(255,0,0,0.1)")

st.plotly_chart(fig_interseccional, use_container_width=True)

with st.expander("Como interpretar este gráfico?"):
    st.markdown("""
    Este gráfico de dispersão ajuda a entender a relação entre gênero e raça nos partidos políticos.
    - **Eixo X (Horizontal):** Quanto mais à direita, maior a porcentagem de mulheres no partido.
    - **Eixo Y (Vertical):** Quanto mais para cima, maior a porcentagem de pessoas pretas e pardas no partido.
    - **Quadrantes:** As linhas cinzas representam a média nacional.
        - **Superior Direito:** Partidos com representatividade acima da média tanto para mulheres quanto para pretos/pardos.
        - **Inferior Esquerdo:** Partidos com representatividade abaixo da média em ambos os quesitos.
        - **Outros Quadrantes:** Partidos acima da média em um quesito e abaixo em outro.
    - **Tamanho da Bolha:** Representa o número total de candidatos do partido.
    """)

col5, col6 = st.columns(2)        
st.header("🍕 Composição Ideológica dos Candidatos Eleitos")

with col5:
    fig_pizza_eleitos = px.pie(
        df_eleitos_espectro,
        names='ESPECTRO_POLITICO',
        values='PERCENTUAL_DO_TOTAL',
        title='Espectros políticos mais votados na eleição',
        hole=0.3,
        color='ESPECTRO_POLITICO', color_discrete_map=PALETA_ESPECTRO
    )

    fig_pizza_eleitos.update_traces(
        textinfo='percent+label',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>Representa: %{value:.2f}% do total de eleitos<extra></extra>'
    )

st.plotly_chart(fig_pizza_eleitos, use_container_width=True)

st.markdown("""
    Entre todos os políticos eleitos durante a eleição, a vasta maioria (66,8%) são de partidos do 'centrão' ou centro-direita, uma tendencia que deve ser observada para ajudar a prever a eleição de 2026.
    """)
      
st.header("🎓 Grau de instrução por espectro político")      
with col6:
    df_melted_escolaridade_espectro = df_escolaridade_espectro.melt(
        id_vars='ESPECTRO_POLITICO',
        value_vars=['tx_baixa_escolaridade', 'tx_escolarizados', 'tx_graduados'],
        var_name= 'Grau de instrução', value_name='Percentual'
    )
    fig_barra_escolaridade= px.bar(
        df_melted_escolaridade_espectro,
        x='ESPECTRO_POLITICO', y='Percentual', color='Grau de instrução',
        title='Grau de instrução por orientação política',
        barmode='stack',
        labels={'ESPECTRO_POLITICO':'Orientação política', 'Percentual': '%'}
    )     

st.plotly_chart(fig_barra_escolaridade, use_container_width=True)

st.markdown("""
    Aqui, podemos notar a diferença no grau de escolaridade dos candidatos, agrupados por espectro político. A Centro-esquerda é a que possui a menor proporção de candidatos com ensino superior, enquanto os partidos que são bem mais à esquerda possuem a maior.
                   Centro-direita e Centro-esquerda possuem as maiores proporções de candidatos com ensino médio completo e superior incompleto. 
    """)
      

col7, col8 = st.columns((2,1))    

with col7:
    st.subheader(" 💰 Mediana de Bens por Partido")
    df_bens_partido_ordenado = df_bens_partido.sort_values(by='mediana_bens', ascending=False)
    fig_bens_partido = px.bar (
        df_bens_partido_ordenado,
        x= 'PARTIDO', y='mediana_bens', title='Mediana de bens por cada partido em Reais',
        labels={'PARTIDO':'Partido', 'mediana_bens': 'Mediana de bens declarados (R$)'}, color='PARTIDO'
    )
    fig_bens_partido.update_yaxes(tickprefix="R$ ")
    st.plotly_chart(fig_bens_partido, use_container_width=True)    

    st.markdown("""
    Aqui foi utilizada a mediana invés da média, dado que a média tendia a ser puxada pra cima devido aos candidatos de cada partido que possuiam grande fortuna declarada. 
                  A mediana representa de forma mais justa o valor possuido por candidato de cada partido.
    """)

with col8:
    media_partidos= df_bens_partido['mediana_bens'].mean()
    df_bens_partido_maior = df_bens_partido.sort_values(by='mediana_bens', ascending=False)
    df_bens_partido_menor = df_bens_partido.sort_values(by='mediana_bens', ascending=True)
    max_bens_partido = df_bens_partido_maior.iloc[0]
    min_bens_partido = df_bens_partido_menor.iloc[0]

    st.metric('Valor médio declarado por cada partido:',
              value=f"{media_partidos:.2f}R$"
              )
    st.metric(
        label='Partido com Maior Mediana de Bens:',
        value=max_bens_partido['PARTIDO'],
        delta=f"R$ {max_bens_partido['mediana_bens']:,.2f}",
        delta_color="normal" 
    )
    st.metric('Partido com menos bens declarados:',
              value=min_bens_partido['mediana_bens'],
              delta= f"R$ {min_bens_partido['mediana_bens']:,.2f}",
              delta_color='inverse'
              )
    
st.header("🔍🏦 Análise Detalhada por Partido")

lista_de_partidos = sorted(df['PARTIDO'].unique())
indice_padrao = lista_de_partidos.index('AVANTE')
partido_selecionado = st.selectbox(
    "Selecione um partido para analisar em detalhes:",
    options=lista_de_partidos,
    index=indice_padrao
)

if partido_selecionado:

    df_partido_unico = df[df['PARTIDO'] == partido_selecionado]
    
    st.subheader(f"Estatísticas para o partido: {partido_selecionado}")

    col_a, col_b, col_c = st.columns(3)
    
    media_bens = df_partido_unico['BENS_TOTAIS'].mean()
    mediana_bens = df_partido_unico['BENS_TOTAIS'].median()
    perc_zero_bens = (df_partido_unico['BENS_TOTAIS'] == 0).mean() * 100
    
    col_a.metric("Média de Bens", f"R$ {media_bens:,.2f}")
    col_b.metric("Mediana de Bens", f"R$ {mediana_bens:,.2f}")
    col_c.metric("% de Candidatos com R$ 0 de Bens", f"{perc_zero_bens:.1f}%")

    st.write("Distribuição do Patrimônio dos Candidatos")

    max_range = df_partido_unico['BENS_TOTAIS'].quantile(0.95) 

    fig_hist = px.histogram(
        df_partido_unico,
        x='BENS_TOTAIS',
        title=f'Distribuição de Bens para o {partido_selecionado}',
        labels={'BENS_TOTAIS': 'Valor dos Bens Declarados (R$)'},
        range_x=[0, max_range] 
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.caption(f"Obs: O gráfico mostra apenas valores até R$ {max_range:,.2f} (95% dos candidatos) para melhor visualização.")    

col9, col10 = st.columns(2)

with col9:
    st.subheader('📚 Escolaridade entre ELEITOS')
    df_eleitos_escolaridade = df_eleitos_total['GRAU_INSTRUCAO'].value_counts(normalize=True).reset_index()
    df_eleitos_escolaridade.columns = ['GRAU_INSTRUCAO','PERCENTUAL_DO_TOTAL']
    df_eleitos_escolaridade['PERCENTUAL_DO_TOTAL'] *= 100
    df_ordenado = df_eleitos_escolaridade.sort_values('PERCENTUAL_DO_TOTAL', ascending=False)
    fig_pizza_eleitos_escolaridade = px.pie(
        df_ordenado,
        names='GRAU_INSTRUCAO',
        values='PERCENTUAL_DO_TOTAL',
        title='Escolaridade entre candidatos eleitos',
        hole=0.3,
        color = 'GRAU_INSTRUCAO'
    )
    st.plotly_chart(fig_pizza_eleitos_escolaridade, use_container_width=True)

with col10:
    st.subheader('🏛️ Escolaridade entre todos CANDIDATOS')
    df_total_escolaridade = df['GRAU_INSTRUCAO'].value_counts(normalize=True).reset_index()
    df_total_escolaridade.columns = ['GRAU_INSTRUCAO', 'PERCENTUAL_DO_TOTAL']
    df_total_escolaridade['PERCENTUAL_DO_TOTAL']*=100
    fig_pizza_total_escolaridade = px.pie(
        df_total_escolaridade,
        names='GRAU_INSTRUCAO',
        values='PERCENTUAL_DO_TOTAL',
        title='Escolaridade entre todos os candidatos cadastrados',
        hole=0.3,
        color='GRAU_INSTRUCAO'
    )

    st.plotly_chart(fig_pizza_total_escolaridade, use_container_width=True)


st.header("⚖️ Comparativo de Escolaridade: Eleitos vs. Total de Candidatos")


df_eleitos_escolaridade['Tipo'] = 'Eleitos'
df_total_escolaridade['Tipo'] = 'Total de Candidatos'

df_comparativo = pd.concat([df_eleitos_escolaridade, df_total_escolaridade])

fig_comparativo = px.bar(
    df_comparativo,
    x='GRAU_INSTRUCAO',
    y='PERCENTUAL_DO_TOTAL',
    color='Tipo', 
    barmode='group',
    title='Comparativo de Escolaridade: Eleitos vs. Total',
    labels={'GRAU_INSTRUCAO': 'Grau de Instrução', 'PERCENTUAL_DO_TOTAL': 'Percentual (%)'}
)

st.plotly_chart(fig_comparativo, use_container_width=True)

st.markdown("""
        Este gráfico ajuda a ver se certos níveis de escolaridade são mais 'bem-sucedidos' em se eleger do que outros.
                Podemos notar que entre todos que se candidataram, apenas 28% possuiam superior completo, mas entre os que foram eleitos, esse número já representa mais de 38% do total.
                Quanto maior o nível de instrução do candidato, maior a chance dele ser eleito.
        """)

st.header("✊🏽 ✊🏾 ✊🏿 RAÇA")
col11, col12 = st.columns((2,1))

with col11:
    df_melted_cor_espectro = df_cor_espectro.melt(
        id_vars='ESPECTRO_POLITICO',
        value_vars=['tx_pretos_pardos', 'tx_brancos', 'tx_indigenas', 'tx_amarelos'],
        var_name='Raça/cor', value_name='Percentual',
    )
    fig_cor_espectro = px.bar(
            df_melted_cor_espectro,
            x='ESPECTRO_POLITICO',
            y='Percentual',
            title='Percentual de raça/cor por espectro político',
            barmode='stack',
            color='Raça/cor',
            labels={'ESPECTRO_POLITICO':'Espectro político', 'Percentual':'Percentual (%)'}
        )
    st.plotly_chart(fig_cor_espectro, use_container_width=True)
    st.markdown("""
    Entre todos os espectros políticos, os partidos mais a esquerda possuem a maior porcentagem de candidatos pretos e pardos, enquanto a direita tem a maior concentração de brancos.
                Asiáticos, apesar de sempre serem uma extrema minoria, tendem a ser em maior grau de partidos de direita, enquanto indígenas vão para os partidos mais a esquerda.
    """)
   
      
with col12:
    st.subheader("🌍 Destaques da Composição Racial")

    total_pretos_pardos_nacional = (df['COR'].isin(['PRETA', 'PARDA'])).mean() * 100
    total_brancos_nacional = (df['COR'] == 'BRANCA').mean() * 100

    st.markdown("**Média Nacional (Todos os Candidatos):**")
    st.markdown(f"**{total_pretos_pardos_nacional:.1f}%** de Pretos e Pardos")
    st.markdown(f"**{total_brancos_nacional:.1f}%** de Brancos")
    st.markdown("---") 

    espectro_max_pp = df_cor_espectro.loc[df_cor_espectro['tx_pretos_pardos'].idxmax()]
    espectro_max_brancos = df_cor_espectro.loc[df_cor_espectro['tx_brancos'].idxmax()]

    st.metric(
        label="Espectro com Maior % de Pretos/Pardos:",
        value=espectro_max_pp['ESPECTRO_POLITICO'],
        delta=f"{espectro_max_pp['tx_pretos_pardos']:.1f}%"
    )

    st.metric(
        label="Espectro com Maior % de Brancos:",
        value=espectro_max_brancos['ESPECTRO_POLITICO'],
        delta=f"{espectro_max_brancos['tx_brancos']:.1f}%"
    )
    
    st.info("As porcentagens referem-se à composição interna de cada espectro.")
      
st.divider()

col13, col14 = st.columns((2,1))      

with col13:
    st.header("🥇 PARTIDOS VENCEDORES")
    st.subheader("Os 10 partidos com mais candidatos eleitos")
    df_top_10_ordenado = df_top_10_partidos.sort_values('numero_de_eleitos', ascending=True)
    fig_10_mais = px.bar(
        df_top_10_ordenado,
        x= 'PARTIDO',
        y='numero_de_eleitos',
        orientation='h',
        title='10 partido com mais eleitos',
        labels={'PARTIDO':'Partido', 'numero_de_eleitos':'Quantidade de eleitos'},
        color='PARTIDO'
    )
    st.plotly_chart(fig_10_mais, use_container_width=True)


with col14:
    st.subheader("🚀 Métricas Principais")
    partido_campeao = df_top_10_partidos.iloc[0]
    total_eleitos_top_10 = df_top_10_partidos['numero_de_eleitos'].sum()
    total_geral_eleitos = len(df_eleitos_total)
    percentual_concentracao = (total_eleitos_top_10 / total_geral_eleitos) * 100
    st.metric(
        label="Partido com Mais Eleitos:",
        value=partido_campeao['PARTIDO'],
        delta=f"{partido_campeao['numero_de_eleitos']:,}".replace(",", ".") + " eleitos"
    )
    st.markdown("---") 
    st.metric(
        label="Concentração nos Top 10 Partidos:",
        value=f"{percentual_concentracao:.1f}%",
        delta=f"{total_eleitos_top_10:,}".replace(",", ".") + f" de {total_geral_eleitos:,}".replace(",", ".") + " eleitos no total"
    )
    
    st.info("Esta métrica mostra o percentual de todos os cargos eletivos que são ocupados pelos 10 maiores partidos.")

st.header("Tabela de Dados Completa")
st.caption("Todos os registros de candidatura utilizados nas análises.")
st.dataframe(df)    