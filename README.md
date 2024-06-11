# CV Evaluation Tool

## Overview

This tool evaluates candidate CVs against a specified job title using OpenAI's GPT-4 model. It reads CVs from either PDF or DOCX files, constructs a prompt based on the job title and CV content, and requests the OpenAI model to assess the candidate's experience.

## Features

- **Read CV Files**: Supports reading CVs from PDF and DOCX files.
- **Validate Input**: Ensures the job title and CV content meet minimum length requirements.
- **Create Prompt**: Constructs a detailed prompt for the LLM to evaluate the candidate's experience.
- **Evaluate Experience**: Uses OpenAI's GPT-4 to evaluate the CV and return structured JSON output.
- **Export Results**: Saves the evaluation results to a JSON file, appending if the file exists.

## Prerequisites

- Python 3.x
- `openai` library
- `fitz` (PyMuPDF)
- `python-docx`
- OpenAI API key

## Installation

1. **Clone the repository:**
   - git clone https://github.com/SirSicard/LLM-CV-Assessment

2. **Navigate to the project directory:**
   - cd your-repository

3. **Install the required packages:**
   - pip install openai PyMuPDF python-docx


## Usage

1. **Set your OpenAI API key:**
   Replace the placeholder API key in the code with your own OpenAI API key or set it as an environment variable for better security.
   
   - openai.api_key = 'your-api-key-here'

2. **Run the tool:**
   You can run the tool by executing the script. It will prompt you to either use an external CV file or input CV text directly.
   
   - python main.py


3. **Evaluate Experience:**
   - If using a file, provide the path to a PDF or DOCX file containing the candidate's CV.
   - If entering CV text directly, paste the CV content when prompted.

4. **View Results:**
   The evaluation result will be printed in the terminal and saved to a JSON file (`Evaluations.json`).
