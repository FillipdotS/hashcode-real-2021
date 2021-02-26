from datetime import datetime
from operator import itemgetter


class Street:
    def __init__(self, origin, destination, name, duration):
        self.origin = origin
        self.destination = destination
        self.name = name
        self.duration = duration
        self.activity = 0
        self.priority = 0


def solve(input_name):
    start_time = datetime.now()
    print("### Starting " + input_name + " ###")

    #
    # Input
    #

    input_file = open("data/" + input_name + ".txt", "r")
    basic_info = input_file.readline().split()

    # simulation_duration = int(basic_info[0])
    # intersection_amount = int(basic_info[1])
    street_amount = int(basic_info[2])
    car_amount = int(basic_info[3])
    # bonus_points = int(basic_info[4])

    # We store the intersections in a dictionary where the key is the intersection id and the value
    # stored is a list of street names
    intersection_incoming = dict()

    # Streets

    # Streets are also stored in a dictionary where the key is the street name and the value stored
    # is that particular instance of Street
    all_streets = {}

    for i in range(0, street_amount):
        street_info = input_file.readline().split()
        street_name = street_info[2]
        origin = street_info[0]
        destination = street_info[1]
        duration = street_info[3]

        all_streets[street_name] = Street(origin, destination, street_name, duration)

        try:
            intersection_incoming[destination].append(street_name)
        except KeyError:
            intersection_incoming[destination] = [street_name]

    # Paths

    for i in range(0, car_amount):
        car_info = input_file.readline().split()
        street_path = car_info[1:]

        all_streets[street_path[0]].priority += 1

        # Activity of a street is amount of cars that drive on it overall throughout the simulation
        for street_name in street_path[:-1]:
            all_streets[street_name].activity += 1

    #
    # Algorithm
    #

    final_intersections = []

    for intersection_id in intersection_incoming:
        incoming_streets = intersection_incoming[intersection_id]

        # Keep track of the highest, lowest and total activity street for this intersection
        highest_street = 1
        lowest_street = 1000
        total_activity = 0

        # Calculate total incoming activity for this intersection
        for street_name in incoming_streets:
            street = all_streets[street_name]
            total_activity += street.activity

            if street.activity > highest_street:
                highest_street = street.activity

            if lowest_street > street.activity > 0:
                lowest_street = street.activity

        # Contains street name with amount of seconds to be green
        # {"name": actual_street.name, "time": actual_street.activity}
        light_schedule = []

        # Some intersections are never used, don't care about scheduling them
        if total_activity > 0:
            for street_name in incoming_streets:
                street = all_streets[street_name]

                # Some streets are never used, don't care about them either
                if street.activity > 0:
                    # Here is where the actual calculation for each light takes place
                    # We used many variations of the algorithm, examples of which are listed below

                    magic_factor = 10  # Was also, 3, 4, 5, 20
                    magic_factor = (1 / 3) * street.activity  # Was also (1/2, 2/3)

                    calculated_time = round(street.activity / total_activity * magic_factor)
                    calculated_time = max(1, calculated_time)

                    calculated_time = max(1, round((1/3) * street.activity))

                    light_schedule.append({"name": street.name, "time": calculated_time, "priority": street.priority})

            final_intersections.append({"i_id": intersection_id, "total_activity": total_activity, "schedule": light_schedule})

    #
    # Output
    #

    output_file = open("output/" + input_name + "_out_" + ".txt", "w")

    output_file.write(str(len(final_intersections)))

    for inter in final_intersections:
        output_file.write("\n" + str(inter["i_id"]))
        output_file.write("\n" + str(len(inter["schedule"])))

        # Reversed for descending order (we want to show the highest priority first)
        sorted_by_priority = sorted(inter["schedule"], key=itemgetter("priority"), reverse=True)

        for light in sorted_by_priority:
            output_file.write("\n" + light["name"] + " " + str(light["time"]))

    #
    # Final stats
    #

    stats = "Completed " + input_name + " in " + str(datetime.now() - start_time) + "\n"
    # stats += "Intersection amount: " + str(intersection_amount) + " | Street amount: " + str(street_amount) + "\n"
    # stats += "Car amount: " + str(car_amount) + " | Bonus points: " + str(bonus_points) + "\n"
    # stats += "Total time: " + str(simulation_duration) + "\n"
    print(stats)


solve("a")
solve("b")
solve("c")
solve("d")
solve("e")
solve("f")
