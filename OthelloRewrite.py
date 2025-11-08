import sys; args = sys.argv[1:]
import time

global board, token, moveLst, width, rowEndSet, opp, rowBegSet, corners, cornerNeighbors, neighbors, edgesLst, cornerEdges, MOVESCACHE, MAKEMOVECACHE, edges, EVALCACHE, terse, OPENINGBOOK

#args = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxx.xxooo....................".split(" ")

width = 8
board = '.'*27+'ox......xo'+'.'*27 
token = ''
terse = True
movesLst = []
MOVESCACHE = {}
MAKEMOVECACHE = {}
EVALCACHE = {}
OPENINGBOOK = {"...........................ox......xo...........................": [19], #x
               "..................ox.......ox......xo...........................": [26],
               "..................ooo.....xxo......xo...........................": [11],
               "..........ox......ooo.....xxo......xo...........................": [12],
               "..........oooo....oxo.....xxo......xo...........................": [17],
               "..........oooo...xoxo....oooo......xo...........................": [3],
               "...x......xxoo...xoxo....oooo.....ooo...........................": [32],
               "..ox......oooo...xoxo....xooo...x.ooo...........................": [1],
               ".xxx......xooo..oooxo....oooo...x.ooo...........................": [4],
               ".xxxx.....xxoo..ooxxo....oooo...xoooo...........................": [5],
               ".xxxxx...ooooo..oooxo....oooo...xoooo...........................": [22],
               ".xxxxx...oooooo.oooxo.x..oooo...xoooo...........................": [23],
               ".xxxxx...ooooox.oooxo.ox.oooo..oxoooo...........................": [39], 
               ".xxxxxo..oooooo.oooxo.ox.oooo..xxoooo..x........................": [7],
               ".xxxxxxx.oooooo.oooxo.ox.oooo..xxoooo..x........................": [42],
               ".xxxxxxx.oxoooo.ooxxo.ox.oxoo..xxoooo..x.ox.....................": [15],
               ".xxxxxxx.oxxxxxxooxxo.ox.oxoo..xxoooo..x.ooo....................": [0],
               "xxxxxxxx.xxxxxxxooxxo.ox.oxoo..xxoooo..x.ooo....................": [8],
               "xxxxxxxxxxxxxxxxoxxxo.ox.oxoo..xxoooo..x.ooo....................": [24],
               "xxxxxxxxxxxxxxxxxxxxo.oxxxxoo..xxoooo..x.ooo....................": [40],
               "xxxxxxxxxxxxxxxxxxxxo.oxxxxoo..xxxooo..xxooo....................": [21],
               "xxxxxxxxxxxxxxxxxxxxxxxxxxxoo..xxxooo..xxooo....................": [29],
               "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxooo..xxooo....................": [37],
               #"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxx.xxooo....................": [44],
               
               "...................x.......xx......xo...........................": [34], #o
               "...................x.......xx.....xoo....x......................": [21],
               "...................x.o.....xxx....xoo....x......................": [20],
               "...........x.......xxo.....xox....xoo....x......................": [37],
               "...........x.......xxxx....xoo....xooo...x......................": [12],
               "...........xxx.....xxxx....xoo....xooo...x......................": [26],
               "...........xxx....xxxxx...xooo....xooo...x......................": [10],
               "..........oxxx....xoxxx...xxxxx...xooo...x......................": [4], 
               "....o.....oxox....xooxx...xxoxx...xxxxx..x......................": [3],
               "..xoo.....xxox....xoxxx...xxoxx...xxxxx..x......................": [1],
               ".oooox....oxxx....xxxxx...xxoxx...xxxxx..x......................": [6],
               ".oooooo..xxxxx....xxxxx...xxoxx...xxxxx..x......................": [25],
               ".oooooo..xxoxx...xxxxxx..oxooxx...xxxxx..x......................": [0],
               "ooooooo..oxoxx...xoxxxx..xxooxx..xxxxxx..x......................": [40],
               "ooooooo..oxoox...xooxxx..xoooxx.xxxxxxx.ox......................": [8],
               "ooooooo.ooxoox..xxxxxxx..xoooxx.xxxxxxx.ox......................": [24],
               "ooooooo.ooooox..ooxxxxx.oooooxx.oxxxxxx.ox......................": [49],
               "ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......xo..............": [56],
               "ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......ox......ox......": [58],
               "ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......oo......ooo.....": [50],
               "ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.oo......ooo.....ooo.....": [42], 
               "ooooooo.ooooox..ooxxxxx.oooxoxx.oooxxxx.ooox....ooo.....ooo.....": [51], 
               "ooooooo.ooooox..ooxoxxx.oooooxx.ooooxxx.oooo....oooo....ooo.....": [14],
               "ooooooo.ooooooo.ooxoxox.oooooxx.ooooxxx.oooo....oooo....ooo.....": [23], 
               "ooooooo.oooooooxooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....": [7], 
               "ooooooooooooooooooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....": [47], 
               "ooooooooooooooooooxoooxooooooox.ooooxxx.oooo..xooooo....ooo.....": [31], 
               "ooooooooooooooooooxoooooooooooooooooxxx.oooo..xooooo....ooo.....": [39], 
               "ooooooooooooooooooxooooooooxooooooooxooooooo.xxooooo....ooo.....": [54]
               }
