from queue import PriorityQueue
from queue import Queue
from tkinter import *
from turtle import *
import time
import numpy as np
from PIL import Image, ImageTk
import random
from tkinter import font as tkfont
import PIL.Image
from tkinter import font as tkfont
from tkinter import messagebox
import time

dr1 = [ -1, 0, 0, 1]
dc1 = [ 0, -1, 1, 0]

dr3 = [ -3, -2, -2, -2, -1, -1, -1, -1, -1,  0,  0,  0, 0, 0, 0,  1,  1, 1, 1, 1,  2, 2, 2, 3]
dc3 = [  0,  -1, 0,  1,  -2, -1, 0,  1,  2, -3, -2, -1, 1, 2, 3, -2, -1, 0, 1, 2, -1, 0, 1, 0]

grid_edge = 40 #size of block
delay_time = 0.4#delay time

#--------------------------------------------------------------------------
#ReadData
def convertSToN(s):
    return [int(index) for index in s]

def ReadMaze(filename):
    maze = []
    size = []
    pos = []
    f = open (filename, 'r')
    size = f.readline()
    
    l = f.readlines()
    for i in range(len(l)):
        tmp = l[i].split()
        maze.append(convertSToN(tmp))
    pos = maze.pop(-1)
    
    size = convertSToN(size.split())
    return maze, size, pos

#-------------------------------------------------------------
#Graphic

#draw maze
def draw_map(maze, maze_size, cv_first, level):
    for height in range(maze_size[0]): 
        for width in range(maze_size[1]):
            if maze[height][width] == 1:
                Draw_of_something(cv_first, wall_image, (width, height))
            if level < 3:
                if maze[height][width] == 2:
                    Draw_of_something(cv_first, food_image, (width, height))
            if maze[height][width] == 3:
                if level > 1:
                    Draw_of_something(cv_first, creep_image, (width, height))
                else:
                    maze[height][width] = 0
            
    ###draw outline of map
    top = 3
    left = 3
    cv_first.create_line(left, top, 1000, top, fill = 'orange', width = 2) #top
    cv_first.create_line(left, top, left, 600, fill = 'orange', width = 2) #left
    cv_first.create_line(1000, 1, 1000, 600, fill = 'orange', width = 2) #right
    cv_first.create_line(1, 600, 1000, 600, fill = 'orange', width = 2) #bot
    
    if level < 3:
        Draw_paramanter(1020, 100, "Score", 0)               ##score
        Draw_paramanter(1020, 250, "Time", 0)           ##time
        Draw_paramanter(1020, 400, "Length", 0)         ##length

    return map

def menuMaze(cv_first,maze_img,start_img):
    cv_first.delete("all")
    
    cv_first.create_image(0, 0, anchor=NW, image=maze_img)
    

    b_back = Button(cv_first,bg = '#473522', width=30,text='back', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:MenuStart(cv_first,start_img,maze_img, thanks_bg) ) 
    b_back.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_back_windows = cv_first.create_window(1070, 530, anchor=NW, window=b_back)
    
    b_maze1 = Button(cv_first,bg = '#fc9403', width=30,text='map 1', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: trans_to_map("map1.txt",img,maze_img,start_img)) 
    b_maze1.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze1_windows = cv_first.create_window(140, 265, anchor=NW, window=b_maze1)

    b_maze2 = Button(cv_first,bg = '#fc9403', width=30,text='map 2', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: trans_to_map("map2.txt",img,maze_img,start_img))
    b_maze2.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze2_windows = cv_first.create_window(550, 265, anchor=NW, window=b_maze2)

    b_maze3 = Button(cv_first,bg = '#fc9403', width=30,text='map 3', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: trans_to_map("map3.txt",img,maze_img,start_img))
    b_maze3.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze3_windows = cv_first.create_window(950, 265, anchor=NW, window=b_maze3)

    b_maze4 = Button(cv_first,bg = '#fc9403', width=30,text='map 4', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: trans_to_map("map4.txt",img,maze_img,start_img))
    b_maze4.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze4_windows = cv_first.create_window(300, 540, anchor=NW, window=b_maze4)

    b_maze5 = Button(cv_first,bg = '#fc9403', width=30,text='map 5', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: trans_to_map("map5.txt",img,maze_img,start_img))
    b_maze5.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze5_windows = cv_first.create_window(750, 540, anchor=NW, window=b_maze5)
    root.update()

    cv_first.update()

