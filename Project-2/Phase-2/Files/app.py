from flask import Flask, render_template, request, jsonify
from flask import Response
app = Flask(__name__)

pub_to_topics = {}
topics_to_subscribers = {'Movies':[], 'Sports':[], 'World': [], 'Politics':[]}
topics_to_content = {'Movies': [], 'Sports':[], 'World':[], 'Politics':[]}

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/selectPubSub', methods=['POST'])
def selectPubSub():
	pubsubtype = request.form['pubsubtype']
	topic = request.form['topic']
	userid = request.form['userid']

	# print(userid)
	if pubsubtype == 'Publisher':
		pub_to_topics[userid] = topic
	else:
		value = topics_to_subscribers[topic]
		if userid not in value:
			topics_to_subscribers[topic].append(userid)
	print(pub_to_topics)
	print(topics_to_subscribers)
	if pubsubtype and topic:
		return jsonify({'pubsubtype' : pubsubtype})

	return jsonify({'error' : 'Missing data!'})

@app.route('/publisher', methods=['POST'])
def publisher():
	content = request.form['content']
	topic = request.form['topic_2']
	topics_to_content[topic].append(content)
	print(topics_to_content)
	if content:
		return jsonify({'content' : content})

	return jsonify({'error' : 'Missing data!'})


@app.route("/stream")
def stream():
	# messages = "abcwddwd"
	# previous_messages = "ab"
	# print('here124')
	# def eventStream():
	# 	print('there1')
	# 	messages = "abcwddwd"
	# 	previous_messages = "ab"
	# 	while True:
	# 		# Pull data from the database
	# 		# and see if there's a new message
	# 		if len(messages) > len(previous_messages):
	# 			print("data: {}\n\n".format(messages[len(messages)-1]))
	# 			yield "data: {}\n\n".format(messages[len(messages)-1])
	userid = request.args['userid']
	print(userid)
	posts_to_be_published = 'data: '
	# posts_to_be_published += '\n'
	for key, value in topics_to_subscribers.items():
		if userid in value:
			posts_to_be_published += 'Topic Name: ' + key + ':' + '  '
			posts_to_be_published += str(topics_to_content[key])
			# posts_to_be_published += '\n'
	posts_to_be_published+='\n\n'
	print(posts_to_be_published)
	return Response(posts_to_be_published, mimetype="text/event-stream")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
