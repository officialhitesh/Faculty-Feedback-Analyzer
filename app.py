from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
def get_sentiment(text):
    if pd.isna(text) or text.strip() == "":
        return "Neutral"
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

#Scaling the Values to 1-5
feedback_mapping = {
    'Strongly Agree': 5,
    'Agree': 4,
    'Neutral': 3,
    'Disagree': 2,
    'Strongly Disagree': 1
}

#Render Home Page 
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return "No file uploaded", 400

    # Read CSV
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))

    feedback_columns = ['punctuality', 'regularity', 'clarity', 'interactivity',
                        'doubt_solving', 'notes_provided', 'overall_satisfaction']

    # Calculate average scores
    avg_scores = {}
    for col in feedback_columns:
        if col in df.columns:
            numeric_values = df[col].map(feedback_mapping)
            avg_scores[col] = round(numeric_values.mean(), 2)

    # Sentiment analysis
    sentiment_counts = {}
    if 'comment' in df.columns:
        df['Sentiment'] = df['comment'].apply(get_sentiment)
        sentiment_counts = df['Sentiment'].value_counts().to_dict()

    chart_images = {}

    # Generate bar charts
    for col in feedback_columns:
        if col in df.columns:
            plt.figure()
            df[col].value_counts().sort_index().plot(
                kind='bar', color='skyblue')
            plt.title(f"{col.capitalize()} Ratings")
            plt.xlabel("Rating")
            plt.ylabel("Count")
            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            chart_images[col] = "data:image/png;base64," + \
                base64.b64encode(img.getvalue()).decode()
            plt.close()

    # Generate sentiment pie chart
    if sentiment_counts:
        plt.figure()
        plt.pie(sentiment_counts.values(), labels=sentiment_counts.keys(),
                autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
        plt.title("Sentiment Distribution")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_images['sentiment'] = "data:image/png;base64," + \
            base64.b64encode(img.getvalue()).decode()
        plt.close()

    return render_template("report.html",
                           avg_scores=avg_scores,
                           chart_images=chart_images,
                           has_comments=bool(sentiment_counts))


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
