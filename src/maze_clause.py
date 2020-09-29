#!/usr/bin/env python
'''
maze_clause.py

Specifies a Propositional Logic Clause formatted specifically
for Grid Maze Pathfinding problems. Clauses are a disjunction of
MazePropositions (2-tuples of (symbol, location)) mapped to
their negated status in the sentence.
'''
import unittest
import sys
from pprint import pprint

# "X" is a symbol
# (1, 1) is the location of the symbol
# True/False is the negated status
# (("X", (1, 1)), True) is an assignment of a truth value to the proposition

class MazeClause:
    
    def __init__(self, props):
        """
        Constructor parameterized by the propositions within this clause;
        argument props is a list of MazePropositions, like:
        [(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)]

        Conversion into prop logic: X(1,1) v X(2,1) v ~Y(1,2)
        
        :props: a list of tuples formatted as: (MazeProposition, NegatedBoolean)
        """
        self.props = {}
        self.valid = False # Might change as you're loading in the props
        # TODO: Process list of propositions to make a correctly
        # formatted MazeClause

        print("MAZE > CONSTRUCTOR PROPS > props:")
        pprint(props)

        for tup in props:

            symbol = tup[0]
            truth = tup[1]

            if symbol in self.props:
                print("  SYMBOL EXISTS, checking TRUTH value")

                if truth != self.props[symbol]:
                    print("  SYMBOL EXISTS > TRUTH value is negated, we're done!")
                    self.props = {}
                    self.valid = True
            else:

                print("  SYMBOL DOES NOT EXIST > tup:")
                pprint(tup)
                self.props[symbol] = truth
                print("MAZE > CONSTRUCTOR PROPS > props > update self.props:")
                pprint(self.props)
    
    def get_prop(self, prop):
        """
        Returns:
          - None if the requested prop is not in the clause
          - True if the requested prop is positive in the clause
          - False if the requested prop is negated in the clause
          
        :prop: A MazeProposition as a 2-tuple formatted as: (Symbol, Location),
        for example, ("P", (1, 1))
        """
        # TODO: This is currently implemented incorrectly; see
        # spec for details!

        print("INCOMING PROP:")
        pprint(prop)
        # pprint(self.props)
        if prop in self.props:
            print("PROP IN PROPS: YES")
            pprint(prop)
            return self.props[prop]
        else:
            print("PROP IN PROPS: NO")
            pprint(prop)
            return None

        return False
    
    def is_valid(self):
        """
        Returns:
          - True if this clause is logically equivalent with True
          - False otherwise
        """
        return self.valid
    
    def is_empty(self):
        """
        Returns:
          - True if this is the Empty Clause
          - False otherwise
        (NB: valid clauses are not empty)
        """

        if self.valid:
            return False

        return not bool(self.props)
    
    def __eq__(self, other):
        """
        Defines equality comparator between MazeClauses: only if they
        have the same props (in any order) or are both valid
        """
        return self.props == other.props and self.valid == other.valid
    
    def __hash__(self):
        """
        Provides a hash for a MazeClause to enable set membership
        """
        # Hashes an immutable set of the stored props for ease of
        # lookup in a set
        return hash(frozenset(self.props.items()))
    
    # Hint: Specify a __str__ method for ease of debugging (this
    # will allow you to "print" a MazeClause directly to inspect
    # its composite literals)
    # def __str__ (self):
    #     return ""
    
    @staticmethod
    def resolve(c1, c2):
        """
        Returns a set of MazeClauses that are the result of resolving
        two input clauses c1, c2 (Hint: result will only ever be a set
        of 0 or 1 MazeClause, but it being a set is convenient for the
        inference engine) (Hint2: returning an empty set of clauses
        is different than returning a set containing the empty clause /
        contradiction)
        
        :c1: A MazeClause to resolve with c2
        :c2: A MazeClause to resolve with c1
        """
        results = set()
        # TODO: This is currently implemented incorrectly; see
        # spec for details!

        print("RESOLVE > C1.props:")
        pprint(c1.props)

        print("RESOLVE > C2.props:")
        pprint(c2.props)

        # Tuples to be passed to the resulting MazeClause
        # tuples = []
        tuples = set()

        for tup1, bool1 in c1.props.items():
            print("RESOLVE > TUP1:")
            print(tup1)
            print(bool1)

            addToSet = True
            for tup2, bool2 in c2.props.items():
                print("  RESOLVE > TUP2:")
                print("  ", end = '')
                print(tup2)
                print("  ", end = '')
                print(bool2)
                if tup1 == tup2:
                    print("    EQUAL!")
                    if bool1 != bool2:
                        print("      OPPOSITE SIGNS!")
                        addToSet = False
            
            if addToSet:
                print("      ADDING TO SET!")
                tuples.add((tup1, bool1))

        for tup1, bool1 in c2.props.items():
            print("RESOLVE > TUP1:")
            print(tup1)
            print(bool1)

            addToSet = True
            for tup2, bool2 in c1.props.items():
                print("  RESOLVE > TUP2:")
                print("  ", end = '')
                print(tup2)
                print("  ", end = '')
                print(bool2)
                if tup1 == tup2:
                    print("    EQUAL!")
                    if bool1 != bool2:
                        print("      OPPOSITE SIGNS!")
                        addToSet = False
            
            if addToSet:
                print("      ADDING TO SET!")
                tuples.add((tup1, bool1))

        print("TUPLES:")
        print(tuples)

        result = MazeClause(tuples)
        results.add(result)
        return results
    

