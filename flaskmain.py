import json
from flask import Flask, render_template_string, request, redirect , url_for, session
import random 
import os 

app = Flask(__name__)
app.secret_key = 'some-secret-key'

# load the questions 
with open('questions.json','r') as f:
    all_questions = json.load(f) 


group_order = ['group1', 'group2', 'group3', 'final']

def get_current_group():
    return group_order[session.get('current_group', 0)]

def get_group_questions(group):
    if group == 'final':
        return all_questions[group]
    if f'{group}_shuffled' not in session:
        q_list = random.sample(all_questions[group], 3)
        session[f'{group}_shuffled'] = q_list
    return session[f'{group}_shuffled']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'current_group' not in session:
        session['current_group'] = 0
        session['q_index'] = 0

    group = get_current_group()
    questions = get_group_questions(group)
    q_index = session['q_index']

    # If all questions in current group are done
    if q_index >= len(questions):
        session['current_group'] += 1
        session['q_index'] = 0
        if session['current_group'] >= len(group_order):
            return render_template_string('''
                <h1>🎉 You defeated Bugathor! 🎉</h1>
                <form action="/reset"><button type="submit">Play Again</button></form>
            ''')
        return redirect(url_for('index'))

    current_question = questions[q_index]

    if request.method == 'POST':
        selected = request.form.get('answer')
        if selected == current_question['answer']:
            session['q_index'] += 1
            return redirect(url_for('index'))
        else:
            return redirect(url_for('game_over'))

    # Render question
    options_html = ''
    for letter, text in current_question['options'].items():
        options_html += f'''
        <form method="POST" style="margin-bottom:10px;">
            <input type="hidden" name="answer" value="{letter}">
            <button type="submit">{letter}. {text}</button>
        </form>
        '''

    html = f'''
    <h1>{current_question['question']}</h1>
    {options_html}
    '''
    return render_template_string(html)

@app.route('/gameover')
def game_over():
    return render_template_string('''
        <h1>💀 Game Over 💀</h1>
        <p>You picked the wrong answer. Bugathor wins... for now.</p>
        <form action="/reset">
            <button type="submit">Try Again</button>
        </form>
    ''')

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
