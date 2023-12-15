Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import pandas as pd
... import time
... from google.cloud import language_v1
... from google.cloud.language_v1 import types
... from langdetect import detect
... from google.api_core.exceptions import InvalidArgument
... 
... # IMPORTANT
... # This is the code I used to connected with google's natural language processing
... # It isn't going to run unless you have my json key and cloud access
... # You could probably adapt it for your console? But I am not sure exactly how
... # you might go about doing that. Check all file paths and then for the nlp stuff
... # I do not know. Sorry. 
... 
... client = language_v1.LanguageServiceClient()
... 
...  
... df = pd.read_csv('/home/epaul1/data.csv')
... 
... def annotate_text(text):
...     document = types.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
... 
...     try:
...         response = client.annotate_text(
...             document=document,
...             features={
...                 "extract_syntax": True,
...                 "extract_entities": True,
...                 "extract_document_sentiment": True,
...                 "extract_entity_sentiment": True,
...                 "classify_text": True
...             }
...         )
...         return response
...     except InvalidArgument as e:
...         print(f"Error processing text: {e}")
...         return None
... 
... analysis_results = []
... 
... for index, row in df.iterrows():
...     # 'title' and 'content' columns have to be combined to hit 20 word min
...     text_to_analyze = (str(row['title']) + " " + str(row['content'])).strip()
... 
...     if len(text_to_analyze.split()) < 20:
...         continue  # if not, skip this row
...                     # graceful error handling is just see no evil
... 
...     # figure out the language of the text
    try:
        language = detect(text_to_analyze)
        if language != 'en':
            continue
    except:
        continue  # skip if language detection fails

    annotation = annotate_text(text_to_analyze)
    if annotation is None:
        continue

    # process and store parts annotation
    entities_info = [{'name': entity.name, 'type': entity.type} for entity in annotation.entities]
    syntax_info = [{'token': token.text.content, 'part_of_speech': token.part_of_speech.tag} for token in annotation.tokens]
    classification_info = [{'name': category.name, 'confidence': category.confidence} for category in annotation.categories] if annotation.categories else []
    sentiment_score = annotation.document_sentiment.score
    sentiment_magnitude = annotation.document_sentiment.magnitude

    analysis_results.append({
        'article_id': row['article_id'],
        'sentiment_score': sentiment_score,
        'sentiment_magnitude': sentiment_magnitude,
        'entities': str(entities_info),  
        'syntax': str(syntax_info),      
        'classification': str(classification_info)  
    })

    # with the standard quota limit of 600 queries/min this takes. 13. hours.
    # this code is not reproducable at all and I am so sorry
    # but using google's stuff is a dangerous game because if you don't stay within bounds
    # it gets expensive so fast
    # and I am nowhere near being able to get around their rules
    
    time.sleep(0.1)
    

results_df = pd.DataFrame(analysis_results)

# it's another local file path because she is Large and we don't have enough lfs space in the BEAR repo.
# cannot express how sorry I am for how difficult I have made this for y'all 

results_df.to_csv('/home/epaul1/results_df.csv', index=False)
