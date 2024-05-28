from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained(
    "Kaludi/Reviews-Sentiment-Analysis", use_auth_token=True)

tokenizer = AutoTokenizer.from_pretrained(
    "Kaludi/Reviews-Sentiment-Analysis", use_auth_token=True)

inputs = tokenizer(
    "I don't feel like you trust me to do my job.", return_tensors="pt")

outputs = model(**inputs)
