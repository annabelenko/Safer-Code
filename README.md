 # Good Code vs. Bad Code: Classifier or LLM?

## Overview
This project explores the effectiveness of using classifiers versus large language models (LLMs) to distinguish between "good" and "bad" code. The goal is to encourage cleaner and safer code for developers by leveraging AI-powered tools.

## Dataset
We worked with human-evaluated examples from Microsoft’s [dataset](https://github.com/microsoft/NoFunEval), which contains 164 labeled examples of "good" and "bad" code. This dataset formed the basis for training and evaluating our models.

## Methodology
1. **Classifiers**: 
   - We used TF-IDF for feature extraction and tested various algorithms, including Logistic Regression, K-Nearest Neighbors (KNN), and Random Forest Classifier (RFC).
   - The classifiers were evaluated on accuracy, precision, recall, and F1-score. KNN (k=100) performed the best, achieving ~55% accuracy.

2. **LLM Evaluation**:
   - We tested OpenAI’s GPT-3.5 and GPT-4 models.
   - By carefully designing prompts and configuring parameters (e.g., temperature, token limits, context windows), we assessed their ability to analyze and classify code snippets effectively.

## Insights
- GPT-4 stands out for its capability to handle complex and ambiguous cases, making it a strong candidate for this task.

## Next Steps
- Expand the dataset to improve generalization.
- Introduce harder examples to challenge the models.
- Validate that LLMs aren’t relying on superficial cues or biases in the data.

## Tools and Technologies
- **Languages**: Python
- **Libraries**: Scikit-learn, Flask. We also played around with CWE Library
- **Models**: OpenAI GPT-3.5 and GPT-4
- **Evaluation Metrics**: Precision, Recall, F1-Score, Accuracy

## Why It Matters
Encouraging better coding practices is vital for building robust and secure software. By exploring the strengths and weaknesses of classifiers and LLMs, this project aims to provide actionable insights to help developers write cleaner, safer code.
 
<img width="984" alt="Screenshot 2025-01-24 at 2 43 42 PM" src="https://github.com/user-attachments/assets/c9e73287-295c-4231-83ad-b98b0e365d10" />

<img width="983" alt="Screenshot 2025-01-24 at 2 44 36 PM" src="https://github.com/user-attachments/assets/8854fb41-78ec-40dd-acf9-363fde68a4a6" />
