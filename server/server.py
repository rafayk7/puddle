from flask import Flask, render_template

app = Flask(__name__)

@app.route('/deploy')
def deploy():
    title = "RESNET18"
    heading = "RESNET 18 Text NLP Analysis"
    description = "This model does this htis this htis this text classification wowowowoowow"
    usecase = "used for news, news, news, news, news"

    return render_template('text_input_template.html', title=title, heading=heading, description=description, usecase=usecase)

if __name__=="__main__":
    app.run(debug=True)