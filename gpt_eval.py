import os
import re
import openai
import pandas as pd

def extract_quoted_text_json(s: str) -> str:  
    pattern = r'```json(.*?)```'
    match = re.search(pattern, s, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return s

 
PROMPT_TEMPLATE = """You are a macroeconomics expert. You task is to evaluate five answers to an economic-related question on four dimensions: Domain Relevance， Time Relevance, Analytical Depth, and Information Richness. For each dimension, assign a score ranging from 0 (worst) to 5 (best) based on the criteria provided below. 

Domain Relevance: Assess how closely the answer aligns with the economic indicators or content mentioned in the prompt. A score of 5 means the answer is directly related to the economic domain or indicator discussed in the question, while a score of 0 suggests the answer does not relate to the specified economic domain or indicators at all.
Time Relevance: Evaluate how well the answer aligns with the specific time period or timing mentioned in the question. A score of 5 indicates the answer is perfectly timed or aligned with the temporal aspects of the question, while a score of 0 means the answer does not match the timing or time period specified at all.
Information Richness: Determine the range of relevant information points included in the answer. A score of 5 reflects a comprehensive coverage of the information related to the question. A score of 0 means the answer lacks relevant information entirely.
Analytical Depth: Evaluate the depth of analysis within the answer. A score of 5 means the answer provides deep insights, complex reasoning, or critical analysis of the question and its related components. A score of 0 indicates a very superficial or no analysis.

You do not need to justify your scores.The evaluation must be provided in a JSON format like this:
```json
{{
  "Answer X": {{
    "Domain Relevance": "<score>",
    "Time Relevance": "<score>",
    "Information Richness": "<score>",
    "Analytical Depth": "<score>"
  }}
}}
Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}
Answer C: {answer_c}
Answer D: {answer_d}
Answer E: {answer_e}
"""

class Evaluation:
    def __init__(self, openai_api_key) -> None:
        openai.api_key = openai_api_key

    def evaluate(self, question, answer_a, answer_b, answer_c, answer_d, answer_e):
        prompt = PROMPT_TEMPLATE.format(question=question, answer_a=answer_a, 
                                        answer_b=answer_b, answer_c=answer_c,
                                        answer_d=answer_d, answer_e=answer_e)
        try:
            response = openai.chat.completions.create(
                    model='gpt-3.5-turbo-0125',
                    messages=[{"role": "system", "content": prompt}],
                )
            return extract_quoted_text_json(response.choices[0].message.content)
        except Exception as e:
            print(e)
            return ""

def evaluate_row(row, evaluator):
    # Extract question, answer_a, and answer_b from the row
    question = row['question']
    answer_a = row['copilot_response']
    answer_b = row['pp_response']
    answer_c = row['arag_response']
    answer_d = row['arag_response_pre']
    answer_e = row['arag_response_post']

    # Perform the evaluation using these values
    return evaluator.evaluate(question, answer_a, answer_b, answer_c, answer_d, answer_e)

def process_excel_with_apply(filename, evaluator):
    input_file_path = os.path.join('./data/', filename)
    output_file_path = os.path.join('./results/', filename)

    df = pd.read_excel(input_file_path)

    for i in range(10):  # Adjust based on your needs
        column_name = f'Evaluation Results_{i+1}'
        
        if column_name in df.columns:
            for index, row in df.iterrows():
                if pd.isna(row[column_name]):
                    df.at[index, column_name] = evaluate_row(row, evaluator)
        else:
            evaluations = df.apply(lambda x: evaluate_row(x, evaluator), axis=1)
            df[column_name] = evaluations
    
    df.to_excel(output_file_path, index=False)

if __name__ == '__main__':
    openai_api_key = "your_openai_api_key_here"
    filename = 'arag_results.xlsx'
    evaluator = Evaluation(openai_api_key=openai_api_key)
    
    process_excel_with_apply(filename, evaluator)