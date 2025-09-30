import pandas as pd
import google.generativeai as genai
import textwrap

# Configura tu API KEY
GOOGLE_API_KEY = "AIzaSyBaRLhIMkaPOfcvylSODg_YVWVI8PNzPxI"
genai.configure(api_key=GOOGLE_API_KEY)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-2.5-flash")

def to_markdown(text):
    text = text.replace("•", "  *")
    print(textwrap.indent(text, "> ", predicate=lambda _: True))

# Carga datos
df = pd.read_csv("data\\data_prueba.csv", sep=";")

# Selecciona algunos ejemplos para el prompt (por ejemplo, 3 positivos y 3 negativos)
ejemplos = []
columna1 = 'denuncia'#<-- cambiar nombre
columna2 = 'etiqueta'#<-- cambiar nombre
positivos = df[df[columna2] == 1]
negativos = df[df[columna2] == 0]
for _, row in pd.concat([positivos, negativos]).iterrows():
    ejemplos.append(f'Denuncia: "{row[columna1]}"\nRespuesta: {row[columna2]}')

def clasificar_denuncia(denuncia, ejemplos):
    prompt = (
        "Dada la siguiente denuncia, responde solo con 1 si es delito o 0 si no lo es.\n"
        "Ejemplos:\n"
        + "\n\n".join(ejemplos) +
        f"\n\nAhora clasifica esta denuncia:\nDenuncia: \"{denuncia}\"\nRespuesta:"
    )
    response = model.generate_content(prompt)
    return response.text.strip()