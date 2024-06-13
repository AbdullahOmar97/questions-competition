import requests
from urllib.parse import parse_qs

def handler(event, context):
    """
    Parameters:
    event (dict): The event data containing request parameters.
    context (object): The context in which the function is called.

    Returns:
    dict: A dictionary containing the HTTP status code and the response body.
    """
    params = event.get('queryStringParameters') or {}
    amount = params.get('amount', '10')
    category = params.get('category')

    # Construct the URL based on the presence of category parameter
    if category:
        url = f"https://opentdb.com/api.php?amount=10&category={category}"
    else:
        url = f"https://opentdb.com/api.php?amount={amount}"

    # Fetch data from Open Trivia Database API
    response = requests.get(url)
    data = response.json()

    # Check if the response contains valid questions
    if data.get("response_code") == 0:
        questions = data.get("results", [])
        question_list = [f"Q{i + 1}: {q['question']} A: {q['correct_answer']}" for i, q in enumerate(questions)]
        return {
            'statusCode': 200,
            'body': "\n".join(question_list)
        }
    else:
        return {
            'statusCode': 400,
            'body': "Error fetching questions"
        }
