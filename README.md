<div align="center">
  <h1 align="center">ARAG: Analysis and Retrieval Augmented Generation for Comprehensive Reasoning over Socioeconomic Data (Performance Evaluation)
</h1>
</div>

## Abstract
Recent advancements in Large Language Models (LLMs) have significantly impacted the field of question answering systems, particularly with LLM-based data analysis and Retrieval-Augmented Generation (RAG). Yet, their independent application has limited the scope in scenarios requiring a synthesis of both data analysis and contemporary information retrieval. To bridge this gap, we introduce the Analysis and Retrieval Augmented Generation (ARAG) framework, which blends data analysis with the retrieval of up-to-date information. Based on the framework, we build a system for interpreting the dynamics of socioeconomic indicators and how ARAG explores the reasons behind the indicators' dynamics through data analysis of correlated indicators and retrieval of relevant facts from news sources. The comparison of ARAG with Microsoft Copilot and Perplexity showed that ARAG significantly outperformed in delivering in-depth analytical insights and was remarkably more robust to misinformation across various queries.

## Results
<table border="0" style="border: none;">
  <tr>
    <td>
      <img src="figs/fig4.png" width="500" alt="Chart 1" /><br />
      <em>Comparison of ARAG with Microsoft Copilot and Perplexity.</em>
    </td>
    <td style="padding-left: 20px;">
      <img src="figs/fig5.png" width="500" alt="Chart 2" /><br />
      <em>Ablation study of ARAG.</em>
    </td>
  </tr>
</table>

## Data
- `arag_results.xlsx`: Responses of ARAG, MS Copilot, and Perplexity over 50 queries (Chinese). 
- `arag_results_en.xlsx`: Responses of ARAG, MS Copilot, and Perplexity in English traslated via ERNIE Bot 4.0.
- `negative_sample_results_arag.xlsx`: Responses of ARAG over 20 queries with misleading information.
- `negative_sample_results_copilot.xlsx`: Responses of MS Copilot over 20 queries with misleading information. 
- `negative_sample_results_perplexity.xlsx`: Responses of Perplexity over 20 queries with misleading information. 

## Result Files
- `arag_results.xlsx`: Evaluation results ARAG, MS Copilot, and Perplexity over 50 queries and 10 realizations.
- `average_scores.csv`: Average socres of ARAG, MS Copilot, and Perplexity over 50 queries. 
