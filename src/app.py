import argparse
import json
import os
from updated_manual_inference import load_static,predict, _execute_query
from flask import Flask, request
from config import read_arguments_manual_inference
app = Flask(__name__)

args = read_arguments_manual_inference()
args.model_to_load = "/Users/shubham.c.sharma/Desktop/sql-project/ValueNet/saved_model/trained_model.pt"
args,model,tokenizer,related_to_concept,is_a_concept, schemas_raw, schemas_dict = load_static(args)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/testing',methods=['GET'])
def testing():
    print("request.args: ", request.args)
    question = request.args['question']

    args.database = request.args['database']
    args.database_path = os.path.join(args.data_dir, "original", "database", args.database, args.database + ".db")
    print(args.database_path)

    result = predict(question,args,model,tokenizer,related_to_concept,is_a_concept, schemas_raw, schemas_dict)
    table, columns = _execute_query(result, args.database_path)

    data = {}
    data['sql'] = result
    data["table"] = table
    data["columns"] = columns
    return data

@app.route('/')
def helloIndex():
    return 'This is insights'


if __name__ == "__main__":
    app.run(debug=True)