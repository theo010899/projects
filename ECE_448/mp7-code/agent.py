import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.reset()
        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def state_space(self, state):
        adjoing_wall = [0,0]
        food_dir = [0,0]
        adjoined_body = [0,0,0,0]

        # if state != None:
        snake_head_x = state[0]
        snake_head_y  = state[1]
        snake_body  = state[2]
        food_x = state[3]
        food_y = state[4]
        #initlize adjoining wall
        if snake_head_x == 40:
            adjoing_wall[0] = 1
        if snake_head_x == 480:
            adjoing_wall[0] = 2
        if snake_head_y == 40:
            adjoing_wall[1] = 1
        if snake_head_y == 480:
            adjoing_wall[1] = 2

        #initialize food dir
        if food_x < snake_head_x:
            food_dir[0] = 1
        if food_x > snake_head_x:
            food_dir[0] = 2
        if food_y < snake_head_y:
            food_dir[1] = 1
        if food_y > snake_head_y:
            food_dir[1] = 2

        #initialize adjoined body
        
        for link in snake_body:
            x = link[0]
            y = link[1]
            if y == snake_head_y - 40 and x == snake_head_x:
                adjoined_body[0] = 1
            if y  == snake_head_y + 40 and x == snake_head_x:
                adjoined_body[1] = 1
            if y == snake_head_y and x  == snake_head_x - 40:
                adjoined_body[2] = 1
            if y == snake_head_y and x  == snake_head_x + 40:
                adjoined_body[3] = 1

        return tuple((adjoing_wall[0], adjoing_wall[1],food_dir[0], food_dir[1], adjoined_body[0], adjoined_body[1], adjoined_body[2], adjoined_body[3]))
    
    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        # print(self.Q)
        # reward function
        action = None
        reward = -0.1
        if points > self.points:
            reward = 1
        elif dead:
            reward = -1

        # descritize the state
        cur_state = self.state_space(state)
        # self.s = self.state_space(self.s)
        # print(cur_state)
        # up,down,left,right = self.Q[cur_state]
        # print("UP = ", up)
        # print("DOWN = ", down)
        # print("LEFT = ", left)
        # print("RIGHT = ", right)
        # start training loop
        if self._train:
            if self.s != None:
            # choosing the max QPrime with tie-breaking priority
            # print(cur_state)
                q_prime = max(self.Q[cur_state])
                # print(self.s, " ", cur_state)
                q_state = self.Q[self.s[0],self.s[1], self.s[2], self.s[3], self.s[4], self.s[5], self.s[6], self.s[7], self.a]
                alpha = self.C/(self.C + self.N[self.s[0],self.s[1], self.s[2], self.s[3], self.s[4], self.s[5], self.s[6], self.s[7], self.a])
                self.Q[self.s[0],self.s[1], self.s[2], self.s[3], self.s[4], self.s[5], self.s[6], self.s[7], self.a] = q_state + alpha * (reward + (self.gamma * q_prime) - q_state)
            
        F = []
        for i in range(4):
            q = self.Q[cur_state[0],cur_state[1], cur_state[2], cur_state[3], cur_state[4], cur_state[5], cur_state[6], cur_state[7], i]
            n = self.N[cur_state[0],cur_state[1], cur_state[2], cur_state[3], cur_state[4], cur_state[5], cur_state[6], cur_state[7], i]
            # print(q, " ", n, " ", self.Ne)
            if n < self.Ne:
                F.append(1)
            else:
                F.append(q)
        # print(F)
        F.reverse()
        action = 3 - (F.index(max(F)))
        # print(F)
        
        # action = 3 - action
        # print(self.s)
        if not dead:
            self.N[cur_state[0],cur_state[1], cur_state[2], cur_state[3], cur_state[4], cur_state[5], cur_state[6], cur_state[7], action] += 1
            self.s = cur_state
            self.a = action
            self.points = points
        # else:
        #     action = 3 - np.argmax(self.Q[cur_state])
        #     print(action)

        # if self._train == 0:
        #     print(cur_state)
        if dead:
            self.reset()

        return action
