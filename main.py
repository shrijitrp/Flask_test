from flask import Flask
from flask import redirect,url_for,render_template,request,flash,session
#from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
sc = StandardScaler()  


database = pd.read_excel("F:/Durham_College_AI/1- semester/Capstone/Song_dataset.xls")
database.drop(["Unnamed: 0"],inplace = True,axis = 1)
user_info = pd.read_csv("F:/Durham_College_AI/1- semester/Capstone/user_info.csv")

app = Flask(__name__)
app.secret_key ="Shrijit"


#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/User_info"
#db = SQLAlchemy(app)


    

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        if user_info["Email"].str.contains(email).any():
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
        return redirect(url_for("search"))
    else:
        return render_template("info.html")


@app.route("/search",methods=["POST","GET"])
def search():
        if request.method == "POST":
            song = request.form["search"] 
            return redirect(url_for("content",song = song))
        else:
            if session["artist"]:
                  return render_template("search.html", temp = get_artist_songs(session["artist"]) )
            else:
                 return render_template("search1.html")
             

@app.route("/<song>")
def content(song): 
    found = database[database['Tracks'].str.match(song)]     
    if not found.empty:
        uri = list(found["uri"])
        track = list(found["Tracks"])
        artist = list(found["Artist"])
        recommendation = get_recommendations(song)
        return render_template("content.html",Track = track,Artist = artist,Uri = uri,Recommendation = recommendation)    
    else:
        return redirect(url_for("search"))
    



  
content_input = database.drop(["Artist","Tracks","uri","Genres","duration_ms"],axis = 1)
content_input[content_input.columns[content_input.dtypes == "float64"].values] = sc.fit_transform(content_input[content_input.columns[content_input.dtypes == "float64"].values])   
content_similarity = cosine_similarity(content_input)
content_similarity_df = pd.DataFrame(content_similarity,index = content_input.index,columns = content_input.index)

def get_recommendations(song):
    id = database[database["Tracks"]== song].index.values[0]
    temp = content_similarity_df[id].sort_values(ascending = False).index.values[1:20]
    x = list(database.iloc[temp]["Tracks"])
    y = list(database.iloc[temp]["Artist"])
    z = list(database.iloc[temp]["uri"])
    recommendation = set([i +" by " + j + " : " +  k for i,j,k in zip(x,y,z)])
    return list(recommendation)

def get_artist_songs(artist):
    recommendation = []
    for name in artist:
        x = (database[(database['Artist'] == name)].sample(n = 3))["Tracks"]
        y = (database[(database['Artist'] == name)].sample(n = 3))["Artist"]
        z = (database[(database['Artist'] == name)].sample(n = 3))["uri"]
        recommendation.append(([i +" by " + j + " : " +  k for i,j,k in zip(x,y,z)]))
    return recommendation


    
if __name__ == "__main__":
    app.run(debug = False) 