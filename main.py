from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = 'bugathor_the_great'

with open('questions.json') as f:
    QUESTIONS = json.load(f)

@app.route('/')
def index():
    # Just render the landing page, don't set question index here
    return render_template('index.html')

@app.route('/start')
def start():
    # This route starts the quiz and resets question index
    session['question_index'] = 0
    return redirect(url_for('question'))

@app.route('/question')
def question():
    idx = session.get('question_index', 0)
    if idx >= len(QUESTIONS):
        return redirect(url_for('final'))
    q = QUESTIONS[idx]
    return render_template('question.html', question=q)

@app.route('/answer', methods=['POST'])
def answer():
    idx = session.get('question_index', 0)
    selected = request.form.get('answer')
    correct = QUESTIONS[idx]['answer']

    if selected == correct:
        session['question_index'] = idx + 1
        return redirect(url_for('question'))
    else:
        return redirect(url_for('gameover'))

@app.route('/gameover')
def gameover():
    return render_template('gameover.html')

@app.route('/final')
def final():
    return render_template('final.html')

if __name__ == '__main__':
    app.run(debug=True)