import pika
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import HTMLParser, itertools, re
from nltk import word_tokenize
from nltk.corpus import stopwords


cachedStopWords = stopwords.words("english")

def get_sentiment_textblob(text):
    """
    # @param text: blob of text
    # @return list of (sentiment, score) -> ('pos', '0.33')
    """
    blob = TextBlob(str(text))
    score = blob.sentiment.polarity
    # score = '{0:.2f}'.format(blob.sentiment.p_pos - blob.sentiment.p_neg)
    sentiment = "Neutral"
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    print(sentiment, score)
    return [sentiment, score]

def preprocess_text(tweet):
    tweet = tweet.decode("utf8").encode('ascii', 'ignore')
    text = tweet.lower()
    html_parser = HTMLParser.HTMLParser()
    html_parsed_text = html_parser.unescape(text)
    standardized_text = ''.join(''.join(s)[:2] for _,s in itertools.groupby(html_parsed_text))
    cleaned_text = ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",standardized_text).split())
    stemmed_text = ' '.join([word for word in cleaned_text.split() if word not in cachedStopWords])
    return word_tokenize(cleaned_text)

def setup_messaging_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='twitter_mq', durable=True)

    channel.basic_qos(prefetch_count=1)

    return channel
