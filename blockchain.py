# Initial code borrowed from https://www.superdatascience.com/blockchain/
# Extended by Janghoon Lee

import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:

    def __init__(self):
        self.chain = []  # Initialize the chain
        self.transactions = []  # Initialize transactions
        self.create_block(proof=1, previous_hash='0')  # Create genesis block
        self.nodes = set()  # Initialize network nodes

    # Create a block function
    def create_block(self, proof, previous_hash):
        # Initialize a block object
        block = {
            # Get the length of this object instance's chain and add 1
            'index': len(self.chain) + 1,
            # Get current datetime in string format
            'timestamp': str(datetime.datetime.now()),
            # Get proof
            'proof': proof,
            # Get all transactions in the object's transaction list
            'transactions': self.transactions,
            # Get previous hash
            'previous_hash': previous_hash
        }

        # Truncate object's transaction list
        self.transactions = []
        self.chain.append(block)

        return block

    # Get the last block in the chain
    def get_previous_block(self):
        return self.chain[-1]

    # Get proof of work
    def get_proof_of_work(self, previous_proof):
        # Initialize effort
        new_proof = 1
        # Initialize work validity status
        check_proof = False

        # While the work is not valid
        while check_proof is False:
            # Declare the hash operation with SHA256
            hash_operation = hashlib.sha256(
                str(new_proof*2 + previous_proof).encode()).hexdigest()
            # Declare the leading zeros as 4
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    # Get hash value of the block
    def get_hash(self, block):
        # Encode the block object to string json format
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # Return the hash value of the block
        return hashlib.sha256(encoded_block).hexdigest()

    # Check validity of the chain of the object instance
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        # Loop for the length of the chain
        while block_index < len(chain):
            block = chain[block_index]

            # Return invalid if previous block's hash does not match
            if block['previous_hash'] != self.get_hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof*2 + previous_proof).encode()).hexdigest()

            # Return invalid if the block hash does not have leading 4 zeors
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

    # Add transaction to current block
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    # Add url info to the chain node list
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # Update current chain for consensus protocol
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        # Replace this node's chain if a longer chain was found
        if longest_chain:
            self.chain = longest_chain
            return True

        return False
