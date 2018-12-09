from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import json

# load pickle below
#lr = joblib.load('kiva-predictor.pkl')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def make_prediction():
    data = request.get_json(force=True)
    #convert our json to a numpy array
    one_hot_data = input_to_one_hot(data)
    predict_request = gbr.predict([one_hot_data])
    output = [predict_request[0]]
    print(data)
    return jsonify(results=output)

def input_to_one_hot(data):
    # initialize the target vector with zero values
    enc_input = np.zeros(40)
    # set the numerical input as they are
    enc_input[0] = data['English language']
    enc_input[1] = data['Description length']
    enc_input[2] = data['Loan amount']
    enc_input[3] = data['Loan image provided']
    enc_input[4] = data['Loan video provided']
    enc_input[5] = data['Loan use length']
    enc_input[6] = data['Currency exchange coverage rate']
    enc_input[7] = data['USD']
    enc_input[8] = data['Sector']
    enc_input[9] = data['Distribution model field partner']
    enc_input[10] = data['Repayment interval']

    cols = ['age', 'sex', 'urban', 'ssnyn', 'vt', 'histatus', 'ms_1', 'ms_2', 'ms_3', 'ms_4', 'ms_5', 'educ_1', 'educ_2', 'educ_5', 'educ_8', 'educ_9', 'educ_12', 'educ_13', 'pob_0', 'pob_101', 'pob_102', 'pob_103', 'pob_104', 'pob_105', 'pob_106', 'pob_107', 'pob_108','pob_110', 'pob_900', 'esr_1', 'esr_2', 'esr_3', 'esr_4', 'esr_5', 'hitype_0', 'hitype_1', 'hitype_2', 'hitype_3', 'hitype_4', 'hitype_5']
    ##################### MS #########################
    # get the array of ms categories
    ms = ['1', '2', '3', '4', '5']
    # redefine the the user input to match the column name
    redefinded_user_input = 'ms_'+data['ms']
    # search for the index in columns name list
    ms_column_index = cols.index(redefinded_user_input)
    #print(mark_column_index)
    # fullfill the found index with 1
    enc_input[ms_column_index] = 1
    ##################### Education Type ####################
    # get the array of education type
    educ_type = ['1', '2', '5', '8', '9', '12', '13']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'educ_'+data['educ']
    # search for the index in columns name list
    educ_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[educ_column_index] = 1
    ##################### POB ####################
    # get the array of POB type
    pob_type = ['0', '101', '102', '103', '104', '105', '106', '107', '108', '110','900']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'pob_'+data['pob']
    # search for the index in columns name list
    pob_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[pob_column_index] = 1
    ##################### Employment ####################
    # get the array of POB type
    esr_type = ['1', '2', '3', '4', '5']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'esr_'+data['esr']
    # search for the index in columns name list
    esr_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[esr_column_index] = 1
    ##################### Health Insurance Type ####################
    # get the array of HI Type
    hi_type = ['1', '2', '3', '4', '5']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'hitype_'+data['hitype']
    # search for the index in columns name list
    hitype_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[hitype_column_index] = 1
    return enc_input

@app.route('/api',methods=['POST'])
def get_delay():
    result = request.form
    age = result['age']
    sex = result['sex']
    ms = result['ms']
    educ = result['educ']
    pob = result['pob']
    esr = result['esr']
    urban = result['urban']
    ssnyn = result['ssnyn']
    vt = result['vt']
    histatus = result['histatus']
    hitype = result['hitype']

    user_input = {'age':age, 'sex':sex, 'ms':ms, 'educ':educ, 'pob':pob, 'esr':esr, 'urban':urban, 'ssnyn':ssnyn, 'vt':vt, 'histatus':histatus, 'hitype':hitype}

    print(user_input)

    a = input_to_one_hot(user_input)
    a = a.reshape(1, -1)

    mort_pred = lr.predict_proba(a)
    mort_pred = np.around((mort_pred[0,1]), 2)

    return json.dumps({'mort_pred':mort_pred});
    # return render_template('result.html',prediction=price_pred)

if __name__ == "__main__":
    app.run(port=8080, debug=True, use_reloader=False)
