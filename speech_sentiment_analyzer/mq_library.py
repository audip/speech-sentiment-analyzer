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
    blob = TextBlob(str(text), analyzer=NaiveBayesAnalyzer())
    sentiment = blob.sentiment.classification
    score = '{0:.4f}'.format(blob.sentiment.p_pos - blob.sentiment.p_neg)
    return [sentiment, score]

def preprocess_text(tweet):
    # tweet = tweet.decode("utf8").encode('ascii', 'ignore')
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

    channel.exchange_declare(exchange='twitter_exchange',
                                     type='fanout')

    result = channel.queue_declare(durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='twitter_exchange',
                               queue=queue_name)
    return channel, queue_name
