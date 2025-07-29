from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)

# Paste your Logic App's trigger URL
LOGIC_APP_URL = "https://prod-29.centralindia.logic.azure.com:443/workflows/e15fab1c46c64c15a8793e480aa32568/triggers/When_a_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=VnwbzzMdgjEZpZywnjd8D4hqHDlMdd13J7gTpHkg94k"

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        payload = {
            "name": name,
            "email": email,
            "message": message
        }
        requests.post(LOGIC_APP_URL, json=payload)

        return redirect('/thankyou')

    return render_template('feedback.html')

@app.route('/thankyou')
def thankyou():
    return "<h2>Thank you for your feedback!</h2>"

if __name__ == '__main__':
    app.run(debug=True)
