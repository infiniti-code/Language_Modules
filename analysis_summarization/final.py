
import twitter

api = twitter.Api(consumer_key='FZ2CWGMLhRN9dc1NCLvD4Whux',
                 consumer_secret='068Q0CYmNtbtaivPSntWCt40QC5Yu5Ku5AOiw0hB1LJFvay89p',
                 access_token_key='960867938864586753-GDERwMnBFrAeEO1LDGHynH02Fq6JjLa',
                 access_token_secret='979YFk00sn1uOj6PbDQi5fKt4RyB45KpQgWzhCAXoZjUi')

print(api.VerifyCredentials())



def analysis_plot(var):
    def createTestData(search_string):
        try:
            tweets_fetched=api.GetSearch(search_string, count=100)

            print ("Great! We fetched "+str(len(tweets_fetched))+" tweets with the term "+search_string+"!!")

            return [{"text":status.text,"label":None} for status in tweets_fetched]
        except:
            print ("Sorry there was an error!")
            return None

    search_string=input("Hi there! What are we searching for today?")
    testData=createTestData(search_string)

    # Let's try that out





    # In[5]:

    testData[0:9]


    def createTrainingCorpus(corpusFile,tweetDataFile):
        import csv
        corpus=[]
        with open(corpusFile,'rb') as csvfile:
            lineReader = csv.reader(csvfile,delimiter=',',quotechar="\"")
            for row in lineReader:
                corpus.append({"tweet_id":row[2],"label":row[1],"topic":row[0]})

        import time
        rate_limit=180
        sleep_time=900/180

        trainingData=[]
        for tweet in corpus:
            try:
                status=api.GetStatus(tweet["tweet_id"])
                #Returns a twitter.Status object
                print ("Tweet fetched" + status.text)
                tweet["text"]=status.text
                trainingData.append(tweet)
                time.sleep(sleep_time) # to avoid being rate limited
            except:
                continue
        with open(tweetDataFile,'wb') as csvfile:
            linewriter=csv.writer(csvfile,delimiter=',',quotechar="\"")
            for tweet in trainingData:
                try:
                    linewriter.writerow([tweet["tweet_id"],tweet["text"],tweet["label"],tweet["topic"]])
                except Exception as e:
                    print (e)
        return trainingData


    def createLimitedTrainingCorpus(corpusFile,tweetDataFile):
        import csv
        corpus=[]
        with open(corpusFile,'r', encoding="utf8") as csvfile:
            lineReader = csv.reader(csvfile,delimiter=',',quotechar="\"")
            for row in lineReader:
                corpus.append({"tweet_id":row[2],"label":row[1],"topic":row[0]})

        trainingData=[]
        for label in ["positive","negative"]:
            i=1
            for tweet in corpus:
                if tweet["label"]==label and i<=50:
                    try:
                        status=api.GetStatus(tweet["tweet_id"])
                        tweet["text"]=status.text
                        trainingData.append(tweet)
                        i=i+1
                    except Exception as e:
                        print (e)

        with open(tweetDataFile,'wb') as csvfile:
            linewriter=csv.writer(csvfile,delimiter=',',quotechar="\"")
            # We'll add a try catch block here so that we still get the training data even if the write
            # fails
            for tweet in trainingData:
                try:
                    linewriter.writerow([tweet["tweet_id"],tweet["text"],tweet["label"],tweet["topic"]])
                except Exception as e:
                    print (e)
        return trainingData

    corpusFile="C:\\Users\\Praful\\Desktop\\Dataset//corpus.csv"
    tweetDataFile="C:\\Users\\Praful\\Desktop\\Dataset//tweetDataFile.csv"

    trainingData=createLimitedTrainingCorpus(corpusFile,tweetDataFile)
    # This will have saved our 150 tweets to a file and also returned a list with all the tweet data we
    # need for training


    # In[20]:

    # 2b. A class to preprocess all the tweets, both test and training
    # We will use regular expressions and NLTK for preprocessing
    import re
    from nltk.tokenize import word_tokenize
    from string import punctuation
    from nltk.corpus import stopwords


    class PreProcessTweets:
        def __init__(self):
            self._stopwords=set(stopwords.words('english')+list(punctuation)+['AT_USER','URL'])

        def processTweets(self,list_of_tweets):
            # The list of tweets is a list of dictionaries which should have the keys, "text" and "label"
            processedTweets=[]
            # This list will be a list of tuples. Each tuple is a tweet which is a list of words and its label
            for tweet in list_of_tweets:
                processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
            return processedTweets

        def _processTweet(self,tweet):
            # 1. Convert to lower case
            tweet=tweet.lower()
            # 2. Replace links with the word URL
            tweet=re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
            # 3. Replace @username with "AT_USER"
            tweet=re.sub('@[^\s]+','AT_USER',tweet)
            # 4. Replace #word with word
            tweet=re.sub(r'#([^\s]+)',r'\1',tweet)
            tweet=word_tokenize(tweet)
            return [word for word in tweet if word not in self._stopwords]

    tweetProcessor=PreProcessTweets()
    ppTrainingData=tweetProcessor.processTweets(trainingData)
    ppTestData=tweetProcessor.processTweets(testData)



    import nltk
    def buildVocabulary(ppTrainingData):
        all_words=[]
        for (words,sentiment) in ppTrainingData:
            all_words.extend(words)
        wordlist=nltk.FreqDist(all_words)
        # This will create a dictionary with each word and its frequency
        word_features=wordlist.keys()
        # This will return the unique list of words in the corpus
        return word_features

    def extract_features(tweet):
        tweet_words=set(tweet)
        features={}
        for word in word_features:
            features['contains(%s)' % word]=(word in tweet_words)
        return features

    word_features = buildVocabulary(ppTrainingData)
    trainingFeatures=nltk.classify.apply_features(extract_features,ppTrainingData)

    NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)

    # Support Vector Machines
    from nltk.corpus import sentiwordnet as swn
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer


    svmTrainingData=[' '.join(tweet[0]) for tweet in ppTrainingData]
    # Creates sentences out of the lists of words

    vectorizer=CountVectorizer(min_df=1)
    X=vectorizer.fit_transform(svmTrainingData).toarray()
    # We now have a term document matrix
    vocabulary=vectorizer.get_feature_names()

    # Now for the twist we are adding to SVM. We'll use sentiwordnet to add some weights to these
    # features

    swn_weights=[]

    for word in vocabulary:
        try:
            synset=list(swn.senti_synsets(word))
            common_meaning =synset[0]
            if common_meaning.pos_score()>common_meaning.neg_score():
                weight=common_meaning.pos_score()
            elif common_meaning.pos_score()<common_meaning.neg_score():
                weight=-common_meaning.neg_score()
            else:
                weight=0
        except:
            weight=0
        swn_weights.append(weight)


    swn_X=[]
    for row in X:
        swn_X.append(np.multiply(row,np.array(swn_weights)))
    # Convert the list to a numpy array
    swn_X=np.vstack(swn_X)


    labels_to_array={"positive":1,"negative":2}
    labels=[labels_to_array[tweet[1]] for tweet in ppTrainingData]
    y=np.array(labels)

    # Let's now build our SVM classifier
    from sklearn.svm import SVC
    SVMClassifier=SVC()
    SVMClassifier.fit(swn_X,y)


    NBResultLabels=[NBayesClassifier.classify(extract_features(tweet[0])) for tweet in ppTestData]

    # Now SVM
    SVMResultLabels=[]
    for tweet in ppTestData:
        tweet_sentence=' '.join(tweet[0])
        svmFeatures=np.multiply(vectorizer.transform([tweet_sentence]).toarray(),np.array(swn_weights))
        SVMResultLabels.append(SVMClassifier.predict(svmFeatures)[0])





    print(NBResultLabels.count*100)
    if NBResultLabels.count('positive')>NBResultLabels.count('negative'):
        print ("NB Result Positive Sentiment" + str(100*NBResultLabels.count('positive')/len(NBResultLabels))+"%")
    else:
        print ("NB Result Negative Sentiment" + str(100*NBResultLabels.count('negative')/len(NBResultLabels))+"%")




    if SVMResultLabels.count(1)>SVMResultLabels.count(2):
        print ("SVM Result Positive Sentiment" + str(100*SVMResultLabels.count(1)/len(SVMResultLabels))+"%")
    else:
        print ("SVM Result Negative Sentiment" + str(100*SVMResultLabels.count(2)/len(SVMResultLabels))+"%")





    testData[0:10]



    NBResultLabels[0:10]



    SVMResultLabels[0:10]
