from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
import os

# Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load model and vectorizer
with open('model/sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# DB Model
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        vectorized = vectorizer.transform([text])
        prediction = model.predict(vectorized)[0]
        sentiment = "Positive" if prediction == 1 else "Negative"

        new_analysis = Analysis(text=text, sentiment=sentiment)
        db.session.add(new_analysis)
        db.session.commit()

        return render_template('home.html', sentiment=sentiment, text=text)

    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    analyses = Analysis.query.order_by(Analysis.id.desc()).all()
    return render_template('dashboard.html', analyses=analyses)

@app.route('/delete/<int:id>')
def delete(id):
    analysis = Analysis.query.get_or_404(id)
    db.session.delete(analysis)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
