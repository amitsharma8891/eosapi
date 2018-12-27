import os
import envoy
import subprocess
from flask import current_app, jsonify, request
from flask import Flask
from flask_cors import CORS
import settings
app = Flask(__name__)
CORS(app)


@app.route("/hello")
def hello():
    # subprocess.
    # data = subprocess.call('curl localhost:9000/users/5', stdout=subprocess.PIPE)
    r = envoy.run('curl localhost:9000/users/5')
    print(r.std_out)
    # process = subprocess.run('curl localhost:9000/users/5')
    # print(process)
    # stdout = process.communicate()[0]
    # print('STDOUT:{}'.format(stdout))
    # print(data)
    return ''


@app.route("/setmultisigpermissions",  methods=['POST'])
def setmultisigpermissions():
    content = request.json
    print(content)
    multiSigAccount = content['multisig_account']
    proposer = content['proposer']
    signatory1 = content['signatory1']
    signatory2 = content['signatory2']
    # set for active
    command = """
        cleos --url https://api-kylin.eosasia.one:443 set account permission %s active '{"threshold":2,"keys":[],"accounts":[{"permission":{"actor":"%s","permission":"active"},"weight":1},{"permission":{"actor":"%s","permission":"active"},"weight":1},{"permission":{"actor":"%s","permission":"active"},"weight":1}],"waits":[]}' owner -p %s@owner
    """
    command = command % (multiSigAccount, proposer, signatory1, signatory2, multiSigAccount )
    print(command)
    subprocess.call(command, shell=True)
    #cleos --url https://api-kylin.eosasia.one:443 set account permission mymultisig14 owner '{"threshold":2,"keys":[],"accounts":[{"permission":{"actor":"mcttoken1233","permission":"owner"},"weight":1},{"permission":{"actor":"mcttoken1234","permission":"owner"},"weight":1},{"permission":{"actor":"mcttoken1235","permission":"owner"},"weight":1}],"waits":[]}' -p mymultisig14@owner


    ownerCommand = """
        cleos --url https://api-kylin.eosasia.one:443 set account permission %s owner `{"threshold":2,"keys":[],"accounts":[{"permission":{"actor":"%s","permission":"owner"},"weight":1},{"permission":{"actor":"%s","permission":"owner"},"weight":1},{"permission":{"actor":"%s","permission":"owner"},"weight":1}],"waits":[]}` -p %s@owner
    """
    ownerCommand = ownerCommand % (multiSigAccount, proposer, signatory1, signatory2, multiSigAccount )
    # print(ownerCommand)
    # set for owner
    # r = envoy.run(command)
    # subprocess.call(command, shell=True)
    # print("output", r.std_out)
    return ''


@app.route("/propose",  methods=['POST'])
def propose():
    # cleos --url https://api-kylin.eosasia.one:443 multisig propose electricbill
    # '[{"actor": "mcttoken1234", "permission": "active"},{"actor": "mcttoken1235", "permission": "active"}]'
    # '[{"actor": "mymultisig14", "permission": "active"}]'
    # eosio.token transfer '{"from":"mymultisig14", "to":"mcttoken1233", "quantity":"25.0000 EOS", "memo":"Pay mcttoken1233 some money"}'
    # -p mcttoken1233@active
    content = request.json
    contractName = content['contract_name']
    multiSigAccount = content['multisig_account']
    proposer = content['proposer']
    signatory1 = content['signatory1']
    signatory2 = content['signatory2']
    memo = content['memeo']

    command = """
        cleos --url https://api-kylin.eosasia.one:443 multisig propose %s '[{"actor": "%s", "permission": "active"},{"actor": "%s", "permission": "active"}]' '[{"actor": "%s", "permission": "active"}]' eosio.token transfer '{"from":"%s", "to":"%s", "quantity":"5.0000 EOS", "memo":"%s"}' -p %s@active
    """
    command = command % (contractName, signatory1, signatory2, multiSigAccount, multiSigAccount, proposer, memo, proposer)

    print(command)
    subprocess.call(command, shell=True)
    return ''

@app.route("/review",  methods=['POST'])
def review():
    # cleos --url https://api-kylin.eosasia.one:443  multisig review mcttoken1233 electricbill   --- proposer will only review this
    content = request.json
    proposer = content['proposer']
    contract_name = content['contract_name']
    command = """
        cleos --url https://api-kylin.eosasia.one:443  multisig review %s %s
    """
    command = command % (proposer, contract_name)
    subprocess.call(command, shell=True)
    return ''

@app.route("/approve", methods=['POST'])
def approve():
    # cleos --url https://api-kylin.eosasia.one:443 multisig approve mcttoken1233 electricbill
    # '{"actor": "mcttoken1234", "permission": "active"}' -p mcttoken1234@active

    content = request.json
    proposer = content['proposer']
    contract_name = content['contract_name']
    signatory = content['signatory']

    command = """
           cleos --url https://api-kylin.eosasia.one:443 multisig approve %s %s `{"actor": "%s", "permission": "active"}` -p %s@active
       """
    command = command % (proposer, contract_name, signatory, signatory)
    subprocess.call(command, shell=True)

    return ''


@app.route("/execute", methods=['POST'])
def execute():
    #cleos --url https://api-kylin.eosasia.one:443 multisig exec mcttoken1233 electricbill -p mcttoken1233@active

    content = request.json
    proposer = content['proposer']
    contract_name = content['contract_name']
    command = """
        cleos --url https://api-kylin.eosasia.one:443 multisig exec %s %s -p %s@active
    """
    command = command % (proposer, contract_name, proposer)
    subprocess.call(command, shell=True)
    return ''





if __name__ == '__main__':
    app.run(host=settings.SERVER_HOST, port=settings.PORT)
# subprocess.call('mysql -u root -p -e "CREATE DATABASE flasktest; GRANT ALL ON flasktest.* TO root@localhost IDENTIFIED BY `flask123`; FLUSH PRIVILEGES"', shell=True)
