from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'hello'

# Needs to be '0.0.0.0' for it to be accessing on host when run on vagrant.
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


