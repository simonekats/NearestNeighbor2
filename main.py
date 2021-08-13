####################################################

TRAVEL_TIME = {
    ('Lightship Chesapeake', 'Concord Point'): 0.8,
    ('Lightship Chesapeake', 'Point Lookout'): 2.3,
    ('Lightship Chesapeake', 'Sandy Point'): 0.7166666666666667,
    ('Lightship Chesapeake', 'Drum Point'): 1.62,
    ('Concord Point', 'Point Lookout'): 3.1166666666666667,
    ('Concord Point', 'Sandy Point'): 1.45,
    ('Concord Point', 'Drum Point'): 2.23,
    ('Point Lookout', 'Sandy Point'): 2.1166666666666667,
    ('Point Lookout', 'Drum Point'): 0.7666666666666667,
    ('Sandy Point', 'Drum Point'): 1.4333333333333333
}

LIGHTS = list(set([item for k in TRAVEL_TIME.keys() for item in k]))

# Helper Functions
def list_minus(L, x):
    """Returns a list of L that does not have x in it."""
    return list(set(L)-set([x,]))


def travel_time(x, y):
    """Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time"""
    global TRAVEL_TIME
    try:
        tm = TRAVEL_TIME[(x,y)] # could do this w/frozen sets, but that's a little much
    except:
        tm = TRAVEL_TIME[(y,x)]
    return tm


cache = {}


MIN_TIME = 0.0
ROUTES = []
STEP_COUNT = 0


def get_routes(lighthouse, lh_list, route, total_time):
    global STEP_COUNT
    global ROUTES
    global MIN_TIME
    STEP_COUNT += 1
    # if lighthouse list is empty
    if not lh_list:
        # total time equals the travel time from last lighthouse to first lighthouse
        total_time += travel_time(route[-1], lighthouse)
        # add lighthouse to route
        route.append(lighthouse)
        if MIN_TIME == 0 or total_time < MIN_TIME:
            MIN_TIME = total_time
            ROUTES = route

    # if lighthouse list is not empty
    else:
        if route:
            # total time equals the travel time from last lighthouse to first lighthouse
            total_time += travel_time(route[-1], lighthouse)
        ## append lighthouse to the route
        route.append(lighthouse)
        # for lighthouse in the lighthouse list, call get routes with parameters:
        # lighthouse, listminus with the list minus current listhouse, shallow copy of route and total time
        for lh in lh_list:
            get_routes(lh, list_minus(lh_list, lh), route[:], total_time)


lighthouse_index = 0


def fastest_tour(x, L):
    """Accepts string x, list L, returns float time, ordered list of fastest tour."""
    """L is assumed not to have x in it."""
    """I will add reasonable comments here, and always be sure to check for errors."""
    """I will not change the function signature or its return parameters."""
    """If I have any questions, I'll ask my instructor or come to office hours."""
    # make variables global
    global lighthouse_index
    global MIN_TIME
    global ROUTES

    ## call get routes with variables x, starting lighthouse, and the list of all other lighthouses L
    get_routes(x, L, [], 0)
    ## if the index of the lighthouse is the last one then minimum time is the minimum time of route map
    if lighthouse_index == len(LIGHTS) - 1:
        return MIN_TIME, ROUTES

    lighthouse_index += 1
    # new list uses the function list minus and subtracts the lighthouse we start with from the entire list
    new_list = list_minus(LIGHTS, LIGHTS[lighthouse_index])
    return fastest_tour(LIGHTS[lighthouse_index], new_list)


if __name__ == "__main__":
    t, r = fastest_tour(LIGHTS[0], list_minus(LIGHTS, LIGHTS[0]))
    print("time = {}, route = '{}'".format(t, ", ".join(r)))



