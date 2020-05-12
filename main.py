from flask import Flask, render_template, request

app = Flask('JobScrapper')


@app.route('/')
def hello_world():
    return render_template('potato.html')


@app.route('/report')
def report():
    word = request.args.get('word')
    return render_template('report.html', searchingBy=word, potato="sexy")


if __name__ == '__main__':
    app.run()
