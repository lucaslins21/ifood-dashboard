import streamlit as st
import pandas as pd
import plotly.express as px

#configurações da página
st.set_page_config(page_title="Dashboard iFood", layout="wide")

st.title("📦 Meu Dashboard do iFood")

#carrega os dados
df = pd.read_csv("pedidos.csv")

#remove pedidos com status que não interessam
df = df[~df["status"].isin(["DECLINED", "CANCELLED"])]

#converte datas
df["data_pedido"] = pd.to_datetime(df["data_pedido"])
df["ano"] = df["data_pedido"].dt.year
df["ano_mes"] = df["data_pedido"].dt.to_period("M").astype(str)

#filtro por ano
anos_disponiveis = sorted(df["ano"].unique(), reverse=True)
ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis)
df_filtrado = df[df["ano"] == ano_selecionado]

#métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("Total gasto", f"R$ {df_filtrado['valor'].sum():.2f}")
col2.metric("Número de pedidos", len(df_filtrado))
col3.metric("Ticket médio", f"R$ {df_filtrado['valor'].mean():.2f}")

st.markdown("---")

#gráfico: Top restaurantes por gasto
gastos_por_restaurante = df_filtrado.groupby("restaurante")["valor"].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(gastos_por_restaurante, x=gastos_por_restaurante.values, y=gastos_por_restaurante.index,
              orientation='h', labels={'x': 'Valor Total (R$)', 'y': 'Restaurante'}, title="Top 10 Restaurantes por Gasto")
st.plotly_chart(fig1, use_container_width=True)

#gráfico: Gastos por mês
gastos_por_mes = df_filtrado.groupby("ano_mes")["valor"].sum().reset_index()
fig2 = px.line(gastos_por_mes, x="ano_mes", y="valor", markers=True, title="Gastos por Mês")
st.plotly_chart(fig2, use_container_width=True)

#tabela final: oculta colunas irrelevantes
st.markdown("### Tabela de Pedidos")
colunas_para_mostrar = [col for col in df_filtrado.columns if col not in ["id_usuario", "data_registro"]]
st.dataframe(df_filtrado[colunas_para_mostrar].sort_values("data_pedido", ascending=False).reset_index(drop=True))

