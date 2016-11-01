***QUESTION***: _Observe what you see with the agent's behavior as it takes
random
actions. Does the smartcab eventually make it to the destination? Are there any
other interesting observations to note?_

Yes, the cab makes it to its destination eventually. It can take a really long
time though, and it's actually not guaranteed to ever reach the destination
(intuition --- it is possible for the random sequence of moves to just all be
left
turns, although this is ridiculously unlikely). This is actually limited to
100 steps past the deadline in `environment.py`. The car makes no attempt to
minimize the length of its route, or to avoid other vehicles, it just eventually
stumbles onto its destination.

***QUESTION:*** _What states have you identified that are appropriate for
modeling the **smartcab** and environment? Why do you believe each of these
states to be appropriate for this problem?_

The appropriate parts of the smartcab's state are ``'light'``: the light at the
current intersection, ``'oncoming'``: the presence of oncoming traffic,
``'left'``: the presence of traffic approaching from the left, and
``'next_waypoint'``: the current direction of travel. ``'light'`` tells us
whether or not we can proceed in the current direction or turn left, depending
on the actions of other cars. `'oncoming'` can restrict whether or not we can
turn left given a green light. ``'next_waypoint'`` differentiates the current
direction of our movement. Our current orientation decides where we will end up
given an action and our current position.

It's worth noting that ``'right'`` is not necessary. On a green light, there is no
restriction on our movement due to traffic approaching from the right. On a red
light, the only move we're allowed to make is a ``'left'`` turn, but this again
is
unaffected by approaching traffic from the right.

I have also chosen to keep `'deadline'` out of the state. My reasoning is
that whether or not the deadline has actually passed should not affect the
optimal strategy for maximizing the agent's reward. In general, the agent is
attempting to minimize travel time, the approach of the deadline should not
affect this motive. Further, with `enforce_deadline` set to `True` the
simulation will end as soon as the deadline has been missed. Including the
actual deadline value would increase the size of the state space by a very large
amount, especially if the deadline can be arbitrarily large. This would make
Q-learning much more difficult. Keeping a binary value that tells us whether or
not we have failed to reached the deadline is also not helpful as stated
previously; the failure of the trial will give us just as much information as
keeping a binary variable would.

***OPTIONAL:*** _How many states in total exist for the **smartcab** in this
environment? Does this number seem reasonable given that the goal of Q-Learning
is to learn and make informed decisions about each state? Why or why not?_

There are 2 states for `'light'`, 4 states each for `'oncoming'` and `'left'`,
and
3 states for `'waypoint'`. In total there are $2*4*4*3=96$ possible states. There
are 4 possible actions, making a total of 384 possible states. This  is a
relatively small number of states, and should be very amenable to Q-learning.

***QUESTION:*** _What changes do you notice in the agent's behavior when
compared to the basic driving agent when random actions were always taken? Why
is this behavior occurring?_

The agents movements are much more measured. They are clearly no longer random,
as the agent now continues along the same path much more often, and seems to
gradually move closer to the target. In general, the agent converges on the
destination in much less time than it did with the random action selection.

This is due to the presence of an adaptive policy. The agent will generally act
in a manner that has historically maximized utility, while occasionally taking a
random action to explore the unknown.

***QUESTION:*** _Report the different values for the parameters tuned in your
basic implementation of Q-Learning. For which set of parameters does the agent
perform best? How well does the final driving agent perform?_

I ran 100 trials for each setting of parameters.

Here $\gamma$ is the discount rate, $\alpha$ is the learning rate and $\epsilon$
is the exploration rate (**NOTE:** in my code I used $1-\epsilon$ and called it
the exploration rate, it just seems more intuitive to me that way). 'avg.
reward' is the mean total reward over all the trials. 'avg. steps' is the
mean number of steps taken to get to the destination. 'missed deadline' is
the percentage of time that the smartcab does not make it to the destination in
time. `'violations'` is the mean of the mean number traffic laws broken for each
trial.

