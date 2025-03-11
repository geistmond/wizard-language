# Discrete Event Simulation Demo
# Movie theater simulation is an example of a resource manager simulation -- starting there
# This will become some other resource that involves a wait, like a powerup

import simpy # SimPy is used for discrete event simulation with consumables wheras SymPy is for symbolic computation
import statistics
import secrets

wait_times = []

class Theater(object):
    def __init__(self, 
                 env, 
                 num_cashiers,
                 num_servers,
                 num_ushers):
        self.env = env
        self.cashiers = simpy.Resource(env, num_cashiers)
        self.servers = simpy.Resource(env, num_servers)
        self.ushers = simpy.Resource(env, num_ushers)
        
    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(secrets.SystemRandom().randint(1,3))
        
    def check_ticket(self, moviegoer):
        yield self.env.timeout(3/60)
        
    def sell_food(self, moviegoer):
        yield self.env.timeout(secrets.SystemRandom().randint(1,5))
        

def go_to_movies(env, moviegoer, theater):
    arrival_time = env.now
    
    with theater.cashiers.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))
        
    with theater.ushers.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))
        
    if secrets.choice([True,False]):
        with theater.servers.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))
            
    wait_times.append(env.now - arrival_time)
    

def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)
    for moviegoer in range(3):
        env.process(go_to_movies(env, moviegoer, theater))
    while True:
        yield env.timeout(0.20) # interval to wait between people
        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))
        

def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    minutes, minutes_decimal = divmod(average_wait, 1)
    seconds = minutes_decimal * 60
    return round(minutes), round(seconds)

def get_user_input():
    num_cashiers = input("Number of cashiers working: ")
    num_servers = input("Number of servers working: ")
    num_ushers = input("Number of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. Simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher.",
        )
        params = [1, 1, 1]
    return params

def main():
    secrets.SystemRandom().seed(123)
    #num_cashiers, num_servers, num_ushers = get_user_input()
    num_cashiers, num_servers, num_ushers = 10, 10, 10
    
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)
    
    mins, secs = get_average_wait_time(wait_times)
    print(f"The average wait time is {mins} minutes and {secs} seconds.")
    

if __name__ == "__main__":
    main()
