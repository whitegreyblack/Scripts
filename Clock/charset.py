import braille

__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"

# unused -- testing different character sets to represent numbers
lbracket = u'\u28CF'
rbracket = u'\u28F9'
lparenth = u'\u288E'
rparenth = u'\u2871'
lfilledp = u'\u28BE'
rfilledp = u'\u2877'

# unused -- testing literal character maps -- changed to cell mapping instead
blocks = {
    0: [
        # 0 1 2 3 4 5 6 7 8 9  (7x10)
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],  # 0
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],  # 1
        [1, 1, 0, 0, 0, 0, 1, 1, 1, 1],  # 2
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],  # 3
        [1, 1, 1, 1, 0, 0, 0, 0, 1, 1],  # 4
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],  # 5
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]   # 6
    ],
    1: [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, ]
    ],
    2: [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    3: [
        [0, 0, 2, 3, 2, 3, 2, 3, 0, 0],
        [2, 3, 0, 0, 0, 0, 0, 0, 2, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [0, 0, 0, 0, 2, 3, 2, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [2, 3, 0, 0, 0, 0, 0, 0, 2, 3],
        [0, 0, 2, 3, 2, 3, 2, 3, 0, 0]
    ]
}

# character key sets which represents a single cell in the grid map

# character key set creates a circular pattern for cells
circle = {
    0: braille.dot['to'][5],
    1: braille.dot['to'][8],
    2: braille.dot['tr'][8],
    3: braille.dot['tr'][5],
    4: braille.dot['bo'][5],
    5: braille.dot['bo'][8],
    6: braille.dot['br'][8],
    7: braille.dot['br'][5],
}
# character key set creates a block pattern for cells
squarekey = {
    0: braille.dot['to'][8],
    1: braille.dot['to'][8],
    2: braille.dot['to'][8],
    3: braille.dot['to'][8],
    4: braille.dot['to'][8],
    5: braille.dot['to'][8],
    6: braille.dot['to'][8],
    7: braille.dot['to'][8],
}

# 5 by 7 cell mapping -- each cell represents a 4x2 character set
number = {
    ':': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0], ],
    0: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
    1: [[0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0], ],
    2: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1], ],
    3: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
    4: [[0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0], ],
    5: [[1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
    6: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
    7: [[1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]],
    8: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
    9: [[0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0], ],
}
