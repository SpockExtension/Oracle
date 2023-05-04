import zmq
import requests

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

public_ip = get_public_ip()
print(f"My public IP address is {public_ip}")

def load_nodes_file():
    with open('nodes.txt', 'r') as f:
        nodes = f.readlines()
        nodes = [node.strip() for node in nodes]
        return nodes

def connect_to_node(socket, address):
    try:
        socket.connect(f"tcp://{address}:5555")
    except zmq.ZMQError as e:
        print(f"Error connecting to {address}: {e}")

# Set up ZMQ sockets for PUB and SUB
context = zmq.Context()

pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5555") # Bind to port 5555

sub_socket = context.socket(zmq.SUB)
sub_socket.bind("tcp://*:5556") # Bind to port 5556
sub_socket.setsockopt_string(zmq.SUBSCRIBE, '') # Subscribe to all messages

# Infinite loop to send and receive messages
while True:
    # Load node addresses from the nodes.txt file
    node_addresses = load_nodes_file()

    # Connect to any new nodes
    for address in node_addresses:
        if address != public_ip:
            connect_to_node(pub_socket, address)
            connect_to_node(sub_socket, address)

    # Send a message using the PUB socket
    message = input("Enter a message to send: ")
    pub_socket.send_string(message)
    to_add_keypair = {}

    # Receive any messages on the SUB socket
    try:
        message = sub_socket.recv_string(flags=zmq.NOBLOCK)
        print(f"Received message: {message}")
    except zmq.Again:
        pass

# Clean up sockets and context when done
pub_socket.close()
sub_socket.close()
context.term()
