# 🚀 Gen AI Orchestrator for Email and Document Triage/Routing

## 📌 Table of Contents
- [Introduction]
- [Inspiration]()
- [What It Does]
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This Project is created based on Generative AI (GenAI) for Orchestrating Emails and Documents Triage/Routing for financial systems.



## 💡 Inspiration
Modern enterprises, especially in the financial sector, receive thousands of emails and documents daily. Manually triaging, classifying, and routing this information is time-consuming and error-prone. Inspired by the need for intelligent automation, we built a solution using Generative AI to streamline this process—minimizing human effort, reducing turnaround time, and improving accuracy in decision-making.

## ⚙️ What It Does
This AI-powered tool automates the triage and routing of emails and documents in financial systems. 
• Extracts key financial data from unstructured content

• Classifies requests by type and urgency

• Detects and flags duplicate or redundant information

• Utilizes Mistral-7B for advanced text understanding and classification

• Helps streamline operations by integrating into existing document workflows

## 🛠️ How We Built It
## 1. Input Handling & Multi-Format Support

• Accepts various document types: PDFs, DOCX, and EML files.

• Pre-processes documents for consistent structure and encoding.

## 2. GenAI-Powered Information Extraction

• Utilizes Mistral-7B with 4-bit quantization for efficient, GPU-optimized inference.

• Extracts relevant financial data and metadata using context-aware prompts.

## 3. Smart Classification Engine

• Classifies emails/documents into request types and subtypes.

• Leverages extracted fields and document intent for accurate routing.

## 4. Duplicate Detection Logic

• Compares extracted fields across documents using similarity scoring.

• Flags potential duplicates to reduce redundancy in processing.

## 5. Structured Output for Integration

• Converts processed data into clean JSON format.

• Enables easy integration with downstream systems or databases.

## 🚧 Challenges We Faced
## Handling Diverse File Formats
Parsing and standardizing content across PDFs, DOCX, and EML files required robust pre-processing logic due to inconsistencies in formatting and metadata structures.

## Model Performance and Optimization
Integrating Mistral-7B with limited compute resources was challenging. We had to use quantization techniques (4-bit) to balance accuracy and performance on available GPUs.

## Data Classification Accuracy
Ensuring high accuracy in classifying request

## 🏃 How to Run
### 🚀 How to Run the Project

1. **Clone the Repository**

```bash
git clone https://github.com/orgs/ewfx/teams/gaied-ai-next-gen-tech
cd gaied-next-gen-tech
```

2. **Install Dependencies**

- For **Python** projects:

```bash
pip install -r requirements.txt
```


3. **Start the Application**

```bash
python main.py
```


## 🏗️ Tech Stack
 
#### 🖥️ Programming Language
- **Python 3.9+**

#### 🧠 AI & NLP
- **Hugging Face Transformers** – for loading and running **Mistral-7B** model  
- **BitsAndBytes** – for 4-bit quantization to run LLM on low-memory GPUs  
- **PyTorch** – backend framework to run the quantized LLM  
- **Mistral-7B-Instruct-v0.1** –

## 👥 Team
## Name : AI-SQUAD
## Members: 
## 1.Suresh Padala
## 2.Ranjana Arjariya
## 3.Garima Raha
## 4.Gangashekar Adumulla