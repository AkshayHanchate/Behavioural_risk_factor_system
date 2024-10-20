from flask import Flask, request, jsonify, abort
import pandas as pd

app = Flask(__name__)

# Load only the first 50 rows of your DataFrame for the API (test with small sample)
df = pd.read_csv('2019.csv')  # First 50 rows for testing

# Define a simple API key for authentication
API_KEY = 'Accessgranted@4463'

@app.route('/data', methods=['GET'])
def fetch_data():
    # Check for API key in headers or query parameters
    api_key = request.headers.get('x-api-key') or request.args.get('api_key')
    if api_key != API_KEY:
        abort(403, description="Forbidden: Invalid API Key")

    # Get the page and page_size parameters (defaults: page=1, page_size=50)
    page = int(request.args.get('page', 1))  # Default to page 1 if not provided
    page_size = int(request.args.get('page_size', 50))  # Default to 50 records per page

    # Calculate the start and end indices for pagination
    start = (page - 1) * page_size
    end = start + page_size

    # Apply pagination to the DataFrame (use df instead of df_5000)
    paginated_data = df.iloc[start:end]

    # If the page exceeds the number of records, return an empty list
    if paginated_data.empty:
        return jsonify([]), 200

    # Convert the paginated data to JSON and return the response
    return jsonify(paginated_data.to_dict(orient='records')), 200


if __name__ == '__main__':
    app.run(debug=True)