def Draw_paramanter(x_pos, y_pos, tmp_text, tmp_point):
    cv_first.create_rectangle(x_pos,y_pos,x_pos + 160,y_pos + 100,fill = '#f3d1dc', width = 5 , outline = '#f5719c')
    cv_first.create_line(x_pos, y_pos + 30, x_pos + 160, y_pos+ 30, fill = '#f5719c', width = 5)
    cv_first.create_text(x_pos + 75, y_pos + 15,fill="black",font="Tahoma 15 bold", text=tmp_text)
    cv_first.create_text(x_pos + 75, y_pos + 65,fill="black",font="Time 15 bold", text=tmp_point)

###Draw Pacman at position
def draw_pacman(cv_first, cur_pos):
    cv_first.create_oval(cur_pos[1]*grid_edge, cur_pos[0]*grid_edge, cur_pos[1]*grid_edge + grid_edge, cur_pos[0]*grid_edge + grid_edge, fill='yellow')
    cv_first.create_arc(cur_pos[1]*grid_edge, cur_pos[0]*grid_edge, cur_pos[1]*grid_edge + grid_edge, cur_pos[0]*grid_edge + grid_edge,
    fill='black', style=PIESLICE, start=330, extent=60)

def Draw_of_something(cv_first, tmp_image, tmp_pos):
    cv_first.create_image(tmp_pos[0] * grid_edge + 1, tmp_pos[1]*grid_edge + 1, image=tmp_image, anchor=NW)

#-------------------------------------------------------------------------------------------
#Menu

def end_game(cv_first, win, maze_img, start_img):
    if win == True:
        messagebox.showinfo("Result","PACMAN win")
        cv_first.delete("all")

        cv_first.create_text(600,200,fill = '#fc9403', text = 'Wanna play again?', font = 'tahoma 30 bold')
        b_again = Button(cv_first,bg = '#fc9403', width=30,text='Play again', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:menuMaze(cv_first,maze_img,start_img))
        b_again.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
        b_again_windows = cv_first.create_window(520, 320, anchor=NW, window=b_again)
        
        b_quit = Button(cv_first,bg = '#fc9403', width=30,text='Exit', font = tkfont.Font(family="Comic Sans MS", size="13"), command = quit)
        b_quit.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
        b_quit_windows = cv_first.create_window(520, 420, anchor=NW, window=b_quit)
    else:
        messagebox.showinfo("Result","PACMAN lose")
        cv_first.delete("all")

        cv_first.create_text(600,200,fill = '#fc9403', text = 'Wanna play again?', font = 'tahoma 30 bold')
        b_again = Button(cv_first,bg = '#fc9403', width=30,text='Play again', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:menuMaze(cv_first,maze_img,start_img))
        b_again.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
        b_again_windows = cv_first.create_window(520, 320, anchor=NW, window=b_again)
        
        b_quit = Button(cv_first,bg = '#fc9403', width=30,text='Exit', font = tkfont.Font(family="Comic Sans MS", size="13"), command = quit)
        b_quit.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
        b_quit_windows = cv_first.create_window(520, 420, anchor=NW, window=b_quit)


def menu_level(cv_first,maze, size, start_pos, level_img,maze_img,start_img):
    cv_first.delete("all")
    cv_first.create_image(0, 0, anchor=NW, image=level_img)
    b_lv1 = Button(cv_first,bg = '#fc9403', width=30,text='Level 1', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: Level_Zero(cv_first,maze,size,start_pos, 1,maze_img,start_img)) 
    b_lv1.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_lv1_windows = cv_first.create_window(520, 420, anchor=NW, window=b_lv1)

    b_lv2 = Button(cv_first,bg = '#fc9403', width=30,text='Level 2', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: Level_Zero(cv_first,maze,size,start_pos, 2,maze_img,start_img))
    b_lv2.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_lv2_windows = cv_first.create_window(650, 420, anchor=NW, window=b_lv2)

    b_lv3 = Button(cv_first,bg = '#fc9403', width=30,text='Level 3', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: Level_Three(cv_first,maze,size,start_pos,maze_img,start_img))
    b_lv3.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_lv3_windows = cv_first.create_window(520, 470, anchor=NW, window=b_lv3)

    b_lv4 = Button(cv_first,bg = '#fc9403', width=30,text='Level 4', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda: Level_Four(cv_first,maze,size,start_pos,maze_img,start_img))
    b_lv4.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_lv4_windows = cv_first.create_window(650, 470, anchor=NW, window=b_lv4)

    b_end = Button(cv_first,bg = '#fc9403', width=30,text='Exit', font = tkfont.Font(family="Comic Sans MS", size="13"), command= quit)
    b_end.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_end_windows = cv_first.create_window(585, 520, anchor=NW, window=b_end)

    b_back = Button(cv_first,bg = '#473522', width=30,text='back', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:menuMaze(cv_first,maze_img,start_img)) 
    b_back.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_back_windows = cv_first.create_window(1070, 530, anchor=NW, window=b_back)
    cv_first.update()


