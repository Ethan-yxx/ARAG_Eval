import re
import pandas as pd
import time
import os
import json
from datetime import datetime
import requests

# Extract JSON content from response text
def extract_quoted_text_json(s: str) -> str:  
    pattern = r'```json(.*?)```'
    match = re.search(pattern, s, re.DOTALL)
    return match.group(1).strip() if match else s

# Updated Prompt Template
PROMPT_TEMPLATE = """You are a macroeconomics expert. Your task is to evaluate five answers to an economics-related question on four dimensions: Domain Relevance, Time Relevance, Analytical Depth, and Information Richness. For each dimension, assign a score ranging from 0 (worst) to 5 (best) based on the criteria provided below. 

Domain Relevance: Evaluate if the information aligns with economic principles and is professional. A score of 5 means the answer is directly related to the economic domain or indicator discussed in the question, while a score of 0 means the answer is unrelated to the specified economic domain or indicators.
Time Relevance: Evaluate if the data and information in the answer match the time frame of the question's indicators. A score of 5 means the answer’s data and information align with the time frame, while 0 means it uses data or information from a different time period.
Information Richness: Evaluate if the answer goes beyond the indicators mentioned in the question and provides more comprehensive information. A score of 5 reflects extensive coverage of the information related to the question, while 0 means the answer lacks relevant information entirely.
Analytical Depth: Evaluate if the answer provides deep insights, complex reasoning, or critical analysis related to the question and its components. A score of 5 means the answer demonstrates significant analytical depth, while 0 means it is superficial or lacks analysis.

Scoring Guideline: Scores between answers must differ by at least 0.5 points, with 0.5 as the minimum scoring interval. Scores cannot be identical across answers in any dimension. 
You do not need to justify your scores. Provide your evaluation in the following JSON format:

```json
{{
  "Answer A": {{
    "Domain Relevance": "<score>",
    "Time Relevance": "<score>",
    "Information Richness": "<score>",
    "Analytical Depth": "<score>"
  }},
  "Answer B": {{
    "Domain Relevance": "<score>",
    "Time Relevance": "<score>",
    "Information Richness": "<score>",
    "Analytical Depth": "<score>"
  }},
  "Answer C": {{
    "Domain Relevance": "<score>",
    "Time Relevance": "<score>",
    "Information Richness": "<score>",
    "Analytical Depth": "<score>"
  }},
  "Answer D": {{
    "Domain Relevance": "<score>",
    "Time Relevance": "<score>",
    "Information Richness": "<score>",
    "Analytical Depth": "<score>"
  }},
  "Answer E": {{
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

# Baidu Wenxin API URL
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k-latest?access_token=" + 'Your Access Token'

class Evaluation:
    def __init__(self) -> None:
        pass

    def evaluate(self, question, answer_a, answer_b, answer_c, answer_d, answer_e):
        prompt = PROMPT_TEMPLATE.format(
            question=question, answer_a=answer_a, 
            answer_b=answer_b, answer_c=answer_c,
            answer_d=answer_d, answer_e=answer_e
        )
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }]
        })

        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            raw_result = json.loads(response.text)
            print("Raw response:", raw_result)
            return extract_quoted_text_json(raw_result.get("result", ""))
        else:
            print("Error:", response.status_code, response.text)
            return None
    

def evaluate_row(row, evaluator):
    question = row['question']
    answer_a = row['gpt4o_response']
    answer_b = row['pp_response']
    answer_c = row['arag_response']
    answer_d = row['arag_response_pre']
    answer_e = row['arag_response_post']
    return evaluator.evaluate(question, answer_a, answer_b, answer_c, answer_d, answer_e)

def process_excel_with_apply(file_path, evaluator, num_runs=5):
    df = pd.read_excel(file_path)

    for i in range(num_runs):
        evaluations = df.apply(lambda row: evaluate_row(row, evaluator), axis=1)
        df[f'Evaluation Results_{i}'] = evaluations

    now = datetime.now()  
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f'./results/evaluated_results_{timestamp}_eb.xlsx'
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

if __name__ == '__main__':
    file_path = './data/arag_results.xlsx'
    evaluator = Evaluation()
    
    # Process the Excel file
    process_excel_with_apply(file_path, evaluator, num_runs=5)