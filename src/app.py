from flask import Flask, redirect, render_template, request, send_file
from indeed import get_jobs
from indeed import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        fromDb = db.get(word)
        if fromDb:
            jobs = fromDb
        else:    
            jobs = get_jobs(word)
            db[word] = jobs
    else: redirect("/")
    return render_template("report.html", searchingBy=word, resultNum=len(jobs), jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)