def MenuStart(cv_first,start_img,maze_img,thanks_bg):
    cv_first.delete('all')
    cv_first.create_image(0, 0, anchor=NW, image=start_img)
    b_maze = Button(cv_first,bg = '#473522', width=30,text='Maze', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:  menuMaze(cv_first,maze_img,start_img)) 
    b_maze.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_maze_windows = cv_first.create_window(520, 410, anchor=NW, window=b_maze)

    b_cre = Button(cv_first,bg = '#473522', width=30,text='Credit', font = tkfont.Font(family="Comic Sans MS", size="13"), command =  lambda: credit(cv_first,thanks_bg,start_img,maze_img ) ) 
    b_cre.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_cre_windows = cv_first.create_window(520, 470, anchor=NW, window=b_cre)

    b_quit = Button(cv_first,bg = '#473522', width=30,text='Exit', font = tkfont.Font(family="Comic Sans MS", size="13"), command =  root.destroy ) 
    b_quit.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_quit_windows = cv_first.create_window(520, 530, anchor=NW, window=b_quit)
    cv_first.update()
    root.update()

def credit(cv_first,thanks_bg,start_img,maze_img):
    cv_first.delete('all')
    cv_first.create_image(0, 0, anchor=NW, image=thanks_bg)
    cv_first.create_text(600 , 100,fill="#df03fc",font="Helvetica 20 bold italic", text="Special thanks to teacher Le Ngoc Thanh for helping us complete this project")
    
    cv_first.create_text(550, 250,fill="#7b03fc",font=" Helvetica 17 bold italic", text="Tran Huy Vu                       ")
    cv_first.create_text(750 , 250,fill="#7b03fc",font="Helvetica 17 bold italic", text="18127257")
    cv_first.create_text(547 , 280,fill="#7b03fc",font="Helvetica 17 bold italic", text="Tran Bui Tai Nhan             ")
    cv_first.create_text(750 , 280,fill="#7b03fc",font="Helvetica 17 bold italic", text="18127168")
    cv_first.create_text(550 , 310,fill="#7b03fc",font="Helvetica 17 bold italic", text="Phan Nhat Minh                  ")
    cv_first.create_text(750 , 310,fill="#7b03fc",font="Helvetica 17 bold italic", text="18127153")
    cv_first.create_text(550 , 340,fill="#7b03fc",font="Helvetica 17 bold italic", text="To Dong Phat                      ")
    cv_first.create_text(750 , 340,fill="#7b03fc",font="Helvetica 17 bold italic", text="18127176")
    b_back = Button(cv_first,bg = '#473522', width=30,text='back', font = tkfont.Font(family="Comic Sans MS", size="13"), command = lambda:MenuStart(cv_first,start_img,maze_img, thanks_bg) ) 
    b_back.configure(width = 10, height = 1, activebackground = "#33B5E5", relief = FLAT)
    b_back_windows = cv_first.create_window(1070, 530, anchor=NW, window=b_back)
    cv_first.update()

def trans_to_map(tmp_map,level_img,maze_img,start_img):
    cv_first.delete("all")
    maze, size, start_pos = ReadMaze(tmp_map)
    
    cv_first.create_image(0, 0, anchor=NW, image=level_img)
    menu_level(cv_first,  maze, size, start_pos, level_img,maze_img,start_img)
    
    cv_first.update()
    root.update()

#----------------------------------------------------------------------------
#level 1,2

class Node:
    def __init__(self, id, dist):
        self.id = id
        self.dist = dist
       
    def __lt__(self, other):
        if self.dist == other.dist:
            return self.id <= other.id
        return self.dist <= other.dist

