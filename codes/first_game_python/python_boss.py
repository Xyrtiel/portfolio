import pygame
import random
import time
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
res = (1200, 800)
screen = pygame.display.set_mode(res)

# Charger et jouer la musique en boucle
pygame.mixer.music.load('codes/first_game_python/music/other_background_music.mp3') # Lancement du fichier audio
pygame.mixer.music.set_volume(0.5) # Réglage du Volume
pygame.mixer.music.play(-1)  # -1 pour jouer en boucle
trumpet_sound = pygame.mixer.Sound('codes/first_game_python/music/trumpet_sound.wav')  # Charger le fichier audio de la trompette

# Charger les images
fond = pygame.image.load('codes/first_game_python/images/overwatch2_background.png').convert()
character_image = pygame.image.load('codes/first_game_python/images/character.png')
character_image = pygame.transform.scale(character_image, (70, 70))  # Agrandir le personnage
boss_image = pygame.image.load('codes/first_game_python/images/boss.png')  # Ajouter l'image du boss
boss_image = pygame.transform.scale(boss_image, (100, 100))  # Ajuster la taille du boss

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
SPARKLE_COLOR = (255, 223, 0)  # Couleur des paillettes

# Configuration de la police et du texte
smallfont = pygame.font.SysFont('Corbel', 25)
play_text = smallfont.render('Jouer', True, WHITE)
quit_text = smallfont.render('Quitter', True, WHITE)
score_font = pygame.font.SysFont('Corbel', 30)
timer_font = pygame.font.SysFont('Corbel', 50)
life_font = pygame.font.SysFont('Corbel', 25)

# Dimensions et position des boutons
button_width = 260
button_height = 40
button_x = (res[0] - button_width) / 2
play_button_y = (res[1] - button_height) / 2
quit_button_y = play_button_y + button_height + 10

# Calcul des coordonnées pour centrer le texte dans les boutons
play_text_x = button_x + (button_width - play_text.get_width()) / 2
play_text_y = play_button_y + (button_height - play_text.get_height()) / 2
quit_text_x = button_x + (button_width - quit_text.get_width()) / 2
quit_text_y = quit_button_y + (button_height - quit_text.get_height()) / 2

# Position initiale et vitesse du personnage
xCoord = 360
yCoord = 360
xSpeed = 0
ySpeed = 0

# Etat du jeu
game_mode = False

# Variables pour le boss
boss_appeared = False
boss_current_life = 100
boss_max_life = 100
boss_position = (0, 0)
attack_positions = []
attack_spawn_time = time.time()
attack_interval = 2  # Temps entre les attaques du boss
stunned_time = 0
is_stunned = False

# Minuteur
timer_duration = 60  # Durée du minuteur en secondes
start_time = time.time()  # Temps de départ du minuteur

# Variables pour les paillettes
sparkles = []

# Compteur de touchés du boss
boss_hits = 0
max_boss_hits = 3

# Variables pour la boule verte
green_ball_position = None
green_ball_spawn_time = 0
green_ball_duration = 5  # La boule verte suit le joueur pendant 5 secondes
green_ball_interval = 30  # La boule verte apparaît toutes les 30 secondes

# Variables pour la téléportation du boss
teleportation_time = time.time()  # Temps de la dernière téléportation
teleport_interval = 3  # Intervalle entre les téléportations du boss

# Boules violettes poursuivant le joueur
purple_balls = []

# Boucle principale
clock = pygame.time.Clock()
done = False

def move_boss():
    global boss_position, boss_current_life, boss_movement_time, is_moving, sparkles, boss_hits
    if not is_moving:
        # Déplace le boss à une nouvelle position aléatoire
        boss_position = (random.randint(0, res[0] - 100), random.randint(0, res[1] - 100))
        # Réduit les PV du boss de 0,1 % (sans dépasser 0)
        boss_current_life = max(0, boss_current_life - boss_max_life * 5)
        # Réinitialise le compteur de touches si le boss a été touché
        if boss_current_life <= 0:
            boss_hits += 1
            if boss_hits >= max_boss_hits:
                print("Le boss a été vaincu!")
                # Logique de fin de jeu ou autres actions lorsque le boss est vaincu
        # Enregistre le temps de début du déplacement
        boss_movement_time = time.time()
        is_moving = True

