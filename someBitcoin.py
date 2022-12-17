import requests
import base58
import hashlib
import binascii
import bech32
from bech32 import bech32_decode


class someBitcoin:
    address = 0

    def __init__(self):
        print("build bitcoin")

    def __str__(self) -> str:
        return f'<the private Key is: {self.privateKey}, the public key is : {self.publicKey}, the address is : {self.address}>'

    # *********************************** get_balance ************************************************************8
    # get_balance return the balance of the specific bitcoin according to his address using api of blockcypher.com
    # this api is free, becouse of that its takes a few seconds for it to retrieve the information from the api.
    def get_balance(self, address):
        res = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{self.address}/balance')
        return res.json()['balance']

    # ******************************** validate_bitcoin_address ******************************************
    # this function check if the address is valid or not.
    def validate_bitcoin_address(self, address: str) -> bool:
        try:
            # check bech32 format
            if self.address[0] == 'b':
                prefix, data = bech32_decode(address)
                if bech32(prefix, data) == self.address:
                    return True
                else:
                    return False
            # check the other format
            base58Decoder = base58.b58decode(self.address).hex()
            print("Base58 Decoder: ", base58Decoder)
        except:
            return False
        prefixAndHash = base58Decoder[:len(base58Decoder) - 8]
        checksum = base58Decoder[len(base58Decoder) - 8:]
        print("\t|___> Prefix & Hash: ", prefixAndHash)
        print("\t|___> Checksum: ", checksum)
        print("--------------------------------------")
        hash = prefixAndHash
        for x in range(1, 3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
            print("Hash#", x, " : ", hash)
        print("--------------------------------------")
        if (checksum == hash[:8]):
            print("[TRUE] checksum is valid!")
            return True
        else:
            print("[FALSE] checksum is not valid!")
            return False
