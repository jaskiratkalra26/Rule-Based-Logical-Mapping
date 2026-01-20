# Rule-Based Logical Mapping

## 📌 Project Overview

**Rule-Based Logical Mapping** is a Python-based, deterministic rule engine that converts human-readable textual rules into structured logical conditions. This module forms a critical component of an AI/NLP pipeline — handling text validation, preprocessing, routing decisions, and safety checks before downstream models or retrieval workflows execute.

This project is designed to be **explainable, modular, and easily extendable** with custom rules and metadata, making it ideal for real-world pipelines in Conversational AI, RAG systems, and enterprise NLP solutions.

---

## 🚀 Features

✔ Normalizes and cleans raw text  
✔ Detects and processes semantic intent  
✔ Handles offensive content, PII, and noise removal  
✔ Supports rule metadata for tracing and explainability  
✔ Pipeline-ready for embeddings, retrieval, and LLM usage  

---

## 🧠 What This Solves

- Converts plain English rules into executable Python logic  
- Ensures text is preprocessed safely and consistently  
- Makes decisions on text routing without heavy ML dependencies  
- Enables explainable rule outcomes via structured metadata

---

## 📋 Core Rules Included

| Rule ID | Category | Description |
|---------|----------|-------------|
| R1 | Validation | Ensure text is non-empty |
| R2 | Validation | Ensure text contains at least N words |
| R3 | Intent | Detect if text is a question and classify domain |
| R4 | Text Sanitization | Offensive / abusive word masking |
| R5 | PII Masking | Mask email addresses and phone numbers |
| R6 | Noise Removal | Remove URLs and web artifacts |
| R7 | Normalization | Unicode & whitespace normalization |
| R8 | Sentence Structuring | Sentence boundary segmentation |
| R9 | Chunking | Model-aware token or word chunking |
| R10 | Markup Cleanup | Remove HTML/markup tags |

> ✨ You can extend this list with your own rules using the pattern shown in this project.

---


---

## 🧠 How It Works

1. **Rule Definitions**  
   Each rule is defined with clear textual explanations in `textual_rules.md`.

2. **Logical Functions**  
   Deterministic Python functions implement each rule in `rule_functions.py`.

3. **Metadata Binding**  
   `rule_metadata.py` ties rule IDs, descriptions, categories, and function names for traceability.

4. **Rule Engine**  
   `rule_engine.py` loads rules dynamically and executes them against input text, returning structured results.

---
Rule-Based-Logical-Mapping/
│
├── README.md
│
├── requirements.txt
│
├── rules/
│   ├── __init__.py
│   │
│   ├── textual_rules.md
│   │
│   ├── rule_metadata.py
│   │
│   ├── rule_functions.py
│   │
│   └── rule_engine.py
│
├── examples/
│   ├── __init__.py
│   └── demo.py
│
├── tests/
│   ├── __init__.py
│   └── test_rules.py
│
└── docs/
    └── design_decisions.md


## 🛠 Installation

**Clone the repo:**

```bash
git clone https://github.com/jaskiratkalra26/Rule-Based-Logical-Mapping.git
cd Rule-Based-Logical-Mapping





