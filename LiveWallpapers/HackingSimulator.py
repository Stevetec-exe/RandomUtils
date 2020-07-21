import pygame
import random
import python_generator
import configparser
import os


# To exit the programm press Q 6 times.
# This is done so you can hit your keyboard like a 'true' hacker :)
class Graph:
    def __init__(self,color,minh,maxh,delta_x,delta_y,width,speed):
        self.color = color
        self.max_height = maxh
        self.min_height = minh
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.width = width
        self.height = maxh
        self.target = 0
        self.speed = speed
        self.speed_factor = 0

        self.update_target(True)
        self.static = False

    def render(self,display):
        pygame.draw.rect(display,self.color,[self.delta_x,self.delta_y-self.height,int(self.width),int(self.height)])

    def update(self):
        if not self.static:
            self.height += self.speed*self.speed_factor
            self.update_target()

    def update_target(self,force_update = False):
        while abs(self.target-self.height) < self.speed * 2 or force_update:
            force_update = False
            self.target = random.randint(self.min_height,self.max_height)

            if self.height > self.target:
                self.speed_factor = -1
            else:
                self.speed_factor = 1


class TextObject:
    def __init__(self,font,delta):
        self.font = font
        self.text = ""
        self.target_text = python_generator.get_random_python()
        self.timer = 0
        self.delta_offset = delta
        self.color = [75,75,75]
        self.static = False

    def render(self,display):
        text = self.font.render(self.text,True,self.color)
        display.blit(text,self.delta_offset)

    def update(self):
        if not self.static and random.randint(0,2) == 0:
            if self.timer < len(self.target_text):
                self.text += self.target_text[self.timer]
            elif self.timer == len(self.target_text)+5:
                self.target_text = python_generator.get_random_python()
                self.timer = 0
                self.text = self.target_text[0]
            self.timer += 1


class ProgressBar:
    def __init__(self,delta,size,font,text,speed):
        self.delta = delta
        self.size = size
        self.color = [200,100,50]
        self.txt = font.render(text,True,[255,255,255])

        self.fill = 10
        self.speed = speed

    def render(self,display):
        pygame.draw.rect(display,self.color,[self.delta[0],self.delta[1],self.fill,self.size[1]])
        pygame.draw.rect(display,[255,255,255],[self.delta[0],self.delta[1],self.size[0],self.size[1]],2)
        display.blit(self.txt,[self.delta[0]+5,self.delta[1]+self.size[1]/2-10])

    def update(self):
        self.fill += self.speed
        if self.fill > self.size[0]:
            self.fill = 10

class NodeMesh:
    def __init__(self,delta,size,speed):
        self.delta = delta
        self.size = size
        self.nodes = [[random.randint(0,size[0]),random.randint(0,size[1])] for i in range(20)]
        self.targets = [[random.randint(0,size[0]),random.randint(0,size[1])] for i in range(20)]
        self.color = [255,255,255]
        self.speed = speed
        self.selected = 0

    def render(self,display):
        for node_id,node_raw in enumerate(self.nodes):
            node = [node_raw[0]+self.delta[0],node_raw[1]+self.delta[1]]
            col = self.color
            if node_id == self.selected:
                col = [255,0,0]
            for tid,target_raw in enumerate(self.nodes):
                target = [target_raw[0]+self.delta[0],target_raw[1]+self.delta[1]]
                if target != node:
                    if tid != self.selected:
                        width = 1
                        if node_id == self.selected:
                            width = 3
                        pygame.draw.line(display,col,node,target,width)
            int_node = [int(node[0]),int(node[1])]
            pygame.draw.circle(display,[255,255,255],int_node,3)

    def update(self):
        for i in range(len(self.nodes)):
            if abs(self.nodes[i][0] - self.targets[i][0]) < 5 and abs(self.nodes[i][1]) - self.targets[i][1] < 5:
                self.targets[i] = [random.randint(0,self.size[0]),random.randint(0,self.size[1])]

            dx,dy = 1,1
            if self.nodes[i][0] - self.targets[i][0] > 0:
                dx = -1
            if self.nodes[i][1] - self.targets[i][1] > 0:
                dy = -1
            self.nodes[i][0] += dx*self.speed
            self.nodes[i][1] += dy*self.speed
        if random.randint(0,10) == 0:
            self.selected = random.randint(0,len(self.nodes)-1)


def ip_range(start):
    ip = start
    while True:
        yield str(ip).replace("[","").replace("]","").replace(",",".")
        ip[3] += 10
        if ip[3] >= 256:
            ip[3] = 0
            ip[2] += 1
            if ip[2] >= 256:
                ip[2] = 0
                ip[1] += 1
                if ip[1] >= 256:
                    ip[1] = 0
                    ip[0] += 1
                    if ip[0] >= 256:
                        ip = [0,0,0,0]


