# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from os import path as osp

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from django.conf import settings


from gen_flow.apps.common.security import gmpy2_pkcs10aep_cipher

def generate_key_pair(team_id):
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    pem_private = private_key.export_key()
    pem_public = public_key.export_key()

    key_dir = osp.join(settings.BASE_DIR, 'keys', 'teams', str(team_id))
    os.makedirs(key_dir, exist_ok=True)
    key_file = 'private.pem'
    with open( osp.join(key_dir, key_file), 'wb') as f:
        f.write(pem_private)

    return pem_public.decode()

prefix_hybrid = b'HYBRID:'


def encrypt(text, public_key):
    if isinstance(public_key, str):
        public_key = public_key.encode()

    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)

    ciphertext, tag = cipher_aes.encrypt_and_digest(text.encode())

    rsa_key = RSA.import_key(public_key)
    cipher_rsa = gmpy2_pkcs10aep_cipher.new(rsa_key)

    enc_aes_key = cipher_rsa.encrypt(aes_key)

    encrypted_data = enc_aes_key + cipher_aes.nonce + tag + ciphertext

    return prefix_hybrid + encrypted_data

def get_decrypt_decoding(team_id: str):
    key_dir = osp.join(settings.BASE_DIR, 'keys', 'teams', team_id)
    key_file = osp.join(key_dir, 'private.pem')

    try:
        with open(key_file, 'r') as f:
            private_key = f.read()
    except FileNotFoundError:
        raise PrivkeyNotFoundError('Private key not found, tenant_id: {tenant_id}'.format(tenant_id=team_id))

    rsa_key = RSA.import_key(private_key)
    cipher_rsa = gmpy2_pkcs10aep_cipher.new(rsa_key)

    return rsa_key, cipher_rsa

def decrypt_token_with_decoding(encrypted_text, rsa_key, cipher_rsa):
    if encrypted_text.startswith(prefix_hybrid):
        encrypted_text = encrypted_text[len(prefix_hybrid) :]

        enc_aes_key = encrypted_text[: rsa_key.size_in_bytes()]
        nonce = encrypted_text[rsa_key.size_in_bytes() : rsa_key.size_in_bytes() + 16]
        tag = encrypted_text[rsa_key.size_in_bytes() + 16 : rsa_key.size_in_bytes() + 32]
        ciphertext = encrypted_text[rsa_key.size_in_bytes() + 32 :]

        aes_key = cipher_rsa.decrypt(enc_aes_key)

        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        decrypted_text = cipher_aes.decrypt_and_verify(ciphertext, tag)
    else:
        decrypted_text = cipher_rsa.decrypt(encrypted_text)

    return decrypted_text.decode()


def decrypt(encrypted_text, tenant_id):
    rsa_key, cipher_rsa = get_decrypt_decoding(tenant_id)

    return decrypt_token_with_decoding(encrypted_text, rsa_key, cipher_rsa)

class PrivkeyNotFoundError(Exception):
    pass