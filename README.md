# Blockchain Demo

This is a demo project for general purpose blockchain developed with Python and Flask.

# Setup
1. Install Python according to your OS requirements: [link](https://realpython.com/installing-python/)
2. Install Python package manager (pip): [link](https://pip.pypa.io/en/stable/installing/)
3. Clone this repository in a directory of your choice
4. Change to the root directory of the cloned repository
5. Install the dependencies: `pip install requirements.txt`
6. Run the application: `python miner.py`
7. Access the server at `localhost:5000`

# Routes: Receives methods=['GET']
* Get every block in the chain: `localhost:5000`
* Mine new blocks: `localhost:5000/mine`
* Check validity of the blockchain: `localhost:5000/validity`
