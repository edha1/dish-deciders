import pandas as pd 
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import isodate
import re 


#Alvin · Updated 5 years ago

# Food.com - Recipes and Reviews
# Data on over 500,000 recipes and 1,400,000 reviews from Food.com

df = pd.read_csv("recipes.csv") # read in the file 

vectoriser = TfidfVectorizer(stop_words='english', ngram_range=(1,2)) # create vectoriser

# Cleaning the data in the file

# method to clean the text in the data set and inputs to increase reliability (keep only alphanumeric values and whitespaces)
def clean_text(text): 
    if isinstance(text, str):
        text = text.lower()
    else:
        return ''  # or return text, or None, depending on your use case
    text = text.lower()
    text = re.sub("[^a-zA-Z0-9 ]", "", text) 
    return text

# clean the name column: 
def clean_names(text): 
    text = re.sub("[^a-zA-Z0-9 ]", "", text) 
    return text

# the durations are in  ISO 8601 format, so we convert this to minutes
def categorise_prep_time(time): 
    if time < 15: 
        return "Very quick cooking time, less than 15 minutes"
    elif time < 30: 
        return "Quick cooking time, less than 30 minutes"
    elif time < 60: 
        return "Medium cooking time, less than one hour"
    else: 
        return "Long cooking time, more than one hour"

def iso_duration_to_minutes(duration_str):
    # convert to string and strip whitespace (to handle non-string inputs)
    duration_str = str(duration_str).strip()
    
    if duration_str == '' or duration_str.lower() == 'nan':
        # handle empty strings 
        return "Unknown time"
    if '-' in duration_str[2:]:  # skip the 'PT' prefix
        return "Unknown time"
    duration = isodate.parse_duration(duration_str)
    minutes = duration.total_seconds() / 60
    return categorise_prep_time(minutes)

# create a new column for this data 
df['TotalTimeMinutes'] = df['TotalTime'].apply(iso_duration_to_minutes)

# clean the keywords column information (make it a list of words separated by whitespaces to all for vectorisation)
def clean_tags(s):
    if not isinstance(s, str):
        return ''
    s_clean = re.sub(r'^c\(|\)$', '', s) # remove the brackers 
    s_clean = s_clean.replace('"', '') # remove the double quotes 
    s_clean = s_clean.replace(',', '') # replace any commas with spaces
    return s_clean.strip()

df['CleanedKeywords'] = df['Keywords'].apply(clean_tags) # clean the keywords 
df['CleanedIngredients'] = df['RecipeIngredientParts'].apply(clean_tags)
df['CleanedName'] = df['Name'].apply(clean_names)

# have a 'low calories' category 
def categorise_calories(calories): 
    if calories < 2000: 
        return "low calorie"
    else: 
        return "calories"
    
df['CategorisedCalories'] = df['Calories'].apply(categorise_calories)


# create a new column that combines all the words that contribute to finding a recommendation 
df['combined_data'] = (
    df['CleanedKeywords'].apply(clean_text).fillna('') + ' ' +
    df['CategorisedCalories'].apply(clean_text).fillna('') + ' ' +
    df['Description'].apply(clean_text).fillna('') + ' ' +
    df['CleanedIngredients'].apply(clean_text).fillna('') + ' ' +
    df['RecipeCategory'].apply(clean_text).fillna('') + ' ' +
    df['TotalTimeMinutes'].apply(clean_text).fillna('')
)

tfidf = vectoriser.fit_transform(df["combined_data"]) # create the vector for this column

# get recommendations from the user input (text)
def get_recommendations_json(text): 
    text = clean_text(text)
    query_vector = vectoriser.transform([text]) # make tfidf vector for input stream 
    similarity_val = cosine_similarity(query_vector, tfidf).flatten() # get an array of similarity scores 

    # get top 10 similarities 
    indices = np.argpartition(similarity_val, -10)[-10:] 
    results = df.iloc[indices].iloc[::-1]
    
    return results[['CleanedName', 'AuthorName', 'TotalTimeMinutes', 'Calories', 'CleanedIngredients']]





