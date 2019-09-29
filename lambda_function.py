import json
import boto3
import base64
from algosdk import account, algod, mnemonic, transaction

def lambda_handler(event, context):
    """
    Main function executed at Lambda runtime. Retrieves hot wallet
    key pair, generates and signs and transaction, and posts to the 
    network.
    """

    # Retrieve Algorand Hot Wallet public and secret key from Secrets Manager
    pk, sk = get_keypair()
    # Convert retrieved secret key from mnemonic to private key
    sk = mnemonic.to_private_key(sk) 

    # Instantiate algod client to get network params for transaction
#    node_address = <your-node-address>
#    node_token = <your-node-token>
    algodclient = algod.AlgodClient(node_token, node_address)
    
    # Get suggested transaction parameters and specify other params
    params = algodclient.suggested_params()
    sender = pk
    receiver = "3IE2GDYYSI56U53AQ6UUWRGAIGG5D4RHWLMCXJOPWQJA2ABF2X2OLFXGJE"
    fee = 0 # will use minimum transaction fee of 1000 microalgos
    first = params.get("lastRound")
    last = first + 1000
    gh = params.get("genesishashb64")
    amt = 1 
    
    # Build Algorand transaction
    tx = transaction.PaymentTxn(
                sender, 
                fee, 
                first, 
                last, 
                gh, 
                receiver, 
                amt
        ) 

    # Sign the transaction with your retrieved secret key
    signed_tx = tx.sign(sk)
    
    # Use algodclient to send the signed transaction to the network
    txid = algodclient.send_transaction(signed_tx)
    return {"TransactionID": txid}
    
def get_keypair():
    """
    Retrieve hot wallet public/private key pair from Secrets Manager.
    """
    
    secret_name = "algorand/testnet/hotwallet" # change to your secret's name
    region_name = "us-east-2" # change to your secret's region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    keypair = json.loads(get_secret_value_response.get('SecretString'))
    return (keypair.get("AlgorandPublicKey"), keypair.get("AlgorandSecretKey"))
