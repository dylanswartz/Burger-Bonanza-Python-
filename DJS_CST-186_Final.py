# Dylan Swartz
# CST-186 Fall 2009
# Final Project
# Burger Bonanza

# CREDITS
# Artwork - Morgan Boshaw
# Music and Sound - http://flashkit.com/ & http://www.soundsnap.com/

# Game Instructions:
# Click on or near your pet to feed them a cheeseburger.
# Collect the coins that your pets drop. Save up money to
# purchase new pets and larger cheeseburgers that will fill
# them up for a longer time. Don't let your pets starve - you
# only have four lives before its GAME OVER!

import os, sys, random, pygame, math
from pygame.locals import *
from livewires import games, color

games.init(screen_width = 800, screen_height = 600, fps = 50)

class Instructions(games.Sprite):
    """ Game instructions menu """
    image = pygame.image.load("images/instructions.png").convert_alpha()

    def __init__(self, game, x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize object """
        super(Instructions, self).__init__(image = Instructions.image,
                                    x = x, y = y)
        self.game = game
        
    def update(self):
        """ Check to see if a button is being clicked """
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if games.mouse.get_x() < self.game.backBtn.right \
                   and games.mouse.get_x() > self.game.backBtn.left \
                   and games.mouse.get_y() < self.game.backBtn.bottom \
                   and games.mouse.get_y() > self.game.backBtn.top:
                    self.game.backBtn.action()

class Menu(games.Sprite):
    """ Game main menu """
    def __init__(self, game, image = pygame.image.load("images/menu.png").convert_alpha(), \
                 x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize object """
        super(Menu, self).__init__(image = image,
                                    x = x, y = y)
        self.game = game
        
    def update(self):
        """ Check to see if a button is being clicked """
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if games.mouse.get_x() < self.game.playBtn.right \
                   and games.mouse.get_x() > self.game.playBtn.left \
                   and games.mouse.get_y() < self.game.playBtn.bottom \
                   and games.mouse.get_y() > self.game.playBtn.top:
                    self.game.playBtn.action()
                elif games.mouse.get_x() < self.game.instructionsBtn.right \
                   and games.mouse.get_x() > self.game.instructionsBtn.left \
                   and games.mouse.get_y() < self.game.instructionsBtn.bottom \
                   and games.mouse.get_y() > self.game.instructionsBtn.top:
                    self.game.instructionsBtn.action()
                    


class PlayBtn(games.Sprite):
    """ PlayBtn - Starts Game """
    image = pygame.image.load("images/playBtn.png").convert_alpha()
    def __init__(self, game, x = games.screen.width - 380, y = games.screen.height - 90):
        """ Intialize object """
        super(PlayBtn, self).__init__(image = PlayBtn.image, x = x, y = y)
        self.game = game

    def update(self):
        # check for mouse over and click
        super(PlayBtn, self).update()
        if games.mouse.get_x() < self.right \
        and games.mouse.get_x() > self.left \
        and games.mouse.get_y() < self.bottom \
        and games.mouse.get_y() > self.top:

            hover = pygame.image.load("images/playBtnHover.png").convert_alpha()
            self.set_image(hover)
        else:
            nonhover = pygame.image.load("images/playBtn.png").convert_alpha()
            self.set_image(nonhover)

    def action(self):
        self.game.play()

class InstructionBtn(games.Sprite):
    """ Navigates to the instructions page """
    image = pygame.image.load("images/instructionsBtn.png").convert_alpha()
    def __init__(self, game, x = games.screen.width - 190, y = games.screen.height - 90):
        """ Intialize object """
        super(InstructionBtn, self).__init__(image = InstructionBtn.image, x = x, y = y)
        self.game = game

    def update(self):
        # check for mouse over and click
        super(InstructionBtn, self).update()
        if games.mouse.get_x() < self.right \
        and games.mouse.get_x() > self.left \
        and games.mouse.get_y() < self.bottom \
        and games.mouse.get_y() > self.top:

            hover = pygame.image.load("images/instructionsBtnHover.png").convert_alpha()
            self.set_image(hover)
        else:
            nonhover = pygame.image.load("images/instructionsBtn.png").convert_alpha()
            self.set_image(nonhover)

    def action(self):
        self.game.add_instructions()

class BackBtn(games.Sprite):
    """ Navigates back to main menu """
    image = pygame.image.load("images/backBtn.png").convert_alpha()
    def __init__(self, game, x = games.screen.width - 95, y = games.screen.height - 40):
        """ Intialize object """
        super(BackBtn, self).__init__(image = BackBtn.image, x = x, y = y)
        self.game = game

    def update(self):
        super(BackBtn, self).update()
        if games.mouse.get_x() < self.right \
        and games.mouse.get_x() > self.left \
        and games.mouse.get_y() < self.bottom \
        and games.mouse.get_y() > self.top:

            hover = pygame.image.load("images/backBtnHover.png").convert_alpha()
            self.set_image(hover)
        else:
            nonhover = pygame.image.load("images/backBtn.png").convert_alpha()
            self.set_image(nonhover)

    def action(self):
        self.game.rem_instructions()


class Pet(games.Sprite):
    """ A pet that walks around, gets hungry, and drops money"""
    speed = 0.5
        
    def update(self):
        """ Randomly move the pet around, update hunger, poop, and eat """
        self.walk()
        self.elevate()
        self.check_collide()
        self.poop()
        self.updateHunger()

        if self.game.lives < 0:
            self.destroy()

    def updateHunger(self):
        # update hunger
        self.tickCount += 1
        if self.tickCount % 120 == 0:
            self.hunger -= self.decrement

        if self.hunger <= 0:
            #pet dies
            self.game.numPets -= 1
            self.game.lives -= 1

            if self.game.numPets < 1:
                # game over
                self.game.game_over()
            
            image = pygame.image.load("images/deadLive.png").convert_alpha()
            if self.game.lives == 3:
                self.game.live4.set_image(image)
            elif self.game.lives == 2:
                self.game.live3.set_image(image)
            elif self.game.lives == 1:
                self.game.live2.set_image(image)
            elif self.game.lives == 0:
                self.game.live1.set_image(image)
            elif self.game.lives < 0:
                # game over
                self.game.game_over()
                
            # destroy pet
            self.destroy()
            
    def walk(self):
        """Walk around aimlessly"""
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
            if self.angle == 270:
                self.angle = 90
            elif self.angle == 90:
                self.angle = 270
            # about 90 px is the log at the top
        if self.bottom > games.screen.height - 40 or self.top < 90:
            self.dy = -self.dy
            
            if self.angle == 0:
                self.angle = 180
            elif self.angle == 180:
                self.angle = 0

        # Random number to determine when to change direction
        randNum = random.randint(1,200)
        stopped = 0
        if randNum == 1:
            self.dy = 0
            self.dx = 0
            stopped = 1

        if stopped:
            direction = random.randint(1,4)
            if direction == 1: # move up
                self.angle = 180
                self.dy = self.speed * -1
                stopped = 0
            elif direction == 2: # move right
                self.angle = 270
                self.dx = self.speed
                stopped = 0
            elif direction == 3: # move down
                self.angle = 0
                self.dy = self.speed
                stopped = 0
            elif direction == 4: # move left
                self.angle = 90
                self.dx = self.speed * -1
                stopped = 0

    def check_collide(self):
        """ Check for collision with burger. """
        for sprite in self.overlapping_sprites:
            size = sprite.handle_collide()

            # eat food
            if size:
                if size == 1:
                    self.hunger += 10
                elif size == 2:
                    self.hunger += 20
                elif size == 3:
                    self.hunger += 30
                    
                if self.hunger > 100:
                    self.hunger = 100
                self.hasToPoop = 1

    def click(self):
        #does nothing on click
        return 0

    def handle_collide(self):
        #return false (cannot eat a pet)
        return 0

    def getHunger(self):
        """ returns pet hunger """
        return self.hunger

class Bert(Pet):
    """ Bert pet """
    image = pygame.image.load("images/bert.png").convert_alpha()

    def __init__(self, game, x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize object """
        super(Bert, self).__init__(image = Bert.image,
                        x = x, y = y,
                        dy = Bert.speed)
        self.hunger = hunger
        self.decrement = 3 # amount to remove from hunger every tick
        self.tickCount = 0
        self.hasToPoop = hasToPoop
        self.game = game
        self.game.numPets += 1

    def poop(self):
        """ If pet has to poop, then poop. (Poop = coin)"""
        if self.hasToPoop == 1:
            # If random number equals 1 then poop (drop coin)
            randNum = random.randint(1,600)
            if randNum == 1:
               self.hasToPoop = 0
               new_coin = BronzeCoin(game = self.game, x = self.x, y = self.y)
               games.screen.add(new_coin)
               self.elevate()

class Kasha(Pet):
    """ Kasha pet """
    image = pygame.image.load("images/kasha.png").convert_alpha()

    def __init__(self, game, x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize object """
        super(Kasha, self).__init__(image = Kasha.image,
                        x = x, y = y,
                        dy = Kasha.speed)
        self.hunger = hunger
        self.decrement = 2.5
        self.tickCount = 0
        self.hasToPoop = hasToPoop
        self.game = game
        self.game.numPets += 1

    def poop(self):
        if self.hasToPoop == 1:
            randNum = random.randint(1,600)
            if randNum == 1:
               self.hasToPoop = 0
               new_coin = SilverCoin(game = self.game, x = self.x, y = self.y)
               games.screen.add(new_coin)
               self.elevate()
               
class Pentalope(Pet):
    """ Pentalope pet """
    image = pygame.image.load("images/pentalope.png").convert_alpha()

    def __init__(self, game, x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize object """
        super(Pentalope, self).__init__(image = Pentalope.image,
                        x = x, y = y,
                        dy = Pentalope.speed)
        self.hunger = hunger
        self.decrement = 2
        self.tickCount = 0
        self.hasToPoop = hasToPoop
        self.game = game
        self.game.numPets += 1

    def poop(self):
        if self.hasToPoop == 1:
            randNum = random.randint(1,600)
            if randNum == 1:
               self.hasToPoop = 0
               new_coin = GoldCoin(game = self.game, x = self.x, y = self.y)
               games.screen.add(new_coin)
               self.elevate()

class Garlyn(Pet):
    """ Garlyn pet """
    image = pygame.image.load("images/garlyn.png").convert_alpha()

    def __init__(self, game, x = 400, y = 300, hunger = 100, hasToPoop = 0):
        """ Intialize a Garlyn object """
        super(Garlyn, self).__init__(image = Garlyn.image,
                        x = x, y = y,
                        dy = Garlyn.speed)
        self.hunger = hunger
        self.decrement = 1
        self.tickCount = 0
        self.hasToPoop = hasToPoop
        self.game = game
        self.game.numPets += 1

    def poop(self):
        if self.hasToPoop == 1:
            randNum = random.randint(1,600)
            if randNum == 1:
               self.hasToPoop = 0
               new_coin = Diamond(game = self.game, x = self.x, y = self.y)
               games.screen.add(new_coin)
               self.elevate()
 
class Player(games.Sprite):
    """ hand image controlled by mouse """
    image = pygame.image.load("images/hand.png").convert_alpha()
    
    def __init__(self, game, x = games.mouse.x, y = games.mouse.y):
        """Intilize player object"""
        super(Player, self).__init__(image = Player.image,
                          x = x, y = y)
        self.game = game

    def handle_collide(self):
        #return false (cannot eat the hand)
        return 0

    def update(self):
        """ move to mouse coordinates, and handle events """ 
        self.x = games.mouse.x
        self.y = games.mouse.y

        # assume the player is droping a burger,
        # until they click money. If they click money
        # the burger flag is changed to false
        burgerFlag = 1
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.quit()
            elif event.type == MOUSEBUTTONDOWN and self.game.lives >= 0:
            
                for sprite in self.overlapping_sprites:
                    click = sprite.click()
                    if click:
                        burgerFlag = 0
                
            if event.type == MOUSEBUTTONDOWN and burgerFlag and self.game.lives >= 0:
                if event.button == 1:
                    if self.y > 90 \
                       and self.y < games.screen.height - 60 \
                       and self.game.money >= 25:
                        self.game.updateMoney(amount = -25)
                        if self.game.burgerSize == 1:
                            new_burger = SmallBurger(game = self.game, x = self.x, y = self.y)
                        elif self.game.burgerSize == 2:
                            new_burger = MediumBurger(game = self.game, x = self.x, y = self.y)
                        elif self.game.burgerSize == 3:
                            new_burger = LargeBurger(game = self.game, x = self.x, y = self.y)
                        games.screen.add(new_burger)
        self.elevate()


class Burger(games.Sprite):
    """ burger class """
    def update(self):
        if self.game.lives < 0:
            self.destroy()

    def handle_collide(self):
        self.destroy()
        return self.size

    def click(self):
        #does nothing on click
        return 0

class SmallBurger(Burger):
    """ Small burger, feeds pet 10%"""
    image = pygame.image.load("images/burger.png").convert_alpha()
    def __init__(self, game, x = games.mouse.x, y = games.mouse.y, size = 1):
        """ Intialize a Burger object """
        super(SmallBurger, self).__init__(image = SmallBurger.image, x = x, y = y)
        self.size = size
        self.game = game
        if not self.game.muted:
            self.game.burgerSound.play()

class MediumBurger(Burger):
    """ Medium burger, feeds pet 20%"""
    image = pygame.image.load("images/burger2.png").convert_alpha()
    def __init__(self, game, x = games.mouse.x, y = games.mouse.y, size = 1):
        """ Intialize a Burger object """
        super(MediumBurger, self).__init__(image = MediumBurger.image, x = x, y = y)
        self.size = size
        self.game = game
        if not self.game.muted:
            self.game.burgerSound.play()

class LargeBurger(Burger):
    """ Large burger, feeds pet 30%"""
    image = pygame.image.load("images/burger3.png").convert_alpha()
    def __init__(self, game, x = games.mouse.x, y = games.mouse.y, size = 1):
        """ Intialize a Burger object """
        super(LargeBurger, self).__init__(image = LargeBurger.image, x = x, y = y)
        self.size = size
        self.game = game
        if not self.game.muted:
            self.game.burgerSound.play()

class BronzeCoin(games.Sprite):
    """ Bronze coin, worth 100 """
    image = pygame.image.load("images/coin1.png").convert_alpha()
    def __init__(self, game, x = 0, y = 0, value = 100):
        """ Intialize a coin object """
        super(BronzeCoin, self).__init__(image = BronzeCoin.image, x = x, y = y)
        self.value = value
        self.game = game
        
    def update(self):
        if self.game.lives < 0:
            self.destroy()

    def handle_collide(self):
        #return false (cannot eat coins)
        return 0

    def click(self):
        if not self.game.muted:
            self.game.coinSound.play()
        self.game.updateMoney(amount = self.value)
        self.destroy()
        return 1

class SilverCoin(games.Sprite):
    """ Silver coin, worth 200"""
    image = pygame.image.load("images/coin2.png").convert_alpha()
    def __init__(self, game, x = 0, y = 0, value = 200):
        """ Intialize a coin object """
        super(SilverCoin, self).__init__(image = SilverCoin.image, x = x, y = y)
        self.value = value
        self.game = game

    def update(self):
        if self.game.lives < 0:
            self.destroy()

    def handle_collide(self):
        #return false (cannot eat coins)
        return 0

    def click(self):
        if not self.game.muted:
            self.game.coinSound.play()
        self.game.updateMoney(amount = self.value)
        self.destroy()
        return 1

class GoldCoin(games.Sprite):
    """ Gold coin, worth 500"""
    image = pygame.image.load("images/coin3.png").convert_alpha()
    def __init__(self, game, x = 0, y = 0, value = 500):
        """ Intialize a coin object """
        super(GoldCoin, self).__init__(image = GoldCoin.image, x = x, y = y)
        self.value = value
        self.game = game

    def update(self):
        if self.game.lives < 0:
            self.destroy()

    def handle_collide(self):
        #return false (cannot eat coins)
        return 0

    def click(self):
        if not self.game.muted:
            self.game.coinSound.play()
        self.game.updateMoney(amount = self.value)
        self.destroy()
        return 1

class Diamond(games.Sprite):
    """ Diamond, worth 1000 """
    image = pygame.image.load("images/diamond.png").convert_alpha()
    def __init__(self, game, x = 0, y = 0, value = 1000):
        """ Intialize a diamond object """
        super(Diamond, self).__init__(image = Diamond.image, x = x, y = y)
        self.value = value
        self.game = game
        
    def update(self):
        if self.game.lives < 0:
            self.destroy()
            
    def handle_collide(self):
        #return false (cannot eat diamonds)
        return 0

    def click(self):
        if not self.game.muted:
            self.game.coinSound.play()
        self.game.updateMoney(amount = self.value)
        self.destroy()
        return 1

class QuitBtn(games.Sprite):
    """ Goes back to main menu """
    image = pygame.image.load("images/quitBtn.png").convert_alpha()
    def __init__(self, game, x = games.screen.width - 50, y = games.screen.height - 20):
        """ Intialize object """
        super(QuitBtn, self).__init__(image = QuitBtn.image, x = x, y = y)

        self.game = game
        
    def click(self):
        restart()
        return 0

    def handle_collide(self):
        #return false (cannot eat quit btn)
        return 0

class MuteBtn(games.Sprite):
    """ Kills all sound"""
    image = pygame.image.load("images/audio.png").convert_alpha()
    def __init__(self, game, x = 30, y = games.screen.height - 30):
        """ Intialize object """
        super(MuteBtn, self).__init__(image = MuteBtn.image, x = x, y = y)

        self.game = game
        
    def click(self):
        if self.game.muted:
            self.game.unmute()
            image = pygame.image.load("images/audio.png").convert_alpha()
            self.set_image(image)
        else:
            self.game.mute()
            image = pygame.image.load("images/noAudio.png").convert_alpha()
            self.set_image(image)
        return 0

    def handle_collide(self):
        #return false (cannot eat mute btn)
        return 0

class BertBtn(games.Sprite):
    """ Creates new bert object and takes 100 coins"""
    def __init__(self, game, image = pygame.image.load("images/BertBtn_gray.png").convert_alpha(), disabled = 1, x = 260, y = 46):
        """ Intialize object """
        super(BertBtn, self).__init__(image = image, x = x, y = y)
        self.game = game
        self.price = 100

        self.disabled = disabled

    def update(self):
        if self.disabled:
            if self.game.money >= self.price:
                new_image = pygame.image.load("images/BertBtn.png").convert_alpha()
                self.set_image(new_image)
                self.disabled = 0
                self.game.level_up()
        
    def click(self):
        if not self.disabled:
            if self.game.money >= self.price:
                #create new pet (start in random place away from edges)
                new_pet = Bert(game = self.game,
                               x = random.randint(150,games.screen.width - 100),
                               y = random.randint(150,games.screen.height - 150))
                games.screen.add(new_pet)
                self.game.updateMoney(amount = -self.price)
                if not self.game.muted:
                    self.game.purchaseSound.play()
            else:
                if not self.game.muted:
                    self.game.errorSound.play()
        else:
            if not self.game.muted:
                self.game.errorSound.play()
        return 1

    def handle_collide(self):
        #return false (cannot eat btn)
        return 0
        
class KashaBtn(games.Sprite):
    """ Creates new kasha object and takes 200 coins"""
    def __init__(self, game, image = pygame.image.load("images/KashaBtn_gray.png").convert_alpha(), disabled = 1, x = 315, y = 46):
        """ Intialize object """
        super(KashaBtn, self).__init__(image = image, x = x, y = y)
        self.game = game
        self.price = 200

        self.disabled = disabled
        
    def update(self):
        if self.disabled:
            if self.game.money >= self.price:
                new_image = pygame.image.load("images/KashaBtn.png").convert_alpha()
                self.set_image(new_image)
                self.disabled = 0
                self.game.level_up()

        
    def click(self):
        if not self.disabled:
            if self.game.money >= self.price:
                #create new pet (start in random place away from edges)
                new_pet = Kasha(game = self.game,
                               x = random.randint(150,games.screen.width - 100),
                               y = random.randint(150,games.screen.height - 150))
                games.screen.add(new_pet)
                self.game.updateMoney(amount = -self.price)
                if not self.game.muted:
                    self.game.purchaseSound.play()
            else:
                if not self.game.muted:
                    self.game.errorSound.play()
        else:
            if not self.game.muted:
                self.game.errorSound.play()
        return 1

    def handle_collide(self):
        #return false (cannot eat btn)
        return 0
        
class PentalopeBtn(games.Sprite):
    """ Creates new pentelope object and takes 500 coins"""
    def __init__(self, game, image = pygame.image.load("images/PentalopeBtn_gray.png").convert_alpha(), disabled = 1, x = 370, y = 46):
        """ Intialize object """
        super(PentalopeBtn, self).__init__(image = image, x = x, y = y)
        self.game = game
        self.price = 500

        self.disabled = disabled
        

    def update(self):
        if self.disabled:
            if self.game.money >= self.price:
                new_image = pygame.image.load("images/PentalopeBtn.png").convert_alpha()
                self.set_image(new_image)
                self.disabled = 0
                self.game.level_up()
            
    def click(self):
        if not self.disabled:
            if self.game.money >= self.price:
                #create new pet (start in random place away from edges)
                new_pet = Pentalope(game = self.game,
                               x = random.randint(150,games.screen.width - 100),
                               y = random.randint(150,games.screen.height - 150))
                games.screen.add(new_pet)
                self.game.updateMoney(amount = -self.price)
                if not self.game.muted:
                    self.game.purchaseSound.play()
            else:
                if not self.game.muted:
                    self.game.errorSound.play()
        else:
            if not self.game.muted:
                self.game.errorSound.play()
        return 1

    def handle_collide(self):
        #return false (cannot eat btn)
        return 0
    
class GarlynBtn(games.Sprite):
    """ Creates new Garlyn object and takes 1000 coins"""
    def __init__(self, game, image = pygame.image.load("images/GarlynBtn_gray.png").convert_alpha(), disabled = 1, x = 425, y = 46):
        """ Intialize a Garlyn object """
        super(GarlynBtn, self).__init__(image = image, x = x, y = y)
        self.game = game
        self.price = 1000

        self.disabled = disabled

        
    def update(self):
        if self.disabled:
            if self.game.money >= self.price:
                new_image = pygame.image.load("images/GarlynBtn.png").convert_alpha()
                self.set_image(new_image)
                self.disabled = 0
                self.game.level_up()
        
    def click(self):
        if not self.disabled:
            if self.game.money >= self.price:
                #create new pet (start in random place away from edges)
                new_pet = Garlyn(game = self.game,
                               x = random.randint(150,games.screen.width - 100),
                               y = random.randint(150,games.screen.height - 150))
                games.screen.add(new_pet)
                self.game.updateMoney(amount = -self.price)
                if not self.game.muted:
                    self.game.purchaseSound.play()
            else:
                if not self.game.muted:
                    self.game.errorSound.play()
        else:
            if not self.game.muted:
                self.game.errorSound.play()
        return 1

    def handle_collide(self):
        #return false (cannot eat btn)
        return 0


class BurgerBtn(games.Sprite):
    """ Upgrades burger size, 1st costs 100, 2nd costs 200"""
    def __init__(self, game, image = pygame.image.load("images/burgerBtn.png").convert_alpha(), x = 525, y = 46):
        """ Intialize object """
        super(BurgerBtn, self).__init__(image = image, x = x, y = y)
        self.game = game
        self.price = 100

        
    def update(self):
        if self.game.burgerSize == 2:
            new_image = pygame.image.load("images/burgerBtn2.png").convert_alpha()
            self.set_image(new_image)
            self.price = 200
        elif self.game.burgerSize == 3:
                self.destroy()
        
    def click(self):
        if self.game.money >= self.price:
            # upgrade burger
            self.game.burgerSize += 1
            self.game.updateMoney(amount = -self.price)
            if not self.game.muted:
                self.game.purchaseSound.play()
        else:
            if not self.game.muted:
                self.game.errorSound.play()
        return 1

    def handle_collide(self):
        #return false (cannot eat btn)
        return 0

class TopCoin(games.Sprite):
    """ Gold coin icon at the top of the screen"""
    image = pygame.image.load("images/topCoin.png").convert_alpha()
    def __init__(self, x = games.screen.width - 35, y = 35):
        """ Intialize object """
        super(TopCoin, self).__init__(image = TopCoin.image, x = x, y = y)
        
    def click(self):
        # does nothing
        return 0

    def handle_collide(self):
        #return false (cannot eat)
        return 0

class LiveIcon(games.Sprite):
    """ Live icons at the top of the screen"""
    image = pygame.image.load("images/live.png").convert_alpha()
    def __init__(self, game, x = 30, y = 45):
        """ Intialize object """
        super(LiveIcon, self).__init__(image = LiveIcon.image, x = x, y = y)
        self.game = game
        
    def click(self):
        # does nothing
        return 0

    def handle_collide(self):
        #return false (cannot eat)
        return 0

class Game(object):
    """ The game its self. """
    def __init__(self):
        """ Initialize Game object. """
        self.create_menu()
        games.mouse.is_visible = True

    def create_menu(self):
        # create menu
        self.main_menu = Menu(game = self)
        games.screen.add(self.main_menu)

        # create play button
        self.playBtn = PlayBtn(game = self)
        games.screen.add(self.playBtn)

        # create instructions button
        self.instructionsBtn = InstructionBtn(game = self)
        games.screen.add(self.instructionsBtn)
        
    def add_instructions(self):
        # destroy existing objects
        self.playBtn.destroy()
        self.instructionsBtn.destroy()
        self.main_menu.destroy()
        
        # create page
        self.instructions = Instructions(game = self)
        games.screen.add(self.instructions)

        # create back button
        self.backBtn = BackBtn(game = self)
        games.screen.add(self.backBtn)

    def rem_instructions(self):
        # destroy instructions
        self.instructions.destroy()
        self.backBtn.destroy()
        self.create_menu()

    def play(self):
        """ Start Game """
        # destroy menu
        self.playBtn.destroy()
        self.instructionsBtn.destroy()
        self.main_menu.destroy()
        # muted?
        self.muted = 0

        # load sounds
        self.coinSound = games.load_sound("sounds/coin.wav")
        self.purchaseSound = games.load_sound("sounds/ChaChing.wav")
        self.errorSound = games.load_sound("sounds/button.wav")
        self.burgerSound = games.load_sound("sounds/plop.wav")
        self.burgerSound.set_volume(0.7)

        # load & play music
        games.music.load("sounds/TropicalMusic.wav")
        pygame.mixer.music.set_volume(0.7)
        games.music.play(-1)
        
        # set money
        self.money = 50

        # set lives
        self.lives = 4

        # set number of pets
        self.numPets = 0

        # burger size
        self.burgerSize = 1

        # create live icons
        self.live1 = LiveIcon(game = self)
        games.screen.add(self.live1)
        
        self.live2 = LiveIcon(game = self, x = 80)
        games.screen.add(self.live2)
        
        self.live3 = LiveIcon(game = self, x = 125)
        games.screen.add(self.live3)
        
        self.live4 = LiveIcon(game = self, x = 170)
        games.screen.add(self.live4)
        
        # create quit btn
        quitBtn = QuitBtn(game = self)
        games.screen.add(quitBtn)

        # mute button
        muteBtn = MuteBtn(game = self)
        games.screen.add(muteBtn)

        # create top coin (to represent score)
        tCoin = TopCoin()
        games.screen.add(tCoin)

        # create money display
        self.moneyDisplay = games.Text(value = self.money,
                                    size = 40,
                                    color = color.white,
                                    top = 20,
                                    right = games.screen.width - 70,
                                    is_collideable = False)
        
        games.screen.add(self.moneyDisplay)

        # create bert btn
        bertBtn = BertBtn(game = self)
        games.screen.add(bertBtn)

        # create kasha btn
        kashaBtn = KashaBtn(game = self)
        games.screen.add(kashaBtn)
        
        # create pentalope btn
        pentalopeBtn = PentalopeBtn(game = self)
        games.screen.add(pentalopeBtn)
        
        # create garlyn btn
        garlynBtn = GarlynBtn(game = self)
        games.screen.add(garlynBtn)

        # create burger btn
        burgerBtn = BurgerBtn(game = self)
        games.screen.add(burgerBtn)

        # create first pet
        pet1 = Bert(game = self)
        games.screen.add(pet1)

        # create second pet (start in random place away from edges)
        pet2 = Bert(game = self, x = random.randint(200,games.screen.width - 150),
                    y = random.randint(200,games.screen.height - 150))
        games.screen.add(pet2)

        # create player
        self.the_player = Player(game = self)
        games.screen.add(self.the_player)
        games.mouse.is_visible = False

    def load(self):
        # load and set background
        backgroundImage = games.load_image("images/background.png", transparent = False)
        games.screen.background = backgroundImage

        # start play
        games.screen.mainloop()

    def mute(self):
        games.music.stop()
        self.muted = 1

    def unmute(self):
        games.music.load("sounds/TropicalMusic.wav")
        games.music.play(-1)
        self.muted = 0
        
    def updateMoney(self, amount = 0):
        self.money += amount
        self.moneyDisplay.value += amount
        self.moneyDisplay.right = games.screen.width - 70

    def game_over(self):
        """ Game ends, kill objects, prevent clicking, redirect to menu"""
        games.music.stop()
        self.lives = - 1
        # show message for 15 seconds
        self.message = "Game Over"
        end_message = games.Message(value = self.message,
                                    size = 90,
                                    color = color.white,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 15 * games.screen.fps,
                                    after_death = restart,
                                    is_collideable = False)
        games.screen.add(end_message)

        # load and play sound
        if not self.muted:
            gameOverSound = games.load_sound("sounds/gameover.wav")
            gameOverSound.play()

    def level_up(self):
        """ Displays "Level Up!" """
        lvl_message = games.Message(value = "Level Up!",
                                    size = 50,
                                    color = color.white,
                                    x = games.screen.width/2,
                                    y = games.screen.height/4,
                                    lifetime = 5 * games.screen.fps,
                                    is_collideable = False)
        games.screen.add(lvl_message)

def restart():
    """ Restart game """
    games.music.stop()
    objects = games.screen.get_all_objects()
    for object in objects:
        object.destroy()

    main()

def main():
    # The main functions starts everything
    the_game = Game()
    the_game.load()

# Call Main
main()
