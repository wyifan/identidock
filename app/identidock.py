# need to update pip using pip3 install --upgrade pip
from flask import Flask, Response, request
import requests
import hashlib
import redis

app = Flask(__name__)
salt = "UNIQUE_SALT"
default_name = 'Joe Blogs'
cache = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/hello')
def hello_world():
	return 'Hello Docker!\n'

@app.route('/', methods=['GET','POST'])
def mainpage():
	name = default_name

	if request.method == 'POST':
		name = request.form['name']

	salted_name = salt + name
	name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

	header = '<html><head><title>Identidock</title></head><body>'

	body = '''<form method="POST">
			Hello <input type="text" name="name" value="{}">
			<input type="submit" value="submit">
			</form>
			<p>You look like a:
			<img src="/monster/{}" />
			'''.format(name, name_hash)

	footer = '</body></html>'

	return header + body + footer

@app.route('/monster/<name>')
def get_identicon(name):
	image = cache.get(name)
	
	if image is None:
		print("Cache miss", flush= True)
		r = requests.get("http://dnmonster:8080/monster/" + name + '?size=80')
		image = r.content

		# set to the cache
		cache.set(name, image)

	return Response(image, mimetype='image/png')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
 