from flask import Flask, render_template, request, url_for, redirect, Response
from sentiment import Sentiment
import emoji
s=Sentiment()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
temp2={}
global var
@app.route("/result", methods=['GET', 'POST'])
def new():
    if request.method=="GET":
        global temp2
        if request.args.get("tweet")!=None:
            tweet=request.args.get("tweet")
            temp2['tweet']=tweet
            print(tweet)
            s.tweet=temp2['tweet']
            var=s.getSentiment()
    return render_template("result.html",tweet=tweet,var=var)
@app.route("/index")
def fun():

    return render_template("index.html")


temp3={}
@app.route("/sample", methods=['GET', 'POST'])
def sample():
    if request.method=="GET":
        global temp3
        if request.args.get("fname")!=None:
            fname=request.args.get("fname")
            temp3['fname']=fname
            print(fname)
            s.fname=temp3['fname']
            s.process()
            pos=s.pos_count
            neg=s.neg_count
            neutral=s.neutral_count
    return render_template("sample.html",fname=fname.upper(),pos=pos,neg=neg,neutral=neutral)


def method_name():
    pass


if __name__ == "__main__":
   
    app.run(debug=True)