for s in args:
    terse = False if s == "v" or s == "V" else True
    if len(s) == 64 and "_" not in s and not s.isdigit():
        board = s.lower()
    if s in {*'XxoO'}:
        token = s.lower()
    if s.isdigit():
        if int(s) <= 63:
            movesLst.append(s)
        else:
            mvs = [s[i:i+2] for i in range(0, len(s), 2)]
            for idx, m in enumerate(mvs):
                if "_" in m:
                    m = m.replace("_", "")
                    mvs[idx] = m
            movesLst += mvs
    if len(s) == 2 and not s.isdigit():
        movesLst.append(s.upper())
    elif "_" in s:
        mvs = [s[i:i+2] for i in range(0, len(s), 2)]
        for idx, m in enumerate(mvs):
            if "_" in m:
                m = m.replace("_", "")
                mvs[idx] = m
        movesLst += mvs

if token == '':
    c = board.count("x") + board.count("o")
    token = "x" if c%2 == 0 else "o"

if "-2" in movesLst: movesLst.remove("-2")

rowEndSet = {(width * i) - 1 for i in range(1, width+1)}
rowBegSet = {i for i in range(0, len(board), width)}

corners = {0, 7, 56, 63}
cornerNeighbors = {1:0, 8:0, 9:0, 6:7, 14:7, 15:7, 48:56, 49:56, 57:56, 54:63, 55:63, 62:63}

edgesLst = [[0,1,2,3,4,5,6,7], [0,8,16,24,32,40,48,56], [56,57,58,59,60,61,62,63], [7,15,23,31,39,47,55,63]]
edges = {0:"th", 1:"th", 2:"h", 3:"th", 4:"th", 5:"th", 6:"th", 7:"th", 
        8:"lv", 16:"lv", 24:"lv", 32:"lv", 40:"lv", 48:"lv", 56:"lv", 57:"bh", 
        58:"bh", 59:"bh", 60:"bh", 61:"bh", 62:"bh", 63:"bh", 55:"rv", 47:"rv", 39:"rv", 31:"rv", 23:"rv", 15:"rv"}
