from flask import Flask, render_template

app = Flask(__name__,static_folder='.', static_url_path='')

@app.route('/')
def home():
    return app.send_static_file('HTML/index.html')

@app.route('/echo/<thing>')
def echo(thing):
    return render_template('HTML/name.html', thing=thing)

app.run(port=9999, debug=True)