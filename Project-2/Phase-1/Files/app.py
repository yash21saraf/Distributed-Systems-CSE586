from flask import Flask, render_template, jsonify, request
import subprocess
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/')
def abcd():
    return render_template("index.html")

@app.route('/', methods = ["POST"])
def abcd_abc():

    python_code = request.form['code']
    with open("python_code.py", "w") as file:
        for line in python_code:
            file.write(line)

    with open("output.txt", "w") as file:
        p = Popen(["python", "python_code.py"], stdout=file, stderr=subprocess.PIPE)
        for line in p.stderr:
            file.write(str(line))

    output_string = ''

    with open("output.txt", "r+") as file:
        output_string += file.read()

    with open("output.txt", "w+") as output:
        subprocess.call(["python", "./script.py"], stdout=output);
    return render_template("index.html",result = output_string, pythoncode = python_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
