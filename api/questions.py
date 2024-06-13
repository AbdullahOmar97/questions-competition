import requests
from urllib.parse import urlencode

def fetch_questions(amount=None, category=None):
    base_url = "https://opentdb.com/api.php?"
    params = {}

    if amount:
        params['amount'] = amount

    if category:
        params['category'] = category

    url = base_url + urlencode(params)
    response = requests.get(url)
    return response.json()

def handler(request):
    params = request.args

    if 'amount' in params:
        amount = params['amount']
        data = fetch_questions(amount=amount)
        return format_response(data)

    elif 'category' in params:
        category = params['category']
        data = fetch_questions(category=category)
        return format_response(data)

    else:
        return {
            'statusCode': 400,
            'body': "Invalid request. Please specify 'amount' or 'category' parameter."
        }

def format_response(data):
    response_code = data.get('response_code', -1)

    if response_code == 0:
        questions = data.get('results', [])
        formatted_output = []

        for i, question in enumerate(questions):
            formatted_output.append(f"Q{i+1}: {question['question']} A: {question['correct_answer']}")

        return {
            'statusCode': 200,
            'body': "\n".join(formatted_output)
        }
    else:
        return {
            'statusCode': 400,
            'body': f"Error: API returned response code {response_code}"
        }