cornerEdges = {32: 56, 1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 63, 8: 56, 40: 56, 16: 56, 48: 56, 24: 56, 56: 63, 0: 56, 39: 63, 
15: 63, 47: 63, 23: 63, 55: 63, 31: 63, 63: 56, 57: 63, 58: 63, 59: 63, 60: 63, 61: 63, 62: 63}
neighbors = {0: [1, 8, 9], 1: [0, 2, 8, 9, 10], 2: [1, 3, 9, 10, 11], 3: [2, 4, 10, 11, 12], 4: [3, 5, 11, 12, 13], 5: [4, 6, 12, 13, 14], 6: [5, 7, 13, 14, 15], 7: [6, 14, 
15], 8: [0, 1, 9, 16, 17], 9: [0, 1, 2, 8, 10, 16, 17, 18], 10: [1, 2, 3, 9, 11, 17, 18, 19], 11: [2, 3, 4, 10, 12, 18, 19, 20], 12: [3, 4, 5, 11, 13, 19, 20, 21], 13: [4, 5, 6, 12, 14, 20, 21, 22], 14: [5, 6, 7, 13, 15, 21, 22, 23], 15: [6, 7, 14, 22, 23], 16: [8, 9, 17, 24, 25], 17: [8, 9, 10, 16, 18, 24, 25, 26], 18: 
[9, 10, 11, 17, 19, 25, 26, 27], 19: [10, 11, 12, 18, 20, 26, 27, 28], 20: [11, 12, 13, 19, 21, 27, 28, 29], 21: [12, 13, 14, 20, 22, 28, 29, 30], 22: [13, 14, 15, 21, 23, 29, 30, 31], 23: [14, 15, 22, 30, 31], 24: [16, 17, 25, 32, 33], 25: [16, 17, 18, 24, 26, 32, 33, 34], 26: [17, 18, 19, 25, 27, 33, 34, 35], 27: [18, 
19, 20, 26, 28, 34, 35, 36], 28: [19, 20, 21, 27, 29, 35, 36, 37], 29: [20, 21, 22, 28, 30, 36, 37, 38], 30: [21, 22, 23, 29, 31, 37, 38, 39], 31: [22, 23, 30, 38, 39], 32: [24, 25, 33, 40, 41], 33: [24, 25, 26, 32, 34, 40, 41, 42], 34: [25, 26, 27, 33, 35, 41, 42, 43], 35: [26, 27, 28, 34, 36, 42, 43, 44], 36: [27, 28, 
29, 35, 37, 43, 44, 45], 37: [28, 29, 30, 36, 38, 44, 45, 46], 38: [29, 30, 31, 37, 39, 45, 46, 47], 39: [30, 31, 38, 46, 47], 40: [32, 33, 41, 48, 49], 41: [32, 33, 34, 40, 42, 48, 49, 50], 42: [33, 34, 35, 41, 43, 49, 50, 51], 43: [34, 35, 36, 42, 44, 50, 51, 52], 44: [35, 36, 37, 43, 45, 51, 52, 53], 45: [36, 37, 38, 
44, 46, 52, 53, 54], 46: [37, 38, 39, 45, 47, 53, 54, 55], 47: [38, 39, 46, 54, 55], 48: [40, 41, 49, 56, 57], 49: [40, 41, 42, 48, 50, 56, 57, 58], 50: [41, 42, 43, 49, 51, 57, 58, 59], 51: [42, 43, 44, 50, 52, 58, 59, 60], 52: [43, 44, 45, 51, 53, 59, 60, 61], 53: [44, 45, 46, 52, 54, 60, 61, 62], 54: [45, 46, 47, 53, 
55, 61, 62, 63], 55: [46, 47, 54, 62, 63], 56: [48, 49, 57], 57: [48, 49, 50, 56, 58], 58: [49, 50, 51, 57, 59], 59: [50, 51, 52, 58, 60], 60: [51, 52, 53, 59, 61], 61: [52, 53, 54, 60, 62], 62: [53, 54, 55, 61, 63], 63: [54, 55, 62]}
def printBoard(board):
    for i in range(0, len(board), width):
        print(board[i:i+width])

