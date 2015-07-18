
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import send_from_directory

# import mongo related things 
# method from donorschoose not working 
# from pymongo import Connection

# method from python_mongo_tutorial
from pymongo import MongoClient

import json
from bson import json_util
from bson.json_util import dumps

# set up connection 
client = MongoClient()

db = client.new_db


# # change routing of logs when running docker 
# logging.basicConfig(stream=sys.stderr) 

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/clustergrammer'

# switch for local and docker development 
# docker_vs_local
##########################################

# for local development 
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/clustergrammer/clustergrammer' ## original 

# # for docker development
# SERVER_ROOT = '/app/clustergrammer'


# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route(ENTRY_POINT + '/<path:path>') ## original 
# @crossdomain(origin='*')
def send_static(path):
  
  return send_from_directory(SERVER_ROOT, path)


@app.route("/clustergrammer/")
def index():
  print('Rendering index template')


  return render_template("index.html")


# Jquery upload file 
############################
@app.route('/clustergrammer/jquery_upload/', methods=['GET','POST'])
def jquery_upload_function():
  import flask 
  import make_exp_clustergram
  import d3_clustergram
  import numpy as np
  
  # # add some database interaction
  # ##################################
  # cursor = db.new_collection.find()

  # # print all documents in database 
  # for doc in cursor:
  #   print(doc)

  # # don't know if I need this 
  # error = None 

  # # python dbeugger
  # ###################
  # import pdb; pdb.set_trace()

  # get the filename 
  inst_filename = flask.request.files['file'].filename
  
  # check that request is a post
  if request.method == 'POST' and allowed_file(inst_filename):

    # read file
    lines = flask.request.files['file'].readlines()

    # initialize dictionary 
    #############################
    network = {}
    network['nodes'] = {}
    network['nodes']['row'] = []
    network['nodes']['col'] = []

    # get the row and column labels and data from lines 
    #####################################################
    for i in range(len(lines)):

      # get inst_line
      inst_line = lines[i].split('\t')

      # strip each element 
      inst_line = [z.strip() for z in inst_line]

      # get column labels from first row 
      if i == 0:
        tmp_col_labels = inst_line

        # add the labels
        for inst_elem in range(len(tmp_col_labels)):

          # skip the first element 
          if inst_elem > 0:
            # get the column label 
            inst_col_label = tmp_col_labels[inst_elem]

            # ignore first element 
            network['nodes']['col'].append(inst_col_label)

      # get row labels 
      if i > 0:

        # save row labels 
        network['nodes']['row'].append(inst_line[0])

        # get data (still strings)
        inst_data_row = inst_line[1:]

        # convert strings to floats 
        inst_data_row = [float(x) for x in inst_data_row]

        # save the row data as an arry 
        inst_data_row =  np.asarray(inst_data_row) 

        # initialize the matrix 
        if i == 1:
          network['data_mat'] = inst_data_row

        # add rows to matrix
        if i > 1:
          network['data_mat'] = np.vstack( (network['data_mat'], inst_data_row) )

    # # check status of matrix   
    # print(network['data_mat'])

    # # convert data_mat to list before exporting as json
    # network['data_mat'] = network['data_mat'].tolist()

    # run make_grammer_clustergram 
    d3_json = make_exp_clustergram.make_grammer_clustergram(network)


    # inst_dict = d3_json

    print(d3_json.keys())
    print(d3_json['links'][0])

    # # make dictionary 
    # inst_dict = {}
    # inst_dict['where'] = [1,1]

    export_dict = d3_json

    inst_dict = {'source': 0, 'target': 0, 'value': -0.79280357071999996}

    # # change numpyfloat to float 
    # export_dict['value'] = float(export_dict['value'])

    export_dict = dict(export_dict)

    print('\n\nexport_dict')
    print(type(export_dict))
    print(export_dict)
    for inst_key in export_dict:
      print(type(export_dict[inst_key]))

    print('\n\n')
    

    print('inst_dict')
    print(type(inst_dict))
    print(inst_dict)
    for inst_key in inst_dict:
      print(type(inst_dict[inst_key]))

    print('\n\n')

    # # # d3_json_export = flask.jsonify(d3_json)
    # d3_json_export = d3_json['row_nodes'][0]

    # print(type(d3_json_export))

    # from bson import Binary, Code
    # from bson.json_util import dumps

    # save json as new collection 
    ##################################
    # db.networks.insert( inst_dict )    
    db.networks.insert( export_dict )    

    # return the network in json form 
    return flask.jsonify(d3_json)

  else:
    print('error in file upload - check filetype')

    return error

  # # return an error if the request is not a post 
  # else:
  #   return 'erorr'



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 