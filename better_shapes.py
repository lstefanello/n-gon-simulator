import pygame
import random
import math
import matplotlib.pyplot as plt

class Ngon:
    def __init__(self, width, height, n, r):
        self.vertices = [] # the array of vertex coordinates relative to the 2*r x 2*r pygame surface
        self.xverts = [] # array of x coordinates of vertices relative to the whole screen
        self.yverts = [] # array of y coordinates of vertices relative the whole screen
            
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.theta = random.uniform(0, math.pi*2) #random rotation added to polygon
        
        self.bottomleft = [self.x - r, self.y - r] #the bottomleft coordinate of the bounding box of the polygon, this gets passed to blit() to be drawn on screen
        
        self.alpha = 1
        self.surf = pygame.Surface((2*r, 2*r)) #this is the surface we draw the polygon onto
        self.surf.set_colorkey((0, 0 ,0))
        self.surf.set_alpha(self.alpha)
        
        self.intersection = False
        self.double_intersection = False
        
        #generates the locations of the vertices for an ngon.
        for i in range (1, n+1):
            self.vertices.append((r + r * math.cos((i *(2 * math.pi) / n) + self.theta), r + r * math.sin((i * (2 * math.pi) / n) + self.theta))) #relative to pygame surface
            self.xverts.append(self.x + r * math.cos((i * (2 * math.pi) / n) + self.theta)) #relative to screen
            self.yverts.append(self.y + r * math.sin((i * (2 * math.pi) / n) + self.theta)) #relative to screen
        
        self.extremes = [min(self.xverts), max(self.xverts), min(self.yverts), max(self.yverts)] #leftmost vertext, rightmost vertex, bottommost vertex, topmost vertex        
        
#constructs all the polygons
def init():
    shape = []
    width = int(input("Width? (in pixels) ")) 
    height = int(input("Height? (in pixels) ")) 
    n = int(input("Number of sides? "))
    r = int(input("Circumradius? "))
    t = int(input("Number of trials? "))
        
    for i in range (0, t):
        shape.append(Ngon(width, height, n, r))
        
    parameters = (width, height, n, r)
    
    return shape, parameters

#computes the probability and compares with our prediction, the actual simulation
def simulate(ngons, parameters):
    #the formulae I came up with. p_a is the probability that a regular ngon intersects a horizontal line
    #p_b is the probability that a regular ngon intersects a vertical line
    #p_t is the probability of the union of a and b.
    #the window boundaries are treated as these lines.
    #parameters = (width, height, n, r)
    p_a = (2 * parameters[3] * parameters[2] * math.cos((math.pi * (parameters[2] - 2))/(2 * parameters[2]))) / (parameters[1] * math.pi)
    p_b = (2 * parameters[3] * parameters[2] * math.sin( math.pi / parameters[2])) / (parameters[0] * math.pi)
    p_t = (p_a + p_b) - (p_a * p_b)
    intersections = 0
    double_intersections = 0
        
    for i in range (0, len(ngons)):
        if ngons[i].extremes[0] <= 0 or ngons[i].extremes[1] >= parameters[0] or ngons[i].extremes[2] <= 0 or ngons[i].extremes[3] >= parameters[1]: #if the most extreme vertices are out of bounds, there must be an intersection
            intersections += 1
            ngons[i].intersection = True
            if (ngons[i].extremes[0] <= 0 and ngons[i].extremes[2] <= 0) or (ngons[i].extremes[0] <= 0 and ngons[i].extremes[3] >= parameters[1])  or (ngons[i].extremes[1] >= parameters[0] and ngons[i].extremes[2] <= 0) or (ngons[i].extremes[1] >= parameters[0] and ngons[i].extremes[3] >= parameters[1]): 
                double_intersections += 1
                ngons[i].double_intersection = True
                ngons[i].color = (0, 128, 0)
            else:
                ngons[i].color = (244, 32, 105)
        else:
            ngons[i].color = (247, 208, 203)
        
        pygame.draw.polygon(ngons[i].surf, ngons[i].color, ngons[i].vertices) #attach the polygon to a surface to be rendered later
        print("Experimental probability (single intersection): ", intersections/(i+1))
    
    print("Predicted probability (single intersection): ", p_t)
    print("Error: ", intersections/(i+1) - p_t)
    print("Experimental probability (double intersection): ", double_intersections/(i+1))
    print("Predicted probability (double intersection): ", p_a*p_b)
   
def plot(ngons):
    xintersects = []
    yintersects = []
    xother = []
    yother = []
    d_x_int = []
    d_y_int = []
    
    for i in range (0, len(ngons)):
        if ngons[i].intersection == True and ngons[i].double_intersection == False:
            xintersects.append(ngons[i].x)
            yintersects.append(ngons[i].y)
        elif ngons[i].double_intersection == True:
            d_x_int.append(ngons[i].x)
            d_y_int.append(ngons[i].y)
        else:
            xother.append(ngons[i].x)
            yother.append(ngons[i].y)
    
    plt.scatter(xother, yother, c='black', marker=",")
    plt.scatter(xintersects, yintersects,c='red', marker=",")
    plt.scatter(d_x_int, d_y_int, c='green', marker=",")
    plt.show()

def event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True

#blit polygon surfaces to the screen + fade in animation
def render(screen, ngons, ticks):
    if ticks < len(ngons):
        while ngons[ticks].alpha < 200: #make the polygon fade in, incrementally adjusting its alpha value
            screen.blit(ngons[ticks].surf, ngons[ticks].bottomleft) #draw the surace we set up in simulate()
            ngons[ticks].alpha += 5
            ngons[ticks].surf.set_alpha(ngons[ticks].alpha)
            pygame.display.flip()
            pygame.time.wait(15)
      
def main():
    exit = False
    ticks = 0
    
    shape, parameters = init() #brings all the polygons into existence
    simulate(shape, parameters) #do the actual simulation before the render  
    
    p_confirm = input("show plot? (y/n) ")
    while(p_confirm != "y" and p_confirm != "n"):
        p_confirm = input("show plot? (y/n) ")
        
    if (p_confirm == "y"):
        plot(shape)
    
    a_confirm = input("show animation? (y/n) ")
    while(a_confirm !="y" and a_confirm != "n"):
         a_confirm = input("show animation? (y/n) ")
         
    if(a_confirm == "y"):
        pygame.init()
        screen = pygame.display.set_mode((parameters[0], parameters[1]))
        clock = pygame.time.Clock()
        pygame.display.set_caption("n-gon mania")
    
        while not exit:
            exit = event()  
            render(screen, shape, ticks)
            clock.tick(60)
            ticks += 1

        pygame.quit()
    
main()