def findMoves(brd, tkn):
    key = (brd, tkn)
    if key in MOVESCACHE:
        return MOVESCACHE[key]
    opp = "o" if tkn == 'x' else 'x'
    moves = set()
    flipDct = {}
    for idx, c in enumerate(brd):
        if c == tkn:
            i = idx - 1                      # row left
            flag = False
            flip = []
            while i > 0 and brd[i] == opp and i not in rowBegSet and idx not in rowBegSet:
                flip.append(i)
                i -= 1
                flag = True
            if i >= 0 and brd[i] == '.' and flag:
                #print("rl", idx, i)
                flipDct[i] = flipDct.get(i, []) + flip
                moves.add(i)

            i = idx + 1                      # row right
            flag = False
            flip = []
            while i < len(brd) and brd[i] == opp and i not in rowEndSet and idx not in rowEndSet:
                flip.append(i)
                i += 1
                flag = True
            if i < len(brd) and brd[i] == '.' and flag:
                #print("rr", idx, i)
                flipDct[i] = flipDct.get(i, []) + flip
                moves.add(i)

            i = idx + width                  # col down
            flag = False
            flip = []
            while i < len(brd) and brd[i] == opp:
                flip.append(i)
                i += width
                flag = True
            if i < len(brd) and brd[i] == '.' and flag:
                #print("cd", idx, i)
                flipDct[i] = flipDct.get(i, []) + flip
                moves.add(i)

            i = idx - width                  # col up
            flag = False
            flip = []
            while i > 0 and brd[i] == opp:
                flip.append(i)
                i -= width
                flag = True
            if i >= 0 and brd[i] == '.' and flag:
                #print("cu", idx, i)
                flipDct[i] = flipDct.get(i, []) + flip
                moves.add(i)

            flag = False
            flip = []
            if idx not in rowEndSet and idx + width + 1 not in rowEndSet:  #diagNeg down
                i = idx + width + 1
                while i < len(brd) and brd[i] == opp:
                    if i + width + 1 in rowEndSet and brd[i+width+1] == opp:
                        i = i - width - 1
                        break
                    flip.append(i)
                    i = i + width + 1
                    flag = True
                if i < len(brd) and brd[i] == '.' and flag:
                    #print("dnd", idx, i)
                    flipDct[i] = flipDct.get(i, []) + flip
                    moves.add(i)

            flag = False
            flip = []
            if idx not in rowBegSet and idx - width - 1 not in rowBegSet:  #diagNeg up
                i = idx - width - 1
                while i > 0 and brd[i] == opp:
                    if i - width - 1 in rowBegSet and brd[i-width-1] == opp:
                        i = i + width + 1
                        break
                    flip.append(i)
                    i = i - width - 1
                    flag = True
                if i >= 0 and brd[i] == '.' and flag:
                    #print("dnu", idx, i)
                    flipDct[i] = flipDct.get(i, []) + flip
                    moves.add(i)

            flag = False
            flip = []
            if idx not in rowBegSet and idx + width - 1 not in rowBegSet:  #diagPos down
                i = idx + width - 1
                while i < len(brd) and brd[i] == opp:
                    if i + width - 1 in rowBegSet and brd[i+width-1] == opp:
                        i = i - width + 1
                        break
                    flip.append(i)
                    i = i + width - 1
                    flag = True
                if i < len(brd) and brd[i] == '.' and flag:
                    #print("dpd", idx, i)
                    flipDct[i] = flipDct.get(i, []) + flip
                    moves.add(i)

            flag = False
            flip = []
            if idx not in rowEndSet and idx - width + 1 not in rowEndSet:  #diagPos up
                i = idx - width + 1
                while i > 0 and brd[i] == opp:
                    if i - width + 1 in rowEndSet and brd[i-width+1] == opp:
                        i = i + width - 1
                        break
                    flip.append(i)
                    i = i - width + 1
                    flag = True
                if i >= 0 and brd[i] == '.' and flag:
                    #print("dpu", idx, i)
                    flipDct[i] = flipDct.get(i, []) + flip
                    moves.add(i)
            
    for move in moves:
        brd = brd[:move] + "*" + brd[move+1:]
    MOVESCACHE[key] = (brd, flipDct)
    #printbrd(brd)
    return brd, flipDct

def makeMove(brd, tkn, mv, dct):
    key = (brd, tkn, mv)
    if key in MAKEMOVECACHE:
        return MAKEMOVECACHE[key]
    brd = brd[:mv] + tkn + brd[mv+1:]
    for t in dct[mv]:
        brd = brd[:t] + tkn + brd[t+1:]
    MAKEMOVECACHE[key] = brd
    return brd

