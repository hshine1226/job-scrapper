from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file


app = Flask('JobScrapper')
# Fake Database

db = {}


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/report')
def report():
    word = request.args.get('word')

    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs

    else:
        return redirect('/')

    return render_template('report.html', searchingBy=word, jobs=jobs, resultsNumber=len(jobs))


@app.route('/export')
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()

        save_to_file(jobs, word)
        return send_file(f"{word}.csv", attachment_filename=f"{word}.csv", as_attachment=True)

    except:
        return redirect('/')


if __name__ == '__main__':
    app.run()
