# I - IMPORT AND INITIALIZE=
import pygame
import sprites

pygame.init()
pygame.mixer.init()

# DISPLAY
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Metal Selug")



def main():
    keepGoing = True
    while keepGoing:
        status1 = title_screen()
        if status1 == 0:
            status2 = level1()
            if status2[0] == 0:
                status3 = boss(*status2[1:])
                if status3 == 1:
                    if gameover():
                        keepGoing = False
                elif status3 == 2:
                    keepGoing = False
            elif status2[0] == 1:
                if gameover():
                    keepGoing = False
            elif status2[0] == 2:
                keepGoing = False
        elif status1 == 1:
            if instructions():
                keepGoing = False
        elif status1 == 2:
            keepGoing = False

    pygame.mouse.set_visible(True)
    pygame.quit()


def instructions(): #The Entities
    bkgd = pygame.image.load('images\\instructions.png').convert()
    button = sprites.Button(3)
    allSprites = pygame.sprite.Group(button)

    clock = pygame.time.Clock()             #Assign
    keepGoing = True

    while keepGoing:                        #Loop
        clock.tick(30)                      #TIME
        for event in pygame.event.get():    #Event Handling
            if event.type == pygame.QUIT:
                keepGoing = False
                exitstatus = 1
                if button.get_pressed():
                    keepGoing = False
                    exitstatus = 0
        screen.blit(bkgd, (0, 0))           #Refresh The Screen
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    return exitstatus


def title_screen():                          #Funtion for Title Screen
    bkgd = pygame.image.load('images\\title screen.jpg').convert()  #Entities
    animations = [sprites.Animation(i) for i in range(2)]
    buttons = [sprites.Button(i) for i in range(3)]
    allSprites = pygame.sprite.Group(animations[0])
    sfx = pygame.mixer.Sound('sounds\\menu.wav')        #Song Played in Main menu
    sfx.play()
    clock = pygame.time.Clock()                         #Put the time
    keepGoing = True
    pygame.mouse.set_visible(True)
    while keepGoing:                                    #Loop again
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                exitstatus = 2
        if animations[0].get_done():                    #Handles text animation
            allSprites.add(animations[1])

        if animations[1].get_done():
            allSprites.add(buttons)
        if buttons[0].get_pressed():                    #Check if the player pressed any buttons
            keepGoing = False
            exitstatus = 0
        elif buttons[1].get_pressed():
            keepGoing = False
            exitstatus = 1
        elif buttons[2].get_pressed():
            keepGoing = False
            exitstatus = 2
        screen.blit(bkgd, (0, 0))                       #Refresh The Screen again
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    return exitstatus