def playTheGameTerse(brd, tkn, mvlst):
    opp = "o" if tkn == "x" else "x"
    if not mvlst:
        brd, dct = findMoves(brd, tkn)
        moves = list(dct.keys())
        if not dct:
            tkn, opp = opp, tkn
            brd, dct = findMoves(brd, tkn)
            moves = list(dct.keys())
        printBoard(brd)
        brd = brd.replace("*", ".")
        print(f"{brd} {brd.count('x')}/{brd.count('o')}")
        print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n" )
        return tkn, brd
    for idx, mv in enumerate(mvlst):
        if mv.isdigit():
            mv = int(mv)
        elif "-" in mv:
            mv = int(mv)
        else:
            mv = coordinateToIndex(mv)
        brd, dct = findMoves(brd, tkn)
        moves = list(dct.keys())
        if mv == -1 and idx != len(mvlst) - 1:
            tkn, opp = opp, tkn
            continue
        brd = brd.replace("*", ".")
        if (idx == len(mvlst) - 1 and mvlst[-1] != "-1") or (mvlst[-1] == "-1" and idx == len(mvlst) - 2):
            print(f"{tkn} plays to {mv}") 
        brd = makeMove(brd, tkn, mv, dct)
        brd, dct = findMoves(brd, opp)
        if not dct:
            brd, dct = findMoves(brd, tkn)
        if (idx == len(mvlst) - 1 and mvlst[-1] != "-1") or (mvlst[-1] == "-1" and idx == len(mvlst) - 2):
            printBoard(brd)
        brd = brd.lower()
        brd = brd.replace("*", ".") 
        tkn, opp = opp, tkn
        if idx == len(mvlst) - 2 and mvlst[-1] == "-1":
            if not dct or mv == -1:
                tkn, opp = opp, tkn
            brd, dct = findMoves(brd, tkn) 
            if not dct or mv == -1:
                tkn, opp = opp, tkn    
                brd, dct = findMoves(brd, tkn) 
            moves = list(dct.keys())  
            brd = brd.replace("*", ".")
            print(f"{brd} {brd.count('x')}/{brd.count('o')}")
            if brd.count(".") > 0 and findMoves(brd, tkn)[1]:
                print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n")
            return tkn, brd
        if idx == len(mvlst) - 1 and mvlst[-1] != "-1":
            if not dct or mv == -1:
                tkn, opp = opp, tkn
            brd, dct = findMoves(brd, tkn) 
            if not dct or mv == -1:
                tkn, opp = opp, tkn    
                brd, dct = findMoves(brd, tkn) 
            moves = list(dct.keys())  
            brd = brd.replace("*", ".")
            print(f"{brd} {brd.count('x')}/{brd.count('o')}")
            if brd.count(".") > 0 and findMoves(brd, tkn)[1]:
                print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n")
            return tkn, brd
    return tkn, brd

def playTheGame(brd, tkn, mvlst):
    opp = "o" if tkn == "x" else "x"
    if not mvlst:
        brd, dct = findMoves(brd, tkn)
        moves = list(dct.keys())
        if not dct:
            tkn, opp = opp, tkn
            brd, dct = findMoves(brd, tkn)
            moves = list(dct.keys())
        printBoard(brd)
        brd = brd.replace("*", ".")
        print(f"{brd} {brd.count('x')}/{brd.count('o')}")
        print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n" )
        return tkn, brd
    for idx, mv in enumerate(mvlst):
        if mv.isdigit():
            mv = int(mv)
        elif "-" in mv:
            mv = int(mv)
        else:
            mv = coordinateToIndex(mv)
        brd, dct = findMoves(brd, tkn)
        moves = list(dct.keys())
        if not dct and mv != -1:
            mvlst.insert(idx+1, str(mv))
            tkn, opp = opp, tkn
            continue
        if mv == -1:
            tkn, opp = opp, tkn
            continue
        printBoard(brd)
        brd = brd.replace("*", ".")
        print(f"{brd} {brd.count('x')}/{brd.count('o')}")
        print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n" )
        print(f"{tkn} plays to {mv}")
        brd = makeMove(brd, tkn, mv, dct)
        tkn, opp = opp, tkn
        if idx == len(mvlst) - 1:
            if not dct or mv == -1:
                tkn, opp = opp, tkn
            brd, dct = findMoves(brd, tkn) 
            if not dct or mv == -1:
                tkn, opp = opp, tkn    
                brd, dct = findMoves(brd, tkn) 
            moves = list(dct.keys())  
            printBoard(brd)
            brd = brd.replace("*", ".")
            print(f"{brd} {brd.count('x')}/{brd.count('o')}")
            print(f"Possible moves for {tkn}: {str(moves)[1:-1]}\n")
    return tkn, brd