def Find_Something(maze, size, Something):
    Position = list()
    
    for i in range(size[0]):
        for j in range(size[1]):
            if maze[i][j] == Something:
                Position.append([i, j])

    return Position

def Find_Nearest_Food(Pos, Foods):
    Min = 1e9
    Food_pos = [ -1, -1]

    for i in Foods:
        distance = abs(Pos[0] - i[0]) + abs(Pos[1] - i[1])
        if distance < Min:
            Min = distance
            Food_pos = [i[0], i[1]]
    
    return Food_pos

def Path_Return(path, list_path, i, Start_Pos):
    if path[i[0]][i[1]][0] == Start_Pos[0] and path[i[0]][i[1]][1] == Start_Pos[1]:
       return list_path
    else:
        list_path = Path_Return(path, list_path, path[i[0]][i[1]], Start_Pos)
        list_path.append(path[i[0]][i[1]])
        return list_path

#type = 0 -> PACMAN, #type = 1 -> Monster
def AStart(maze, size, Start, Goal, type):
    path = (-1)*np.ones((size[0], size[1], 2), dtype = 'int')
    dist = 100000*np.ones((size[0], size[1]), dtype = 'int')

    pq_frontier = PriorityQueue()
    pq_frontier.put(Node(Start, 0))
    dist[Start[0]][Start[1]] = 0

    while not pq_frontier.empty():
        top = pq_frontier.get()
        u = top.id
        w = dist[u[0]][u[1]]
        if u[0] == Goal[0] and u[1] == Goal[1]:
            return True, path

        for i in range(4):
            neighbor = [u[0] + dr1[i], u[1] + dc1[i]]
            if neighbor[0] > -1 and neighbor[1] > -1 and neighbor[0] < size[0] and neighbor[1] < size[1]:
                if maze[neighbor[0]][neighbor[1]] == 0 or (maze[neighbor[0]][neighbor[1]] == 2 and type == 0) or (maze[neighbor[0]][neighbor[1]] == 3 and type == 1):
                    heuristic = abs(neighbor[0] - Goal[0]) + abs(neighbor[1] - Goal[1])
                    if w + 1 + heuristic < dist[neighbor[0]][neighbor[1]]:
                        dist[neighbor[0]][neighbor[1]] = w + 1
                        pq_frontier.put(Node(neighbor, dist[neighbor[0]][neighbor[1]] + heuristic))
                        path[neighbor[0]][neighbor[1]] = u
    return False, path

def Level_Zero(cv_first, maze, size, Start_Pos, level,maze_img,start_img):
    cv_first.delete("all")
    count_point = 0
    count_time = 0
    count_length = 0
    
    map = draw_map(maze, size, cv_first, level)
    draw_pacman(cv_first, Start_Pos)

    root.update()
    time.sleep(delay_time)

    Foods = Find_Something(maze, size, 2)
    #Ham nay tim vi tri Food
    
    while len(Foods) != 0:
        Target = Find_Nearest_Food(Start_Pos, Foods)
        Foods.remove(Target)

        ans, path = AStart(maze, size, Start_Pos, Target, 0)
        #Ans = true la tim duoc. Ma tam thoi chua dung toi. lv1, lv2 nhat dinh se phai duoc duong. Khong thi do loi~ map
        list_path = list()
        list_path = Path_Return(path, list_path, Target, Start_Pos)
        list_path.append(Target)

        for i in list_path:

            Hide_Something(cv_first, [Start_Pos])
            Start_Pos[0] = i[0]
            Start_Pos[1] = i[1]
            draw_pacman(cv_first, Start_Pos)

            if Start_Pos in Foods:
                Foods.remove(Start_Pos)
                count_point+= 20

            count_length += 1
            count_point -= 1
            count_time += delay_time
            if Start_Pos == Target:
                count_point+= 20


            Draw_paramanter(1020, 100, "Score", count_point)               ##score
            Draw_paramanter(1020, 250, "Time", int(count_time))           ##time
            Draw_paramanter(1020, 400, "Length", count_length)         ##length
            

            root.update() #update canvas
            time.sleep(delay_time) #delay by second 

    end_game(cv_first, True, maze_img, start_img)
    
            
            

#-------------------------------------------------------------------
#level 3 up

#Ham Move cua di~ Minh
def Move_Left(object):
    object[0] -= 1
    return object

