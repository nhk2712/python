from random import randint

# Declare essential constants
EMPTY = 0
PLAYER = 1
WALL = 2
TRAP = 3
COIN = 4

# Create game's matrix and print it
matrix = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL],
    [WALL, WALL, WALL, EMPTY, WALL, WALL, EMPTY, WALL, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL],
    [WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]
]

def printMat():
    global matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]==WALL: print('#',end="")
            elif matrix[i][j]==PLAYER: print('&',end="")
            elif matrix[i][j]==EMPTY: print(' ',end="")
            elif matrix[i][j]==TRAP: print('x',end="")
            elif matrix[i][j]==COIN: print('.',end="")
        print()

printMat()
print()

# The state of playing or not
isPlay = True

# Define player class
class Player:
    def __init__(self,row,col,coin=0):
        self.row = row
        self.col = col
        matrix[self.row][self.col]=PLAYER # Put player in his position
        self.coin = coin
        self.health=3
        self.name=input("Enter player's name: ")
        self.show()

    def behave(self,cmd):
        for i in range(len(cmd)): 
            if cmd[i]=="down":
                cont=self.move(1,0)
                if cont==False:break
            elif cmd[i]=="up":
                cont=self.move(-1,0)
                if cont==False:break
            elif cmd[i]=="right":
                cont=self.move(0,1)
                if cont==False:break
            elif cmd[i]=="left":
                cont=self.move(0,-1)
                if cont==False:break
            elif cmd[i]=="trap":
                matrix[self.row][self.col]=TRAP
            elif cmd[i]=="skip":
                print("Skipped")
                break
        self.show()

    def move(self,x,y):
        # Cannot move to <player> or <wall>
        if matrix[self.row+x][self.col+y]!=WALL and matrix[self.row+x][self.col+y]!=PLAYER:
            # Before moving
            if matrix[self.row][self.col]==PLAYER: matrix[self.row][self.col]=EMPTY
            
            # Moving
            self.row+=x
            self.col+=y

            # After moving
            if matrix[self.row][self.col]==TRAP:
                self.health-=1
                if self.health>0:
                    matrix[self.row][self.col]=PLAYER
                    return True
                else:
                    self.die()
                    return False
            elif matrix[self.row][self.col]==COIN:
                self.coin+=1
                matrix[self.row][self.col]=PLAYER
                createCoin()
                return True
            else: # <empty>
                matrix[self.row][self.col]=PLAYER
                return True
        else:
            print("Cannot move")
            return False
              
    def show(self):
        printMat()
        print("Row: {}, col: {}, coin: {}, health: {}".format(self.row,self.col,self.coin,self.health))

    def surrender(self):
        print("Surrendered")
        self.health=0
        self.end()

    def die(self):
        print("Died")
        self.end()

    def end(self):
        global isPlay
        print(self.name+" lost")
        isPlay=False
        matrix[self.row][self.col]=EMPTY
        self.row=-1
        self.col=-1

# Init player
p1 = Player(1,1)
p2=Player(len(matrix)-2,len(matrix[0])-2)

def createCoin():
    r=randint(1,len(matrix)-2)
    c=randint(1,len(matrix[0])-2)
    if matrix[r][c]==EMPTY: matrix[r][c]=COIN
    else: createCoin()

createCoin()
printMat()
print()

def getCmd(cmd,player):
    for i in range(len(cmd)):
            cmd[i]=input()
            if cmd[i]=="surrender":
                player.surrender()
                player.show()
                break
            elif cmd[i]=="skip": break
            elif cmd[i]=="locate":
                player.show()
                getCmd(cmd,player)
                break

# The main game loop
def turn():
    # Get user's command
    cmd = [None]*3
    if isPlay: 
        print(p1.name+"'s turn")
        getCmd(cmd,p1)

    if isPlay: 
        p1.behave(cmd)

    cmd2=[None]*3
    if isPlay: 
        print(p2.name+"'s turn")
        getCmd(cmd2,p2)

    if isPlay: 
        p2.behave(cmd2)
        turn()
turn()