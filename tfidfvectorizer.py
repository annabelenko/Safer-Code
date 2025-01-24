import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset
df = pd.read_csv('cwe_data.csv')

# Separate the bad and good code examples
bad_code = df['Bad Code']
safe_code = df['Good Code']

# Create labeled data for classification
data = pd.DataFrame({
    'code': bad_code.tolist() + safe_code.tolist(),
    'label': ['unsafe'] * len(bad_code) + ['safe'] * len(safe_code)
})

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['code'])  # Convert code into feature vectors
y = data['label']  # Target labels

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))