def Move_Right(object):
    object[0] += 1
    return object

def Move_Down(object):
    object[1] -= 1
    return object

def Move_Up(object):
    object[1] += 1
    return object

def Is_Valid_Move(maze, size, pos):
    if (pos[0] < 0 or pos[1] < 0 or pos[0] >= size[0] or pos[1] >= size[1] or maze[pos[0]][pos[1]] == 1 or maze[pos[0]][pos[1]] == 2):
        return False
    return True

def monsters_Move_3(maze, size, origin_pos, monsters):
    select = [[1, 2, 3, 4] for _ in range(len(monsters))]

    for i in range(len(monsters)):
        move = []
        for j in range(4):
            move.append([origin_pos[i][0] + dr1[j], origin_pos[i][1] + dc1[j]])
        for j in range(4):
            if not Is_Valid_Move(maze, size, move[j]):
                select[i].remove(j+1)


    for i in range(len(monsters)):
        if monsters[i] != origin_pos[i]:
            maze[monsters[i][0]][monsters[i][1]] = 4
            monsters[i] = origin_pos[i]
            maze[origin_pos[i][0]][origin_pos[i][1]] = 3
        else:
            tmp = random.choice(select[i])
            if tmp == 1:
                monsters[i] = Move_Left(monsters[i])
            elif tmp == 2:
                monsters[i] = Move_Down(monsters[i])
            elif tmp == 3:
                monsters[i] = Move_Up(monsters[i])
            elif tmp == 4:
                monsters[i] = Move_Right(monsters[i])
            maze[monsters[i][0]][monsters[i][1]] = 3
            maze[origin_pos[i][0]][origin_pos[i][1]] = 4


    return maze, monsters

#done

def Fill_Danger_Cells(maze, size):

    Temp_Maze = maze

    for i in range(size[0]):
        for j in range(size[1]):
            if Temp_Maze[i][j] == 3:
                for k in range(4):
                    if Temp_Maze[i + dr1[k]][j+dc1[k]] == 0:
                        Temp_Maze[i + dr1[k]][j+dc1[k]] = 4

    return Temp_Maze



def Nearest_Unexplored_Cell(maze, size, Pos, Explored):
    visited = (-1)*np.ones((size[0], size[1]), dtype = 'int')
    path = (-1)*np.ones((size[0], size[1], 2), dtype = 'int')
    q = Queue()

    visited[Pos[0]][Pos[1]] = 1
    q.put(Pos)

    while not q.empty():
        u = q.get()
        
        for i in range(4):
            neighbor = [u[0] + dr1[i], u[1] + dc1[i]]
            if neighbor[0] > -1 and neighbor[1] > -1 and neighbor[0] < size[0] and neighbor[1] < size[1]:
                if neighbor not in Explored:
                        path[neighbor[0]][neighbor[1]] = u
                        return True, neighbor, path
                if maze[neighbor[0]][neighbor[1]] == 0 or maze[neighbor[0]][neighbor[1]] == 2:
                    if visited[neighbor[0]][neighbor[1]] == -1:
                        visited[neighbor[0]][neighbor[1]] = 1
                        path[neighbor[0]][neighbor[1]] = u
                        q.put(neighbor)
    return False, Pos, path

def Explored_Sight_3(maze, size, cv_first, PACMAN_Pos, Sight, food, target):
    Inside_Foods = list()

    for i in range(24):
            neighbor = [PACMAN_Pos[0] + dr3[i], PACMAN_Pos[1] + dc3[i]]
            if neighbor[0] > -1 and neighbor[1] > -1 and neighbor[0] < size[0] and neighbor[1] < size[1]:
                if maze[neighbor[0]][neighbor[1]] == 2:
                    Draw_of_something(cv_first, food_image, (neighbor[1], neighbor[0]))
                    Inside_Foods.append(neighbor)
                    if neighbor == target:
                        continue
                    if neighbor not in food:
                        food.append(neighbor)
                if neighbor not in Sight:
                    Sight.append(neighbor)

    return Sight, Inside_Foods

def Hide_Something(cv_first, list_something):
    for i in list_something:
        cv_first.create_rectangle(i[1] * grid_edge + 1, i[0] * grid_edge + 1, (i[1] + 1) * grid_edge + 1, (i[0]+ 1) * grid_edge + 1, fill='black')