def boss_action():
    global attack_positions, boss_current_life, res, purple_balls

    current_time = time.time()

    if not boss_appeared or is_stunned:
        return

    # Calculer la perte de vie en pourcentage
    life_percentage = (boss_max_life - boss_current_life) / boss_max_life * 100

    # Vérifier le pourcentage de vie pour déclencher une nouvelle attaque
    if life_percentage % 2 == 0:  # Déclencher une attaque toutes les 2 %
        # Limiter le nombre d'attaques ajoutées à chaque déclenchement
        num_attacks_to_add = 1  # Par exemple, ajouter une seule attaque à chaque fois

        for _ in range(num_attacks_to_add):
            # Ajouter une boule bleue si le nombre actuel est inférieur à un certain seuil
            blue_ball_count = sum(1 for attack in attack_positions if attack['color'] == BLUE)
            if blue_ball_count < 10:  # Limiter à 10 boules bleues simultanées
                attack_x = random.randint(0, res[0])
                attack_y = random.randint(0, res[1])
                attack_dir_x = random.uniform(-2, 2)
                attack_dir_y = random.uniform(-2, 2)
                attack_positions.append({'x': attack_x, 'y': attack_y, 'dir_x': attack_dir_x, 'dir_y': attack_dir_y, 'color': BLUE})

        # Ajouter des boules rouges si le pourcentage de vie est inférieur à 70 %
        if life_percentage % 5 == 0 :
            red_ball_count = sum(1 for attack in attack_positions if attack['color'] == RED)
            if red_ball_count < 5:  # Limiter à 5 boules rouges simultanées
                for _ in range(3):
                    attack_x = random.randint(0, res[0])
                    attack_y = random.randint(0, res[1])
                    attack_dir_x = random.uniform(-3, 3)
                    attack_dir_y = random.uniform(-3, 3)
                    attack_positions.append({'x': attack_x, 'y': attack_y, 'dir_x': attack_dir_x, 'dir_y': attack_dir_y, 'color': RED})

        # Ajouter des boules violettes si le pourcentage de vie est inférieur à 40 %
        if life_percentage % 10 == 0:
            purple_ball_count = len(purple_balls)
            if purple_ball_count < 3:  # Limiter à 3 boules violettes simultanées
                for _ in range(2):
                    purple_ball_x = random.randint(0, res[0])
                    purple_ball_y = random.randint(0, res[1])
                    purple_balls.append({'x': purple_ball_x, 'y': purple_ball_y, 'color': PURPLE, 'target_x': xCoord + 35, 'target_y': yCoord + 35, 'time_spawned': current_time})

    # Mise à jour des attaques existantes
    new_attack_positions = []
    for attack in attack_positions:
        attack['x'] += attack['dir_x']
        attack['y'] += attack['dir_y']

        # Vérifier les collisions avec le personnage
        if (xCoord < attack['x'] + 20 and xCoord + 70 > attack['x'] and
            yCoord < attack['y'] + 20 and yCoord + 70 > attack['y']):
            sparkles = []  # Réinitialiser les paillettes à chaque collision
            for _ in range(50):
                sparkles.append({'x': xCoord + 35, 'y': yCoord + 35, 'vx': random.uniform(-5, 5), 'vy': random.uniform(-5, 5), 'life': random.uniform(0.5, 1.5)})
            print(f"Personnage touché par une attaque! Vie actuelle: {boss_current_life}")  # Pour le débogage
        else:
            # Ne garder que les attaques visibles à l'écran
            if 0 <= attack['x'] <= res[0] and 0 <= attack['y'] <= res[1]:
                new_attack_positions.append(attack)
    attack_positions = new_attack_positions

    # Mise à jour des boules violettes
    new_purple_balls = []
    for ball in purple_balls:
        if time.time() - ball['time_spawned'] < 5:
            # Mettre à jour la direction pour suivre le joueur
            angle = math.atan2((yCoord + 35) - ball['y'], (xCoord + 35) - ball['x'])
            ball['x'] += math.cos(angle) * 3
            ball['y'] += math.sin(angle) * 3
        else:
            # Continuer en ligne droite après 5 secondes
            ball['x'] += 3
        new_purple_balls.append(ball)
    purple_balls = new_purple_balls

