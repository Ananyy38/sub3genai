from taming_llm import LLMClient, create_structured_prompt, extract_section, stream_until_marker, classify_with_confidence, compare_prompt_strategies

def test_complete():
    client_instance = LLMClient()
    prompt_text = "I hate animals"
    result = client_instance.complete(prompt_text)
    print("Complete function result:")
    print(result)

def test_structured_prompt():
    prompt = create_structured_prompt("This is a sample input text.", "What is the main idea?")
    print("Structured prompt:")
    print(prompt)

def test_extract_section():
    sample_completion = """
    # Analysis Report
    ## Input Text
    Sample input.
    ## Question
    What is analyzed?
    ## Analysis
    The analysis result is positive.
    """
    analysis = extract_section(sample_completion, "## Analysis")
    print("Extracted Analysis:")
    print(analysis)

def test_stream_until_marker():
    client_instance = LLMClient()
    prompt_text = "Stream this text until marker. STOP"
    result = stream_until_marker(client_instance.client, client_instance.model, prompt_text, "STOP")
    print("Stream until marker result:")
    print(result)

def test_classify_with_confidence():
    client_instance = LLMClient()
    categories = ["Positive", "Negative", "Neutral"]
    result = classify_with_confidence(client_instance.client, client_instance.model, "The product was great!", categories)
    print("Classification with confidence:")
    print(result)

def test_compare_prompt_strategies():
    categories = ["Positive", "Negative", "Neutral"]
    texts = ["The service was excellent!", "The product did not meet expectations."]
    result = compare_prompt_strategies(texts, categories)
    print("Prompt strategy comparison:")
    print(result)

if __name__ == "__main__":
    test_complete()
    test_structured_prompt()
    test_extract_section()
    test_stream_until_marker()
    test_classify_with_confidence()
    test_compare_prompt_strategies()
