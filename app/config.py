
import os
import binascii


class Config:
    SECRET_KEY = binascii.b2a_hex(os.urandom(20))
