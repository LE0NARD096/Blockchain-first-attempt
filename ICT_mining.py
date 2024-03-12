# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:11:28 2023

@author: masci
"""

from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
    def compute_hash(self):
        # Funzione che ritorna l'hash del contenuto del blocco
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 5
    def __init__ (self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        
    def create_genesis_block(self): 
        genesis_block = Block(0, [], time.time(), "0")                          # La funzione genera il blocco di genesi e lo aggiunge alla blockchain.
        genesis_block.hash = genesis_block.compute_hash()                       # creazione dinamica dell'attributo hash
        self.chain.append(genesis_block)                                        # aggiunge il primo blocco alla chain
        
    @property
    def last_block(self):
        return self.chain[-1]                                                   # Proprietà che prende l'ultimo blocco della catena. 

    
    def proof_of_work (self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1                                                    # La funzione verifica diversi valori di nonce fino a quando non trova il valore hash soddisfacente.
            computed_hash = block.compute_hash()
        return computed_hash                                    

    def is_valid_proof(self, block, block_hash):
        return(block_hash.startswith('0' * Blockchain.difficulty) and 
               block_hash == block.compute_hash())                              # Controlla se block_hash è il valore hash valido del blocco e se soddisfa i criteri di difficoltà

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash                                    # Verifica che l'hash precedente sia corretto e corrisponda al valore hash del nuovo blocco
        if previous_hash != block.previous_hash:  
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)                       # Funzione che aggiunge della transazione all'array delle transazioni non confermate

    def mine(self):
        if not self.unconfirmed_transactions:                                   # se non ci sono transazioni pendenti, ritorna falso
            return False
        last_block = self.last_block
        new_block = Block (index = last_block.index + 1,                        # - assegna un nuovo indice sulla base dell'indice dell'ultimo blocco incrementato di una unità
                          transactions = self.unconfirmed_transactions,         # - imposta dentro il blocco tutte le transazioni pendenti
                          timestamp = time.time (),
                          previous_hash = last_block.hash)                      # - imposta come previous_hash, l'hash dell'ultimo blocco
        proof = self.proof_of_work(new_block)                                   # calcola la proof-of-work del nuovo blocco
        self.add_block(new_block, proof)                                        # aggiunge il nuovo blocco alla blockchain
        self.unconfirmed_transactions = []                                      # svuota l'array delle transazioni pendenti
        return new_block.index, proof                           