def draw_health_bar():
    global boss_current_life
    boss_life_bar_width = 200
    boss_life_bar_height = 20
    boss_life_bar_x = (res[0] - boss_life_bar_width) / 2
    boss_life_bar_y = res[1] - boss_life_bar_height - 10
    pygame.draw.rect(screen, BLACK, (boss_life_bar_x, boss_life_bar_y, boss_life_bar_width, boss_life_bar_height))
    
    # Calculer la largeur de la barre de vie en fonction des PV restants
    life_width = boss_life_bar_width * (boss_current_life / boss_max_life)
    pygame.draw.rect(screen, GREEN, (boss_life_bar_x, boss_life_bar_y, life_width, boss_life_bar_height))
    
    # Dessiner la partie rouge de la barre de vie
    pygame.draw.rect(screen, RED, (boss_life_bar_x + life_width, boss_life_bar_y, boss_life_bar_width - life_width, boss_life_bar_height))

    # Ajouter le texte "Poilur" au-dessus de la barre de vie
    poilur_text = score_font.render("Bulbizarre", True, WHITE)
    screen.blit(poilur_text, (boss_life_bar_x + (boss_life_bar_width - poilur_text.get_width()) / 2, boss_life_bar_y - poilur_text.get_height() - 5))

def draw_sparkles():
    global sparkles
    new_sparkles = []
    for sparkle in sparkles:
        sparkle['x'] += sparkle['vx']
        sparkle['y'] += sparkle['vy']
        sparkle['life'] -= 0.05
        if sparkle['life'] > 0:
            pygame.draw.circle(screen, SPARKLE_COLOR, (int(sparkle['x']), int(sparkle['y'])), 5)
            new_sparkles.append(sparkle)
    sparkles = new_sparkles

def draw_green_ball():
    global green_ball_position, green_ball_spawn_time
    if green_ball_position:
        # Dessiner la boule verte
        pygame.draw.circle(screen, GREEN, (int(green_ball_position[0]), int(green_ball_position[1])), 20)

        # Vérifier si la boule verte a dépassé sa durée
        if time.time() - green_ball_spawn_time > green_ball_duration:
            green_ball_position = None

def spawn_green_ball():
    global green_ball_position, green_ball_spawn_time
    current_time = time.time()
    if not green_ball_position and (current_time - green_ball_spawn_time) >= green_ball_interval:
        # Positionner la boule verte au hasard
        green_ball_position = (random.randint(0, res[0]), random.randint(0, res[1]))
        green_ball_spawn_time = current_time

def draw_menu():
    screen.fill(BLACK)

    # Dessiner le bouton "Jouer"
    mouse = pygame.mouse.get_pos()
    if button_x <= mouse[0] <= button_x + button_width and play_button_y <= mouse[1] <= play_button_y + button_height:
        pygame.draw.rect(screen, color_light, [button_x, play_button_y, button_width, button_height])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, play_button_y, button_width, button_height])
    
    # Dessiner le texte sur le bouton "Jouer"
    screen.blit(play_text, (play_text_x, play_text_y))

    # Dessiner le bouton "Quitter"
    if button_x <= mouse[0] <= button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
        pygame.draw.rect(screen, color_light, [button_x, quit_button_y, button_width, button_height])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, quit_button_y, button_width, button_height])
    
    # Dessiner le texte sur le bouton "Quitter"
    screen.blit(quit_text, (quit_text_x, quit_text_y))