| $\gamma$ | $\alpha$ | $1-\epsilon$ | avg. reward | avg. steps | missed deadlines | violations |
|----------|----------|--------------|-------------|------------|------------------|------------|
|        1 |        1 |            1 |       0.055 |      28.48 | 84.0%            |       7.84 |
|        1 |        1 |          0.5 |      11.605 |      24.51 | 60.0%            |       3.13 |
|        1 |        1 |         0.75 |        5.15 |      27.34 | 77.0%            |       5.21 |
|        1 |        1 |         0.25 |      14.382 |     23.433 | 49.3%            |      1.638 |
|        1 |        1 |        0.125 |       15.54 |      21.58 | 39.0%            |       0.83 |
|        1 |        1 |       0.0625 |       16.22 |      20.64 | 34.0%            |       0.57 |
|        1 |        1 |      0.03125 |      17.705 |      17.28 | 22.0%            |       0.31 |
|        1 |        1 |         0.03 |      16.735 |      19.76 | 32.1%            |      0.164 |
|        1 |        1 |         0.01 |      16.504 |     19.671 | 32.1%            |      0.088 |
|      0.5 |        1 |      0.03125 |       22.87 |      15.08 | 2.0%             |       0.27 |
|     0.25 |        1 |      0.03125 |      21.815 |      12.42 | 1.0%             |       0.22 |
|    0.125 |        1 |      0.03125 |       21.47 |      13.68 | 6.0%             |       0.95 |
|   0.1875 |        1 |      0.03125 |       22.93 |      13.94 | 1.0%             |        0.7 |
|     0.25 |      0.5 |      0.03125 |       22.72 |      12.92 | 1.0%             |       0.26 |
|     0.25 |     0.25 |      0.03125 |      21.925 |      13.59 | 2.0%             |       0.33 |


My final parameter selection is 0.25 for the discount factor, 0.03125
explore rate (i.e. 0.96875 is $\epsilon$) and 0.5 learning rate.

I ran a further 10,000 trials with this parameterization, and found
an average reward of 22.3196, 13.25 average steps, 0.77% of deadlines missed and
0.1361 violations per trial.

The vehicle makes it to its destination before the deadline about 99.23% of the
time. It has a traffic violation in about 1 in 7 trials. The total reward is
between 22 and 23, and it takes about 13 steps to reach the destination.

***QUESTION:*** _Does your agent get close to finding an optimal policy, i.e.
reach the destination in the minimum possible time, and not incur any penalties?
How would you describe an optimal policy for this problem?_

On our grid, the average distance between 2 points will be 2 in the vertical
direction and about 2 in the horizontal direction. That means that if the car
going in the right direction, it can get there in 4 moves on average. If going
in the wrong direction, the car can turn around by moving in a loop, which
requires 4 moves, for a total of about 8 moves. That means that in the average
case, the car should be able to reach its destination in about 6 moves. In
truth,
the lower bound should be slightly higher, as I haven't factored in the
possibility of waiting at a red light as part of the optimal strategy (I've made
the implicit assumption that at every turn the cab can move 1 intersection
closer to the destination).

So with 6 moves established as a theoretical lower bound, how well does our
smartcab do? With the parameters I ultimately chose, it makes about 13 moves
on average. This is close to 2 times what the car could do if it was omniscient.
Our smartcab cannot be omniscient however. Considering that the smartcab is
learning its way as it goes along, I think that this performance is great!
Recalling that the number of possible state-action pairs is 348, by the time the
cab has made ~13 moves, it can't really have full information about the costs
and rewards of its actions yet. The fact that it can on average make it to the
destination with only about twice as many moves as strictly necessary, having
seen only a small fraction of the state-action pairs possible means it is
performing very well. Further, the cab only misses it's deadline about 0.77% of
the time.

An optimal policy for this problem would always make the right move, the one
maximizes utility or expected reward. In this case, the optimal policy is to
almost always make a move one step closer to the destination, when such a move
is
legal. At other times, it may make sense due to traffic conditions to take a
longer route, since the goal is not to optimize trip distance, but trip time.
Thus the shortest distance does not necessarily correspond to the best path to
take.

An optimal agent will certainly not commit any violations. In my code, I could
make my agent avoid illegal actions in the
update method by checking if the chosen action is illegal and making it choose
again until it selects a legal move, but this feels like "cheating" and seems
like it would be against the spirit of the assignment. In the real world, the
vehicle would not necessarily have *perfect* information about the intersection
that it's at, and driving laws and best practices are probably a lot more
complex
than can be captured in a few if statements. It is still necessary for our agent
to attempt *some* illegal moves so that it learns which moves are actually
illegal.
