"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from util import is_prime, next_prime

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    "*** REPLACE THIS LINE ***"
    result = list(dice() for num in range(num_rolls))
    if 1 in result:
        return 0
    return sum(result)
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    "*** REPLACE THIS LINE ***"
    if num_rolls == 0:
        sum_res = 1 + int(max(s for s in str(opponent_score)))
    else:
        sum_res = roll_dice(num_rolls, dice)
    if is_prime(sum_res):
        return next_prime(sum_res)
    return sum_res
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    "*** REPLACE THIS LINE ***"
    assert score >= 0, 'Score must be not negetive'
    if (score + opponent_score) % 7 == 0:
        return four_sided
    return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    "*** REPLACE THIS LINE ***"
    num = list(s for s in str('%02d'%(score0)))
    num = num[::-1]
    num1 = list(s for s in str('%02d'%(score1)))
    if ''.join(num[0:2]) == ''.join(num1[-2:]):
        return True
    return False
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"
    Done = False
    while not Done:
        try:
            num0 = strategy0(score0, score1)
            dice_type = select_dice(score0, score1)
            tmpScore = take_turn(num0, score1, dice_type)
            score0 += tmpScore
            if tmpScore == 0:
                score1 += num0
            if is_swap(score0, score1):
                score0, score1 = score1, score0
            if score0 >= goal or score1 >= goal:
                return score0, score1

            num1 = strategy1(score1, score0)
            dice_type = select_dice(score1,score0)
            tmpScore = take_turn(num1, score0, dice_type)
            score1 += tmpScore
            if tmpScore == 0:
                score0 += num1
            if is_swap(score0, score1):
                score0, score1 = score1, score0
            if score0 >= goal or score1 >= goal:
                return score0, score1
        except AssertionError:
            Done = True
    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    "*** REPLACE THIS LINE ***"
    i, res = 0, 0
    def func(*args):
        nonlocal i, res
        while i < num_samples:
            res += fn(*args)
            i += 1
        return res/num_samples
    return func
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"
    nums = []
    for i in range(1,11):
        num = make_averaged(roll_dice, num_samples)(i,dice)
        nums.append(num)
    return nums.index(max(nums)) + 1
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:
        print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    num = 1 + int(max(s for s in str(opponent_score)))

    if is_prime(num):
        num = next_prime(num)

    return 0 if num >= margin else num_rolls
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    num = 1 + int(max(s for s in str(opponent_score)))

    if is_prime(num):
        num = next_prime(num)
    if is_swap(score+num, opponent_score) and opponent_score > score+num:
        return 0
    return num_rolls
    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    # num = 1 + int(max(s for s in str(opponent_score)))
    #
    # if is_prime(num):
    #     num = next_prime(num)
    #
    # set_up = False
    # for i in range(1, 11):
    #     if is_swap(i+opponent_score, score) and opponent_score > score:
    #         set_up_num = i
    #         set_up = True
    #
    # num_rolls = []
    #
    # for i in range(1, 11):
    #     if gene_expectation(i, score, opponent_score) > num:
    #         num_rolls.append(i)
    #
    # if num + score >= 100 and not is_swap(score+num, opponent_score):
    #     return 0
    # if set_up:
    #     return set_up_num
    # if num_rolls:
    #     return num_rolls.pop()
    #
    # return 0  # Replace this statement
    # END Question 10
    setup = False
    for n in range(1,11):
        if is_swap(n + opponent_score, score) and opponent_score > score:
            setup_num_rolls = n
            setup = True



    free_p = 1 + max([int(i) for i in str(opponent_score)][-2::])
    if is_prime(free_p):
        free_p = next_prime(free_p)

    SHOT = False
    p_num_rolls = []
    for n in range(1,11):
        if gene_expectation(n, score, opponent_score) > free_p:
            p_num_rolls.append(n)
            SHOT = True

    if free_p + score >= 100 and not is_swap(free_p + score, opponent_score):
        return 0
    elif setup:
        num_rolls = setup_num_rolls
        return num_rolls
    elif SHOT and score <= 94:
        if len(p_num_rolls) >= 2:
            return p_num_rolls[1]
        else:
            return p_num_rolls[0]

    elif is_swap(free_p + score, opponent_score) and free_p + score > opponent_score:
        return 5
    else:
        return 0

def gene_expectation(n, score, opponent_score):
    if (score + opponent_score) % 7 == 0:
        return (((2+3+4)/4)**n)*n - (1-(3/4)**n)*n
    return (((2+3+4+5+6)/6)**n)*n - (1-(5/6)**n)*n


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
