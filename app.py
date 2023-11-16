from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, surveys 

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'helloworld'

toolbar = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/satisfaction_survey')
def satisfaction_questions():
    session[RESPONSES_KEY] = []
    return redirect("/customer_questions/0")

@app.route("/CS_answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']
    responses = session.get(RESPONSES_KEY, [])
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(surveys['satisfaction'].questions):
        return redirect("/complete")
    else:
        return redirect(f"/customer_questions/{len(responses)}")

@app.route("/customer_questions/<int:qid>")
def show_question(qid):
    survey = surveys['satisfaction']
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if len(responses) != qid:
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/customer_questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("customer_questions.html", question=question)

@app.route('/complete')
def survey_complete():
    return render_template('complete.html')

@app.route('/personality_survey')
def personality_questions():
    return render_template("personality_survey.html")

if __name__ == '__main__':
    app.run(debug=True)