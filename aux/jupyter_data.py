import pandas as pd

df = pd.read_csv("Registro Taller Jupyter matemática.csv.zip")
df["País"] = df["País"].str.rstrip(",.- ").str.title()
df = df.replace(
    {
        float("nan"): None,
        "Salta, Argentina": "Argentina",
        "Wakanda": None,
        "Srgentina": "Argentina",
        "Chil3": "Chile",
        "Mexico": "México",
        "Peru": "Perú",
        "Republica Dominicana": "República Dominicana",
        "Pais Vasco": "España",
        "Canada": "Canadá",
        "Panama": "Panamá",
    }
)

paises = sorted(df["País"].dropna().unique().tolist())
print(f"{len(paises)} países diferentes")
print(", ".join(paises))
