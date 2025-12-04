from passlib.context import CryptContext
import requests

API_STATUS_URL = "http://127.0.0.1:8001/status/"

def servidor_online():
    try:
        response = requests.get(API_STATUS_URL, timeout=2)
        return response.status_code == 200
    except:
        return False

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)
