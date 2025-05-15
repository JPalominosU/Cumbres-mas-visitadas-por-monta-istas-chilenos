import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Cumbres Más Visitadas", layout="wide")

st.title("🏔️ Cumbres Más Visitadas por Montañistas Extranjeros")
st.markdown("""
Este dashboard permite visualizar las estadísticas de las cumbres más visitadas por montañistas extranjeros y chilenos residentes en el extranjero.
Los datos provienen del archivo que has subido.
""")

# Estilo de visualización con Seaborn
sns.set_theme(style="whitegrid")

# Cargar archivo desde el usuario
archivo = st.file_uploader("Sube el archivo de datos (.xlsx)", type=["xlsx"])

if archivo is not None:
    @st.cache_data
    def cargar_datos(archivo):
        # Cargar el archivo
        df = pd.read_excel(archivo)

        # Limpiar datos (eliminar filas con valores nulos en columnas clave)
        df = df.dropna(subset=["Expedición", "N° de Andinista", "Cumbre"])

        return df

    # Cargar y mostrar los datos
    df = cargar_datos(archivo)

    # Filtro por cumbre
    cumbres = sorted(df['Cumbre'].dropna().unique())
    cumbre_sel = st.selectbox("Selecciona una cumbre", cumbres)
    df_filtrado = df[df['Cumbre'] == cumbre_sel]

    # Validación si hay datos para la cumbre seleccionada
    if df_filtrado.empty:
        st.warning(f"No hay datos disponibles para la cumbre '{cumbre_sel}'.")
    else:
        # Mostrar tabla de datos
        st.subheader(f"📊 Datos de la cumbre: {cumbre_sel}")
        st.dataframe(df_filtrado[['Expedición', 'N° de Andinista', 'País']].reset_index(drop=True))

        # Gráfico de visitas por país
        st.subheader("📈 Número de andinistas por país")
        conteo = df_filtrado.groupby("País")["N° de Andinista"].sum().sort_values(ascending=False)

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        conteo.plot(kind='bar', ax=ax, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        ax.set_ylabel("Número de Andinistas")
        ax.set_title(f"Visitas a la cumbre: {cumbre_sel}")
        st.pyplot(fig)

        # Opción para descargar datos filtrados
        st.download_button(
            label="📥 Descargar datos filtrados",
            data=df_filtrado.to_csv(index=False).encode('utf-8'),
            file_name=f'datos_{cumbre_sel}.csv',
            mime='text/csv'
        )

else:
    st.info("Por favor, sube un archivo de datos (.xlsx) para continuar.")
