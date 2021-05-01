from math import sqrt
from math import floor

#--class definitions-------------------------------------------------------------------

class Node:
    def __init__(self,state,g,mode,parent):
        self.state=state
        self.g=g
        self.h=0
        self.mode=mode
        self.parent=parent

    def f(self):
        self.h=0
        if self.mode==1:
            return self.g
        size_of_game=len(self.state)
        dimensions=sqrt(size_of_game)
        for i in range(size_of_game):
            if self.state[i]==0:
                continue
            horizontal_distance=(i%dimensions)-((self.state[i]-1)%dimensions)
            vertical_distance=floor(i/dimensions)-floor((self.state[i]-1)/dimensions)
            euclidean_distance=sqrt(horizontal_distance**2+vertical_distance**2)
            manhattan_distance=abs(horizontal_distance)+abs(vertical_distance)
            if self.mode==2:
                self.h+=manhattan_distance
            if self.mode==3:
                self.h+=euclidean_distance
        return self.h+self.g

    def display(self):
        dimensions=sqrt(len(self.state))
        print("-------------")
        print("f(n) = "+str(self.f()))
        print("g(n) = "+str(self.g))
        print("h(n) = "+str(self.h))
        for i in range(len(self.state)):
            if i%dimensions==0:
                print("")
            if self.state[i]==0:
                print("*"),
                print(" "),
            else:
                print(self.state[i]),
                print(" "),
        print("")

class Problem:
    def __init__(self,start):
        self.start_state=start
        self.goal_state=[1,2,3,4,5,6,7,8,0]
        self.frontier=[]
        self.max_q=0
        self.explored=[]

    def update_frontier(self,current_state):
        size_of_game=len(current_state.state)
        g=current_state.g+1
        dimensions=int(sqrt(size_of_game))
        i=None
        for x in range(size_of_game):
            if current_state.state[x]==0:
                i=x
        x_coordinate=i%dimensions
        y_coordinate=floor(i/dimensions)
        if x_coordinate+1<=2:
            new_state=list(current_state.state)
            new_state[i],new_state[i+1]=new_state[i+1],new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node=Node(new_state,g,current_state.mode,current_state)
                self.frontier.append(node)
        if x_coordinate-1>=0:
            new_state=list(current_state.state)
            new_state[i],new_state[i-1]=new_state[i-1],new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node=Node(new_state,g,current_state.mode,current_state)
                self.frontier.append(node)
        if y_coordinate+1<=2:
            new_state=list(current_state.state)
            new_state[i],new_state[i+dimensions]=new_state[i+dimensions],new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node=Node(new_state,g,current_state.mode,current_state)
                self.frontier.append(node)
        if y_coordinate-1>=0:
            new_state=list(current_state.state)
            new_state[i],new_state[i-dimensions]=new_state[i-dimensions],new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node=Node(new_state,g,current_state.mode,current_state)
                self.frontier.append(node)
        if len(self.frontier)>self.max_q:
            self.max_q=len(self.frontier)

    def check_frontier(self,check_state):
        for i in self.frontier:
            if i.state==check_state:
                return False
        return True

    def remove_state(self):
        min_f=None
        for i in self.frontier:
            if min_f:
                if i.f()<min_f.f():
                    min_f=i
            else:
                min_f=i
        self.frontier.remove(min_f)
        return min_f

#--helper functions--------------------------------------------------------------------

def intro():
    print("Welcome to otheh001 (862029595) 8 puzzle solver.")
    choice=int(input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle: "))
    puzzle=[]
    SIZE=9
    dimensions=sqrt(SIZE)
    if choice==2:
        for i in range(SIZE):
            x_coordinate=int(i%dimensions)
            y_coordinate=int(floor(i/dimensions))
            cell=input("Enter cell["+str(y_coordinate)+"]["+str(x_coordinate)+"]: ")
            puzzle.append(cell)
    else:
        puzzle=[8,7,1,6,0,2,5,4,3]
    print("\nEnter your choice of algorithm")
    print("\"1\" for Uniform Cost Search")
    print("\"2\" for A* with the Manhattan Distance heuristic")
    print("\"3\" for A* with the Euclidean Distance heuristic")
    mode=input("Here: ")
    print("")
    return (puzzle,mode)
    
def display_path(result):
    cost=result.g
    if result:
        # Reverses order that trace is printed
        '''left=result
        right=result.parent
        prev=None
        while right:
            left.parent=prev
            prev=left
            left=right
            right=right.parent
        left.parent=prev
        while left:
            left.display()
            left=left.parent'''
        while result:
            result.display()
            result=result.parent
        print("-------------")
        print("This solution took "+str(cost)+" moves")
        print("The maximum size of the frontier is "+str(problem.max_q))
    else:
        print("There is no solution")

def graph_search(problem,node):
    if node.state==problem.goal_state:
        return node
    problem.update_frontier(node)
    print("Searching...\n")
    while (True):
        if not problem.frontier:
            return None
        current_state=problem.remove_state()
        if current_state.state in problem.explored:
            continue
        problem.explored.append(current_state.state)
        if current_state.state==problem.goal_state:
            #current_state.parent=None
            return current_state
        problem.update_frontier(current_state)

#--main--------------------------------------------------------------------------------

puzzle_mode_tuple=intro()
problem=Problem(puzzle_mode_tuple[0])
node=Node(problem.start_state,0,puzzle_mode_tuple[1],None)
result=graph_search(problem,node)
display_path(result)