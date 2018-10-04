from flask import Flask, render_template,request,redirect,url_for # For flask implementation  
from bson  import ObjectId # For ObjectId to work  
from pymongo import MongoClient  
import os  
  
app = Flask(__name__)  
title = "USER Information"  
heading = "Store User information"  
  
client = MongoClient("mongodb://127.0.0.1:27017") #host uri  
db = client.mymongodb                             #Select the database  
users = db.user                                   #Select the collection name  

def redirect_url():  
    #redirect
    return request.args.get('next') or request.referrer or url_for('index')  

@app.route("/list")  
def lists ():  
    #List all users
    users_list = users.find()  
    status_list="active"  
    status_info=" "
    return render_template('list.html',a1=a1, a2=a2,users=users_list,t=title,h=heading)

@app.route("/")
def index():
    #Display user addition form
    status_info="active"
    status_list=" "
    return render_template('index.html', a1=a1, a2=a2)

@app.route("/action", methods=['POST'])  
def action ():  
    #Adding a user 
    name=request.values.get("name")  
    email=request.values.get("email")  
    username=request.values.get("username")
    company=request.values.get("company") 
    website=request.values.get("website")
    address=request.values.get("address") 
    about=request.values.get("about")  
    users.insert({ "name":name, 
                   "email":email, 
                   "username": username, 
                   "company":company,
                   "website":website,
                   "address":address,
                   "about":about
                   })  
    return redirect("/list")  

@app.route("/remove")  
def remove ():  
    #Deleting a user with various references  
    key=request.values.get("_id")  
    users.remove({"_id":ObjectId(key)})  
    return redirect("/list")  

@app.route("/update")  
def update ():  
    id=request.values.get("_id")  
    user=users.find({"_id":ObjectId(id)})  
    return render_template('update.html',users=user,h=heading,t=title)

@app.route("/action3", methods=['POST'])  
def action3 ():  
    #Updating a user with various references  
    name=request.values.get("name")  
    email=request.values.get("email")  
    username=request.values.get("username")
    company=request.values.get("company") 
    website=request.values.get("website")
    address=request.values.get("address")   
    about = request.values.get("about")
    id=request.values.get("_id")  
    users.update({"_id":ObjectId(id)},
         {'$set':{ "name":name, 
                   "email":email, 
                   "username": username, 
                   "company":company,
                   "website":website,
                   "address":address,
                   "about":about}})  
    return redirect("/list")    

@app.route("/search", methods=['GET'])  
def search():  
    #Searching a user with various references  
    key=request.values.get("key")  
    refer=request.values.get("refer")  
    users_list = users.find({refer:key})  
    return render_template('searchlist.html',users=users_list,t=title,h=heading)

@app.route("/<username>")
def user_details(username):
    key='username'
    users_list = users.find({key:username})
    return render_template('about.html', users=users_list, t=title, h=heading  )
    


if __name__ == "__main__":  
  
    app.run(debug=True)  