while not done:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                xSpeed = -3
            if ev.key == pygame.K_RIGHT:
                xSpeed = 3
            if ev.key == pygame.K_UP:
                ySpeed = -3
            if ev.key == pygame.K_DOWN:
                ySpeed = 3

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT:
                xSpeed = 0
            if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
                ySpeed = 0

        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if not game_mode:
                if button_x <= mouse[0] <= button_x + button_width:
                    if play_button_y <= mouse[1] <= play_button_y + button_height:
                        game_mode = True
                        start_time = time.time()  # Réinitialiser le minuteur au début du jeu
                    elif quit_button_y <= mouse[1] <= quit_button_y + button_height:
                        pygame.quit()
                        exit()
            else:
                pass
    
    boss_movement_time = time.time()
    if game_mode:
        # Mettre à jour la position du personnage
        xCoord += xSpeed
        yCoord += ySpeed

        # Empêcher le personnage de sortir de l'écran
        xCoord = max(0, min(xCoord, res[0] - 70))
        yCoord = max(0, min(yCoord, res[1] - 70))

        if not boss_appeared:
            boss_appeared = True
            boss_position = (res[0] // 2 - 50, 50)  # Position initiale du boss

        current_time = time.time()  # Obtenir le temps actuel

        # Gestion des attaques du boss
        boss_action()

        # Vérifier la collision entre le personnage et le boss
        if (xCoord < boss_position[0] + 100 and xCoord + 70 > boss_position[0] and
            yCoord < boss_position[1] + 100 and yCoord + 70 > boss_position[1]):
            boss_position = (random.randint(0, res[0] - 100), random.randint(0, res[1] - 100))  # Déplacer le boss

            # Appliquer les dégâts normaux au boss
            boss_current_life -= boss_max_life * 0.01

            # Appliquer les dégâts supplémentaires si la boule verte est présente
            if green_ball_position:
                boss_current_life -= boss_max_life * 0.03
            
            trumpet_sound.play()

            sparkles = []  # Réinitialiser les paillettes à chaque collision
            for _ in range(50):  # Créer des paillettes
                sparkles.append({'x': xCoord + 35, 'y': yCoord + 35, 'vx': random.uniform(-5, 5), 'vy': random.uniform(-5, 5), 'life': random.uniform(0.5, 1.5)})
            print(f"Personnage touché par le boss! Vie actuelle: {boss_current_life}")  # Pour le débogage


        # Vérifier la collision entre la boule verte et le personnage
        if green_ball_position and (xCoord < green_ball_position[0] + 20 and xCoord + 70 > green_ball_position[0] and
                                   yCoord < green_ball_position[1] + 20 and yCoord + 70 > green_ball_position[1]):
            # Attacher la boule au joueur pendant 5 secondes
            green_ball_spawn_time = time.time()
            green_ball_position = None  # La boule disparaît après avoir attaché

        # Gérer le mouvement du boss si ses PV sont faibles
        if boss_current_life <= boss_max_life * 0.2:
            if current_time - boss_movement_time >= 3:
                move_boss()
                is_moving = False  # Réinitialiser le déplacement pour le prochain cycle

        # Dessiner sur l'écran
        screen.blit(fond, (0, 0))
        screen.blit(character_image, (xCoord, yCoord))

        # Dessiner le boss
        screen.blit(boss_image, boss_position)

        # Dessiner les attaques du boss
        for attack in attack_positions:
            pygame.draw.circle(screen, attack['color'], (int(attack['x']), int(attack['y'])), 10)  # Dessiner les attaques en tant que cercles colorés

        # Dessiner les boules violettes poursuivant le joueur
        for ball in purple_balls:
            pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), 10)

        draw_health_bar()

        # Dessiner les paillettes
        draw_sparkles()

        # Dessiner la boule verte si elle est active
        draw_green_ball()

        # Gérer l'apparition de la boule verte
        spawn_green_ball()

    else:
        # Dessiner le menu
        screen.fill(BLACK)

        # Dessiner le bouton "Jouer"
        mouse = pygame.mouse.get_pos()
        if button_x <= mouse[0] <= button_x + button_width and play_button_y <= mouse[1] <= play_button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, play_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, play_button_y, button_width, button_height])
        
        # Dessiner le texte sur le bouton "Jouer"
        screen.blit(play_text, (play_text_x, play_text_y))

        # Dessiner le bouton "Quitter"
        if button_x <= mouse[0] <= button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, quit_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, quit_button_y, button_width, button_height])
        
        # Dessiner le texte sur le bouton "Quitter"
        screen.blit(quit_text, (quit_text_x, quit_text_y))

    pygame.display.flip()
    clock.tick(60)
