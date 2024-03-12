# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:54:43 2023

@author: masci
"""

from ICT_mining import Blockchain
import time

start_time=time.time()
blockchain = Blockchain()
transaction1 = {"sender": "Alice", "recipient": "Bob", "amount": 1.5}
transaction2 = {"sender": "Bob", "recipient": "Charlie", "amount": 0.8}
transaction3 = {"sender": "Charlie", "recipient": "Alice", "amount": 4.5}
transaction4 = {"sender": "Dankan", "recipient": "Charlie", "amount": 0.5}

blockchain.add_new_transaction(transaction1)
mined_block_index,nonce = blockchain.mine()
blockchain.add_new_transaction(transaction2)
mined_block_index,nonce = blockchain.mine()
blockchain.add_new_transaction(transaction3)
mined_block_index,nonce = blockchain.mine()
blockchain.add_new_transaction(transaction4)
mined_block_index,nonce = blockchain.mine()

end_time=time.time()
exe_time=end_time-start_time

chain=blockchain.chain
for block in chain:
    print(f"Index: {block.index}")
    print(f"Transactions: {block.transactions}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Hash: {block.hash}")
    print(f"nonce: {block.nonce}")
    print(f"Execution time: {exe_time} s.")
    