import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        self.new_block(previus_hash=1, proof=100)

    def new_block(self, proof, previus_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previus_hash': previus_hash or self.hash(self.chain[-1])
        }

        self.current_transaction = []

        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        proof= 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        block_string = json.dump(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        pass


app = Flask(__name__)

node_uuid = str(uuid4()).replace('-', '')

blockchain = Blockchain()
