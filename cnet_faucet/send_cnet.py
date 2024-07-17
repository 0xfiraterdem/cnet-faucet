import time
from pathlib import Path
import requests
from multiversx_sdk import Transaction, TransactionComputer, ProxyNetworkProvider, UserSigner


class NonceManager:
    def __init__(self):
        self.nonce = self._get_initial_nonce()

    def _get_initial_nonce(self):
        response = requests.get("https://testnet-api.cyber.network/accounts/erd1ejne2lth0aelfufn5f8efas5deek8qrdw68qv5p9q3yjvu7a74ns5g6872?fields=nonce")
        data = response.json()
        return data.get("nonce")

    def get_nonce(self):
        return self.nonce

    def increment_nonce(self):
        self.nonce += 1


signer = UserSigner.from_pem_file(Path("cnet_faucet/wallet.pem"))
provider = ProxyNetworkProvider("https://testnet-gateway.cyber.network")

nonce_manager = NonceManager()

def send_transaction(receiver):
    nonce = nonce_manager.get_nonce()
    tx = Transaction(
        nonce=nonce,
        sender="erd1ejne2lth0aelfufn5f8efas5deek8qrdw68qv5p9q3yjvu7a74ns5g6872",
        receiver=receiver,
        value=1000000000000000000000,
        gas_limit=50000,
        chain_id="55",
    )

    transaction_computer = TransactionComputer()
    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

    hashes = provider.send_transaction(tx)
    print("Transaction hashes:", hashes)

    # Nonce değerini artır
    nonce_manager.increment_nonce()


