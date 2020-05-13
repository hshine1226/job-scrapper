from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_indeed_jobs
from exporter import save_to_file

app = Flask('JobScrapper')
# Fake Database
# 직무 검색을 하게 되면 검색 결과를 데이터베이스에 저장하고, 저장된 결과는 재검색시에 scrapping을 생략한다.
db = {}


@app.route('/')
def hello_world():
    return render_template('potato.html')


@app.route('/report')
def report():
    word = request.args.get('word')

    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            indeed_jobs = existingJobs
        else:
            indeed_jobs = get_indeed_jobs(word)
            db[word] = indeed_jobs

    else:
        return redirect('/')

    return render_template('report.html', searchingBy=word, jobs=indeed_jobs, resultsNumber=len(indeed_jobs))


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
