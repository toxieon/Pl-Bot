from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Discord Bot OK"

def run():
    app.run(host='0.0.0.0', port=8080)

# Move `keep_alive` outside of `run()`
def keep_alive():
    t = Thread(target=run)
    t.start()
