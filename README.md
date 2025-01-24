# Safer-Code

Title: Good Code vs. Bad Code: Use a Classifier or LLM?
Objective: Encourage cleaner, safer code for developers by evaluating classifiers and large language models (LLMs).

Methodology
	1.	Dataset:
	•	Human-evaluated examples from [Microsoft’s dataset](https://github.com/microsoft/NoFunEval).
	•	164 examples labeled as “good” or “bad” code.
	2.	Classifiers Tested:
	•	TF-IDF Vectorizer: Text feature extraction.
	•	Algorithms: Logistic Regression, K-Nearest Neighbors (KNN), Random Forest Classifier (RFC).
	•	Results: Accuracy varies across classifiers, with KNN (k=130) performing best (~55%).
	3.	LLM Evaluation:
	•	Model: GPT-3.5 vs. GPT-4.
	•	Techniques: Prompt engineering, fine-tuned datasets, validation through human input.
	•	Configuration: Adjustments for temperature, token limits, context window, and role.

Insights
	•	Classifiers offer moderate accuracy but struggle with nuanced coding examples.
	•	GPT-4 demonstrates potential for analyzing complex cases, making it suitable for tasks beyond the scope of simple classifiers.

Next Steps
	•	Expand dataset for better model generalization.
	•	Introduce harder examples for robust validation.
	•	Mitigate potential exploitation of obvious cues or biases by LLMs.

Tools and Technologies
	•	Languages: Python
	•	Libraries: Scikit-learn, Flask
	•	Models: OpenAI’s GPT-3.5 and GPT-4
	•	Evaluation Metrics: Precision, Recall, F1-Score, Accuracy
 
<img width="984" alt="Screenshot 2025-01-24 at 2 43 42 PM" src="https://github.com/user-attachments/assets/c9e73287-295c-4231-83ad-b98b0e365d10" />

<img width="983" alt="Screenshot 2025-01-24 at 2 44 36 PM" src="https://github.com/user-attachments/assets/8854fb41-78ec-40dd-acf9-363fde68a4a6" />
