
from flask import Flask, request, render_template_string
import webbrowser
import threading

app = Flask(__name__)

# -----------------------------
# Fake Detection Logic
# -----------------------------
def analyze_username(username):

    username = username.lower()
    score = 0

    numbers = sum(c.isdigit() for c in username)
    underscores = username.count("_")

    if numbers >= 5:
        score += 2

    if underscores >= 3:
        score += 2

    if len(username) <= 3:
        score += 1

    suspicious_words = ["free","giveaway","offer","follow","official123"]

    for word in suspicious_words:
        if word in username:
            score += 3

    risk = min(score * 20,100)

    if risk >= 60:
        result = "⚠️ Suspicious / Possibly Fake"
    else:
        result = "✅ Likely Real Account"

    return result, risk


# -----------------------------
# HTML Page
# -----------------------------
html = """

<html>

<head>

<title>AI Instagram Account Analyzer</title>

<style>

body{
font-family:Arial;
background:white;
text-align:center;
}

.container{
background:#f2f2f2;
padding:40px;
border-radius:10px;
width:360px;
margin:auto;
margin-top:120px;
box-shadow:0 0 10px rgba(0,0,0,0.2);
}

input{
width:90%;
padding:10px;
margin:10px;
border-radius:5px;
border:1px solid #ccc;
}

button{
padding:10px 20px;
background:#4CAF50;
color:white;
border:none;
border-radius:5px;
cursor:pointer;
font-weight:bold;
}

button:hover{
background:#45a049;
}

</style>

</head>

<body>

<div class="container">

<h2>AI Instagram Account Analyzer</h2>

<form method="post">

Enter Instagram Username<br>

<input name="username" required><br>

<button type="submit">Analyze Account</button>

</form>

<h3>{{result}}</h3>

<p>{{risk}}</p>

{% if link %}

<a href="{{link}}" target="_blank">

<button>Open Instagram Profile</button>

</a>

{% endif %}

</div>

</body>

</html>

"""

# -----------------------------
# Main Route
# -----------------------------
@app.route("/",methods=["GET","POST"])
def home():

    result=""
    risk=""
    link=""

    if request.method=="POST":

        username=request.form["username"].strip().replace(" ","")

        result_value, risk_value = analyze_username(username)

        result=result_value
        risk="Risk Score : "+str(risk_value)+"%"

        if risk_value < 60:
            link="https://www.instagram.com/"+username+"/"

    return render_template_string(html,result=result,risk=risk,link=link)


# -----------------------------
# Auto open browser
# -----------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__=="__main__":
    threading.Timer(1,open_browser).start()
    app.run(debug=True)