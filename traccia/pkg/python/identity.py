import os
import json
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
import base64

class AgentIdentity:
    def __init__(self, private_key=None):
        if private_key is None:
            # 生成新的密钥对
            self.private_key = ed25519.Ed25519PrivateKey.generate()
        else:
            self.private_key = private_key
        self.public_key = self.private_key.public_key()
    
    @classmethod
    def from_private_key_bytes(cls, private_bytes: bytes):
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
        return cls(private_key)
    
    def sign(self, data: bytes) -> bytes:
        return self.private_key.sign(data)
    
    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(signature, data)
            return True
        except Exception:
            return False
    
    def get_public_key_base64(self) -> str:
        return base64.b64encode(self.public_key.public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )).decode('ascii')
    
    def get_private_key_base64(self) -> str:
        return base64.b64encode(self.private_key.private_bytes(
            encoding=Encoding.Raw,
            format=PrivateFormat.Raw,
            encryption_algorithm=NoEncryption()
        )).decode('ascii')
    
    @classmethod
    def from_public_key_base64(cls, public_key_b64: str):
        # 仅用于验证，不需要私钥
        public_bytes = base64.b64decode(public_key_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
        # 创建一个只包含公钥的身份（仅验证用）
        identity = cls.__new__(cls)
        identity.private_key = None
        identity.public_key = public_key
        return identity

def generate_keypair() -> tuple[str, str]:
    """返回 (private_key_base64, public_key_base64)"""
    identity = AgentIdentity()
    return identity.get_private_key_base64(), identity.get_public_key_base64()