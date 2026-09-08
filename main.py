import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

valores_n = [10, 100, 1000, 10000, 100000]
probabilidad_teorica = 1 / 6
resultados = []

Path("graficos").mkdir(exist_ok=True)
Path("datos").mkdir(exist_ok=True)

for n in valores_n:
    tiradas = np.random.randint(1, 7, size=n)

    for cara in range(1, 7):
        cantidad = np.sum(tiradas == cara)
        frecuencia = cantidad / n
        error = abs(frecuencia - probabilidad_teorica)

        resultados.append({
            "N": n,
            "Cara": cara,
            "Cantidad": int(cantidad),
            "Frecuencia_relativa": frecuencia,
            "Probabilidad_teorica": probabilidad_teorica,
            "Error_absoluto": error
        })

df = pd.DataFrame(resultados)
df.to_csv("datos/resultados.csv", index=False)

for n in valores_n:
    datos_n = df[df["N"] == n]

    plt.figure(figsize=(8, 5))
    plt.bar(datos_n["Cara"], datos_n["Frecuencia_relativa"] * 100)
    plt.axhline(probabilidad_teorica * 100, linestyle="--", label="Valor teórico = 16,67%")
    plt.title(f"Frecuencia relativa de cada cara - N = {n:,}".replace(",", "."))
    plt.xlabel("Cara del dado")
    plt.ylabel("Frecuencia relativa (%)")
    plt.xticks(range(1, 7))
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"graficos/frecuencias_N_{n}.png", dpi=150)
    plt.close()

errores = (
    df.groupby("N")["Error_absoluto"]
    .mean()
    .reset_index()
    .rename(columns={"Error_absoluto": "Error_absoluto_promedio"})
)

errores["Error_absoluto_promedio_porcentaje"] = errores["Error_absoluto_promedio"] * 100
errores.to_csv("datos/errores_promedio.csv", index=False)

plt.figure(figsize=(8, 5))
plt.plot(
    errores["N"],
    errores["Error_absoluto_promedio_porcentaje"],
    marker="o"
)
plt.xscale("log")
plt.title("Disminución del error promedio al aumentar N")
plt.xlabel("Cantidad de tiradas N")
plt.ylabel("Error absoluto promedio (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig("graficos/error_promedio_por_N.png", dpi=150)
plt.close()

print(df.to_string(index=False))
print()
print(errores.to_string(index=False))
