from creature import Creature
from point import Point
from dice import Dice

class CombatSimulation:
    def __init__(self, max_rounds):
        """
        Combat simulation between two creatures.

        Args:
            max_rounds (int) - the maximum number of rounds declaring it a draw
        """
        self.max_rounds = max_rounds

    def run(self, creature1, creature2, verbose=False):
        """
        Runs a single simulation.

        Args:
            creature1, creature2 (Creature) - the opponents
            verbose (bool) - whether or not to print the results
        Returns:
            res (tuple) - res[0] = the winner (Creature) and res[1] = rounds played (int)
        """
        c1 = creature1
        c2 = creature2
        for r in range(self.max_rounds):
            if verbose:
                print '--- Round {}\n{}\' life: {}\n{}\'s life: {}\n'.format(r, c1.name, c1.life, c2.name, c2.life)

            ar1 = c1.attack(c2)
            ar2 = c2.attack(c1)

            if verbose:
                print '{0} {1} {2}.\n{2} {3} {0}.\n\n'.format(c1.name, ar1, c2.name, ar2)

            if not c1.alive() and c2.alive():
                if verbose:
                    print '{} won!'.format(c2.name)

                return (c2, r)
            if not c2.alive() and c1.alive():
                if verbose:
                    print '{} won!'.format(c1.name)

                return (c1, r)

        return (None, self.max_rounds)

    @staticmethod
    def run_suite(simulations=100):
        MAX_ROUNDS = 50

        name_a = 'Orc'
        name_b = 'Troll'
        matches = []

        # Run matches
        for i in range(simulations):
            orc = Creature(name_a, 1, Point(0, 0))
            troll = Creature(name_b, 1, Point(0, 0))

            cs = CombatSimulation(MAX_ROUNDS)

            result = cs.run(orc, troll)

            matches.append({'winner': result[0], 'rounds': result[1]})

        # Aggregate results
        a_wins = 0
        b_wins = 0
        a_rounds = 0
        b_rounds = 0
        draws = 0
        for match in matches:
            if match.get('winner', False):
                if match['winner'].name == name_a:
                    a_wins += 1
                    a_rounds += match['rounds']
                elif match['winner'].name == name_b:
                    b_wins += 1
                    b_rounds += match['rounds']
            else:
                draws += 1

        print 'SIMULATION RESULTS:\n{} won {} times\n{} won {} times\n{} draws\n'.format(name_a, a_wins, name_b, b_wins, draws)


if __name__ == '__main__':
    CombatSimulation.run_suite()