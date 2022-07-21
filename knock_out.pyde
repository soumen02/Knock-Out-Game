#importing sound time, random, os and math
#CAUTION! the game sound might be loud so please lower the volume!
add_library('minim') 
import os, random, time, math
path = os.getcwd()
minim = Minim(this)

#setting window size               
WIDTH = 1400
HEIGHT = 720

#flag to move to next stages and restart game
stage = 0
gamestart = False  

#each player has 5 lives, 4 grenades has a shieldActive to check if shield is active
class Player: 
    def __init__(self, x, y, r, g, dir, name, img_name, img_w, img_h, num_frames):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        self.key_handler = {"left":False, "right":False, UP: False, DOWN: False} 
        self.dir = dir
        self.lives = 5
        self.name = name
        self.dead = False
        self.grenades = 4
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.num_frames = num_frames
        self.frame = 0
        self.shield = False
        self.shieldActive = False
        self.shieldeat = False    
        self.grenadehit = False #checks if it is in contact with grenade explosion
        self.shieldLast =  4
        
    #displays image based on the direction it is facing    
    def display(self):
        self.update()
        if self.dir == "right":
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2,self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == "left":
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
        
        #if shield is eatan, it actives a Timer class. It also sets shield active to True
        if self.shieldeat:
            self.shielddelay = Timer()
            self.shieldActive = True
            self.shieldeat = False
            
        #when shield is eaten, it triggers this to be True and starts running the Timer. The shield active is set to False after 4 seconds (self.shieldLast = 4)
        if self.shieldActive:   
            self.shielddelay.run()
            if self.shielddelay.counter < self.shieldLast:
                self.displayShield()
            elif self.shielddelay.counter >= self.shieldLast:
                self.shieldActive = False
          
    
    def gravitynfriction(self):
        #this acts as gravity 
        if self.y + self.r >= self.g and self.grenadehit == False:
            self.vy = 0
        else:
            self.vy += 0.7
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
        #sets the ground to the platform if the player's y position is above the platform and between the platforms x positions
        for p in game.platforms:
            if self.y + self.r <= p.y and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w and self.key_handler[DOWN] != True:
                self.g = p.y
                break
            else:
                self.g = game.g
                
        #if the player touches the lava platform, the player is dead        
        for p in game.lava_platform:
            if p.y <= self.y + self.r <= p.y + p.h and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w:
                if self.shieldActive != True:
                    self.dead = True
                    self.respawn()
            elif p.y <= self.y - self.r <= p.y + p.h and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w:
                if self.shieldActive != True:
                    self.dead = True
                    self.respawn()
         #if the player reaches the ground, the player is dead and respawns       
        if self.y + self.r == game.g:
            self.dead = True
            self.respawn()

            
            
        if self.vx == 0:
            self.vx = 0 
            return
        
         #this acts as friction so the player's movements are smoother       
        elif self.vx > 0 :
            self.vx += -0.05 * self.vx
            return

        elif self.vx < 0 :
            self.vx += 0.05 * -self.vx
            return
        
        
    #calls the gravity and fricition function
    def update(self):
        self.gravitynfriction()
        #displays the player's image according the the frame
        if frameCount%5 == 0 and self.vx != 0 and self.vy < 1 and self.key_handler["right"] == True:
            self.frame = (self.frame + 1) % self.num_frames
        if frameCount%5 == 0 and self.vx != 0 and self.vy < 1 and self.key_handler["left"] == True:
            self.frame = (self.frame + 1) % self.num_frames
            
        #Allows double jump
        if self.y + self.r == self.g:
            self.isGrounded = True
            self.can_double_jump = True 
        else:
            self.isGrounded = False
        if self.key_handler[UP] == True:
            if self.isGrounded == True:
                self.vy = -12
                self.key_handler[UP] = False
            else:
                if self.can_double_jump == True:
                    self.vy = -12
                    self.can_double_jump = False
                 
        #moves left and right
        if self.key_handler["left"] == True and self.vx > -7:
            self.vx += - 1
            self.dir = "left"
        elif self.key_handler["right"] == True and self.vx < +7:
            self.vx += 1
            self.dir = "right"
            
        #updates x position
        self.x += self.vx
        self.y += self.vy
        
    #respawns the player according the the assigned coordinates, lives decrease by 1 and the gun is reset to the basic gun (pistol)
    def respawn(self):
        if self.name == "player1" : 
            self.x = 1100
            self.y = 100
            game.gun1 = Weapons("gun1")
            self.lives -= 1
            
        elif self.name == "player2" : 
            self.x = 300
            self.y = 100
            game.gun2 = Weapons("gun2")
            self.lives -= 1
        self.vx = 0 
    
    #displays sheild and decreases the size and lightens the color of shield as time increases.
    def displayShield(self):
        noFill()
        stroke(153+self.shielddelay.counter*30,51+self.shielddelay.counter*50,255+self.shielddelay.counter*0)
        strokeWeight(6-self.shielddelay.counter)
        ellipse(self.x, self.y, 100-self.shielddelay.counter*15, 100-self.shielddelay.counter*15)

