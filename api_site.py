import flask
from flask import request, jsonify
from scrape_data import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Players Records</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/<playerid>', methods=['GET'])
def api_all(playerid):
	url = 'https://stats.espncricinfo.com/ci/engine/player/{}.html?class=1;template=results;type=allround;view=match'.format(playerid)
	record = get_record_by_innings(url,'json')
	return record

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')