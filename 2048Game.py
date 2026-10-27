import random
import keyboard
import msvcrt

class Game:
    board:list[list[str]]
    length:int
    width:int
    difficulty:float
    stdscr:any
    score:int
    def __init__(self, length, width, difficulty:float):
        self.length=length
        self.width=width
        self.difficulty=difficulty
        self.board=[['*']*self.width for i in range(self.length)]
        self.score=0

    def get_key(self) -> str:
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):          # direction key will send a prefix character
            arrow = msvcrt.getwch()
            return {'H': 'w', 'K': 'a', 'P': 's', 'M': 'd'}.get(arrow, '')
        return ch.lower()
    def play(self):
        # generate two num with either 2 or 4
        print("Let's play the game")
        self.generate_num()
        self.generate_num()
        self.print_board()
        while not self.game_over():
            # print("enter loop")
            dir = self.get_key()
            if dir in ('q', '\x03'):         # q or Ctrl+C exit
                print("bye-bye")
                return
            if dir[0]=='w':
                if self.up_move_judge():
                    self.up_move()
                    self.generate_num()
            elif dir[0]=='a':
                if self.left_move_judge():
                    self.left_move()
                    self.generate_num()
            elif dir[0]=='s':
                if self.down_move_judge():
                    self.down_move()
                    self.generate_num()
            elif dir[0]=='d':
                if self.right_move_judge():
                    self.right_move()
                    self.generate_num()
            else:
                print("illegal argument")
                continue
            self.print_board()
            
        print("game over")

    def generate_num(self)->None:
        empty_coor:List[Tuple[int]]=[]
        for i in range(self.length):
            for j in range(self.width):
                if self.board[i][j]=='*':
                    empty_coor.append((i, j))
        idx=random.randint(0, len(empty_coor)-1)
        generate_four_random=random.uniform(0, 1)
        if generate_four_random<self.difficulty:
            self.board[empty_coor[idx][0]][empty_coor[idx][1]]='4'
        else:
            self.board[empty_coor[idx][0]][empty_coor[idx][1]]='2'

    def left_move(self):
        for i in range(self.length):
            num_list:List[int]=[]
            res_list:List[int]=[]
            for j in range(self.width):
                if self.board[i][j]!='*':
                    num_list.append(int(self.board[i][j]))
            combine=False
            for k in range(0, len(num_list)):
                if combine and num_list[k]==num_list[k-1]:
                    combine=False
                    res_list.pop()
                    res_list.append(num_list[k]*2)
                    self.score+=num_list[k]*2
                else:
                    combine=True
                    res_list.append(num_list[k])
            for k in range(len(res_list)):
                self.board[i][k]=str(res_list[k])

            for k in range(len(res_list), self.width):
                self.board[i][k]='*'
                
    def right_move(self):
        for i in range(self.length):
            num_list:list[int]=[]
            res_list:list[int]=[]
            for j in range(self.width-1, -1, -1):
                if self.board[i][j]!='*':
                    num_list.append(int(self.board[i][j]))
            combine=False
            for k in range(0, len(num_list)):
                if combine and num_list[k]==num_list[k-1]:
                    combine=False
                    res_list.pop()
                    res_list.append(num_list[k]*2)
                    self.score+=num_list[k]*2
                else:
                    combine=True
                    res_list.append(num_list[k])
            for k in range(len(res_list)):
                self.board[i][self.width-1-k]=str(res_list[k])
            for k in range(len(res_list), self.width):
                self.board[i][self.width-1-k]='*' 
            
    def up_move(self):
        for j in range(self.width):
            num_list:list[int]=[]
            res_list:list[int]=[]
            for i in range(self.length):
                if self.board[i][j]!='*':
                    num_list.append(int(self.board[i][j]))
            combine=False
            for k in range(0, len(num_list)):
                if combine and num_list[k]==num_list[k-1]:
                    combine=False
                    res_list.pop()
                    res_list.append(num_list[k]*2)
                    self.score+=num_list[k]*2
                else:
                    combine=True
                    res_list.append(num_list[k])
            for k in range(len(res_list)):
                self.board[k][j]=str(res_list[k])
            for k in range(len(res_list), self.length):
                self.board[k][j]='*'

    def down_move(self):
        for j in range(self.width):
            num_list:List[int]=[]
            res_list:List[int]=[]
            for i in range(self.length-1, -1, -1):
                if self.board[i][j]!='*':
                    num_list.append(int(self.board[i][j]))
            combine=False
            for k in range(0, len(num_list)):
                if combine and num_list[k]==num_list[k-1]:
                    combine=False
                    res_list.pop()
                    res_list.append(num_list[k]*2)
                    self.score+=num_list[k]*2
                else:
                    combine=True
                    res_list.append(num_list[k])
            for k in range(len(res_list)):
                self.board[self.length-1-k][j]=str(res_list[k])
            for k in range(len(res_list), self.length):
                self.board[self.length-1-k][j]='*' 

    def up_move_judge(self)->bool:
        for j in range(self.width):
            asteroid_start=False
            for i in range(self.length):
                if self.board[i][j]=='*':
                    asteroid_start=True
                elif asteroid_start or (i!=0 and self.board[i][j]==self.board[i-1][j]):
                    return True
        return False
                
    def left_move_judge(self)->bool:
        for i in range(self.length):
            asteroid_start=False
            for j in range(self.width):
                if self.board[i][j]=='*':
                    asteroid_start=True
                elif asteroid_start or (j!=0 and self.board[i][j]==self.board[i][j-1]):
                    return True
        return False
    
    def right_move_judge(self)->bool:
        for i in range(self.length):
            asteroid_start=False
            for j in range(self.width-1, -1, -1):
                if self.board[i][j]=='*':
                    asteroid_start=True
                elif asteroid_start or (j!=self.width-1 and self.board[i][j]==self.board[i][j+1]):
                    return True
        return False
    
    def down_move_judge(self)->bool:
        for j in range(self.width):
            asteroid_start=False
            for i in range(self.length-1, -1, -1):
                if self.board[i][j]=='*':
                    asteroid_start=True
                elif asteroid_start or (i!=self.length-1 and self.board[i][j]==self.board[i+1][j]):
                    return True
        return False

    def game_over(self)->bool:
        return not self.left_move_judge() and not self.right_move_judge() and not self.up_move_judge() and not self.down_move_judge()
           
    
    def print_board(self)->None:
        print(f"score: {self.score}")
        for i in range(self.length):
            for j in range(self.width):
                print(self.board[i][j], end="\t")
            print()

def main():
    height:int
    width:int
    probability_four:float
    while True:
        try:
            print("please input the height")
            height_str=input()
            if height_str=='exit':
                print('bye-bye')
                return
            height=int(height_str)
            print("please input the width")
            width_str=input()
            if width_str=='exit':
                print('bye-bye')
                return
            width=int(width_str)
            print("please input the probability of 4")
            probability_str=input()
            if probability_str=='exit':
                print('bye-bye')
                return
            probability_four=float(probability_str)
            break
        except ValueError:  # Catch ValueError for invalid input
            print("Illegal arguments. Please enter valid numbers.")
    
    game = Game(height, width, probability_four)
    game.play()

if __name__ == "__main__":
    main()