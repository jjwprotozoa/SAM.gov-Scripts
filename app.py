from flask import Flask, render_template, request
import importrequestsV4  # Handles API requests
import transform  # Processes data

app = Flask(__name__)

@app.route("/")
def home():
    # Display home page
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword", "")  # Get keyword from query parameters
    filters = {"keyword": keyword}

    opportunities = fetch_and_filter(filters)
    return render_template("search.html", data=opportunities)

def fetch_and_filter(filters):
    try:
        # Fetch data from API
        api_data = importrequestsV4.fetch()  
        if not api_data:
            raise ValueError("No data received from API.")

        # Process and filter the data
        processed_data = transform.process_data(api_data)
        filtered_opps = apply_filters(processed_data, filters)
        return filtered_opps
    except Exception as e:
        print(f"Error in fetching and filtering data: {e}")
        return []

def apply_filters(opportunities, filters):
    # Implement your filter logic here
    # For now, it returns all opportunities
    # Example: filter by keyword if specified
    if filters["keyword"]:
        return [opp for opp in opportunities if filters["keyword"].lower() in opp['title'].lower()]
    return opportunities

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development
