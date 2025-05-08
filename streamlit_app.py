import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Dashboard iFood", layout="wide")

st.title("📦 Meu Dashboard do iFood")

# Carrega os dados
df = pd.read_csv("pedidos.csv")

# Converte datas
df["data_pedido"] = pd.to_datetime(df["data_pedido"])
df["ano_mes"] = df["data_pedido"].dt.to_period("M").astype(str)

# Filtros
status_opcao = st.multiselect("Filtrar por status do pedido:", df["status"].unique(), default=list(df["status"].unique()))

df_filtrado = df[df["status"].isin(status_opcao)]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("Total gasto", f"R$ {df_filtrado['valor'].sum():.2f}")
col2.metric("Número de pedidos", len(df_filtrado))
col3.metric("Ticket médio", f"R$ {df_filtrado['valor'].mean():.2f}")

st.markdown("---")

# Gastos por restaurante
gastos_por_restaurante = df_filtrado.groupby("restaurante")["valor"].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(gastos_por_restaurante, x=gastos_por_restaurante.values, y=gastos_por_restaurante.index,
              orientation='h', labels={'x': 'Valor Total (R$)', 'y': 'Restaurante'}, title="Top 10 Restaurantes por Gasto")
st.plotly_chart(fig1, use_container_width=True)

# Gastos por mês
gastos_por_mes = df_filtrado.groupby("ano_mes")["valor"].sum().reset_index()
fig2 = px.line(gastos_por_mes, x="ano_mes", y="valor", markers=True, title="Gastos por Mês")
st.plotly_chart(fig2, use_container_width=True)

# Tabela de pedidos
st.markdown("### Tabela de Pedidos")
st.dataframe(df_filtrado.sort_values("data_pedido", ascending=False).reset_index(drop=True))
