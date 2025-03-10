# Taming LLMs with Groq API

## Project Description
This project implements a content classification and analysis tool using the Groq API. The tool performs the following:
- Connects to the Groq API via a custom client.
- Generates structured prompts for content analysis.
- Extracts specific sections from the API response.
- Streams responses until a defined marker is reached.
- Classifies text into categories with confidence analysis.
- Compares different prompt strategies for the same classification tasks.

## Features
- **LLM Client:** Manages API interactions with error handling.
- **Structured Completions:** Functions to generate prompts and extract specific sections.
- **Streaming:** Allows real-time response handling until a specified marker.
- **Classification with Confidence:** Computes a confidence score based on log probabilities.
- **Prompt Strategy Comparison:** Framework for testing different prompt strategies (skeleton implementation).

## Prerequisites
- Python 3.x
- Groq API key
- Required Python packages:
  - `python-dotenv`
  - `groq`

## Setup and Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd sub3genai
   ```
2. **Create and Activate a Virtual Environment:**
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
   ```bash
   pip install python-dotenv groq
   ```
4. **Setup Environment Variables:**
   - Create a file named `.env` in the root directory.
   - Use the `.env.example` file as a template.
   - Example content for `.env`:
     ```dotenv
     apigroq=your_api_key_here
     ```

## File Structure
- **part1_llm_client.py:** Contains the LLMClient class for API interactions.
- **part2_structured_completions.py:** Implements functions for structured prompt creation and section extraction.
- **part3_classification.py:** Implements the classification function with confidence analysis.
- **part4_prompt_comparison.py:** Provides a framework for comparing different prompt strategies.
- **taming_llm.py:** Main application file that ties everything together.
- **test_taming_llm.py:** Test script for individual functions.

## Usage
- **Run the Main Application:**
  ```bash
  python taming_llm.py
  ```
- **Run Tests:**
  ```bash
  python test.py
  ```