def coordinateToIndex(coordinate):
    coordinate = coordinate.upper()
    column = ord(coordinate[0]) - ord('A')
    row = int(coordinate[1]) - 1
    return width * row + column

def o4pref(brd, tkn):
    tkn = tkn.lower()
    brd = brd.lower()
    opp = "o" if tkn == "x" else "x"
    possibleMoves, dct = findMoves(brd, tkn)
    moves = list(dct.keys())
    for move in moves:
            if move in corners and brd[move] == '.':       # play to corner if possible 
                return [0, move]                                 
    for move in moves:  
            if move in cornerNeighbors and brd[cornerNeighbors[move]] == '.' and brd.count(".") > 20:      # avoid x and c-squares
                if len(moves) > 1:      # if it's not the only move, delete it from moves and dct
                    moves = [m for m in moves if m != move]
                    del dct[move]
    safeEdges = findSafeEdges(brd, tkn, moves)   # ex. xoo..... (3), xxxx....(4) are safe edge moves for x
    if safeEdges != -1:
            return [0, safeEdges]
    for move in moves:  # if i can play on an x-square and i have the corresponding corner, i can probably play there
            if move in cornerNeighbors and brd[cornerNeighbors[move]] == tkn:  # also idk if this improves it that much  
                return [0, move]
    currEdges = [move for move in moves if move in edges]    # prefer non-edges to edges, so remove edges if possible
    for mv in currEdges:                                     # note: i tried running 10k games on miniMod w/ and it didn't
            if len(moves) > 1:                                   # increase/decrease the score at all, but ill leave it in for now
                moves.remove(mv)
    return [0, min(dct, key=dct.get)]

def reorder(brd, tkn, dct):
    dct = {k: v for k, v in sorted(dct.items(), key=lambda item: item[1])}
    lst = list(dct.keys())
    if brd[0] == tkn:
        i = 0
        while brd[i] != "." and i < 7:
            i += 1
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
        i = 0
        while brd[i] != "." and i < 56:
            i += 8
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
    if brd[7] == tkn:
        i = 7
        while brd[i] != "." and i > 0:
            i = i - 1
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
        i = 7
        while brd[i] != "." and i < 63:
            i += 8
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
    if brd[56] == tkn:
        i = 56
        while brd[i] != "." and i < 63:
            i = i + 1
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
        i = 56
        while brd[i] != "." and i > 0:
            i = i - 8
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
    if brd[63] == tkn:
        i = 63
        while brd[i] != "." and i > 56:
            i = i - 1
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
        i = 63
        while brd[i] != "." and i < 7:
            i = i - 8
        if i in lst: lst.insert(0, lst.pop(lst.index(i)))
    xcsquares = []
    for mv in lst:
        if mv in cornerNeighbors and brd[cornerNeighbors[mv]] == '.':
            xcsquares.append(mv)
    for mv in xcsquares:
        lst.append(mv)
        lst.remove(mv)  
    cornerMvs = []
    for mv in lst:
        if mv in corners:
            cornerMvs.append(mv)
    for mv in cornerMvs:
        lst.insert(0, lst.pop(lst.index(mv)))
    #REORDERCACHE[key] = lst
    return lst
    
def findSafeEdges(brd, tkn, moves):  # starting from each corner, go left/right/up/down until you find a dot 
    if brd[0] == tkn:
        i = 0
        while brd[i] != "." and i < 7:
            i += 1
        if i in moves: return(i)
        i = 0
        while brd[i] != "." and i < 56:
            i += 8
        if i in moves: return(i)
    if brd[7] == tkn:
        i = 7
        while brd[i] != "." and i > 0:
            i = i - 1
        if i in moves: return(i)
        i = 7
        while brd[i] != "." and i < 63:
            i += 8
        if i in moves: return(i)
    if brd[56] == tkn:
        i = 56
        while brd[i] != "." and i < 63:
            i = i + 1
        if i in moves: return(i)
        i = 56
        while brd[i] != "." and i > 0:
            i = i - 8
        if i in moves: return(i)
    if brd[63] == tkn:
        i = 63
        while brd[i] != "." and i > 56:
            i = i - 1
        if i in moves: return i
        i = 63
        while brd[i] != "." and i < 7:
            i = i - 8
        if i in moves: return i
    return -1

