from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def sell():
	if request.form:
        print(request.form)
	return render_template("sell.html")

if __name__ == '__main__':
	app.run(port=5000,debug=True)