from flask import Flask, render_template, request
import transform
import importrequestv3

app = Flask(__name__)

@app.route("/")
def home():
    opportunties = [] # Fetch and transform data
    
    return render_template("home.html", data=opportunities) 

@app.route("/search") 
def search():
    keyword = request.args.get("keyword") 
    filters = {
        "keyword": keyword  
    }
    
    opportunities = fetch_and_filter(filters) 
    
    return render_template("search.html", data=opportunities) 

def fetch_and_filter(filters):
    
    data = importrequestv3.fetch() 
    opps = transform.process(data)
    
    filtered = apply_filters(opps, filters)
    
    return filtered

if __name__ == "__main__":  
    app.run()