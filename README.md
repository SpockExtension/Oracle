In different processes, make sure to run the following:

1. `python3 -m pip install -r requirements.txt` - install dependencies
2. `python3 src/mempool.py` - pending keypairs to add
3. `python3 src/nonce.py` - endpoint to generate a random nonce
4. `python3 src/oracle.py` - endpoint to create keypair, sign a message and validate a cookie
5. `python3 src/pubSub.py` - TCP connections to sync keypairs
6. `python3 src/challenge.py` - endpoint to create a challenge from nonce.txt

Edit: The docker is breaking again, will update with the right link shortly!
