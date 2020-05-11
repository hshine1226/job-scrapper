from flask import Flask
app = Flask('JobScrapper')


@app.route('/')
def hello_world():
    return 'Hello World!~~~'


@app.route('/contact')
def contact():
    return 'this is contact'


if __name__ == '__main__':
    app.run()
