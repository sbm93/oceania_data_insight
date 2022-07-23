import argparse
import json
import os
from updated_manual_inference import load_static,predict
from flask import Flask, request
from config import read_arguments_manual_inference
app = Flask(__name__)
##routing

args = read_arguments_manual_inference()
args.model_to_load = "/Users/shubham.c.sharma/Desktop/sql-project/ValueNet/saved_model/trained_model.pt"
args,model,tokenizer,related_to_concept,is_a_concept, schemas_raw, schemas_dict = load_static(args)


@app.route('/testing',methods=['GET'])
def testing():
    args.database = "city_record"
    args.database_path = os.path.join(args.data_dir, "original", "database", args.database, args.database + ".db")
    print(request.args)
    question = request.args['question']
    result = predict(question,args,model,tokenizer,related_to_concept,is_a_concept, schemas_raw, schemas_dict)
    data = {}
    data['sql'] = result
    return data

@app.route('/')
def helloIndex():
    return 'Hello World from DashBoard!'


if __name__ == "__main__":
    app.run(debug=True)