# AI-Powered Code Reviewer & Quality Assistant

![Python](https://img.shields.io/badge/Python-3.x-blue)
![AI/NLP](https://img.shields.io/badge/AI-NLP-orange)
![LLM](https://img.shields.io/badge/LLM-Transformer--based-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Open--Source-lightgrey)

## Project Description

AI-Powered Code Reviewer & Quality Assistant is an AI-powered Python application that analyzes Python source code and automatically generates clear, structured, and meaningful docstrings.
The project leverages **transformer-based Large Language Models (LLMs)** to understand code logic and produce high-quality documentation.

The application is built with **Streamlit** to provide an interactive and user-friendly interface, making it suitable for **internship evaluation, professional use, and certification purposes**.

---

## Features

* Automatic generation of Python docstrings
* Analysis of Python functions and logic
* Interactive web-based user interface
* LLM-powered text generation
* Configurable language model support
* Includes unit tests for core components

---

## Techniques Used

### Natural Language Processing (NLP)

* Understanding code semantics using language modeling
* Converting code structure into natural language documentation

### Prompt Engineering

* Carefully designed prompts to guide the LLM for accurate docstring generation
* Context-aware instructions for consistent output

### LLM-based Text Generation

* Uses transformer-based LLMs to generate human-readable docstrings
* Supports configurable LLM backends

---

## Tech Stack

### Programming Language

* Python

### Libraries / Frameworks

* Streamlit
* Requests
* Environment variable management libraries

### AI / ML Technologies

* Natural Language Processing (NLP)
* Large Language Models (LLMs)

---

## LLM Details

* Uses **transformer-based LLMs**
* Default implementation uses **LLaMA** via **Groq API**
* LLM selection is **configurable**, allowing replacement or upgrade of models without changing core logic

---

## Project Structure

```
ai-code-reviewer/
│
├── core/                     # Core application logic
│   ├── docstring_engine/     # LLM-based docstring generation
│   ├── parser/               # Python code parsing logic
│   ├── metrics/              # Code quality and metrics analysis
│   ├── reporter/             # Result and report generation
│   ├── review_engine/        # AI-driven review orchestration
│   ├── validator/            # Docstring and style validation
│   └── __init__.py
│
├── tests/                    # Unit tests for core components
├── examples/                 # Sample Python files
│
├── streamlit_app.py          # Streamlit web application entry point
├── requirements.txt          # Project dependencies
├── env-example.txt           # Environment variable configuration
├── README.md
```

---

## Installation Steps

1. Clone the repository

   ```
   git clone https://github.com/FlashyAdi/ai-code-reviewer.git
   cd ai-code-reviewer
   ```

2. Create and activate a virtual environment (optional but recommended)

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Set the API key as an environment variable

   Linux / macOS:

   ```
   export GROQ_API_KEY="your_api_key_here"
   ```

   Windows:

   ```
   set GROQ_API_KEY=your_api_key_here
   ```

---

## How to Run the Project Locally

```
streamlit run streamlit_app.py
```

After running the command, open the provided local URL in your browser to access the application.

---

## Certification Use Case

This project is suitable for:

* **Infosys Internship / Certification submission**
* Demonstrating practical use of **AI, NLP, and LLMs**
* Showcasing real-world application of prompt engineering and transformer-based models

---

## Author

**Aditya Sharma**

GitHub: [https://github.com/FlashyAdi](https://github.com/FlashyAdi)

---

## License

This project is open-source and intended for educational and internship purposes.
