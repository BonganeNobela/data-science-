import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample data
texts = [
    "I love this product!",
    "This is the worst experience ever.",
    "I am very happy with the service.",
    "I hate how this works.",
    "Amazing quality, will buy again!",
    "Terrible, never coming back."
]
labels = [1, 0, 1, 0, 1, 0]  # 1 = Positive, 0 = Negative

# Vectorize text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = MultinomialNB()
model.fit(X, labels)

# Save model and vectorizer , we will use this in the flask api 
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved!")
