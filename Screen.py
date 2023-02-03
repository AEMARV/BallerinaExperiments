def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret

class Ballerina(Sprite):
    def __init__(self, images, posx, posy,speed,scale=10, phase=0):
        super().__init__()
        self.sprites= images

            #self.sprites[i] = pygame.transform.scale(sprite,(sprite.get_width()//scale,sprite.get_height()//scale))
        self.image = self.sprites[0]
        self.speed= speed
        self.rect = self.image.get_rect()
        self.rect.topleft = [posx, posy]
        self.graphic_index = phase % len(self.sprites)


    def update(self):
        self.graphic_index += self.speed
        if self.graphic_index >= len(self.sprites)-1:
            self.graphic_index -= len(self.sprites)-1
        self.image = self.sprites[int(self.graphic_index)]


class BallerinaPanel:
    DisplayInfo = pygame.display.Info()
    WIDTH, HEIGHT = DisplayInfo.current_w, DisplayInfo.current_h
    BALSZ = WIDTH // 150
    BALSPEED = 1
    FPS = 60
    def __init__(self):
        self.speed = [0, 0]
        self.black = 0, 0, 0
        self.run = False
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.FULLSCREEN)
        pygame.display.set_caption('Radar Panel')
        self.ballerina_group = pygame.sprite.Group()
        pos = [0,0]
        self.sprites = split_animated_gif("../VCU/Spinning_Dancer.gif")
        for i, sprite in enumerate(self.sprites):
            self.sprites[i] = pygame.transform.scale(sprite,
                                                     (self.BALSZ, self.BALSZ))
        for i in range(30000):
            thisspeed = random.random()
            rint = random.randint(0,10000)
            r= math.sqrt(((pos[0] - self.WIDTH/2)**2) + ((pos[1] - self.HEIGHT/2)**2))
            b = Ballerina(self.sprites,pos[0], pos[1],self.BALSPEED,scale=2, phase=int(r))
            self.ballerina_group.add(b)
            pos[0] = pos[0] + b.rect.w
            if pos[0]>self.WIDTH:
                pos[0]=0
                pos[1] = pos[1]+ b.rect.h
                if pos[1]>self.HEIGHT:
                    break

        self.ball = pygame.image.load("../VCU/Spinning_Dancer.gif")

    def draw(self):
        self.ballerina_group.draw( self.WIN)
    def start(self):
        self.run = True
        self.clock = pygame.time.Clock()
        while self.run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.WIN.fill((21,21,21))
            self.ballerina_group.update()
            self.draw()
            pygame.display.update()
        pygame.quit()