def alphabeta(brd, tkn, lowerBnd, upperBnd, cache):
    brd = brd.lower()
    key = (brd, tkn, lowerBnd, upperBnd)
    if key in cache:
        return cache[key]
    opp = "o" if tkn == "x" else "x"
    tknMoves, dct = findMoves(brd, tkn)
    tknMovesLst = list(dct.keys())
    if not dct:
        oppMoves = findMoves(brd, opp)
        if not oppMoves[1]:
            r = [brd.count(tkn) - brd.count(opp)]
            cache[key] = r
            return r
        ab = alphabeta(brd, opp, -upperBnd, -lowerBnd, cache)
        r = [-ab[0]] + ab[1:] + [-1]
        cache[key] = r
        return r
    key = (brd, tkn, lowerBnd, upperBnd)
    best = [lowerBnd-1]
    tknMovesLst = reorder(brd, tkn, dct)
    for mv in tknMovesLst:
            ab = alphabeta(makeMove(brd, tkn, mv, dct), opp, -upperBnd, -lowerBnd, cache)
            score = -ab[0]
            if score < lowerBnd: continue
            if score > upperBnd: 
                r = [score]
                cache[key] = r
                return r
            best = [score] + ab[1:] + [mv]
            lowerBnd = score + 1
    cache[key] = best
    return best

def countFrontiers(brd, tkn, opp):
    tknFrontiers, oppFrontiers = 0, 0
    for idx, c in enumerate(brd):
        if c == opp:
            for n in neighbors[idx]:
                if brd[n] == ".":
                    oppFrontiers += 1
                    break
    for idx, c in enumerate(brd):
        if c == tkn:
            for n in neighbors[idx]:
                if brd[n] == ".":
                    tknFrontiers += 1
                    break
    return tknFrontiers, oppFrontiers

def evalBrd(brd, tkn):
    key = (brd, tkn)
    if key in EVALCACHE:
        return EVALCACHE[key]
    score = 0
    dots = brd.count(".")
    opp = "o" if tkn == "x" else "x"
    for c in corners:
        if brd[c] == tkn:
            score += 50
        elif brd[c] == opp:
            score = score - 50
    if dots > 25:
        for n in cornerNeighbors:
            if brd[n] == tkn and brd[cornerNeighbors[n]] == ".":
                score = score - 30
            elif brd[n] == opp and brd[cornerNeighbors[n]] == ".":
                score = score + 30
    if brd[0] == tkn:
        i = 0
        while brd[i] != "." and i < 7:
            i += 1
            score += 5
        i = 0
        while brd[i] != "." and i < 56:
            i += 8
            score += 5
    if brd[7] == tkn:
        i = 7
        while brd[i] != "." and i > 0:
            i = i - 1
            score += 5
        i = 7
        while brd[i] != "." and i < 63:
            i += 8
            score += 5
    if brd[56] == tkn:
        i = 56
        while brd[i] != "." and i < 63:
            i = i + 1
            score += 5
        i = 56
        while brd[i] != "." and i > 0:
            i = i - 8
            score += 5
    if brd[63] == tkn:
        i = 63
        while brd[i] != "." and i > 56:
            i = i - 1
            score += 5
        i = 63
        while brd[i] != "." and i < 7:
            i = i - 8
            score += 5
    brdTkn, tknMoves = findMoves(brd, tkn)  #add mobility to score
    brdOpp, oppMoves = findMoves(brd, opp)
    if len(tknMoves) > len(oppMoves):
        score += ((10*len(tknMoves))/(len(tknMoves)+len(oppMoves)))
    elif len(tknMoves) < len(oppMoves):
        score += -((10*len(tknMoves))/(len(tknMoves)+len(oppMoves)))
    tf, of = countFrontiers(brd, tkn, opp)
    if tf > of:
        score += -((10*tf)/(tf+of))
    elif tf < of:
        score += ((10*tf)/(tf+of))
    EVALCACHE[key] = score
    return score

