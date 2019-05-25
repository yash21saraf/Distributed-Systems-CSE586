import os
from flask import Flask, render_template, request, jsonify
from flask import Response
from pymongo import MongoClient
app = Flask(__name__)

# client = MongoClient('localhost', 27017)

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
db = client.tododb
pub_to_topics = db.pub_to_topics
topics_to_subscribers = db.topics_to_subscribers
topics_to_content = db.topics_to_content

x = pub_to_topics.delete_many({})
x = topics_to_subscribers.delete_many({})
x = topics_to_content.delete_many({})

def populatePubToTopics(publisher_id, current_topic):
    if (pub_to_topics.find_one({"publisher_id": publisher_id})):
        publisherJson = pub_to_topics.find_one({"publisher_id": publisher_id})
        topicsList = publisherJson["topics"]
        if current_topic not in topicsList:
            topicsList.append(current_topic)
            publisherJson["topics"] = topicsList
            pub_to_topics.update_one({"publisher_id": publisher_id}, {"$set":{'topics':topicsList}}, upsert=False)
    else:
        topics = []
        topics.append(current_topic)
        publisherJson = {"publisher_id": publisher_id,
                         "topics": topics}
        result = pub_to_topics.insert_one(publisherJson)


def populateTopicstoSubscribers(current_topic, subscriber_id):
    if (topics_to_subscribers.find_one({"topics": current_topic})):
        topicJson = topics_to_subscribers.find_one({"topics": current_topic})
        subscriberList = topicJson["subscribers"]
        if subscriber_id not in subscriberList:
            subscriberList.append(subscriber_id)
            topicJson["subscribers"] = subscriberList
            topics_to_subscribers.update_one({"topics": current_topic}, {"$set":{'subscribers':subscriberList}}, upsert=False)

    else:
        subscribers = []
        subscribers.append(subscriber_id)
        topicJson = {"topics": current_topic,
                 "subscribers": subscribers}
        result = topics_to_subscribers.insert_one(topicJson)


def populateTopicstoContent(current_topic, message):
    if (topics_to_content.find_one({"topics": current_topic})):
        topicJson = topics_to_content.find_one({"topics": current_topic})
        contentList = topicJson["content"]
        contentList.append(message)
        topicJson["content"] = contentList
        topics_to_content.update_one({"topics": current_topic}, {"$set":{'content':contentList}}, upsert=False)

    else:
        content = []
        content.append(message)
        topicJson = {"topics": current_topic,
                 "content": content}
        result = topics_to_content.insert_one(topicJson)

def subscriberCheckForData(userid):
    content = 'data: '
    for subJson in topics_to_subscribers.find():
        if userid in subJson["subscribers"]:
            contentJson = topics_to_content.find_one({"topics": subJson["topics"]})
            content += 'Topic Name: ' + contentJson["topics"] + ':' + '  '
            content += str(contentJson["content"])
    return content

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/selectPubSub', methods=['POST'])
def selectPubSub():
    pubsubtype = request.form['pubsubtype']
    topic = request.form['topic']
    userid = request.form['userid']

    if pubsubtype == 'Publisher':
        populatePubToTopics(userid, topic)
    else:
        populateTopicstoSubscribers(topic, userid)
    if pubsubtype and topic:
        return jsonify({'pubsubtype' : pubsubtype})

    return jsonify({'error' : 'Missing data!'})

@app.route('/publisher', methods=['POST'])
def publisher():
    content = request.form['content']
    topic = request.form['topic_2']
    populateTopicstoContent(topic , content)
    if content:
        return jsonify({'content' : content})

    return jsonify({'error' : 'Missing data!'})


@app.route("/stream")
def notify():
	userid = request.args['userid']
	# print(userid)
	posts_to_be_published = subscriberCheckForData(userid)
	posts_to_be_published+='\n\n'
	# print(posts_to_be_published)
	return Response(posts_to_be_published, mimetype="text/event-stream")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
