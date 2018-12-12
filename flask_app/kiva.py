from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import json

# load pickle below
lr = joblib.load('kiva_predictor.pkl')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

"""
'language_english', 'description_length', 'loan_amount',
       'loan_use_length', 'currency_usd', 'tags_exist',
       'num_borrowers_female_pct', 'sector_name_Agriculture',
       'sector_name_Arts', 'sector_name_Clothing', 'sector_name_Construction',
       'sector_name_Education', 'sector_name_Entertainment',
       'sector_name_Health', 'sector_name_Housing',
       'sector_name_Manufacturing', 'sector_name_Personal Use',
       'sector_name_Retail', 'sector_name_Services',
       'sector_name_Transportation', 'sector_name_Wholesale',
       'distribution_model_direct', 'distribution_model_field_partner',
       'repayment_interval_bullet', 'repayment_interval_irregular',
       'repayment_interval_weekly'

repayment_interval_monthly
sector_name_Food
distribution_model_field_partner
"""


def process_input(data):
    # initialize the target vector with zero values
    enc_input = np.zeros(26)
    # set the numerical input as they are
    if data['englishyn'] == 'Yes' :
        enc_input[0] = 1
    else:
        enc_input[0] = 0
    enc_input[1] = len(data['description'])
    enc_input[2] = float(data['loanamount'])
    enc_input[3] = len(data['intendeduse'])
    if data['usd'] == 'Yes' :
        enc_input[4] = 1
    else:
        enc_input[4] = 0
    if len(data['hashtags']) > 0 :
        enc_input[5] = 1
    else:
        enc_input[5] = 0
    enc_input[6] = float(data['females']) / (float(data['females']) + float(data['males']))
    if data['sector'] == 'Agriculture':
        enc_input[7] = 1
    else:
        enc_input[7] = 0
    if data['sector'] == 'Arts':
        enc_input[8] = 1
    else:
        enc_input[8] = 0
    if data['sector'] == 'Clothing':
        enc_input[9] = 1
    else:
        enc_input[9] = 0
    if data['sector'] == 'Construction':
        enc_input[10] = 1
    else:
        enc_input[10] = 0
    if data['sector'] == 'Education':
        enc_input[11] = 1
    else:
        enc_input[11] = 0
    if data['sector'] == 'Entertainment':
        enc_input[12] = 1
    else:
        enc_input[12] = 0
    if data['sector'] == 'Health':
        enc_input[13] = 1
    else:
        enc_input[13] = 0
    if data['sector'] == 'Housing':
        enc_input[14] = 1
    else:
        enc_input[14] = 0
    if data['sector'] == 'Manufacturing':
        enc_input[15] = 1
    else:
        enc_input[15] = 0
    if data['sector'] == 'Personal Use':
        enc_input[16] = 1
    else:
        enc_input[16] = 0
    if data['sector'] == 'Retail':
        enc_input[17] = 1
    else:
        enc_input[17] = 0
    if data['sector'] == 'Services':
        enc_input[18] = 1
    else:
        enc_input[18] = 0
    if data['sector'] == 'Transportation':
        enc_input[19] = 1
    else:
        enc_input[19] = 0
    if data['sector'] == 'Wholesale':
        enc_input[20] = 1
    else:
        enc_input[20] = 0
    if data['distribution_model'] == 'Direct':
        enc_input[21] = 1
    else:
        enc_input[21] = 0
    if data['distribution_model'] == 'Field Partner':
        enc_input[22] = 1
    else:
        enc_input[22] = 0
    if data['repayment_interval'] == 'One Time Payement':
        enc_input[23] = 1
    else:
        enc_input[23] = 0
    if data['repayment_interval'] == 'Whenever you can':
        enc_input[24] = 1
    else:
        enc_input[24] = 0
    if data['repayment_interval'] == 'Weekly':
        enc_input[25] = 1
    else:
        enc_input[25] = 0

    return enc_input

@app.route('/api',methods=['POST'])
def get_delay():
    result = request.form
    loanamount = result['loanamount']
    description = result['description']
    intendeduse = result['intendeduse']
    hashtags = result['hashtags']
    females = result['females']
    males = result['males']
    usd = result['usd']
    englishyn = result['englishyn']
    sector = result['sector']
    repayment_interval = result['repayment_interval']
    distribution_model = result['distribution_model']


    data = {'loanamount':loanamount,'description':description,'intendeduse':intendeduse,'hashtags':hashtags,'females':females,	'males':males,'usd':usd,'englishyn':englishyn,'sector':sector,'repayment_interval':repayment_interval,'distribution_model':distribution_model}
    s = process_input(data)
    s = s.reshape(1, -1)
    pred = lr.predict_proba(s)
    pred = np.around((pred[0,1]), 2)
    print (pred)
    string = "There is a (%f) percent chance you will raise the money in 5 days" % pred;
    return string;
    # return render_template('result.html',prediction=price_pred)

if __name__ == "__main__":
    app.run(port=8080, debug=True, use_reloader=False)
