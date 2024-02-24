# Calorie Count Calculator

This program is intended to function as a microservice for a fitness application that calculates
the daily caloric intake requirements for a patient based on their lifestyle, goals, and body metrics.

In order to programmatically request data, the application should receive a JSON request for new patients or
a string request to retrieve historical data from a prior request. The information should be transferred across
a UDP socket on local host '127.0.0.1' with the port 12345. 
The request to calculate new patient caloric requirements should be structured in the following format:

    new_patient = {"name": "Fred", "goal": "lose", "plan": "one", "assigned": "male",
                  "weight": "150 lbs", "height": "5 9", "age": "28", "active": "moderate"}
    data = json.dumps(m)
            message = data
            print(f"Sending: {message}")

        sock.sendto(message.encode(), (server_address, server_port))

The request to retrieve stored patient caloric requirements should be structured in the following format:

    retrieve_patient = "Fred"
    data = json.dumps(m)
            message = data
            print(f"Sending: {message}")

In order to receive data from either type of request, the UDP socket should wait to receive a return message from
the microservice client. The return message will be an integer value, and should be received in the follow format:

    response, server = sock.recvfrom(1024)
    
    print(f"Received: {response.decode()} from {server}")

The microservice server will remain active and continue to receive client requests on the same UDP socket
until manually shut down by the application user. 

![Untitled Diagram.drawio.png](Untitled%20Diagram.drawio.png)