from flask import Flask , render_template , request
app = Flask(__name__)
import openai

openai.api_key = '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'


def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def main(user_input: str) -> str:
    prompt_list: list[str] = ['You are a AI chatbot and will answer as a AI',
                              '\nHuman: Who made you?',
                              '\nAI: Soham Chaudhuri']

    # while True:
    # user_input: str = input('You: ')
    response: str = get_bot_response(user_input, prompt_list)
    return response


# if __name__ == '__main__':

#     main()

@app.route('/',methods=["GET","POST"])
def hello_world():
    text="uttam"
    cat="happi happi cat"
    if request.method == "GET":
        return render_template('index.html',text=text)
    if request.method == "POST":
        textbox=request.form['textbox']
        ans=main(textbox)
        return render_template('index.html',text=ans)
    # return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)