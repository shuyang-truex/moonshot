from flask import Flask
import os
import socket
import urllib2
from flask import request
import logging

app = Flask(__name__)


@app.route("/")
def hello():
    model_id = request.args.get('model_id', default=1)
    campaign_id = request.args.get('campaign_id', default=1)
    url = "http://scoring-service-{}-{}:8080".format(model_id, campaign_id)
    logging.info(url)
    try:
        content = urllib2.urlopen(url).read()
    except urllib2.URLError, e:
        content = "model does not exist"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>{content}</b>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(),content=content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
