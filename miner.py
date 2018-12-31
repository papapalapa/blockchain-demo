from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.get_proof_of_work(previous_proof)
    previous_hash = blockchain.get_hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'MINING SUCCESS',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/validity', methods=['GET'])
def check_validity():
    response = {
        'is_valid': blockchain.is_chain_valid(blockchain.chain)
    }

    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)