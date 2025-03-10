import os
import time
from dotenv import load_dotenv
import groq

class LLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("apigroq")
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"

    def complete(self, prompt, max_tokens=1000, temperature=0):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
def create_structured_prompt(text, question):
    prompt = f"""
    # Analysis Report
    ## Input Text
    {text}
    ## Question
    3
    {question}
    ## Analysis
    """
    return prompt

def extract_section(completion, section_start, section_end=None):
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)
    if section_end is None:
        return completion[start_idx:].strip()
    end_idx = completion.find(section_end, start_idx)
    if end_idx == -1:
        return completion[start_idx:].strip()
    return completion[start_idx:end_idx].strip()

def stream_until_marker(client, model, prompt, stop_marker, max_tokens=1000, temperature=0):
    accumulated_text = ""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        for chunk in response:
            token_text = None
            if hasattr(chunk.choices[0], "message"):
                token_text = chunk.choices[0].message.content
            else:
                token_text = ""
            accumulated_text += token_text
            print(token_text, end="", flush=True)
            if stop_marker in accumulated_text:
                accumulated_text = accumulated_text.split(stop_marker)[0]
                break
        return accumulated_text.strip()
    except Exception as e:
        print(f"Error during streaming: {e}")
        return None
def classify_with_confidence(client, model, text, categories, confidence_threshold=0.8):
    prompt = f"""
    Classify the following text into exactly one of these categories: {', '.join(categories)}.
    4
    Response format:
    1. CATEGORY: [one of: {', '.join(categories)}]
    2. CONFIDENCE: [high|medium|low]
    3. REASONING: [explanation]
    Text to classify:
    {text}
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0,
            logprobs=True,
            top_logprobs=5
        )
    except groq.BadRequestError as e:
        if "logprobs" in str(e):
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0
            )
            confidence_score = 0.5
        else:
            raise e
    completion = response.choices[0].message.content
    category = extract_section(completion, "1. CATEGORY: ", "\n")
    if "logprobs" in response.choices[0].__dict__ and response.choices[0].logprobs:
        logprob_data = response.choices[0].logprobs
        token_logprobs = logprob_data.get("token_logprobs", [])
        if token_logprobs:
            avg_logprob = sum(token_logprobs) / len(token_logprobs)
            confidence_score = max(0, min(1, (avg_logprob + 10) / 10))
        else:
            confidence_score = 0
    if confidence_score > confidence_threshold:
        return {
            "category": category,
            "confidence": confidence_score,
            "reasoning": extract_section(completion, "3. REASONING: ")
        }
    else:
        return {
            "category": "uncertain",
            "confidence": confidence_score,
            "reasoning": "Confidence below threshold"
        }
def compare_prompt_strategies(texts, categories):
    strategies = {
        "basic": lambda text: f"Classify this text into one of these categories: {', '.join(categories)}. Text: {text}",
        "structured": lambda text: f"""
Classification Task
Categories: {', '.join(categories)}
Text: {text}
Classification: """,
        "few_shot": lambda text: f"""
Here are some examples of text classification:
Example 1:
Text: "The product arrived damaged and customer service was unhelpful."
Classification: Negative
Example 2:
Text: "While delivery was slow, the quality exceeded my expectations."
Classification: Mixed
Example 3:
Text: "Absolutely love this! Best purchase I've made all year."
Classification: Positive
Now classify this text:
Text: "{text}"
Classification: """
    }
    results = {}
    for strategy_name, prompt_func in strategies.items():
        strategy_results = []
        for text in texts:
            prompt = prompt_func(text)
            # Implement timing, classification, and confidence measurement
            # Add results to strategy_results
        results[strategy_name] = strategy_results
    return results