def Move(cv_first, maze, size, PACMAN_Pos, origin_pos):
    draw_pacman(cv_first, PACMAN_Pos)

    monsters = Find_Something(maze, size, 3)
    Hide_Something(cv_first, monsters)
    maze, monsters = monsters_Move_3(maze, size, origin_pos, monsters)
    for i in monsters:
        Draw_of_something(cv_first, creep_image, (i[1], i[0]))

    return maze

def Level_Three(cv_first, maze, size, PACMAN_Pos,maze_img,start_img):
    cv_first.delete("all")
    count_point = 0
    count_time = 0
    count_length = 0
    total_food = len(Find_Something(maze, size, 2))

    map = draw_map(maze, size, cv_first, 3)
    draw_pacman(cv_first, PACMAN_Pos)

    Draw_paramanter(1020, 50, "Food", total_food)      ##food
    Draw_paramanter(1020, 190, "Score", 0)               ##score
    Draw_paramanter(1020, 330, "Time", 0)           ##time
    Draw_paramanter(1020, 470, "Length", 0)         ##length

    root.update() 
    time.sleep(delay_time) #delay by second 

    Sight = list()
    food = []

    origin_Monster_pos = Find_Something(maze, size, 3)

    Sight.append(PACMAN_Pos)
    maze = Fill_Danger_Cells(maze, size)

    #Explore tầm nhìn xung quanh và in ra Food trogn tầm nhìn
    Signt, Inside_Foods = Explored_Sight_3(maze, size, cv_first, PACMAN_Pos, Sight, food, PACMAN_Pos)

    while total_food > 0:
        while not len(food) == 0:
            Target = Find_Nearest_Food(PACMAN_Pos, food)
            food.remove(Target)
            ans, path = AStart(maze, size, PACMAN_Pos, Target, 0)
            if ans == True:
                list_path = list()
                list_path = Path_Return(path, list_path, Target, PACMAN_Pos)
                list_path.append(Target)
                for i in list_path:
                    t1 = int(round(time.time() * 1000)) 

                    Hide_Something(cv_first, Inside_Foods)
                    Hide_Something(cv_first, [PACMAN_Pos])
                    PACMAN_Pos[0] = i[0]
                    PACMAN_Pos[1] = i[1]
                    maze = Move(cv_first, maze, size, PACMAN_Pos, origin_Monster_pos)
                    Signt, Inside_Foods = Explored_Sight_3(maze, size, cv_first, PACMAN_Pos, Sight, food, Target)

                    if PACMAN_Pos in food:
                        maze[PACMAN_Pos[0]][PACMAN_Pos[1]] = 0
                        food.remove(PACMAN_Pos)
                        count_point+= 20
                        total_food -= 1

                    count_length += 1
                    count_point -= 1
                    count_time += delay_time
                    if PACMAN_Pos == Target:
                        maze[PACMAN_Pos[0]][PACMAN_Pos[1]] = 0
                        count_point+= 20
                        total_food -=1

                    Draw_paramanter(1020, 50, "Food", total_food)      ##food
                    Draw_paramanter(1020, 190, "Score", count_point)               ##score
                    Draw_paramanter(1020, 330, "Time", int(count_time))           ##time
                    Draw_paramanter(1020, 470, "Length", count_length)         ##length

                    root.update() #update canvas
                    t2 = int(round(time.time() * 1000))
                    t = float(t2 - t1)/1000
                    if (t < delay_time):
                        time.sleep(delay_time - t) #delay by second 
                
        if total_food == 0:
            break
        ans, Target, path = Nearest_Unexplored_Cell(maze, size, PACMAN_Pos, Sight)
        if ans == True:
            list_path = list()
            list_path = Path_Return(path, list_path, Target, PACMAN_Pos)

            for i in list_path:     
                t1 = int(round(time.time() * 1000))

                Hide_Something(cv_first, Inside_Foods)
                Hide_Something(cv_first, [PACMAN_Pos])
                PACMAN_Pos[0] = i[0]
                PACMAN_Pos[1] = i[1]
                maze = Move(cv_first, maze, size, PACMAN_Pos, origin_Monster_pos)
                Sight, Inside_Foods = Explored_Sight_3(maze, size, cv_first, PACMAN_Pos, Sight, food, PACMAN_Pos)

                count_length += 1
                count_point -= 1
                count_time += delay_time

                Draw_paramanter(1020, 50, "Food", total_food)      ##food
                Draw_paramanter(1020, 190, "Score", count_point)               ##score
                Draw_paramanter(1020, 330, "Time", int(count_time))           ##time
                Draw_paramanter(1020, 470, "Length", count_length)         ##length

                root.update() #update canvas
                t2 = int(round(time.time() * 1000))
                t = float(t2 - t1)/1000
                if (t < delay_time):
                    time.sleep(delay_time - t) 

                if total_food == 0:
                    break
        else:
             end_game(cv_first, False,maze_img,start_img)
             return
    end_game(cv_first, True,maze_img,start_img)

