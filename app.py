import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask,render_template,request

app = Flask(__name__, template_folder="templates")
##################################################

##Step 1: Read CSV File

df = pd.read_csv("movie_dataset.csv")

features = ['keywords','cast','genres','director']

##Step 3: Create a column in DF which combines all selected features
for feature in features:
    df[feature] = df[feature].fillna('')
def combine_features(row):
    try:
        return row["keywords"] + " " + row["cast"] +" "+ row["genres"] +" "+ row["director"]
    except:
        print("Error", row)
df["combine_features"] = df.apply(combine_features,axis=1)

##Step 4: Create count matrix from this new combined column

cv = CountVectorizer()

count_matrix =cv.fit_transform(df["combine_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix

cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

def recommendation(m_name):

    movie_index = get_index_from_title(m_name)

    similar_movies = list(enumerate(cosine_sim[movie_index]))

## Step 7: Get a list of similar movies in descending order of similarity score

    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1],reverse = True)

    return sorted_similar_movies

# ## Step 8: Print titles of first 50 movies
#     i = 0
#     for movie in sorted_similar_movies:
#         print(get_title_from_index(movie[0]))
#         i = i+1
#         if i>50:
#             break


# indices = pd.Series(df.index, index=df['title'])

# all_titles = [df['title'][i] for i in range(len(df['title']))]

# movie_user_likes = 'Avatar'

## Step 6: Get index of this movie from its title



@app.route('/',methods=['GET','POST'])

def main():
    if request.method == 'GET':
        return(render_template('index.html'))
    
    if request.method == 'POST':
        m_name = request.form['search']
        m_name = m_name.capitalize()
        sorted_similar_movies = recommendation(m_name)
        print(sorted_similar_movies)
        i = 0
        my_movies=[]
        for movie in sorted_similar_movies:
            # print(get_title_from_index(movie[0]))
            my_movies.append(get_title_from_index(movie[0]))
            i = i+1
            if i>50:
                break
    return(render_template('positive.html', movie_names=my_movies))

if __name__ == '__main__':
    app.debug = True
    app.run()
