from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import asyncio
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from embedding import get_embedding  # Ensure this is correctly implemented
from cwe.database import Database  # Import the CWE database

# Function to load and filter CWE data
def load_and_prepare_cwe_data():
    # Initialize the CWE database
    db = Database()
    
    # Load all CWEs
    cwe_list = db.get_all()

    # Prepare the data as a DataFrame
    data = []
    for cwe in cwe_list:
        # Each CWE will serve as a "prompt" with its ID and description
        prompt = f"CWE-{cwe.cwe_id}: {cwe.description}"

        # Assign labels (e.g., 1 for 'good' or safe code, 0 for 'bad' or unsafe code)
        label = 0 if "unsafe" in cwe.description.lower() else 1

        python_examples = []

        if cwe.observed_examples:
            examples = cwe.observed_examples.split(',')
            for example in examples:
                if 'python' in example.lower():
                    python_examples.append(example.strip())
                    print(python_examples)

        if python_examples:
            data.append({
                "prompt": prompt,
                "label": label,
                "python_examples": python_examples
            })

    return pd.DataFrame(data)

# Load CWE data
combined_df = load_and_prepare_cwe_data()

# Verify the combined data
if combined_df.empty:
    raise ValueError("Combined dataset is empty. Ensure the CWE database is accessible.")
print("Combined Dataset:")
print(combined_df.head())
print(f"Number of CWE entries: {len(combined_df)}")

# Asynchronous function to generate embeddings with a progress bar
async def generate_embeddings(prompts):
    embeddings = []
    total_prompts = len(prompts)
    bar_length = 50  # Length of the progress bar

    for i, prompt in enumerate(prompts):
        try:
            # Generate the embedding asynchronously
            embedding = await get_embedding(prompt)
            embeddings.append(embedding)

            # Update the progress bar
            progress = (i + 1) / total_prompts  # Calculate progress as a fraction
            bar = '#' * int(progress * bar_length) + '-' * (bar_length - int(progress * bar_length))
            print(f'\rGenerating Embeddings: [{bar}] {int(progress * 100)}%', end='')  # Progress bar with percentage
        except Exception as e:
            print(f"\nError generating embedding for prompt {i}: {e}")
            embeddings.append(None)  # Add a placeholder for failed embeddings

    print("\nDone!")  # Move to the next line after the progress is complete
    return embeddings

# Async main function
async def main():
    # Ensure the 'prompt' column exists before proceeding
    if "prompt" not in combined_df.columns:
        raise ValueError("'prompt' column is missing in the combined dataset.")

    print("Generating embeddings for combined prompts...")
    combined_df["embeddings"] = await generate_embeddings(combined_df["prompt"])

    # Drop rows with missing embeddings
    combined_df.dropna(subset=["embeddings"], inplace=True)

    # Prepare data
    X = np.array(combined_df["embeddings"].tolist())
    y = combined_df["label"]

    # Split data into training and testing sets with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train the model
    print("Training the model...")
    model = KNeighborsClassifier(n_neighbors=2)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    new_dict = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))
    return new_dict

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())