def level1():                                           #Our level 1
    '''main game'''
    player = sprites.Player()                           #Entities / Players
    tank = sprites.Tank()
    playerGrp = pygame.sprite.Group(tank, player)
    current_player = player
    clean_bkgd = pygame.image.load('images\\bkgd.png').convert() #Background
    bkgd = sprites.Background(player)
    wall = sprites.Platform(((1438, 380), (1, 100)))                                    #Map Objects
    platforms = pygame.sprite.Group([sprites.Platform(dimension) for dimension in (
    ((0, 366), (1400, 1)), ((1438, 450), (2507, 1)), ((1845, 342), (110, 1)), ((2032, 260), (348, 1)),
    ((2380, 342), (130, 1)), ((2510, 260), (290, 1)), ((2915, 260), (345, 1)), ((3260, 342), (150, 1)))])
    pBulletsGrp = pygame.sprite.Group()         #Projectiles (bullets and grenades)
    eBulletsGrp = pygame.sprite.Group()
    grenadeGrp = pygame.sprite.Group()
    scoreboard = sprites.ScoreBoard(player, tank)   #Scoreboard
    enemiesGrp = pygame.sprite.Group([sprites.Enemy(midbottom) for midbottom in (   #Enemies
    (500, 366), (800, 366), (1000, 366), (1100, 366), (1200, 366), (1300, 366), (1700, 450), (1800, 450), (1900, 450),
    (2300, 450), (2400, 450), (2500, 450), (2600, 450), (2700, 450), (2800, 450), (2900, 450), (3000, 450), (3100, 450),
    (3200, 450), (3400, 450), (3500, 450), (3600, 450), (3800, 450), (1880, 342), (2040, 260), (2200, 260), (2400, 342),
    (2550, 260), (2700, 260), (2950, 260), (3100, 260), (3280, 342))])
    pygame.mixer.music.load('sounds\\music.mp3')                                    #Music
    pygame.mixer.music.play(-1)

    allSprites = pygame.sprite.OrderedUpdates(enemiesGrp, playerGrp, eBulletsGrp, pBulletsGrp, grenadeGrp)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    while keepGoing:                    #Another While Loop
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                exitstatus = 2
            if not current_player.get_dying():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if pygame.sprite.collide_rect(player,       #Enter the TANK
                                                      tank) and current_player == player and not tank.get_dying():
                            current_player = tank
                            player.kill()
                        elif current_player == tank:                #Exit the TANK
                            player.respawn(tank)
                            playerGrp.add(player)
                            allSprites.add(playerGrp)
                            current_player = player
                            tank.die()
                    elif event.key == pygame.K_l:
                        if current_player == tank:                  #Fire Cannon from the TANK
                            if tank.shoot_cannon():
                                grenadeGrp.add(sprites.TankShell(tank))
                                allSprites.add(grenadeGrp)
                        elif player.get_grenades():                 #Player throw grenade
                            player.throw_grenade()
                            grenadeGrp.add(sprites.Grenade(player))
                            allSprites.add(grenadeGrp)

        if not current_player.get_dying():
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_a]:       #In game movement, left and right
                pass
            elif keys_pressed[pygame.K_a]:
                current_player.move(-1)
            elif keys_pressed[pygame.K_d]:
                current_player.move(1)
            if keys_pressed[pygame.K_j]:                                    #In game action, Jump
                current_player.jump()

            if current_player == tank:                                      #Tank Controls
                if keys_pressed[pygame.K_k]:                                #Tank shooting Machine Gun
                    tank.shoot_mg()
                    pBulletsGrp.add(sprites.TankBullet(bkgd, tank))
                    allSprites.add(pBulletsGrp)
                if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:   #The machine gun rotation
                    pass
                elif keys_pressed[pygame.K_w]:
                    tank.rotate(5)
                elif keys_pressed[pygame.K_s]:
                    tank.rotate(-5)
            else:                                                           #Player Control
                if keys_pressed[pygame.K_k]:
                    if player.get_weapon():                                 #Player shoot Machine Gun
                        pBulletsGrp.add(sprites.MGBullet(bkgd, player, player.shoot()))
                        allSprites.add(pBulletsGrp)
        for item in (player, tank):                                          #Collision Detection
            if pygame.sprite.collide_rect(item, wall):                       #Collision with wall
                item.collide_wall(wall)

            collision = pygame.sprite.spritecollide(item, platforms, False)  #Collision with platform
            if collision:
                item.land(max(platform.rect.top for platform in collision))  #Find lowest platform to step on
            else:
                item.fall()

        for bullet in pygame.sprite.spritecollide(current_player, eBulletsGrp, False):  #Bullet collision with player
            if not current_player.get_dying():
                bullet.kill()
                current_player.hurt(50)

        for enemy in pygame.sprite.spritecollide(tank, enemiesGrp, False):          #The tank collision with enemies
            enemy.die()

        for bullet, enemy in pygame.sprite.groupcollide(pBulletsGrp, enemiesGrp, False, False).items(): #Bullet colision with enemies
            if enemy and not enemy[0].get_dying():
                bullet.kill()
                enemy[0].die()

        for grenade, enemy in pygame.sprite.groupcollide(grenadeGrp, enemiesGrp, False, True).items(): #Grenade collision with enemies
            if enemy:
                grenade.explode()
                for i in enemy:
                    i.die()

        for grenade, platform in pygame.sprite.groupcollide(grenadeGrp, platforms, False, False).items(): #Grenade collision with the platform
            if platform:
                grenade.explode()

        for enemy in enemiesGrp:                #Enemy shooting
            if enemy.get_shooting():
                eBulletsGrp.add(sprites.EnemyBullet(enemy, current_player))
                allSprites.add(eBulletsGrp)

        if tank.get_dying():            #If the tank is destroyed, respawn the player to the current status
            player.respawn(tank)
            playerGrp.add(player)
            allSprites.add(playerGrp)
            current_player = player
        if player.get_dying() == 2:     #Exit game loop when player died
            keepGoing = False
            exitstatus = 1
        if current_player.rect.right >= bkgd.image.get_width():     #Checking if the player has defeated the boss
            keepGoing = False
            exitstatus = 0

        # REFRESH SCREEN
        # We draws all of the sprites in the background
        bkgd.image.blit(clean_bkgd, (0, 0))
        allSprites.update(current_player)
        allSprites.draw(bkgd.image)

        # Update the background based on the position of the player
        bkgd.update(current_player)
        screen.blit(bkgd.image, bkgd.rect)

        # Update the scoreboard
        scoreboard.update(current_player)
        screen.blit(scoreboard.image, scoreboard.rect)

        pygame.display.flip()

    pygame.mixer.music.stop()
    if tank.get_dying():
        return exitstatus, player
    return exitstatus, player, tank


