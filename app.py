from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello DevOps World! This is version 2 - AUTOMATED!"

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) so Docker can expose it
    app.run(host='0.0.0.0', port=5000)
