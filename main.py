import openai  # Import OpenAI library to interact with the OpenAI API.
import os  # Import os for accessing environment variables and file handling.
import json  # Import json to handle JSON data for input and output.
import logging  # Import logging to record the runtime information, errors, and debug messages.
import fitz  # PyMuPDF for PDF reading
import docx  # docx for Word document reading

# API Key from OpenAI, this can easily be upgraded to use environment variables for a more secure code
openai.api_key = ('Insert API key here')  

# Setup logging configuration.
# Level INFO captures informational messages that highlight the progress of the application.
# The format string includes the timestamp, logging level, and the message, which helps in tracing and debugging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Validates the input data ensuring the job title and CV have sufficient length.
def validate_input(job_title, candidate_cv):
    if not job_title or not candidate_cv or len(job_title) < 3 or len(candidate_cv) < 50:
        logging.error("Invalid input: Job title and CV must be provided with sufficient length.")
        return False
    return True

# Reads the content of a file (PDF or DOCX) and returns the text.
def read_file(file_path): 
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            doc = fitz.open(file_path)
            return ''.join(page.get_text() for page in doc)
        elif ext == '.docx':
            doc = docx.Document(file_path)
            return '\n'.join(para.text for para in doc.paragraphs)
    except Exception as e:
        raise ValueError(f"Failed to read {ext} file: {e}")

# Creates a prompt to be sent to the LLM, combining job title and CV details.
def create_prompt(job_title, candidate_cv):
    return (
        f"Evaluate the following CV for the job offer titled '{job_title}'. "
        "Provide a JSON response with the following information: "
        "1. A numerical score (0-100) based on the relevance of experience. "
        "2. A list of related experiences (Position, Company, Duration). "
        "3. An explanation describing why the score was assigned.\n\n"
        f"Job Offer Title: {job_title}\n\n"
        f"Candidate CV:\n{candidate_cv}\n\n"
        "Ensure the JSON output is well-structured and clearly formatted."
    )

# Evaluates the candidate's experience using the LLM, returning the structured JSON output.

def evaluate_experience(job_title, candidate_cv, model="gpt-4", max_tokens=500, temperature=0.7):
    if not validate_input(job_title, candidate_cv):
        return {"error": "Invalid input: Job title and CV must be provided with sufficient length."}

    try:
        prompt = create_prompt(job_title, candidate_cv)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who evaluates job candidates from a CV."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        evaluation_text = response['choices'][0]['message']['content'].strip()
        logging.info("Response received from LLM.")

        # Log the raw response for debugging
        logging.debug(f"Raw response from LLM: {evaluation_text}")

        # Validate JSON response
        try:
            evaluation_data = json.loads(evaluation_text)
            return evaluation_data
        except json.JSONDecodeError:
            logging.error("Received malformed JSON.")
            return {"error": "Malformed JSON received from LLM."}
    
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": str(e)}

# Exports the evaluation data to a JSON file, appending if the file exists.
def export_to_json(data, filename="Evaluations.json"):
    try:
        if os.path.exists(filename):
            with open(filename, 'r+', encoding='utf-8') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.append(data)
                json_file.seek(0)
                json.dump(existing_data, json_file, ensure_ascii=False, indent=2)
        else:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump([data], json_file, ensure_ascii=False, indent=2)
        logging.info(f"Data successfully exported to {filename}.")
    except Exception as e:
        logging.error(f"Failed to export data to {filename}: {e}")

