import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import Counter

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.state = {}
        self.q_table = {}
        self.discount_factor = 0.625
        self.learning_rate = 0.0625
        self.explore_rate = 0.03
        self.stats = {'missed_deadline': 0, 'steps': 0, 'total_reward': 0, 'violations': 0, 'crashes': 0}

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        # simply a tuple of the current intersection and where we're headed next
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'], self.next_waypoint)

        # TODO: Select action according to your policy
        if any(k[0] == self.state for k in self.q_table):
            if random.random() < self.explore_rate:
                action = self.take_random_action()
            else:
                action = self.best_known_action()[0]
        else:
            for a in [None, 'forward', 'left', 'right']:
                self.q_table[(self.state, a)] = 1
            action = self.take_random_action()
            self.q_table[(self.state, action)] = 1

        # Execute action and get reward
        reward = self.env.act(self, action)

        if deadline == 0:
            self.stats['missed_deadline'] += 1


        if inputs['light'] == 'red' and action not in ('right', None):
            self.stats['violations'] += 1
        elif inputs['light'] == 'red' and action == 'right' and inputs['left'] != None:
            self.stats['violations'] += 1
        elif inputs['light'] == 'green' and action == 'left' and inputs['oncoming'] in ('right', 'forward'):
            self.stats['violations'] += 1

        self.stats['steps'] += 1
        self.stats['total_reward'] += reward


        # TODO: Learn policy based on state, action, reward
        new_waypoint = self.planner.next_waypoint()
        new_inputs = self.env.sense(self)
        new_state = (new_inputs['light'], new_inputs['oncoming'], new_inputs['left'], new_waypoint)

        max_neighbor = self.best_known_action()[1]

        self.q_table[(self.state, action)] = (1-self.learning_rate) * (self.q_table[(self.state, action)] + self.learning_rate * (reward + self.discount_factor * max_neighbor))

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

    def take_random_action(self):
        return random.choice([None, 'forward', 'left', 'right'])


    def best_known_action(self):
        max_utility = 0
        best_action = self.take_random_action()

        for (state, action) in self.q_table:
            if(state == self.state and self.q_table[(state, action)] > max_utility):
                max_utility = self.q_table[(state, action)]
                best_action = action
        return (best_action, max_utility)


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    # sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    sim = Simulator(e, update_delay=0.0, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    trials = 10000
    sim.run(n_trials=trials)  # run for a specified number of trials
    print_stats(a.stats, trials)

    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

def print_stats(stats, trials=100):
    avg_reward = stats['total_reward'] / float(trials)
    avg_steps = stats['steps'] / float(trials)
    missed_per = stats['missed_deadline'] * 100. / trials
    violations = stats['violations'] / float(trials)
    print "{}\t{}\t{}%\t{}".format(avg_reward, avg_steps, missed_per, violations)

if __name__ == '__main__':
    run()
