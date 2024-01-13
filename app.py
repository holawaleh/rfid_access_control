from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, worldpp!"


if __name__ == "__main__":
  print("I dey inside if")
  app.run(host='0.0.0.0', port=8080, debug=True)
