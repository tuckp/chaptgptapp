import openai
import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

initialContext = ""

# split the text into a list of sentences with whitespace
sentences = initialContext.split('\n')

# remove whitespace from the beginning and end of each sentence
sentences = [s.strip() for s in sentences]

def get_model_reply(query, context=[]):
    # your secret token goes here
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # combines the new question with a previous context
    context += [query]
    print(context)

    # given the most recent context (4096 characters)
    # continue the text up to 2048 tokens ~ 8192 charaters
    completion = openai.Completion.create(
        engine='text-davinci-003',  # one of the most capable models available
        prompt='\n\n'.join(context)[:4096],
        max_tokens=2048,
        temperature=0.0,  # Lower values make the response more deterministic
    )

    # append response to context
    response = completion.choices[0].text.strip('\n')
    context += [response]

    # list of (user, bot) responses. We will use this format later
    responses = [(u, b) for u, b in zip(context[::2], context[1::2])]

    return responses, context


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    if (request.json.get('query')):
        # get the query from the request
        query = request.json.get('query')

        # get the context from the request
        context = request.json.get('context') or []

        # get the response from the model
        responses, context = get_model_reply(query, context)

        # return the response
        return jsonify({'response': responses[-1][1], 'context': context})
    else:
        return jsonify({'response': 'Error: No query provided'})