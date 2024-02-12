import json
import socket
import threading

# Activity modifiers
NO_ACT = 1.2
LIGHT_ACT = 1.375
MODERATE_ACT = 1.55
HIGH_ACT = 1.725
VHIGH_ACT = 1.9

SEX_MALE = 5
SEX_FEMALE = -151

FULL_PLAN = 500
HALF_PLAN = 250

# Dict to store cal history
history = {}


def microservice_server():
    """
    Server for calorie calculator. Maintains active socket waiting for client request, parses client request,
    and sends requested data on UDP socket.

    :return: none
    """
    # Creates UDP protocol socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Sets ip for local host
    server_address = '127.0.0.1'
    server_port = 12345

    # Binds socket to ip and port
    server_sock.bind((server_address, server_port))

    print("Microservice server is ready to receive requests...")

    try:
        while True:
            # Waits for client request
            message, client_address = server_sock.recvfrom(1024)
            print(f"Received message: {message.decode()} from {client_address}\n")

            try:
                # Decodes message if JSON request
                request = (json.loads(message.decode()))
            except json.decoder.JSONDecodeError:
                # Decodes message if string request
                request = message.decode()

            # Retrieves requested calorie count
            cal_count = calculate(request)

            # Returns requested cals to client
            return_message = str(cal_count).encode()
            server_sock.sendto(return_message, client_address)

            # Event listener to shut down server
            if shutdown_event.is_set():
                break

    finally:
        # Closes socket on server shutdown
        server_sock.close()
        print("Server socket closed.")
        save_data()


def stop_server():
    """
    Waits for any user input to shut down server.

    :return: none
    """
    user_input = input("Input any key to stop server.\n")
    if user_input:
        print("Microservice server is shutting down on next request.")
        shutdown_event.set()
        t2.join()


def calculate(request):
    try:
        name = request["name"]
        goal = request["goal"]
        plan = request["plan"]
        assigned = request["assigned"]
        weight = request["weight"]
        height = request["height"]
        age = request["age"]
        active = request["active"]

        cal_count = round(cals(goal, plan, assigned, weight, height, age, active))
        history[name] = cal_count

    except TypeError:
        try:
            cal_count = history[request]
        except KeyError:
            cal_count = "Error - Name not found."

    return cal_count


def cals(user_goal, user_plan, user_sex, user_weight, user_height, user_age, user_active_level):
    """
    Calculates the total calorie requirements for a given user plan and goal. Type of plan, user goal, plan rigor level,
    user sex, user weight, user height, user age, and activity levels used in calculation. Final calorie requirements
    returned rounded to a whole number.

    :param user_goal: str goal of user "gain", "lose"
    :param user_plan: str type of plan rigour level "one", "half"
    :param user_sex: str sex of user "male", "female"
    :param user_weight: int weight of user in kg or lbs
    :param user_height: int height of user in cm or inches
    :param user_age: int age of user
    :param user_active_level: str "none", "light", "moderate", "high", "very high"

    :return: int calorie count
    """
    # Converts weight between lbs and cm
    if user_weight[-3:] == "lbs":
        weight = int(user_weight[:-3]) / 2.205
    else:
        weight = int(user_weight[:-3])

    # Converts height between cm and in
    if user_height[-2:] == "cm":
        height = int(user_height[:-3])
    else:
        if user_height[-2] == " ":
            feet = int(user_height[:-2])
            inch = int(user_height[-1])
        else:
            feet = int(user_height[:-3])
            inch = int(user_height[-2:])
        inch = feet * 12 + inch
        height = inch * 2.54

    # Sets constant for reported sex
    if user_sex == "male":
        s = SEX_MALE
    else:
        s = SEX_FEMALE

    # Determines activity level modifier constant
    match user_active_level:
        case "none":
            activity = NO_ACT
        case "light":
            activity = LIGHT_ACT
        case "moderate":
            activity = MODERATE_ACT
        case "high":
            activity = HIGH_ACT
        case _:
            activity = VHIGH_ACT

    # Adjusts for weight gain or loss
    if user_goal == "gain":
        mult = 1
    else:
        mult = -1

    # Sets plan rigour level
    if user_plan == "one":
        amount = FULL_PLAN
    else:
        amount = HALF_PLAN

    return ((10 * weight + 6.25 * height - 5.0 * int(user_age)) + s) * activity + mult * amount


def load_data():
    """
    Loads calorie data history from data.json file. Creates new file if one does not exist.

    :return: none
    """
    global history
    try:
        with open("data.json") as infile:
            history = json.load(infile)
    except FileNotFoundError:
        with open("data.json", "w") as outfile:
            json.dump({}, outfile)

    print(history)

def save_data():
    """
    Saves calorie history in data.json file.

    :return: none
    """
    global history
    with open("data.json", "w") as outfile:
        json.dump(history, outfile)


if __name__ == "__main__":
    # Loads data history
    load_data()

    # Creates event for server shutdown
    shutdown_event = threading.Event()

    # Creates thread for cal count server
    t2 = threading.Thread(target=microservice_server)
    t2.start()

    # Creates thread for server shutdown listener
    t1 = threading.Thread(target=stop_server)
    t1.start()