def gameover():
    # Load the background sprites
    bkgd = sprites.GameOver()
    allSprites = pygame.sprite.Group(bkgd)
    # Load the music for sad game over.
    pygame.mixer.music.load('sounds\\gameover.wav')
    pygame.mixer.music.play()

    # Assign the time
    clock = pygame.time.Clock()
    keepGoing = True

    # Loop
    while keepGoing:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                exitstatus = 1

        if bkgd.get_done():
            keepGoing = False
            exitstatus = 0

            #Refresh the screen again
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    return exitstatus


def boss(prev_player, prev_tank=None):
    # Use the previous player or previous tank if we still in one
    player = sprites.Player(prev_player)
    if prev_tank:
        tank = sprites.Tank(prev_tank)
        current_player = tank
        playerGrp = pygame.sprite.Group(tank)
    else:
        tank = None
        current_player = player
        playerGrp = pygame.sprite.Group(player)

    # Clean the background then load the background image for the boss
    clean_bkgd = pygame.image.load('images\\bossbkgd2.png').convert()
    bkgd = sprites.Background(player, 1)

    # Map objects such as platform
    wall = sprites.Platform(((865, 0), (1, 480)))
    platform = sprites.Platform(((0, 432), (1280, 1)))

    # The boss laser projectile
    laser = sprites.Laser()
    pBulletsGrp = pygame.sprite.Group()
    shellGrp = pygame.sprite.Group()
    pGrenadeGrp = pygame.sprite.Group()

    mgicon = sprites.MGIcon()

    # Current scoreboard
    scoreboard = sprites.ScoreBoard(player, tank)

    # The boss
    boss = sprites.Boss()

    # The boss stage sound and also the mission complete sound
    pygame.mixer.music.load('sounds\\boss.mp3')
    pygame.mixer.music.play(-1)
    missioncomplete = pygame.mixer.Sound('sounds\\mission complete.wav')

    allSprites = pygame.sprite.OrderedUpdates(playerGrp, boss, mgicon, pBulletsGrp, shellGrp, pGrenadeGrp, laser)

    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    cutscene = True

    # Loop
    while keepGoing:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                exitstatus = 2
            if not cutscene and not current_player.get_dying():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        # Let the player to exit the tank
                        if current_player == tank:
                            player.respawn(tank)
                            playerGrp.add(player)
                            allSprites.add(playerGrp)
                            current_player = player
                            tank.die()
                    elif event.key == pygame.K_l:
                        # If the player inside of the tank it can shoot cannon
                        if current_player == tank:
                            if tank.shoot_cannon():
                                pGrenadeGrp.add(sprites.TankShell(tank))
                                allSprites.add(pGrenadeGrp)
                        # Player can throw grenade
                        elif player.get_grenades():
                            player.throw_grenade()
                            pGrenadeGrp.add(sprites.Grenade(player))
                            allSprites.add(pGrenadeGrp)

        # Cutscene (not included)
        if cutscene:
            current_player.move(1)
            if current_player.rect.left + 700 >= boss.rect.right:
                cutscene = False
                boss.start()

        elif not current_player.get_dying():
            keys_pressed = pygame.key.get_pressed()
            # left and right movement for the boss stage
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_a]:
                pass
            elif keys_pressed[pygame.K_a]:
                current_player.move(-1)
            elif keys_pressed[pygame.K_d]:
                current_player.move(1)
            # JUMP for the boss stage
            if keys_pressed[pygame.K_j]:
                current_player.jump()

            # The controls for the tank in boss stage
            if current_player == tank:
                # Player can shoot machine gun in the boss stage
                if keys_pressed[pygame.K_k]:
                    tank.shoot_mg()
                    pBulletsGrp.add(sprites.TankBullet(bkgd, tank))
                    allSprites.add(pBulletsGrp)
                    # Rotating machine gun in tank
                if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
                    pass
                elif keys_pressed[pygame.K_w]:
                    tank.rotate(5)
                elif keys_pressed[pygame.K_s]:
                    tank.rotate(-5)
            # Players controls
            else:
                if keys_pressed[pygame.K_k]:
                    # Shooting bullets (projectile)
                    if player.get_weapon():
                        pBulletsGrp.add(sprites.MGBullet(bkgd, player, player.shoot()))
                        allSprites.add(pBulletsGrp)
                    # Shoot using pistol (erased)
                    elif player.shoot():
                        pBulletsGrp.add(sprites.PistolBullet(bkgd, player))
                        allSprites.add(pBulletsGrp)

        # Detect any collision with wall or the tank
        for item in filter(bool, (player, tank)):
            # Collision with wall
            if pygame.sprite.collide_rect(item, wall):
                item.collide_wall(wall, 1)

                # Collision with platforms
            if pygame.sprite.collide_rect(item, platform):
                # Lowest platform to land on
                item.land(platform.rect.top)
            else:
                item.fall()

                # The boss laser collision with the player
        if pygame.sprite.collide_rect(laser, current_player):
            current_player.hurt(50)

            # The icon of machine gun collision with the player
        if pygame.sprite.collide_rect(mgicon, current_player):
            player.pickup()
            mgicon.hide()

        # The shell collision
        for shell in pygame.sprite.spritecollide(current_player, shellGrp, False):
            if not current_player.get_dying():
                shell.explode()
                current_player.hurt(50)

        # Shell collision with the ground
        for shell in pygame.sprite.spritecollide(platform, shellGrp, False):
            shell.explode()

            # Collision between grenade and the boss
        for grenade in pygame.sprite.spritecollide(boss, pGrenadeGrp, False):
            grenade.explode()
            boss.hurt(5)

            # Collision of bullets and boss
        for bullet in pygame.sprite.spritecollide(boss, pBulletsGrp, False):
            bullet.kill()
            boss.hurt(1)

            # Collision grenade with the platform
        for grenade in pygame.sprite.spritecollide(platform, pGrenadeGrp, False):
            grenade.explode()

            # The boss shooting the tank shell
        if boss.get_attack() == 1:
            shellGrp.add(sprites.TankShell())
            allSprites.add(shellGrp)
        # Boss allowed to attack using laser
        elif boss.get_attack() == 2:
            laser.reset()

        # If the tank breaks the player respawn as the last state or status
        if tank and tank.get_dying():
            player.respawn(tank)
            playerGrp.add(player)
            allSprites.add(playerGrp)
            current_player = player

        # Exits game loop if the animation is over
        if player.get_dying() == 2:
            keepGoing = False
            exitstatus = 1

        # Checks if the player have completed the level.
        if boss.get_dead():
            pygame.mixer.music.stop()
            missioncomplete.play()
            screen.blit(pygame.image.load('images\\mission complete.png').convert_alpha(), (109, 167))
            pygame.display.flip()
            pygame.time.wait(8000)
            keepGoing = False
            exitstatus = 0

        # REFRESH SCREEN and load sprites at the background
        bkgd.image.blit(clean_bkgd, (0, 0))
        allSprites.update(current_player)
        allSprites.draw(bkgd.image)

        # Updates background position
        bkgd.update(current_player)
        screen.blit(bkgd.image, bkgd.rect)

        # Update the scoreboard to the screen
        scoreboard.update(current_player)
        screen.blit(scoreboard.image, scoreboard.rect)

        pygame.display.flip()

    return exitstatus


main()