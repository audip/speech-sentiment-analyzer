from setuptools import setup

setup(name='speech_sentiment_analyzer',
      version='1.0',
      description='Sentiment Analyzer for twitter feed to find occurences of hate speech and harassments at events',
      url='https://github.com/audip/speech-sentiment-analyzer',
      author='Aditya Purandare',
      author_email='aditya.p1993@hotmail.com',
      install_requires=['pika','tweepy','nose','HTMLParser','textblob','nltk', 'progressbar', 'pymongo'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
