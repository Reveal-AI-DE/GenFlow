# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import os
from os import path as osp

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings


def generate_key_pair(team_id: str) -> str:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),  # No password protection
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    key_dir = osp.join(settings.BASE_DIR, "keys", "teams", team_id)
    os.makedirs(key_dir, exist_ok=True)
    key_file = "private.pem"
    with open(osp.join(key_dir, key_file), "wb") as f:
        f.write(pem_private)

    return pem_public.decode()


prefix_hybrid = b"HYBRID:"


def encrypt(text: str, public_key: str | bytes) -> bytes:
    if isinstance(public_key, str):
        public_key = public_key.encode()

    # Generate a random AES key
    aes_key = os.urandom(16)

    # Generate a random nonce
    nonce = os.urandom(12)

    # Encrypt the plaintext using AES in GCM mode
    cipher_aes = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher_aes.encryptor()
    ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
    tag = encryptor.tag

    # Encrypt the AES key using the RSA public key
    rsa_key = serialization.load_pem_public_key(public_key, backend=default_backend())
    enc_aes_key = rsa_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
        ),
    )

    # Combine the encrypted AES key, nonce, tag, and ciphertext
    encrypted_data = enc_aes_key + nonce + tag + ciphertext

    return prefix_hybrid + encrypted_data


def get_decrypt_decoding(team_id: str):
    key_dir = osp.join(settings.BASE_DIR, "keys", "teams", team_id)
    key_file = osp.join(key_dir, "private.pem")

    try:
        with open(key_file, "rb") as f:
            private_key = f.read()
    except FileNotFoundError:
        raise Exception("Private key not found, team_id: {team_id}".format(team_id=team_id))

    rsa_key = serialization.load_pem_private_key(
        private_key, password=None, backend=default_backend()
    )

    return rsa_key


def decrypt_token_with_decoding(encrypted_text: str, rsa_key: PrivateKeyTypes) -> str:
    if encrypted_text.startswith(prefix_hybrid):
        encrypted_text = encrypted_text[len(prefix_hybrid) :]

        # Extract the encrypted AES key, nonce, tag, and ciphertext
        rsa_key_size = rsa_key.key_size // 8
        enc_aes_key = encrypted_text[:rsa_key_size]
        nonce = encrypted_text[rsa_key_size : rsa_key_size + 12]
        tag = encrypted_text[rsa_key_size + 12 : rsa_key_size + 28]
        ciphertext = encrypted_text[rsa_key_size + 28 :]

        # Decrypt the AES key using the RSA private key
        aes_key = rsa_key.decrypt(
            enc_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
            ),
        )

        # Decrypt the ciphertext using AES in GCM mode
        cipher_aes = Cipher(
            algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend()
        )
        decryptor = cipher_aes.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    else:
        # If not hybrid encryption, decrypt directly using RSA
        decrypted_text = rsa_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
            ),
        )

    return decrypted_text.decode()


def decrypt(encrypted_text, team_id):
    rsa_key = get_decrypt_decoding(team_id)

    return decrypt_token_with_decoding(encrypted_text, rsa_key)
