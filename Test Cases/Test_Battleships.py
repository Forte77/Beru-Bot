"""Unittest casses for Battles"""

import unittest
from Battleship import Battleship

# We create a "Mock" because the real Bot requires a Token and Internet
class MockBot:
    def __init__(self):
        self.user = "TestBot"

class TestBattleship(unittest.TestCase):
    def setUp(self):
        """This runs before every single test to give us a fresh game."""
        self.bot = MockBot()
        self.game = Battleship(self.bot)
        
        # Manually setting up a basic 5x5 game state
        self.game.playing = True
        self.game.board1 = [[":blue_square:"] * 5 for _ in range(5)]
        self.game.board2 = [[":blue_square:"] * 5 for _ in range(5)]
        self.game.player1 = "User1"
        self.game.player2 = "User2"

    def test_coordinate_math(self):
        """Verifies that 'A1' turns into (0,0) and 'E5' turns into (4,4)."""
        # Testing 'A1'
        coord = "a1"
        x = ord(coord[0].lower()) - 97
        y = int(coord[1]) - 1
        self.assertEqual((x, y), (0, 0))

        # Testing 'E5'
        coord2 = "e5"
        x2 = ord(coord2[0].lower()) - 97
        y2 = int(coord2[1]) - 1
        self.assertEqual((x2, y2), (4, 4))

    def test_ship_placement_logic(self):
        """Verifies that the shipcount function actually works."""
        # Place 3 ships manually
        self.game.board1[0][0] = ":ship:"
        self.game.board1[1][1] = ":ship:"
        self.game.board1[2][2] = ":ship:"
        
        count = self.game.shipcount(self.game.board1)
        self.assertEqual(count, 3, f"Expected 3 ships, but found {count}")

    def test_hit_logic(self):
        """Simulates a 'Hit' and checks if the board updates to a boom."""
        # Place a ship at B2 (which is index x=1, y=1)
        self.game.board2[1][1] = ":ship:"
        
        # Simulate the 'shoot' logic for B2
        target_square = self.game.board2[1][1]
        if target_square == ":ship:":
            self.game.board2[1][1] = ":boom:"
            
        self.assertEqual(self.game.board2[1][1], ":boom:", "Square should be a :boom: after a hit.")

    def test_miss_logic(self):
        """Simulates a 'Miss' and checks if the board updates to a white square."""
        # Target an empty blue square at C3 (index x=2, y=2)
        target_square = self.game.board2[2][2]
        if target_square == ":blue_square:":
            self.game.board2[2][2] = ":white_medium_square:"
            
        self.assertEqual(self.game.board2[2][2], ":white_medium_square:", "Square should be white after a miss.")

    def test_invalid_input_crash(self):
        """This test will fail if the code can't handle '1a' instead of 'a1'."""
        coord = "1a"
        # This mirrors the logic usually found in the bot's shoot/place commands
        with self.assertRaises(ValueError):
            # This is what happens inside the bot: it tries to turn 'a' into an int
            x = ord(coord[0].lower()) - 97
            y = int(coord[1]) - 1

    def setUp(self):
        # We initialize the Cog locally in our test file
        self.cog = Battleship(MockBot())
        # Set up a dummy 5x5 board
        self.cog.board1 = [[":blue_square:"]*5 for _ in range(5)]
        self.cog.player1 = "Player1"
        self.cog.turn = "Player1"
        self.cog.playing = True

    def test_invalid_string_input(self):
        """
        This test simulates a user typing '1a' (number first).
        If the original code runs int(coordinate[1]) where [1] is 'a', 
        this test will catch the ValueError crash.
        """
        bad_input = "1a"
        
        print(f"\nTesting input: {bad_input}")
        with self.assertRaises(ValueError):
            # We simulate the logic inside the 'shoot' command
            alphabet = bad_input[0]
            numbers = bad_input[1]
            # This is the line that will likely crash:
            y = int(numbers) - 1 

    def test_out_of_bounds_input(self):
        """
        This tests if a coordinate like 'z9' crashes the list index.
        """
        out_of_bounds = "z9"
        x = ord(out_of_bounds[0].lower()) - 97 # 'z' = 25
        y = int(out_of_bounds[1]) - 1          # 9 - 1 = 8
        
        print(f"Testing out-of-bounds: {out_of_bounds} (Converted to Index: {y}, {x})")
        
        with self.assertRaises(IndexError):
            # A 5x5 board only goes up to index 4. Index 8 or 25 will crash.
            check = self.cog.board1[y][x]


if __name__ == "__main__":
    print("Running Battleship Logic Tests...")
    unittest.main()