#platform class, takes in x,y, width and height coordiantes with images and is called in the game.display                
class Platform:
    def __init__(self, x, y, w, h, img): #, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/" + img)
    
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)

#lava class, similar to the platform class is called in the game.display    
class Lava:
    def __init__(self, x, y, w, h, img): #, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/" + img)
    
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)

#bullet has rof, power, dir properties
class Bullet():
    def __init__(self, x, y, rof, power, dir, weapon, img_name, img_w, img_h):
        self.x = x
        self.y = y
        self.power = power
        self.dir = dir
        self.weapon = weapon
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        
        self.vx = 20
        
    def update(self):
        if self.dir == "right":
            self.x += self.vx
        if self.dir == "left":
            self.x -= self.vx
    
    def display(self):
        stroke(0, 255, 0)
        strokeWeight(5)
        fill(0, 255, 0)
        image(self.img, self.x - self.img_w//2 + 20, self.y - self.img_h//2 -5 ,self.img_w, self.img_h)
        # ellipse(self.x, self.y, 5, 5)
        
            
        self.update()
    
    # Bullets cancel when they collide with each other
    def checkbullethit(self):
        
        if ((game.player1.x - self.x)**2 + (game.player1.y - self.y)**2) ** 0.5 <= game.player1.r and self.weapon == "gun2":
            return True
            
        if ((game.player2.x - self.x)**2 + (game.player2.y - self.y)**2) ** 0.5 <= game.player2.r and self.weapon == "gun1":
            return True 

        
        
        
class Weapons():
    def __init__(self, weapon, img_name = "pistol.png"):
    #     self.x = x
    #     self.y = y
        self.attack = {"shoot":False, "throw": False}
        self.bullet_list = []
        self.weapon = weapon
        self.img_name = img_name
        self.bulletcounter = 0
        
        # Weapon properties for each gun, (rof = rate of fire)
        if self.img_name == "pistol.png":
            self.img = loadImage(path + "/images/" + img_name)
            self.img_w = 40
            self.img_h = 23
            self.power = 30
            self.rof = 9
            self.ammo = -1
            self.sound = minim.loadFile(path + "/sounds/" + "pistol.mp3")
        elif self.img_name == "sniper.png":
            self.img = loadImage(path + "/images/" + img_name)
            self.img_w = 100
            self.img_h = 35
            self.power = 56
            self.rof = 25
            self.ammo = 10
            self.sound = minim.loadFile(path + "/sounds/" + "sniper.mp3")
        elif self.img_name == "assaultr.png":
            self.img = loadImage(path + "/images/" + img_name)
            self.img_w = 60
            self.img_h = 28
            self.power = 9
            self.rof = 3
            self.ammo = 100
            self.sound = minim.loadFile(path + "/sounds/" + "assultr.mp3")
        
        
    def display(self, x, y, dir):
        stroke(0, 0, 0)
        strokeWeight(5)
        noFill()
        if self.img_name == "pistol.png":
            if dir == "right":
                image(self.img, x - self.img_w//2 + 20, y - self.img_h//2 -2 ,self.img_w, self.img_h)
                # rect(x+15, y-5, 30, 1)
            elif dir == "left":
                image(self.img, x - self.img_w//2 - 20 , y - self.img_h//2 -2 ,self.img_w, self.img_h, 512, 0, 0, 257)            
                # rect(x-30-15, y-5, 30, 1)
        elif self.img_name == "sniper.png":
            if dir == "right":
                image(self.img, x - self.img_w//2 + 20, y - self.img_h//2 -7 ,self.img_w, self.img_h)
                # rect(x+15, y-5, 30, 1)
            elif dir == "left":
                image(self.img, x - self.img_w//2 - 20 , y - self.img_h//2 -7 ,self.img_w, self.img_h, 333, 0, 0, 93)            
                # rect(x-30-15, y-5, 30, 1)
        elif self.img_name == "assaultr.png":
            if dir == "right":
                image(self.img, x - self.img_w//2 + 20, y - self.img_h//2 -4 ,self.img_w, self.img_h)
                # rect(x+15, y-5, 30, 1)
            elif dir == "left":
                image(self.img, x - self.img_w//2 - 20 , y - self.img_h//2 -4 ,self.img_w, self.img_h, 394, 0, 0, 183)            
                # rect(x-30-15, y-5, 30, 1)


            
      # Bullets appended to a list when created
        if self.attack["shoot"] == True and ( frameCount % self.rof == 0 or len(self.bullet_list) == 0):
            self.sound.play()
            self.sound.rewind()
            if dir == "right":
                self.bullet_list.append(Bullet(x+15, y-6, 1, self.power, dir, self.weapon, "bullet.png", 11, 4))
            if dir == "left":
                self.bullet_list.append(Bullet(x-30-15, y-6, 1, self.power, dir, self.weapon, "bullet.png", 11, 4))
                
            self.bulletcounter+=1
            
        if self.bulletcounter == self.ammo :
            if self.weapon == "gun1":
                game.gun1 = Weapons("gun1") 
            if self.weapon == "gun2":
                game.gun2 = Weapons("gun2") 

       # Bullets removed from the list when they leave the coundary of the window (saves memory and makes game faster) 
        for t in self.bullet_list:
            if t.x < 0 or t.x > WIDTH:
                self.bullet_list.remove(t)
       
                 
        if self.attack["throw"] == True and self.weapon == "gun1" and frameCount%7 == 0 :
            try:
                game.player1grenades.pop()
                game.grenade_list.append(Grenade(x+15, y-5, dir, "grenade.png", 20, 20))
                game.player1.grenades -= 1
            except: pass
            
            
        if self.attack["throw"] == True and self.weapon == "gun2" and frameCount%7 == 0:
            try:
                game.player2grenades.pop() 
                game.grenade_list.append(Grenade(x+15, y-5, dir, "grenade.png", 20, 20))
                game.player2.grenades -= 1
            except : pass

#displays the hearts, grenades and ammo shows inf for infinte ammo        
class HUD():
    def __init__(self, x, y, name, img):
        self.lives = 5
        self.x = x
        self.y = y
        self.name = name
        self.w = 20
        self.h = 20
        self.img = loadImage(path + "/images/" + img)
    
    def display(self):
        noStroke()
        if self.name == "life":
            image(self.img, self.x, self.y, self.w, self.h)
        if self.name == "grenade":
            image(self.img, self.x, self.y, self.w, self.h)
            
        #Ammo counter display
        fill(255, 255, 255)
        textSize(15)
        ammodisp2 = game.gun2.ammo - game.gun2.bulletcounter
        if ammodisp2 <= -1:
            ammodisp2 = "inf"
        text(str(ammodisp2), 50, 115)

        
        ammodisp1 = game.gun1.ammo - game.gun1.bulletcounter
        if ammodisp1 <= -1:
            ammodisp1 = "inf"
        text(str(ammodisp1), 1350, 115)
    
        


# Grenade class for throwing of grenades
class Grenade():
    def __init__(self, x, y, dir, img_name, img_w, img_h):
        self.x = x
        self.y = y
        self.dir = dir
        self.blastr = 100
        self.grcounter = 0
        self.vx = 0
        self.vy = -10
        self.r = 10/2
        self.g = game.g
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.knockbackTotal = 30
        self.reductionRatio = 10
        self.grenadeSound = minim.loadFile(path + "/sounds/" + "grenade.mp3")
        
    def display(self):
        # stroke(0, 0, 0)
        # strokeWeight(5)
        # fill(0, 0, 0)
        # ellipse(self.x, self.y, 10, 6)
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2 -2 ,self.img_w, self.img_h)
        
        self.update()  
          
    # Blast animation for explostion of grenade
    def blastanimation(self):
        stroke(0+self.grcounter*2, 0+self.grcounter*2, 0+self.grcounter*2)
        strokeWeight(5)
        noFill()
        if self.grcounter < 100:
            ellipse(self.x, self.y, 10+self.grcounter, 6+self.grcounter)
            self.grcounter += 5
            return
        game.blast_list.remove(self)    
        
    def update(self):
        self.parabolic()
                
        
        #moves left and right
        if self.dir == "left":
            self.vx = -10
        elif self.dir == "right" :
            self.vx = 10
        # else:
        #     self.vx = 0
            
        self.x += self.vx
        self.y += self.vy
        
    # For the parabolic motion of the grenades        
    def parabolic(self):
        
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.7
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
        
        for p in game.platforms:
            if self.y + self.r <= p.y and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w :
                self.g = p.y
                break
            else:
                self.g = game.g
                
        if self.vx == 0:
            self.vx = 0 
            return
        elif self.dir == "right" :
            self.vx += -0.5 * self.vx 
            return

        elif self.dir == "left" :
            self.vx += 0.5 * self.vx
            return
     
    # explode knocksback the player when they are in the proximity of the grenade explosion     
    # Uses to calculate the angle based on the coordinates of the player and grenade 
    # Knockback direction depends on the angle and power depends on the direction
    def explode(self, x, y):        
            
        dist = ((game.player1.x - x)**2 + (game.player1.y - y)**2) ** 0.5
        if  dist <= self.blastr and game.player1.shieldActive != True:
            game.player1.grenadehit = True
            dir = math.atan2(game.player1.y - y, game.player1.x - x)
            game.player1.vy = ( self.knockbackTotal - dist/self.reductionRatio )  * math.sin(dir)
            game.player1.vx = ( self.knockbackTotal  - dist/self.reductionRatio ) * math.cos(dir)
            game.player1.grenadehit = False
            
        dist = ((game.player2.x - x)**2 + (game.player2.y - y)**2) ** 0.5
        if  dist <= self.blastr and game.player2.shieldActive != True:
            game.player2.grenadehit = True
            dir = math.atan2(game.player2.y - y, game.player2.x - x)
            game.player2.vy = ( self.knockbackTotal - dist/self.reductionRatio )  * math.sin(dir)
            game.player2.vx = ( self.knockbackTotal  - dist/self.reductionRatio ) * math.cos(dir)
            game.player2.grenadehit = False        
           
#takes platform as input so that it spawns randomly on the platform        
class Crate():
    def __init__(self, platforms, img, name):
        self.randomPlatform = 0
        self.randomXcoordinate = 0
        self.platforms = platforms
        self.randomPlatform = 0
        self.randomXcoordinate = 0
        self.randomYcoordinate = 0
        self.sizeofCrate = 40
        self.img = loadImage(path + "/images/" + img)
        self.name = name
        self.numCrate = 0
        self.rateofSpawn_crate = 25
        self.item = minim.loadFile(path + "/sounds/" + "item.mp3")
        
    #chooses a random platform
    def choosePlatform(self):
        self.randomPlatform = random.choice(self.platforms)
    #selects random x and y coordinates from the platform chosen
    def selectXandY(self):
        self.randomXcoordinate = random.randint(self.randomPlatform.x, (self.randomPlatform.x + self.randomPlatform.w)- self.sizeofCrate)
        self.randomYcoordinate = self.randomPlatform.y
    #generates the crate    
    def generateCrate(self):
        self.choosePlatform()
        self.selectXandY()
    
    #display the crate    
    def display(self):
        image(self.img, self.randomXcoordinate, self.randomYcoordinate - self.sizeofCrate, self.sizeofCrate, self.sizeofCrate)
        self.gameplayCrate()
        
    def gameplayCrate(self):
        #only generates one crate at a time according to the rate of spawn
        if game.tElapsed %  self.rateofSpawn_crate == 0 and self.numCrate == 0 and game.tElapsed != 0:
            self.numCrate = 1
            self.generateCrate()
        
        #when the player contacts the crate, it removes the crate, and generates a random weapon (sniper or assfultrifle)            
        if ((game.player1.x - self.randomXcoordinate)**2 + (game.player1.y - self.randomYcoordinate)**2) ** 0.5 <= game.player1.r + self.sizeofCrate and self.name == "crate":
            game.crate.pop()
            self.item.play()
            self.item.rewind()
            gunchoice = random.randint(1,2)
            if gunchoice == 1:
                game.gun1 = Weapons("gun1", "sniper.png") 
            elif gunchoice == 2:
                game.gun1 = Weapons("gun1", "assaultr.png")
            game.crate.append(Crate(game.platforms, "crate.png", "crate"))
            self.numCrate = 0
        
        #same code for player2
        if ((game.player2.x - self.randomXcoordinate)**2 + (game.player2.y - self.randomYcoordinate)**2) ** 0.5 <= game.player2.r + self.sizeofCrate and self.name == "crate":
            game.crate.pop()
            self.item.play()
            self.item.rewind()
            gunchoice = random.randint(1,2)
            if gunchoice == 1:
                game.gun2 = Weapons("gun2", "sniper.png") 
            elif gunchoice == 2:
                game.gun2 = Weapons("gun2", "assaultr.png")
            game.crate.append(Crate(game.platforms, "crate.png", "crate"))
            self.numCrate = 0

#acts similarly to crates class        
class BoosterItem():
    def __init__(self, platforms, img, name):
        self.randomPlatform = 0
        self.randomXcoordinate = 0
        self.platforms = platforms
        self.randomPlatform = 0
        self.randomXcoordinate = 0
        self.randomYcoordinate = 0
        self.sizeofItem = 40
        self.img = loadImage(path + "/images/" + img)
        self.name = name
        self.numHeart = 0
        self.numGrenade = 0
        self.counterGrenade = 0
        self.counterHeart = 0
        self.numShield = 0
        self.counter = 0
        self.rateofSpawn_heart = 30
        self.rateofSpawn_grenade = 10
        self.ratioofSpawn_shield = 20
        self.item = minim.loadFile(path + "/sounds/" + "item.mp3")
        
    #chooses a random platform
    def choosePlatform(self):
        self.randomPlatform = random.choice(self.platforms)
     
    #selects random x and y      
    def selectXandY(self):
        self.randomXcoordinate = random.randint(self.randomPlatform.x, (self.randomPlatform.x + self.randomPlatform.w)- self.sizeofItem)
        self.randomYcoordinate = self.randomPlatform.y
        
    def generateItem(self):
        self.choosePlatform()
        self.selectXandY()
    #displays different images for each item   
    def display(self):
        image(self.img, self.randomXcoordinate, self.randomYcoordinate - self.sizeofItem, self.sizeofItem, self.sizeofItem)
        if self.name == "heart":
            self.gameplayHeart()
        if self.name == "grenade":
            self.gameplayGrenade()
        if self.name == "shield":
            self.gameplayShield()
    
    #Acts the same as the creates class            
    def gameplayHeart(self):
        if game.tElapsed % self.rateofSpawn_heart == 0 and self.numHeart == 0 and game.tElapsed != 0:
            self.numHeart = 1
            self.generateItem()
            
        #when the player contacts heart item, it plays the sound live of player increases by 1                
        if ((game.player1.x - self.randomXcoordinate)**2 + (game.player1.y - self.randomYcoordinate)**2) ** 0.5 <= game.player1.r + self.sizeofItem and self.name == "heart":
            game.heart.pop()
            self.item.play()
            self.item.rewind()
            game.heart.append(BoosterItem(game.platforms, "heart.png", "heart"))
            self.numHeart = 0
            game.player1.lives += 1
            game.player1lives.append(HUD(1350 - (game.player1.lives - 1) * 20,50, "life", "heart.png"))
            print(game.player1.lives)
            
        #same for player2    
        if ((game.player2.x - self.randomXcoordinate)**2 + (game.player2.y - self.randomYcoordinate)**2) ** 0.5 <= game.player2.r + self.sizeofItem and self.name == "heart":
            game.heart.pop()
            self.item.play()
            self.item.rewind()
            game.heart.append(BoosterItem(game.platforms, "heart.png", "heart"))
            self.numHeart = 0
            game.player2.lives += 1
            game.player2lives.append(HUD(50 + (game.player2.lives - 1) *20,50, "life", "heart.png"))
    
    def gameplayGrenade(self):
        if game.tElapsed % self.rateofSpawn_grenade == 0 and self.numGrenade == 0 and game.tElapsed != 0:
            self.numGrenade = 1
            self.generateItem()
            
         #if player contacts grenade item, it gives player +1 grenade
        if ((game.player1.x - self.randomXcoordinate)**2 + (game.player1.y - self.randomYcoordinate)**2) ** 0.5 <= game.player1.r + self.sizeofItem and self.name == "grenade":
            game.grenade.pop()
            self.item.play()
            self.item.rewind()
            game.grenade.append(BoosterItem(game.platforms, "grenade.png", "grenade"))
            self.numGrenade = 0
            game.player1.grenades += 1
            game.player1grenades.append(HUD(1350 - (game.player1.grenades - 1 ) * 20, 75, "grenade", "grenade.png"))
       
            
        if ((game.player2.x - self.randomXcoordinate)**2 + (game.player2.y - self.randomYcoordinate)**2) ** 0.5 <= game.player2.r + self.sizeofItem and self.name == "grenade":
            game.grenade.pop()
            self.item.play()
            self.item.rewind()
            game.grenade.append(BoosterItem(game.platforms, "grenade.png", "grenade"))
            self.numGrenade = 0
            game.player2.grenades += 1
            game.player2grenades.append(HUD(50 + (game.player2.grenades - 1) * 20, 75, "grenade", "grenade.png"))
    
                    
    def gameplayShield(self):
        if game.tElapsed % self.ratioofSpawn_shield == 0 and self.numShield == 0 and game.tElapsed != 0:
            self.numShield = 1
            self.generateItem()
         
        #if player contacts the shield item turns shieldeat to True, which actives the shieldActive flag to True and makes player invincible  
        if ((game.player1.x - self.randomXcoordinate)**2 + (game.player1.y - self.randomYcoordinate)**2) ** 0.5 <= game.player1.r + self.sizeofItem and self.name == "shield":
            game.shield.pop()
            self.item.play()
            self.item.rewind()
            game.shield.append(BoosterItem(self.platforms, "shield.png", "shield"))
            self.numShield = 0
            game.player1.shieldeat = True
            
                
        if ((game.player2.x - self.randomXcoordinate)**2 + (game.player2.y - self.randomYcoordinate)**2) ** 0.5 <= game.player2.r + self.sizeofItem and self.name == "shield":
            game.shield.pop()
            self.item.play()
            self.item.rewind()
            game.shield.append(BoosterItem(self.platforms, "shield.png", "shield"))
            self.numShield = 0
            game.player2.shieldeat = True

#timer ticks counter every 60 frames (1sec)                
class Timer:
    def __init__(self):
        self.counter = 0
        
    def run(self):
        if frameCount % 60 == 0:   
            self.counter += 1  

# Game class for start of game 
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        
        #calls the player class
        self.player2 = Player(300, 100, 28, self.g, "right", "player2", "RedChar.png", 70, 60, 2)
        self.player1 = Player(1100, 100, 28, self.g, "left", "player1", "BlueChar.png", 70, 60, 2)
        self.gun1 = Weapons("gun1") # "pistol.png", 40, 23)
        self.gun2 = Weapons("gun2") # "pistol.png", 40, 23)
        self.grenade_list = []
        self.blast_list = []
        self.tElapsed = 0
        self.numCrate = 0
        self.numHeart = 0
        self.storePosition = []
        self.platforms = []
        
        #calls the platform class and appends it into a list
        self.platforms.append(Platform(175, 200, 250, 30, "platform.png"))
        self.platforms.append(Platform(975, 200, 250, 30, "platform.png"))
        self.platforms.append(Platform(325, 300, 250, 30, "platform.png"))
        self.platforms.append(Platform(825, 300, 250, 30, "platform.png"))
        self.platforms.append(Platform(100, 375, 200, 30, "platform.png"))
        self.platforms.append(Platform(1100, 375, 200, 30, "platform.png"))
        self.platforms.append(Platform(300, 450, 150, 30, "platform.png"))
        self.platforms.append(Platform(950, 450, 150, 30, "platform.png"))
        self.platforms.append(Platform(500, 525, 400, 30, "platform.png"))
        self.platforms.append(Platform(225, 600, 250, 30, "platform.png"))
        self.platforms.append(Platform(925, 600, 250, 30, "platform.png"))
        
        self.lava_platform = []
        self.lava_platform.append(Lava(625, 225, 150, 15, "lava.png"))
        self.lava_platform.append(Lava(85, 525, 150, 15, "lava.png"))
        self.lava_platform.append(Lava(1165, 525, 150, 15, "lava.png"))
        
        self.shield = []
        self.shield.append(BoosterItem(self.platforms, "shield.png", "shield"))
        self.storePosition = []
            
        self.player1lives = []
        self.player2lives = []
        for i in range(self.player1.lives):
            self.player1lives.append(HUD(1350 - i * 20,50, "life", "heart.png"))
            self.player2lives.append(HUD(50 + i *20,50, "life", "heart.png"))
            
        self.player1grenades = []
        self.player2grenades = []  
        for i in range(self.player1.grenades):
            self.player2grenades.append(HUD(50 + i * 20, 75, "grenade", "grenade.png"))
            self.player1grenades.append(HUD(1350 - i * 20, 75, "grenade", "grenade.png"))
        
        self.crate = []
        self.crate.append(Crate(self.platforms, "crate.png", "crate"))
        self.heart = []
        self.heart.append(BoosterItem(self.platforms, "heart.png", "heart"))
        self.grenade = []
        self.grenade.append(BoosterItem(self.platforms, "grenade.png", "grenade"))
        
    def display(self):
        global stage
        time2 = time.time()
        self.tElapsed = int(time2 - time1)
        
        for t in self.crate:
            t.display()
            
        for t in self.heart:
            t.display()
        
        for t in self.grenade:
            t.display()
            
        for t in self.shield:
            t.display()
            
        for t in self.platforms:
            t.display()
            
        for t in self.lava_platform:
            t.display()
        #when player is dead it repawns them with a shield
        for t in self.player1lives:
            t.display()
            if self.player1.dead == True:
                self.player1.dead = False
                self.player1.shieldeat = True
                self.player1.shieldActive = True
                self.player1lives.pop()
                
        for t in self.player2lives:
            t.display()
            if self.player2.dead == True:
                self.player2.dead = False
                self.player2.shieldeat = True
                self.player2.shieldActive = True
                self.player2lives.pop()
                
        for t in self.player1grenades:
            t.display()
        for t in self.player2grenades:
            t.display()
                    
        self.player1.display()
        self.gun1.display(self.player1.x , self.player1.y, self.player1.dir)

        self.player2.display()       
        self.gun2.display(self.player2.x , self.player2.y, self.player2.dir)
        
        # Check for bullet collision 
        for i in self.gun1.bullet_list:
            for j in self.gun2.bullet_list:
                if self.checkbulletcollision(i, j):
                    self.gun1.bullet_list.remove(i)
                    self.gun2.bullet_list.remove(j)
        
        
        # Check for grenade hitting the ground            
        for k in self.grenade_list:
            if k.y + k.r >= k.g:
                # self.gun1.grenade_list.remove(k)
                k.explode(k.x, k.y)
                k.grenadeSound.play()
                k.grenadeSound.rewind()
                self.blast_list.append(k)
                self.grenade_list.remove(k)
            k.display()
            
        for k in self.blast_list: 
            
            k.blastanimation()
            

                
        # Check for bullet hit on player
        
        for t in self.gun1.bullet_list:
            if t.checkbullethit():
                self.gun1.bullet_list.remove(t)
                if self.player2.shieldActive != True:
                    if t.dir == "left":
                        self.player2.vx -= t.power
                    if t.dir == "right":
                        self.player2.vx += t.power
            t.display()
        
        for t in self.gun2.bullet_list:
            if t.checkbullethit():
                self.gun2.bullet_list.remove(t)
                if self.player1.shieldActive != True:
                    if t.dir == "right":
                        self.player1.vx += t.power
                    if t.dir == "left":
                        self.player1.vx -= t.power
            t.display()
            
        if game.player1.lives == 0 : 
            stage = 2
            return
        elif game.player2.lives == 0:
            stage = 3
            
            
    def checkbulletcollision(self, bul1, bul2):
        if ((bul1.x - bul2.x)**2 + (bul1.y - bul2.y)**2) ** 0.5 <= bul1.vx/2 + bul2.vx/2:
            return True 
        

                
              
time1 = time.time()  
def setup():  
    global bgimg, youwin, redimg, blueimg, graybg, title, arrow_key, wasd, c, v, forward_slash, period, gamestart  
    size(WIDTH, HEIGHT)  
    frameRate(60)  
    bgimg = loadImage(path + "/images/" + "background.png")  
    redimg = loadImage(path + "/images/" + "redWin.png")  
    blueimg = loadImage(path + "/images/" + "blueWin.png")  
    youwin = loadImage(path + "/images/" + "youWin1.png")  
    graybg = loadImage(path + "/images/" + "grayBackground.jpg")  
    title = loadImage(path + "/images/" + "title.png")  
      
    arrow_key = loadImage(path + "/images/" + "arrow_key.png")  
    wasd = loadImage(path + "/images/" + "wasd.png")  
    c = loadImage(path + "/images/" + "c.png")  
    v = loadImage(path + "/images/" + "v.png")  
    forward_slash = loadImage(path + "/images/" + "forward_slash.png")  
    period = loadImage(path + "/images/" + "period.png")  
    fill(0, 0, 0)  
    textSize(25)  
      
      
def draw():  
    
    # Stage 0 for start screen
    if stage == 0:  
        global graybg, arrow_key, wasd, c, v, forward_slash, period, redimg, blueimg  
        setup()  
        background(graybg)  
        image(title, 300,100, 800, 100)  
        text("Player 2", 300, 300)  
        image(wasd, 100, 400, 200, 140)  
        image(c, 100, 550, 50, 50)  
        text("Shoot", 160, 580)  
        image(v, 100, 610, 50, 50)  
        text("Throw Grenade", 160, 640)  
        image(redimg, 350, 350, 250, 300)  
          
        text("Player 1", 1000, 300)  
        image(arrow_key, 800, 390, 210, 150)  
        image(forward_slash, 800, 550, 50, 50)  
        text("Shoot", 860, 580)  
        image(period, 800, 610, 50, 50)  
        text("Throw Grenade", 860, 640)  
        image(blueimg, 1050, 350, 250, 300)  
          
        text("Press Space bar to Start!", 530, 270)  
     
    # Stage 1 for game play 
               
    elif stage == 1:  
        global gamestart, game  
        if gamestart == True:  
            game = Game(WIDTH, HEIGHT, 900)  
            gamestart = False  
        global bgimg  
        background(bgimg)  
        game.display()  
     
    # Stage 2 for red win
                       
    elif stage == 2:   
        global youwin,redimg, graybg  
        setup()  
        background(graybg)  
        image(youwin,0,0, 1400, 720)  
        image(redimg,225,170, 250, 300, )  
        text("Press R to restart!", 600, 100)
        # background(youwin)  
        
    # Stage 3 for blue win
        
    elif stage == 3:  
        global youwin, blueimg, graybg
        setup()  
        background(graybg)  
        image(youwin,0,0, 1400, 720)  
        image(blueimg,900,170, 250, 300)  
        text("Press R to retart!", 600, 100)
          
def keyPressed(): 
    global stage, gamestart  
    if stage == 1:
        if key == "a":  
            game.player2.key_handler["left"] = True  
        elif key == "d":  
            game.player2.key_handler["right"] = True  
        elif key == "w":  
            game.player2.key_handler[UP] = True  
        elif key == "c":  
            game.gun2.attack["shoot"] = True  
        elif key == "v":  
            game.gun2.attack["throw"] = True  
        elif key == "s":  
            game.player2.key_handler[DOWN] = True  
        elif key == "s":  
            game.player2.key_handler[DOWN] = True  
        elif keyCode == LEFT:  
            game.player1.key_handler["left"] = True  
        elif keyCode == RIGHT:  
            game.player1.key_handler["right"] = True  
        elif keyCode == UP:  
            game.player1.key_handler[UP] = True  
        elif key == "/":  
            game.gun1.attack["shoot"] = True  
        elif key == ".":  
            game.gun1.attack["throw"] = True  
        elif keyCode == DOWN:  
            game.player1.key_handler[DOWN] = True  
          
    if key == " " and stage == 0:  
        stage = 1  
        gamestart = True  
    elif key == "r" and (stage == 2 or stage == 3):  
        stage = 0  
        gamestart = True  
          
          
def keyReleased():  
    global stage  
    if stage == 1:
        if key == "a":  
            game.player2.key_handler["left"] = False  
        elif key == "d":  
            game.player2.key_handler["right"] = False  
        elif key == "w":   
            game.player2.key_handler[UP] = False  
        elif key == "c":  
            game.gun2.attack["shoot"] = False  
        elif key == "v":  
            game.gun2.attack["throw"] = False  
        elif key == "s":  
            game.player2.key_handler[DOWN] = False  
        elif keyCode == LEFT:  
            game.player1.key_handler["left"] = False  
        elif keyCode == RIGHT:  
            game.player1.key_handler["right"] = False  
        elif keyCode == UP:  
            game.player1.key_handler[UP] = False  
        elif key == "/":  
            game.gun1.attack["shoot"] = False  
        elif key == ".":  
            game.gun1.attack["throw"] = False  
        elif keyCode == DOWN:  
            game.player1.key_handler[DOWN] = False  
        