class MazeClauseTests(unittest.TestCase):
    def test_mazeprops1(self):
        print("TEST MAZE PROPS 1")
        mc = MazeClause([(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)])
        print("TEST MAZE PROPS 1 - ASSERT 1")
        self.assertTrue(mc.get_prop(("X", (1, 1))))
        print("TEST MAZE PROPS 1 - ASSERT 2")
        self.assertTrue(mc.get_prop(("X", (2, 1))))
        print("TEST MAZE PROPS 1 - ASSERT 3")
        self.assertFalse(mc.get_prop(("Y", (1, 2))))
        print("TEST MAZE PROPS 1 - ASSERT 4")
        self.assertTrue(mc.get_prop(("X", (2, 2))) is None)
        print("TEST MAZE PROPS 1 - ASSERT 5")
        self.assertFalse(mc.is_empty())
        # raise SystemExit
        # sys.exit()
        
    def test_mazeprops2(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (1, 1)), True)])
        print("TEST 2 - ASSERT 1")
        self.assertTrue(mc.get_prop(("X", (1, 1))))
        print("TEST 2 - ASSERT 2")
        self.assertFalse(mc.is_empty())
        
    def test_mazeprops3(self):
        print("\nTEST 3 - CONSTRUCTOR")
        mc = MazeClause([(("X", (1, 1)), True), (("Y", (2, 1)), True), (("X", (1, 1)), False)])
        # mc = MazeClause([
        #     (("X", (1, 1)), True), (("X", (1, 1)), False),
        #     (("Y", (1, 1)), True), (("Y", (1, 1)), False),
        #     (("Z", (1, 1)), True)
        #     ])
        print("\nTEST 3 - ASSERT 1")
        self.assertTrue(mc.is_valid())
        print("TEST 3 - ASSERT 2")
        self.assertTrue(mc.get_prop(("X", (1, 1))) is None)
        print("TEST 3 - ASSERT 3")
        self.assertFalse(mc.is_empty())
        
    def test_mazeprops4(self):
        print("TEST 4 START")
        mc = MazeClause([])
        self.assertFalse(mc.is_valid())
        self.assertTrue(mc.is_empty())
        print("TEST 4 END")
        
    def test_mazeprops5(self):
        print("\nTEST 5 START")

        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        print("\nTEST 5 - ASSERT 1")
        self.assertEqual(len(res), 0)
        print("TEST 5 END")
        
    def test_mazeprops6(self):
        print("TEST 6")
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([]) in res)
        
    def test_mazeprops7(self):
        print("TEST 7 START")
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (2, 2)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), True), (("Y", (2, 2)), True)]) in res)
        
    def test_mazeprops8(self):
        print("TEST 8 START")
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)
        
    def test_mazeprops9(self):
        print("TEST 9 START")
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)
        
    def test_mazeprops10(self):
        print("TEST 10 START")
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True), (("W", (1, 1)), False)]) in res)
        print("TEST 10 END")
        
if __name__ == "__main__":
    unittest.main(failfast=True)
    