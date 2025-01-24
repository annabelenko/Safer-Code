from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import asyncio
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from embedding import get_embedding  # Ensure this is correctly implemented
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("datasets/data.csv")

# Combine left and right prompts with their respective labels
combined_data = pd.DataFrame({
    "prompt": df["classification_left_prompt"].tolist() + df["classification_right_prompt"].tolist(),
    "label": df["classification_left_label"].tolist() + df["classification_right_label"].tolist()
})


# Verify the combined data
print("Combined Data:")
print(combined_data.head())
print("Class Distribution:")
print(combined_data["label"].value_counts())


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
    print("Generating embeddings for combined prompts...")
    combined_data["embeddings"] = await generate_embeddings(combined_data["prompt"])

    # Prepare data
    X = np.array(combined_data["embeddings"].tolist())
    y = combined_data["label"]

    # Split data into training and testing sets with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train the model
    print("Training the model...")
    model = KNeighborsClassifier(n_neighbors=100)
    model.fit(X_train, y_train)

    # Evaluate the model
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    hi_dict = classification_report(y_test, y_pred, output_dict=True)
    file_path = 'classifications.csv'
    report=open(file_path,'a')
    print(hi_dict,file=report)
    for k, data in hi_dict.items():
        print(f'{k} {data}',file=report)

    # Example data for classifiers and their accuracy values
    data = {
        'classifier': ['LogisticReg','RFC', 'KNN (2)','KNN (5)', 'KNN (10)','KNN (20)','KNN (30)','KNN (40)','KNN (100)','KNN (130)'],
        'accuracy': [11, 7, 30,27,33,42,47,45,55,49]
    }

    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    print(df)

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='classifier', y='accuracy')
    plt.title('Accuracy vs Classifiers')
    plt.xlabel('Classifiers')
    plt.ylabel('Accuracy (%)')
    plt.legend(title='NLPs')
    absolute_path = "/Users/ayeshajamal/permProj/outputgraphs"
    plt.savefig(absolute_path, bbox_inches='tight', dpi=300) # save figure
    plt.show() # show figure 
    

    return hi_dict

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())