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

I ran 1000 trials for each setting of parameters.

Here $\gamma$ is the discount rate, $\alpha$ is the learning rate and $\epsilon$
is the exploration rate (**NOTE:** in my code I used $1-\epsilon$ and called it
the exploration rate, it just seems more intuitive to me that way). 'avg.
reward' is the mean total reward over all the trials. 'avg. steps' is the
mean number of steps taken to get to the destination. 'missed deadline' is
the percentage of time that the smartcab does not make it to the destination in
time. `'violations'` is the mean of the mean number traffic laws broken for each
trial.

| $\gamma$ | $\alpha$ | $1-\epsilon$ | avg. reward | avg. steps | missed deadline | violations |
|----------|----------|--------------|-------------|------------|-----------------|------------|
|        1 |        1 |            1 |       0.172 |     27.744 | 79.6%           |      7.457 |
|        1 |        1 |            0 |     11.2285 |     25.388 | 62.1%           |      0.033 |
|        1 |        1 |          0.5 |      13.709 |     23.559 | 48.8%           |      3.221 |
|        1 |        1 |         0.75 |       7.443 |     26.263 | 67.3%           |      5.219 |
|        1 |        1 |         0.25 |      14.735 |     23.439 | 47.2%           |      1.679 |
|        1 |        1 |        0.125 |     16.0775 |     21.532 | 39.3%           |      0.752 |
|        1 |        1 |       0.0625 |     20.2465 |     16.633 | 13.8%           |       0.32 |
|        1 |        1 |      0.03125 |       16.66 |     18.664 | 30.9%           |      0.169 |
|        1 |        1 |     0.046875 |      15.804 |     20.664 | 37.1%           |      0.297 |
|        1 |        1 |         0.05 |      15.583 |     20.226 | 36.6%           |      0.315 |
|      0.5 |        1 |       0.0625 |     21.2075 |     14.498 | 6.3%            |      2.258 |
|     0.25 |        1 |       0.0625 |     21.4775 |     14.862 | 5.0%            |      2.607 |
|     0.75 |        1 |       0.0625 |      22.525 |     14.514 | 4.3%            |        0.3 |
|    0.875 |        1 |       0.0625 |        22.5 |     14.776 | 4.8%            |      0.305 |
|    0.625 |        1 |       0.0625 |     21.6565 |     14.695 | 5.6%            |      2.834 |
|    0.625 |      0.5 |       0.0625 |       22.29 |     13.813 | 2.0%            |      0.297 |
|    0.625 |     0.75 |       0.0625 |     21.2845 |     14.541 | 4.2%            |      2.675 |
|    0.625 |     0.25 |       0.0625 |     21.9775 |     14.131 | 1.5%            |      0.318 |
|    0.625 |    0.125 |       0.0625 |      22.578 |     13.566 | 1.2%            |      0.356 |
|    0.625 |   0.0625 |       0.0625 |     22.3385 |     14.006 | 1.9%            |       0.34 |
|    0.625 |      0.1 |       0.0625 |     22.4805 |     14.034 | 2.1%            |      0.374 |

My final parameter selection is 0.625 for the discount factor, 0.0625
explore rate (i.e. 0.9375 is $\epsilon$) and 0.125 learning rate.

The vehicle makes it to its destination before the deadline about 98.8% of the
time. It has a traffic violation in about 1 in 3 trials. The total reward is
between 22 and 23, and it takes between 13 and 14 steps to reach our
destination.

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
smartcab do? With the parameters I ultimately chose, it makes about 13-14 moves
on average. This is close to 2 times what the car could do if it was omniscient.
Our smartcab cannot be omniscient however. Considering that the smartcab is
learning its way as it goes along, I think that this performance is great!
Recalling that the number of possible state-action pairs is 348, by the time the
cab has made ~14 moves, it can't really have full information about the costs
and rewards of its actions yet. The fact that it can on average make it to the
destination with only about twice as many moves as strictly necessary, having
seen only a small fraction of the state-action pairs possible means it is
performing very well. Further, the cab only misses it's deadline about 1.2% of
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
than can be captured in a few if statements.
