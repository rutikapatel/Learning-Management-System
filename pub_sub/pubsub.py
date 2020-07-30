from google.cloud import pubsub_v1
from flask import Flask, jsonify, request, json
from concurrent.futures import TimeoutError
app = Flask(__name__)

@app.route("/createsubscriber", methods=['POST'])
def createsubscriber():
    project_id = "server-less-277317"
    topic_id = "chatmodule"
    subscription_id = request.form['email']
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    with subscriber:
        subscription = subscriber.create_subscription(subscription_path, topic_path)

@app.route("/publishmessage", methods=['POST'])
def publishmessage():
    message = request.form['message']
    publisher = pubsub_v1.PublisherClient()
    print(message)
    topic_name = 'projects/server-less-277317/topics/chatmodule';
    sample = message
    sample = sample.encode("utf-8");
    publisher.publish(topic_name,sample)
    return "published"

@app.route("/listsubscription", methods=['GET'])
def listsubscription():
    project_id = "server-less-277317"
    subscriber = pubsub_v1.SubscriberClient()
    project_path = subscriber.project_path(project_id)
    subscribers_names = []
    with subscriber:
        for subscription in subscriber.list_subscriptions(project_path):
            subscribers_names.append(str(subscription.name))

@app.route("/pullmessagesbysubscriber", methods=["POST"])
def pullmessagesbysubscriber():
    project_id = "server-less-277317"
    subscription_id = str(request.form['userid'])
    timeout = 5.0
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print("Received message: {}".format(message))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    return "messages retrieved"



if __name__ == '__main__':
   app.run(debug = True, port=5000)
