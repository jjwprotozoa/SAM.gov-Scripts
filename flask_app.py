from flask import Flask, render_template, request
import transform
import importrequestsV4

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=['GET'])
def search():
    keyword = request.args.get("keyword")
    filters = {"keyword": keyword}
    opportunities = fetch_and_filter(filters)
    return render_template("search.html", data=opportunities)

def fetch_and_filter(filters):
    try:
        data = importrequestsV4.fetch_data(api_key, start_date, end_date, limit)  # Adjust the function call as necessary
        opportunities = transform.process_data(data)
        return apply_filters(opportunities, filters)
    except Exception as e:
        print(f"Error in fetching and filtering data: {e}")
        return []

def apply_filters(opportunities, filters):
    # Implement your filtering logic here
    return opportunities

if __name__ == "__main__":
    app.run(debug=True)
