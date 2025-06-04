"""
订单敏感数据加密模块
用于对收货人姓名、电话、地址等敏感信息进行加密和解密
"""
from django.conf import settings
from cryptography.fernet import Fernet
import base64

class DataEncryptor:
    """
    数据加密器，用于加密和解密敏感数据
    使用Django的SECRET_KEY作为加密密钥的种子
    """
    def __init__(self):
        # 使用Django的SECRET_KEY作为密钥种子
        key_seed = settings.SECRET_KEY.encode()[:32]
        # 确保密钥是32位长，如果不够则填充
        if len(key_seed) < 32:
            key_seed = key_seed.ljust(32, b'=')

        # 生成Fernet密钥
        self.key = base64.urlsafe_b64encode(key_seed)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        """
        加密数据
        :param data: 要加密的字符串数据
        :return: 加密后的字符串
        """
        if not data:
            return data

        try:
            # 将数据转换为bytes并加密
            encrypted_data = self.cipher.encrypt(str(data).encode())
            # 返回加密后的字符串
            return encrypted_data.decode()
        except Exception as e:
            print(f"加密错误: {e}")
            # 如果加密失败，返回原数据，确保功能不中断
            return data

    def decrypt(self, encrypted_data):
        """
        解密数据
        :param encrypted_data: 加密后的字符串
        :return: 解密后的原始字符串
        """
        if not encrypted_data:
            return encrypted_data

        try:
            # 将加密字符串转换为bytes并解密
            decrypted_data = self.cipher.decrypt(encrypted_data.encode())
            # 返回解密后的字符串
            return decrypted_data.decode()
        except Exception as e:
            print(f"解密错误: {e}")
            # 如果解密失败，返回原数据
            return encrypted_data

# 创建单例实例供全局使用
encryptor = DataEncryptor()
