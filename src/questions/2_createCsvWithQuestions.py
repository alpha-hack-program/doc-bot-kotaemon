

# con chatgpt he creado preguntas que parecen mas interesantes para obtener detalles del documento..

import csv

# Define the file path and the data with added explanations
csv_path = "evaluation_questions_with_reasons.csv"

# Data for the CSV with explanations for each question
questions_data_with_reasons = [
    ["Question", "Answer", "Evaluation", "Reason"],
    ["¿En qué grupo y epígrafe de la Ley 2/2020, Anexo I o Anexo II, se sitúa el proyecto?", "", "", 
     "Determinar si el proyecto requiere una evaluación de impacto ambiental simplificada u ordinaria según la clasificación legal."],
    ["¿El proyecto, debido a su naturaleza y el grupo en el que está ubicado, requiere una Evaluación de Impacto Ambiental Simplificada según el Anexo II?", "", "", 
     "Identificar si el proyecto puede optar por el proceso simplificado, que implica menos trámites y un análisis menos detallado."],
    ["¿El proyecto requiere una Evaluación de Impacto Ambiental Ordinaria de acuerdo con los requisitos del Anexo I?", "", "", 
     "Confirmar si el proyecto tiene un impacto significativo y requiere un estudio exhaustivo y detallado de su impacto ambiental."],
    ["¿La actividad del proyecto necesita una Autorización Ambiental Integrada?", "", "", 
     "Verificar si el proyecto debe obtener autorización por sus emisiones, gestión de residuos u otras actividades contaminantes."],
    ["¿En qué epígrafe de la Ley de prevención y control integrados de la contaminación (Real Decreto Legislativo 1/2016) está clasificado el proyecto?", "", "", 
     "Ubicar el proyecto dentro del marco de regulación de la Ley de Prevención y Control Integrado de la Contaminación, para aplicar las normativas correspondientes."],
    ["¿Cuál es la descripción detallada del proyecto?", "", "", 
     "Obtener una visión clara de la actividad y operaciones del proyecto para clasificar correctamente su impacto ambiental."],
    ["¿Qué instalaciones forman parte del proyecto y qué partes se diferencian?", "", "", 
     "Determinar si las distintas partes del proyecto pueden estar sujetas a normativas específicas o requerir evaluaciones separadas."],
    ["¿Qué superficie ocupa el proyecto y cuáles son las áreas afectadas directa o indirectamente?", "", "", 
     "Evaluar la magnitud del proyecto y su impacto en el uso del suelo, biodiversidad y otras características ambientales."]
]

# Write the CSV file with reasons included
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(questions_data_with_reasons)

print(f"CSV file generated: {csv_path}")