def alphabetamid(brd, tkn, upperBnd, lowerBnd, cache, lvl):
    brd = brd.lower()
    key = (brd, tkn, upperBnd, lowerBnd)
    if key in cache:
        return cache[key]
    if not lvl:
        return [evalBrd(brd, tkn)]
    opp = "o" if tkn == "x" else "x"
    tknMoves, dct = findMoves(brd, tkn)
    if not dct:
        ab = alphabetamid(brd, opp, -lowerBnd, -upperBnd, cache, lvl-1)
        cache[key] = ab
        return ab
    key = (brd, tkn, upperBnd, lowerBnd)
    tknMovesLst = reorder(brd, tkn, dct)
    best = [upperBnd-1]
    for mv in tknMovesLst:
            ab = alphabetamid(makeMove(brd, tkn, mv, dct), opp, -lowerBnd, -upperBnd, cache, lvl-1)
            score = -ab[0]
            if score < upperBnd: continue
            if score > lowerBnd: 
                r = [score]
                cache[key] = [score]
                return r
            best = [score] + ab[1:] + [mv]
            upperBnd = score + 1
    cache[key] = best
    return best

def quickMove(brd, tkn):
    tkn = tkn.lower()
    brd = brd.lower()
    opp = "o" if tkn == "x" else "x"
    possibleMoves, dct = findMoves(brd, tkn)
    moves = list(dct.keys())
    if brd in OPENINGBOOK:
        return [0, OPENINGBOOK[brd][0]]
    if moves and brd.count(".") >= 60:
        for move in moves:
            if move in corners and brd[move] == '.':       # play to corner if possible 
                return [0, move]                                 
        for move in moves:  
            if move in cornerNeighbors and brd[cornerNeighbors[move]] == '.' and brd.count(".") > 20:      # avoid x and c-squares
                if len(moves) > 1:      # if it's not the only move, delete it from moves and dct
                    moves = [m for m in moves if m != move]
                    del dct[move]
        safeEdges = findSafeEdges(brd, tkn, moves)   # ex. xoo..... (3), xxxx....(4) are safe edge moves for x
        if safeEdges != -1:
            return [0, safeEdges]
        for move in moves:  # if i can play on an x-square and i have the corresponding corner, i can probably play there
            if move in cornerNeighbors and brd[cornerNeighbors[move]] == tkn:  # also idk if this improves it that much  
                return [0, move]
        currEdges = [move for move in moves if move in edges]    # prefer non-edges to edges, so remove edges if possible
        for mv in currEdges:                                     # note: i tried running 10k games on miniMod w/ and it didn't
            if len(moves) > 1:                                   # increase/decrease the score at all, but ill leave it in for now
                moves.remove(mv)
        return [0, min(dct, key=dct.get)]
    if moves and brd.count(".") < 60 and brd.count(".") >= 14:
        ab = alphabetamid(brd, tkn, -1000, 1000, {}, 4)
        return ab
        #return alphabetamid(brd, tkn, -1000, 1000, {}, 4)[-1]
    elif moves and brd.count(".") < 14:
        ab = alphabeta(brd, tkn, -65, 65, {})
        return ab

def main():
    if not terse:
        tkn, brd = playTheGame(board, token, movesLst)
    else:
        tkn, brd = playTheGameTerse(board, token, movesLst)
    if findMoves(brd, tkn)[1]:
        mypref = quickMove(brd, tkn)       
        print(f"The preferred move is: {mypref[-1]}")
        print(f"Min score: {mypref[0]}; move sequence: {mypref[1:]}")


if __name__ == "__main__": main()

class Strategy:
    # implement all the required methods on your own
    logging = True # turns on logging
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            best_move.value = o4pref(board, player)[-1]
            best_move.value = quickMove(board, player)[-1]
            # Note: It is not required for your Strategy class to have a "legal_moves" method,
            # but you must determine legal moves yourself. The server will NOT accept invalid moves.
            
#Rohan Manroa, pd 4, 2024