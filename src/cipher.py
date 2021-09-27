from bitarray import bitarray
from random import randrange

def xor_cypher(text, key):
        
    number_key = int(key)

    def xor(bit1, bit2):
        return (bit1 + bit2) - 2*(bit1*bit2)

    if len(text) > len(key):
        dif = (len(text) - len(key))
        for i in range(dif):
            key += chr((number_key * i) % 128)

    encrypted_text = bitarray()

    bit_text = bitarray()
    bit_key = bitarray()

    bit_text.frombytes(text.encode('utf-8'))
    bit_key.frombytes(key.encode('utf-8'))

    for S_bit, K_bit in zip(bit_text, bit_key):
        encrypted_text.append(xor(S_bit, K_bit))

    encrypted_text = bitarray(encrypted_text.tolist()).tobytes().decode('utf-8')

    return encrypted_text

def caesar_cypher(text, key, decript=False):

    #All 95 ascii printable characters 
    alphabet = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    key = key % len(alphabet)
    if decript: key *= -1

    encryptedText = ''
    for char in text:
        encryptedText += alphabet[(alphabet.find(char) + key) % len(alphabet)]
        
    return encryptedText
