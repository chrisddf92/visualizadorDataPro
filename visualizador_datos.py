import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")  # Estilo de los gráficos

print("🔥 El script se está ejecutando...")

# 1. Cargar el archivo CSV
def cargar_datos(ruta):
    try:
        df = pd.read_csv(ruta)
        print("✅ Archivo cargado correctamente.")
        return df
    except Exception as e:
        print("❌ Error al cargar el archivo:", e)
        return None

# 2. Mostrar estadísticas básicas
def resumen_datos(df):
    print("\n📊 Vista general del dataset:\n")
    print(df.head())
    print("\n📈 Estadísticas generales:\n")
    print(df.describe())

# 3. Graficar columna según tipo seleccionado
def graficar_columna(df, columna, tipo_grafico):
    if columna not in df.columns:
        print("❌ Columna no encontrada.")
        return

    plt.figure(figsize=(8, 5))

    if pd.api.types.is_numeric_dtype(df[columna]):
        if tipo_grafico == "1":
            sns.histplot(df[columna], kde=True)
            plt.title(f"Distribución de {columna}")
        elif tipo_grafico == "2":
            plt.plot(df[columna])
            plt.title(f"Gráfico de línea de {columna}")
            plt.ylabel(columna)
        else:
            print("⚠️ Opción no válida. Mostrando histograma por defecto.")
            sns.histplot(df[columna], kde=True)
            plt.title(f"Distribución de {columna}")
    else:
        df[columna].value_counts().plot(kind='bar')
        plt.title(f"Frecuencia de valores en {columna}")
        plt.xlabel(columna)
        plt.ylabel("Cantidad")

    plt.tight_layout()
    plt.show()

    guardar = input("💾 ¿Deseas guardar el gráfico como imagen PNG? (s/n): ").lower()
    if guardar == "s":
        nombre_archivo = input("📝 Ingresa el nombre del archivo (sin extensión): ")
        plt.savefig(f"{nombre_archivo}.png")
        print(f"✅ Gráfico guardado como {nombre_archivo}.png")

# 4. Programa principal
def main():
    ruta = input("🗂️ Ingresa la ruta del archivo CSV: ")
    df = cargar_datos(ruta)

    if df is not None:
        resumen_datos(df)

        while True:
            print("\n📚 Columnas disponibles:")
            print(df.columns.tolist())

            columna = input("\n🔍 ¿Qué columna quieres graficar?: ").strip()
            columna = next((c for c in df.columns if c.lower() == columna.lower()), columna)

            print("\n📈 Elige el tipo de gráfico:")
            print("1. Histograma (numérica)")
            print("2. Gráfico de línea (numérica)")
            print("3. Gráfico de barras (categórica)")

            tipo = input("🧭 Opción (1/2/3): ").strip()

            graficar_columna(df, columna, tipo)

            otra = input("\n🔁 ¿Deseas graficar otra columna? (s/n): ").lower()
            if otra != "s":
                print("👋 ¡Gracias por usar el Visualizador de Datos de Christian Duran Dev!")
                break

if __name__ == "__main__":
    main()