#-----------------------------------------------------------------------------------------
#level 4

def Explored_Sight_4(maze, size, cv_first, PACMAN_Pos, Sight, food):

    for i in range(24):
            neighbor = [PACMAN_Pos[0] + dr3[i], PACMAN_Pos[1] + dc3[i]]
            if neighbor[0] > -1 and neighbor[1] > -1 and neighbor[0] < size[0] and neighbor[1] < size[1]:
                if neighbor not in Sight:
                    if maze[neighbor[0]][neighbor[1]] == 1:
                        Draw_of_something(cv_first, wall_image, (neighbor[1], neighbor[0]))
                    if maze[neighbor[0]][neighbor[1]] == 2:
                        Draw_of_something(cv_first, food_image, (neighbor[1], neighbor[0]))
                        food.append(neighbor)
                    Sight.append(neighbor)

    return Sight, food


def Display_Monster_Inside(cv_first, maze, size, monsters, sight):
    monster_insight = list()

    for i in monsters:
        if i in sight:
            monster_insight.append(i)
            Draw_of_something(cv_first, creep_image, (i[1], i[0]))

    return monster_insight


def monsters_Move_4(maze, size, monsters, Goal):
   
    for i in range(len(monsters)):
        ans, path = AStart(maze, size, monsters[i], Goal, 1)
        if not ans:
            for j in range(4):
                step = [monsters[i][0] + dr1[j], monsters[i][1] + dc1[j]]
                if step[0] > -1 and step[1] > -1 and step[0] < size[0] and step[1] < size[1]:
                    if maze[step[0]][step[1]] == 0:
                        maze[monsters[i][0]][monsters[i][1]] = 0
                        maze[step[0]][step[1]] = 3
                        monsters[i] = step
        else:
            list_path = list()
            list_path = Path_Return(path, list_path, Goal, monsters[i])
            list_path.append(Goal)

            maze[monsters[i][0]][monsters[i][1]] = 0
            maze[list_path[0][0]][list_path[0][1]] = 3
            monsters[i][0] = list_path[0][0]
            monsters[i][1] = list_path[0][1]

    return maze, monsters 

def Block_monster_path(maze, size, monsters_insight, PACMAN_Pos, n_unblock_cell):
    max = 0

    temp_maze = list()
    for i in range(size[0]):
        temp = maze[i].copy()
        temp_maze.append(temp)

    for i in monsters_insight:
        ans, path = AStart(maze, size, i, PACMAN_Pos, 1)
        if ans == True:
            list_path = list()
            list_path = Path_Return(path, list_path, PACMAN_Pos, i)
            if len(list_path) > max:
                max = len(list_path)

            if max - len(list_path) >= n_unblock_cell:
                for j in range(len(list_path)):
                    if j < len(list_path) - n_unblock_cell:
                        temp_maze[list_path[j][0]][list_path[j][1]] = 4

    return temp_maze, max

def PACMAN_Move_4(maze, size, cv_first, monsters_insight, PACMAN_Pos, sight, food):
    max = 1
    i = 0

    while i < max:
        temp_maze, max = Block_monster_path(maze, size, monsters_insight, PACMAN_Pos, i)
        i+=1

        temp_food = food.copy()
        while len(temp_food) != 0:
            target = Find_Nearest_Food(PACMAN_Pos, temp_food)
            temp_food.remove(target)
            ans, path = AStart(temp_maze, size, PACMAN_Pos, target, 0)
            if ans == True:
                list_path = list()
                list_path = Path_Return(path, list_path, target, PACMAN_Pos)
                list_path.append(target)

                return [list_path[0][0],list_path[0][1]]

        ans, target, path = Nearest_Unexplored_Cell(temp_maze, size, PACMAN_Pos, sight)
        if ans == True:
            list_path = list()
            list_path = Path_Return(path, list_path, target, PACMAN_Pos)

            return [list_path[0][0], list_path[0][1]] 
    
    #He will die soon : (
    for i in range(4):
        step = [PACMAN_Pos[0] + dr1[i], PACMAN_Pos[1] + dc1[i]]
        if step[0] > -1 and step[1] > -1 and step[0] < size[0] and step[1] < size[1]:
            if maze[step[0]][step[1]] == 0:
                return step

    return PACMAN_Pos

