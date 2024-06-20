from flask import Flask, Response, render_template, request
import time

app = Flask(__name__)

API_KEY = 'password'
value = None
warning = None
new_message = False

@app.route('/')
def index():
    return render_template('source.html')

@app.route('/events')
def events():
    def generate():
        global new_message
        yield "data: Connected\n\n"  # Send a connection confirmation message
        while True:
            yield f"data: {value}\ndata: {warning}\n\n"
            time.sleep(10)

    return Response(generate(), content_type='text/event-stream')

@app.route('/send', methods=['POST'])
def send():
    global value
    global warning

    if request.form.get('api_key') != API_KEY:
        print("Rejected the message!")
        return Response("Unauthorized", status=401)
    value = request.form.get('message', value)
    warning = request.form.get('warning')

    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