config = configparser.ConfigParser()
config.read('settings.ini')
mid=config.getint("WindowFlags","MonitorId")
screenres = [1920,1080]
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920*mid,0)
pygame.init()
flags = 0
if config.getboolean("WindowFlags","Fullscreen"):
    flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(screenres,flags|pygame.NOFRAME)
active = True
font = pygame.font.SysFont('monospace',20)
font2 = pygame.font.SysFont('monospace',30)
render_list = []
g_init_spacing = 20
g_width = 10
g_spacing = 5
if config.getboolean("BackgroundText","visible"):
    for i in range(48):
        render_list.append(TextObject(font,[20,i*30+5]))

plot_names = [config.get("Graph_Red","text"),config.get("Graph_Green","text"),config.get("Graph_Blue","text")]
cn = "Red,Green,Blue".split(",")

for i in range(3):
    if config.getboolean("Graph_"+cn[i],"visible"):
        text = TextObject(font2,[20,screenres[1]/2 + 350 -i*350 + 50])
        text.color = [255,255,255]
        text.static = True
        text.text = plot_names[i]
        render_list.append(text)
if config.getboolean("Graph_Red","visible"):
    for i in range(10):
        render_list.append(Graph([255 - i * 10, 0 + i * 7, 50], 20, 200, g_width * i + g_spacing * i + g_init_spacing, screenres[1]/2 + 350 +50, g_width, 3))
if config.getboolean("Graph_Green","visible"):
    for i in range(10):
        render_list.append(Graph([50,255-i*10,50+i*5], 20, 200, g_width * i + g_spacing * i + g_init_spacing, screenres[1]/2 +50, g_width, 3))
if config.getboolean("Graph_Blue","visible"):
    for i in range(10):
        i2 = 10 -i
        render_list.append(Graph([50,150-i2*10,255-i2*10], 20, 200, g_width * i + g_spacing * i + g_init_spacing, screenres[1]/2 - 350 +50, g_width, 3))

texts = []
indentation = []
tid = 0
parsing = True
while parsing:
    try:
        texts.append(config.get("Text"+str(tid),"text"))
        indentation.append(config.getint("Text"+str(tid),"indent"))
        tid += 1
    except configparser.NoOptionError:
        parsing = False
    except configparser.NoSectionError:
        parsing = False
offset_pixels = config.getint("TextSettings","indentation_pixels")
for i in range(len(texts)):
    txt = TextObject(font,[250+int(indentation[i])*offset_pixels,i*30+100])
    txt.static = True
    txt.color = [255,255,255]
    if indentation[i] == 0:
        txt.text = texts[i]
    else:
        txt.color = [175,175,175]
        txt.text = "- "+texts[i]
    render_list.append(txt)

texts = []
speeds = []
tid = 0
parsing = True
while parsing:
    try:
        texts.append(config.get("LoadingBar"+str(tid),"text"))
        speeds.append(config.getfloat("LoadingBar"+str(tid),"speed"))
        tid += 1
    except configparser.NoOptionError:
        parsing = False
    except configparser.NoSectionError:
        parsing = False
for i in range(len(texts)):
    bar = ProgressBar([720,100+i*60],[500,30],font,texts[i],speeds[i])
    bar.color = [200-i*20,50,50+i*20]
    render_list.append(bar)


binary_text = []

ip_gen = ip_range([0,0,0,0])
ip_display = TextObject(font2,[screenres[0]-520,100])
ip_display.static = True
ip_display.text = "LOADING..."
ip_display.color = [255,200,200]
if config.getboolean("IP","visible"):
    render_list.append(ip_display)

if config.getboolean("Binary","visible"):
    txt = TextObject(font2,[screenres[0]-520,180])
    txt.static = True
    txt.text = config.get("Binary","headline")
    txt.color = [255,255,255]
    render_list.append(txt)
    for i in range(config.getint("Binary","rows")):
        txt = TextObject(font,[screenres[0]-520,220+i*20])
        txt.static = True
        txt.text = "".join([str(random.randint(0,1)) for i in range(30)])
        txt.color = [255,255,255]
        render_list.append(txt)
        binary_text.append(txt)

if config.getboolean("NodeMesh","visible"):
    render_list.append(NodeMesh([770,screenres[1]-410],[400,400],config.getfloat("NodeMesh","speed")))

clock = pygame.time.Clock()
fps = config.getint("WindowFlags","fps")
keydeath = 0
while active:
    clock.tick(fps)
    screen.fill([50,50,50])
    #screen.blit(background,[0,0])
    ip_display.text = "Scanning: "+ip_gen.__next__()
    for gid,g in enumerate(render_list):
        g.update()
        g.render(screen)
    for line in binary_text:
        if random.randint(0,5) == 0:
            line.text = "".join([str(random.randint(0,1)) for i in range(30)])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                keydeath += 1
            else:
                keydeath = 0
        if keydeath > 5 or event.type == pygame.QUIT:
            active = False
pygame.quit()