def Level_Four(cv_first, maze, size, PACMAN_Pos,maze_img,start_img):
    cv_first.delete("all")
    count_point = 0
    count_time = 0
    count_length = 0

    sight = list()
    food = list()

    sight.append(PACMAN_Pos)
    sight, food = Explored_Sight_4(maze, size, cv_first, PACMAN_Pos, sight, food)

    total_food = len(Find_Something(maze, size, 2))
    monsters = Find_Something(maze, size, 3)
    monsters_insight = Display_Monster_Inside(cv_first, maze, size, monsters, sight)
    
    Draw_paramanter(1020, 50, "Food", total_food)      ##food
    Draw_paramanter(1020, 190, "Score", 0)               ##score
    Draw_paramanter(1020, 330, "Time", 0)           ##time
    Draw_paramanter(1020, 470, "Length", 0)         ##length
             
    while total_food > 0:
        t1 = int(round(time.time() * 1000))

        Hide_Something(cv_first, [PACMAN_Pos])
        PACMAN_Pos = PACMAN_Move_4(maze, size, cv_first, monsters_insight, PACMAN_Pos, sight, food)
        if PACMAN_Pos in food:
            count_point += 20
            food.remove(PACMAN_Pos)
            total_food -= 1
            maze[PACMAN_Pos[0]][PACMAN_Pos[1]] = 0

        draw_pacman(cv_first, PACMAN_Pos)

        sight, food = Explored_Sight_4(maze, size, cv_first, PACMAN_Pos, sight, food)

        Hide_Something(cv_first, monsters)
        maze, monsters = monsters_Move_4(maze, size, monsters, PACMAN_Pos)
        monsters_insight = Display_Monster_Inside(cv_first, maze, size, monsters, sight)

        count_length += 1
        count_point -= 1
        count_time += delay_time


        Draw_paramanter(1020, 50, "Food", total_food)      ##food
        Draw_paramanter(1020, 190, "Score", count_point)               ##score
        Draw_paramanter(1020, 330, "Time", int(count_time))           ##time
        Draw_paramanter(1020, 470, "Length", count_length)         ##length


        root.update() #update canvas
        t2 =  int(round(time.time() * 1000))
        t = float(t2 - t1)/1000
        if t < delay_time:
            time.sleep(delay_time - t) #delay by second 


        if PACMAN_Pos in monsters:
            end_game(cv_first, False,maze_img,start_img)
            return
    end_game(cv_first, True,maze_img,start_img)


if __name__ == '__main__':
    root = Tk()
    root.title("pacman")
    cv_first = Canvas(root, width = 1200, height = 600, bg = "black") 
    cv_first.pack()

    start_img = ImageTk.PhotoImage(PIL.Image.open("bg_start.jpg"))
    maze_img = ImageTk.PhotoImage(PIL.Image.open("bg_maze.png"))
    thanks_bg = ImageTk.PhotoImage(PIL.Image.open("thanks_bg.jpg"))
    
    MenuStart(cv_first,start_img,maze_img,thanks_bg)


     
    creep_image = Image.open("creep.png")
    creep_image = creep_image.resize((grid_edge - 2, grid_edge - 2), Image.ANTIALIAS)
    creep_image = ImageTk.PhotoImage(creep_image)

    wall_image = Image.open("wall.jpg")
    wall_image = wall_image.resize((grid_edge - 2, grid_edge - 2), Image.ANTIALIAS)
    wall_image = ImageTk.PhotoImage(wall_image)

    food_image = Image.open("food.jpg")
    food_image = food_image.resize((grid_edge - 2, grid_edge - 2), Image.ANTIALIAS)
    food_image = ImageTk.PhotoImage(food_image)

    img = ImageTk.PhotoImage(PIL.Image.open("bg_level.jpg"))
    
    root.update()

    
    root.mainloop()
