from flask import Flask, render_template, redirect, request, session, make_response,session,url_for, jsonify
import spotipy
import spotipy.util as util
import time
import xlwt
import json
import csv
#from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
sc = StandardScaler()  


database = pd.read_excel("D:/Capstone/Flask_test/dataset/Song_dataset.xls")
user_info = pd.read_csv("D:/Capstone/Flask_test/dataset/user_info.csv")

app = Flask(__name__)
app.secret_key ="Shrijit"
#app.secret_key = SSK


#-------------------------------------------------------------------------
API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

# Set this to True for testing but you probaly want it set to False in production.
SHOW_DIALOG = True

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/User_info"
#db = SQLAlchemy(app)

@app.route('/')
def home():
    #if 'email' in session:
        #return f'Logged in as {session["Email"]}'
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    #error = None
    if request.method == "POST":
        email = request.form["Email"]
        session["email"] = email
        #password = request.form["password"]
        if user_info["Email"].str.contains(email).any():# & user_info["Password"].str.contains(password).any():
            print("Success")
            return redirect(url_for("search"))
        else: 
                return redirect(url_for("info"))        
    else:
        return render_template("login.html")

@app.route("/info",methods = ["POST","GET"])
def info():
    if request.method == "POST":
        name = request.form["name"]
        artist = request.form.getlist("artist")
        genre = request.form["genre"]
        session["artist"] = artist
        session["genre"] = genre
        email = session["email"]
        #session["genre"] = genre
        row = [name,email,genre,artist]
        #row = {"name":name,"email":email,"genres":genre,"artist":artist}
        with open("D:/Capstone/Flask_test/dataset/user_info.csv", "a") as csvFile:
            writer = csv.writer(csvFile)
            #csvFile.write("\n")
            writer.writerow(row)
            # user_info.append(row, ignore_index=True)
            # user_info.to_csv("D:/Capstone/Flask_test/dataset/user_info.csv", index=False)
        csvFile.close()
        return redirect(url_for("search"))
    else:
        return render_template("info.html")


@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "POST":
        song = request.form["search"] 
        # print("WORKING")
        # print(session["artist"])
        return redirect(url_for("content",song = song))
    else:
        print(session["artist"])
        return render_template("search.html", temp = get_artist_songs(session["artist"]))
             

@app.route("/<song>", methods=['GET', 'POST'])
def content(song):  
    found = list(database[database["Tracks"] == song]["uri"])[0]
    recommendation = []
    recommendation = get_recommendations(song, found)
    if recommendation:

        print("ABC")
        return render_template("content.html",Recommendation = recommendation, found = found)#,Track = track,Artist = artist,Uri = uri,Recommendation = recommendation)    
    else:
        print("ERRORONUS")
        return redirect(url_for("search"))
    



  
content_input = database.drop(["Artist","Tracks","uri","Genres","duration_ms"],axis = 1)
content_input[content_input.columns[content_input.dtypes == "float64"].values] = sc.fit_transform(content_input[content_input.columns[content_input.dtypes == "float64"].values])   
content_similarity = cosine_similarity(content_input)
content_similarity_df = pd.DataFrame(content_similarity,index = content_input.index,columns = content_input.index)

def get_recommendations(song, found):
    id = database[database["Tracks"]== song].index.values[0]
    temp = content_similarity_df[id].sort_values(ascending = False).index.values[1:19]
    per = []
    for y in temp:
        x = content_similarity_df.at[y,id]
        per.append(str(x * 100))
    link = list(database.iloc[temp]["uri"])
    #recommendation = set([i +" by " + j + " : " +  k for i,j,k in zip(x,y,z)])
    return zip(link, per)

def get_artist_songs(artist):
    link = []
    for name in artist:
        z = (database[(database['Artist'] == name)].sample(n = 3))["uri"]   
        link.append("https://open.spotify.com/embed/track/" + z)
    return link
    
if __name__ == "__main__":
    app.run(debug = True) 