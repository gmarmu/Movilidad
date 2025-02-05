import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV file
@st.cache_data
def load_data():
    # You can modify the path to point to your CSV file
    df = pd.read_csv('datos_mov_final.csv')
    return df

# Load the data
df = load_data()

# Sidebar filter options
st.sidebar.header("Filtros")

# Filter by column A
unique_A = sorted(df['ANO_ACADEMICO'].unique())
selected_A = st.sidebar.multiselect('Estudiantes graduados en', unique_A, default=unique_A)

# Filter data based on selected values of A
filtered_A_df = df[df['ANO_ACADEMICO'].isin(selected_A)]

# Filter by column B based on the selected A values
unique_B_for_A = filtered_A_df['CENTRO'].unique()

selected_B = st.sidebar.selectbox('Selecciona centro', unique_B_for_A)
#selected_B = unique_B_for_A

# Further filter data based on selected A and B
filtered_df = filtered_A_df[filtered_A_df['CENTRO'].isin([selected_B])]

# Show the filtered dataframe in the main panel (optional)

# Display a boxplot of column C based on the filtered data
st.header("Diferencias de notas medias en movilidad y UAM")
st.text("(Valores por encima de 0 indican mejores notas en movilidad)")

con_puntos = st.checkbox("Mostrar todos puntos de estudiantes",value=True)

plt.figure(figsize=(10, 6))
orden = sorted(set(filtered_df['PLAN']))
ax = sns.boxplot(x='PLAN', y='DIFERENCIA', data=filtered_df, order=orden)
if con_puntos:
    sns.stripplot(x='PLAN', y='DIFERENCIA', data=filtered_df, order=orden)

nn = ["N=" + str(x) for x in filtered_df['PLAN'].value_counts().sort_index().values]
minimo = filtered_df['DIFERENCIA'].min()
for i,n in enumerate(nn):
  ypos = minimo if i%2==0 else minimo+0.3
  ax.text(i,ypos,n,horizontalalignment='center',weight='semibold')

plt.title("Boxplot de diferencia de notas medias en movilidad y UAM")
plt.ylabel("nota media en movilidad - nota media UAM")
plt.xticks(rotation=90)
plt.grid()

# Show the plot
st.pyplot(plt)

#st.write("Datos", filtered_df)
