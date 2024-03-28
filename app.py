from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://Astridalifiah:Jaemin@ac-llkhiiw-shard-00-00.kcbmqee.mongodb.net:27017,ac-llkhiiw-shard-00-01.kcbmqee.mongodb.net:27017,ac-llkhiiw-shard-00-02.kcbmqee.mongodb.net:27017/?ssl=true&replicaSet=atlas-uh2qmt-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        { 'num': int(num_receive) },
        { '$set': { 'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route('/delete', methods=['POST'])
def delete_bucket():
    req_data = request.get_json()
    num = req_data['num']
    db.bucket.delete_one({'num': num})
    return jsonify({'msg': 'Item deleted successfully'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)