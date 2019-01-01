from flask import Flask, jsonify, request
from uuid import uuid4

from blockchain import Blockchain

app = Flask(__name__)

# Initialize the node address
node_address = str(uuid4()).replace('-', '')

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
    blockchain.add_transaction(
        sender=node_address,
        receiver='Janghoon',
        amount=1
    )
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'MINING SUCCESS',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }

    return jsonify(response), 200


@app.route('/validity', methods=['GET'])
def check_validity():
    response = {
        'is_valid': blockchain.is_chain_valid(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']

    # If not all required keys are present
    if not all(key in json for key in transaction_keys):
        return {'message': 'ERROR: KEYS NOT PRESENT'}, 400

    index = blockchain.add_transaction(
        json['sender'],
        json['receiver'],
        json['amount']
    )
    response = {
        'message': f'TRANSACTION ADDED TO {index}',
    }

    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        return {'message': 'ERROR: NODE NOT PRESENT'}, 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'NODES CONNECTED',
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 200


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()

    if is_chain_replaced:
        response = {
            'message': 'CHAIN REPLACED',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'NO CHANGE MADE',
        }

    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
