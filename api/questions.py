import requests

def handler(request):
    """
    Handle incoming HTTP requests to fetch trivia questions from the Open Trivia Database API.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        dict: A dictionary containing the HTTP status code and the response body.
    """
    params = request.args or {}
    amount = params.get('amount', '10')
    category = params.get('category')

    if category:
        url = f"https://opentdb.com/api.php?amount=10&category={category}"
    else:
        url = f"https://opentdb.com/api.php?amount={amount}"

    response = requests.get(url)
    data = response.json()

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