# Main
if __name__ == "__main__":
    job_title = "Comercial de automóviles"
    choice = input("Do you want to use an external CV file? (yes/no): ").strip().lower()
    if choice == 'yes':
        file_path = input("Enter the full path to the CV file: ").strip()
        try:
            candidate_cv = read_file(file_path)
        except ValueError as e:
            logging.error(e)
            print("Failed to read the file. Please provide a valid .pdf, or .docx file.")
            exit(1)
    else:
        # Input any CV text here or use external CV
        candidate_cv = """
        Candidato: Imad Saidi
        Último Puesto Comercial de automoviles
        Última formación reglada FP 1 / Técnico medio
        Idioma EspañolInglésFrancésEuskeraÁrabe
        imadsaidiyassine57@gmail.com
        634151693
        Localidad 20200 Beasain (Guipúzcoa), España
        Fecha de nacimiento 13 octubre 2002
        DNI 48841750P
        Sexo Hombre
        Experiencia
        Enero 2024 / Febrero 2024
        Comercial de automoviles - Autónomo
        Área FuncionalComercial, Ventas
        Sector de la empresaDistribución Mayorista
        Venta de vehículos nuevos o usados a particulares y empresas ,
        tasaciones … etc. Categoría Infojobs: Gran Cuenta, Comercial
        Octubre 2023 / Marzo 2024
        Vendedor/a de puesto de mercado - Mercadona
        Área FuncionalAtención al cliente
        LIMPIEZA, ARQUEO DE LA CAJA, COLOCACIÓN DE PRODUCTOS EN EL LINEAL,
        CONTROL DE CADUCIDADES, ROTACIÓN DEL PRODUCTO Y COLOCACIÓN DE
        ETIQUETAS. Categoría Infojobs: Atencion A Cliente
        Enero 2020 / Enero 2024
        AUXILIAR DE MANTENIMIENTO INDUSTRIAL - AGRISOLUTIONS
        Área FuncionalMantenimiento, Instalación, Reparación
        Mantenimientos preventivos baja complejidad de las instalaciones.
        Colaboración en el mantenimiento del orden y limpieza en el area de
        trabajo. Categoría Infojobs: Mantenimiento
        Marzo 2023 / Septiembre 2023
        Camarero/a de barra - GASTROTEKA ORDIZIA 1990
        Área FuncionalAtención al cliente
        Sector de la empresaHostelería y Turismo
        Atención al cliente , realizar cobros , atender pedidos telefónicos y
        reservas . Categoría Infojobs: Atencion A Cliente
        Diciembre 2020 / Mayo 2023
        limpieza industrial - ZEREGUIN ZERBITZUAK
        Área Funcional-- Sin Especificar --
        limpieza de superficies horizontales y verticales (pavimentos,
        paredes, azoteas, etc.. Limpieza de maquinaria ,
        Mayo 2020 / Noviembre 2020
        Personal de mantenimiento - Bellota Herramientas
        Área FuncionalIngeniería, Fabricación, Producción
        Mantenimiento y ejecución de maquinaria y zona de trabajo . Traslado
        y orden de zona de trabajo ,mantenimiento básico de la zona de
        trabajo . Verificar disponibilidad y estado de insumos y herramientas
        a utilizar. Categoría Infojobs: Industrial
        Formación reglada
        Finalizada en Marzo 2024
        BUP, Bachillerato y COU
        NivelBUP, Bachillerato y COU
        Estudios finalizadosSí
        Finalizada en Junio 2019
        FP 1 / Técnico medio
        NivelFP 1 / Técnico medio
        Estudios finalizadosSí
        Idiomas
        Comprensión de lectura Expresión oral Expresión escrita
        Inglés Básico (A1) Elemental (A2) Básico (A1)
        Español Avanzado (C1) Experto (C2) Avanzado (C1)
        Francés Medio (B1) Avanzado (C1) Medio (B1)
        Euskera Avanzado (C1) Experto (C2) Avanzado (C1)
        Árabe Avanzado (C1) Experto (C2) Avanzado (C1)
        Conocimientos
        EXPERTO
        Gestión de datos
        Microsoft Word
        Resolución de problemas
        Atención al cliente
        Otros datos
        Origen de alta en ePreselecInscripción proceso - InfoJobs
        Estado de la Política de privacidadAceptada
        """

    result = evaluate_experience(job_title, candidate_cv)
    print("Evaluation Result:", json.dumps(result, indent=2, ensure_ascii=False))

    export_to_json(result)
