import socket
import json


def udp_echo_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = '127.0.0.1'
    server_port = 12345

    try:
        # m = {"name": "Fred", "goal": "lose", "plan": "one", "assigned": "male",
        #      "weight": "150 lbs", "height": "5 9", "age": "28", "active": "moderate"}
        #
        # m = {"name": "Sara", "goal": "gain", "plan": "half", "assigned": "female",
        #      "weight": "75 lbs", "height": "5 3", "age": "20", "active": "light"}

        # m = "Fred"

        m = {"name": "Sara", "goal": "gain", "plan": "half", "assigned": "female",
             "weight": "150 lbs", "height": "5 3", "age": "20", "active": "light"}

        data = json.dumps(m)
        message = data
        print(f"Sending: {message}")

        sock.sendto(message.encode(), (server_address, server_port))

        response, server = sock.recvfrom(1024)

        print(f"Received: {response.decode()} from {server}")

    finally:
        sock.close()


if __name__ == "__main__":
    udp_echo_client()
