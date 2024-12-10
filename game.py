import pygame
import random
import sys
import os
from win32com.client import Dispatch
import math
import tkinter as tk
from tkinter import filedialog


pygame.mixer.init()
background_sound = pygame.mixer.Sound('backgroundmusic.wav')
coin_sound = pygame.mixer.Sound('coin.wav')
jump_sound = pygame.mixer.Sound('jump.wav')
hit_sound = pygame.mixer.Sound('hit.wav')

background_sound.set_volume(0.1)  # קביעת ווליום התחלתי נמוך יותר
coin_sound.set_volume(1.0)

class Butterfly:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_y = y
        self.angle = random.random() * 6.28
        self.speed = random.uniform(1, 3)
        
    def update(self):
        self.angle += 0.05
        self.y = self.original_y + math.sin(self.angle) * 30
        
    def draw(self, surface):
        draw_butterfly(surface, self.x, self.y)

def create_shortcut():
    executable_path = os.path.abspath(sys.argv[0])
    working_dir = os.path.dirname(executable_path)
    
    # השתמש בקובץ ההפעלה עצמו כאייקון
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(
        os.path.join(os.path.expanduser('~'), 'Desktop', 'MyGame.lnk'))
    shortcut.Targetpath = executable_path
    shortcut.WorkingDirectory = working_dir
    # האייקון יילקח מקובץ ההפעלה עצמו
    shortcut.IconLocation = f"{executable_path},0"
    shortcut.save()




pygame.init()

def initialize_game():
    global obstacles, butterflies, coins
    
    # ניקוי הרשימות הקיימות
    obstacles.clear()
    butterflies.clear()
    coins.clear()
    
    # הוספת פרפרים
    for i in range(40):
        butterfly_x = random.randint(SAFE_ZONE, 4800)
        butterfly_y = random.randint(100, 400)
        butterflies.append(Butterfly(butterfly_x, butterfly_y))
        obstacles.append({
            'x': butterfly_x,
            'y': butterfly_y,
            'width': 15,
            'height': 15,
            'type': 'butterfly'
        })
    
    # הוספת פטריות
    for x in range(SAFE_ZONE, MAP_WIDTH-100, 120):
        if random.random() > 0.3:
            mushroom_y = WINDOW_HEIGHT - GROUND_HEIGHT - 50
            obstacles.append({
                'x': x,
                'y': mushroom_y,
                'width': 40,
                'height': 50,
                'type': 'mushroom'
            })
    
    # הוספת חלזונות
    for x in range(SAFE_ZONE, MAP_WIDTH-100, 180):
        if random.random() > 0.4:
            snail_y = WINDOW_HEIGHT - GROUND_HEIGHT - 30
            obstacles.append({
                'x': x,
                'y': snail_y,
                'width': 40,
                'height': 30,
                'type': 'snail'
            })
    
    # הוספת מטבעות
    for x in range(SAFE_ZONE, 5000, 100):
        if random.random() > 0.5:
            coin_y = random.randint(WINDOW_HEIGHT - 300, WINDOW_HEIGHT - GROUND_HEIGHT - 50)
            coins.append({'x': x, 'y': coin_y, 'collected': False})



# Set up display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mario Style Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Constants
SAFE_ZONE = 300
GROUND_HEIGHT = 100
MAP_WIDTH = 5000
MAP_HEIGHT = 600

# מכשולים גלובליים
obstacles = []
butterflies = []  # הוספה כאן!
immunity_time = 0

# יצירת מפת המשחק
game_map = [[None for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

def show_lives_screen(lives, player_image):
    # רקע מדורג כחול-שחור
    for y in range(WINDOW_HEIGHT):
        color = (
            0,
            min(255, int(50 + y/3)),
            min(255, int(100 + y/3))
        )
        pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))
    
    # כותרת גדולה במרכז
    title_font = pygame.font.Font(None, 100)
    text = f"You still have {lives} life left!"
    title = title_font.render(text, True, (255, 215, 0))  # זהב
    
    # צל לטקסט
    title_shadow = title_font.render(text, True, (50, 50, 100))
    
    # מיקום מדויק במרכז
    text_x = WINDOW_WIDTH//2 - title.get_width()//2
    text_y = WINDOW_HEIGHT//2 - title.get_height()//2
    
    screen.blit(title_shadow, (text_x + 3, text_y + 3))
    screen.blit(title, (text_x, text_y))
    
    pygame.display.flip()
    pygame.time.wait(1500)



def show_hit_message():
    # רקע שחור שקוף
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # כותרת גדולה ומהבהבת
    title_font = pygame.font.Font(None, 120)
    text = "OOPS!!!"
    title = title_font.render(text, True, (255, 0, 0))
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//2 - 60))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_end_screen(victory):
    screen.fill(WHITE)
    if victory:
        text = font.render("Victory! You reached the end!", True, (0, 255, 0))
    else:
        text = font.render("Game Over! Try again!", True, (255, 0, 0))
   
    screen.blit(text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)  # מחכים 2 שניות

    running = True
    while running:
        # רקע מדורג
        for y in range(WINDOW_HEIGHT):
            color = (
                min(255, int(50 + y/3)),
                min(255, int(100 + y/3)),
                min(255, int(150 + y/3))
            )
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # כותרת ראשית
        title_font = pygame.font.Font(None, 100)
        if victory:
            text = "Victory!"
            color = (0, 255, 0)
        else:
            text = "Game Over!"
            color = (255, 0, 0)
            
        title = title_font.render(text, True, color)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 200))
        
        # כפתורים
        button_font = pygame.font.Font(None, 50)
        play_again = button_font.render("Play Again", True, (255, 255, 255))
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        
        play_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 350, 200, 50)
        quit_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 450, 200, 50)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # צביעת כפתורים עם אפקט hover
        play_color = (0, 200, 0) if play_rect.collidepoint(mouse_pos) else (0, 150, 0)
        quit_color = (200, 0, 0) if quit_rect.collidepoint(mouse_pos) else (150, 0, 0)
        
        pygame.draw.rect(screen, play_color, play_rect)
        pygame.draw.rect(screen, quit_color, quit_rect)
        
        screen.blit(play_again, (WINDOW_WIDTH//2 - play_again.get_width()//2, 360))
        screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 460))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    return True
                if quit_rect.collidepoint(mouse_pos):
                    return False
    
    return False

# def show_start_screen():
#     # טעינת התמונות של השחקנים
#     player1_img = pygame.image.load('player1.png')
#     player2_img = pygame.image.load('player2.png')
#     player3_img = pygame.image.load('player3.png')
#     custom_img = pygame.image.load('upload.png')

#     players = [
#         pygame.transform.scale(player1_img, (150, 150)),
#         pygame.transform.scale(player2_img, (150, 150)),
#         pygame.transform.scale(player3_img, (150, 150)),
#         pygame.transform.scale(custom_img, (150, 150))

#     ]
    
#     # צבעים מיוחדים
#     TITLE_COLOR = (70, 130, 180)  # כחול פלדה
#     BUTTON_COLOR = (46, 139, 87)   # ירוק ים
#     HOVER_COLOR = (60, 179, 113)   # ירוק בינוני
    
#     # פונטים
#     title_font = pygame.font.Font(None, 74)
#     button_font = pygame.font.Font(None, 50)
    
#     selected = None
#     while True:
#         # רקע מדורג
#         for y in range(WINDOW_HEIGHT):
#             color = (
#                 min(255, int(100 + y/5)),
#                 min(255, int(150 + y/5)),
#                 255
#             )
#             pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))
            
#         # כותרת עם צל
#         title = title_font.render("Choose Your Hero!", True, TITLE_COLOR)
#         title_shadow = title_font.render("Choose Your Hero!", True, (50, 50, 50))
#         screen.blit(title_shadow, (WINDOW_WIDTH//2 - 195, 55))
#         screen.blit(title, (WINDOW_WIDTH//2 - 200, 50))
        
#         # מסגרות דקורטיביות לדמויות
#         box_size = 180  # גודל הריבוע החיצוני
#         spacing = 30    # מרווח בין הריבועים
#         total_width = (box_size * 4) + (spacing * 3)  # סה"כ רוחב של כל הריבועים והמרווחים
#         start_x = (WINDOW_WIDTH - total_width) // 2    # נקודת התחלה שתמרכז את כל המערך

#         for i, player in enumerate(players):
#             x = start_x + (i * (box_size + spacing))
#             y = WINDOW_HEIGHT//2 - box_size//2
            
#             # מסגרת חיצונית
#             pygame.draw.rect(screen, (200, 200, 200), (x, y, box_size, box_size))
#             pygame.draw.rect(screen, (255, 255, 255), (x+5, y+5, box_size-10, box_size-10))
            
#             # הדמות עצמה - ממורכזת בתוך הריבוע
#             player_x = x + (box_size - 150)//2  # מרכוז התמונה בתוך הריבוע
#             player_y = y + (box_size - 150)//2
#             screen.blit(player, (player_x, player_y))
            
#             # מסגרת לדמות נבחרת
#             if selected == i:
#                 pygame.draw.rect(screen, (255, 215, 0), (x, y, box_size, box_size), 4)

#         # כפתורי START ו-Instructions
#         mouse_pos = pygame.mouse.get_pos()
        
#         start_rect = None
#         if selected is not None:
#             start_rect = pygame.Rect(WINDOW_WIDTH//2 - 70, WINDOW_HEIGHT - 120, 140, 50)
#             start_color = HOVER_COLOR if start_rect.collidepoint(mouse_pos) else BUTTON_COLOR
#             pygame.draw.rect(screen, start_color, start_rect, border_radius=10)
#             pygame.draw.rect(screen, (255, 255, 255), start_rect, 3, border_radius=10)
            
#             start_text = button_font.render("START", True, (255, 255, 255))
#             screen.blit(start_text, (WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 110))

#         inst_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 180, 200, 40)
#         inst_color = HOVER_COLOR if inst_rect.collidepoint(mouse_pos) else BUTTON_COLOR
#         pygame.draw.rect(screen, inst_color, inst_rect, border_radius=10)
#         pygame.draw.rect(screen, (255, 255, 255), inst_rect, 3, border_radius=10)
        
#         inst_text = font.render("Instructions", True, (255, 255, 255))
#         screen.blit(inst_text, (WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT - 170))
        
#         pygame.display.flip()
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return None
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 # בדיקת בחירת דמות
#                 for i in range(3):
#                     x = start_x + (i * (box_size + spacing))
#                     y = WINDOW_HEIGHT//2 - box_size//2
#                     if (x < mouse_pos[0] < x + box_size and 
#                         y < mouse_pos[1] < y + box_size):
#                         selected = i
                
#                 # בדיקת לחיצה על כפתורים
#                 if selected is not None and start_rect and start_rect.collidepoint(mouse_pos):
#                     return players[selected]
                    
#                 if inst_rect.collidepoint(mouse_pos):
#                     if not show_instructions_screen():
#                         return None


def show_start_screen():
    button_font = pygame.font.Font(None, 18)  
    # טעינת התמונות של השחקנים
    player1_img = pygame.image.load('player1.png')
    player2_img = pygame.image.load('player2.png')
    player3_img = pygame.image.load('player3.png')
    custom_img = pygame.Surface((150, 150)) # תמונת ברירת מחדל לריבוע הרביעי
    custom_img.fill((200, 200, 200))
    upload_text1 = button_font.render("Upload", True, (0, 0, 0))
    upload_text2 = button_font.render("Your Image", True, (0, 0, 0))
    text_rect1 = upload_text1.get_rect(center=(75, 75))  # מרכז התמונה
    text_rect2 = upload_text2.get_rect(center=(75, 75))  # מרכז התמונה
    custom_img.blit(upload_text1, text_rect1)
    custom_img.blit(upload_text1, text_rect2)
  
    
    # צבעים מיוחדים
    TITLE_COLOR = (70, 130, 180)  # כחול פלדה
    BUTTON_COLOR = (46, 139, 87)   # ירוק ים
    HOVER_COLOR = (60, 179, 113)   # ירוק בינוני
    
    # פונטים
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)
    
    # חישוב מחדש של המיקומים עבור 4 ריבועים
    box_size = int(WINDOW_WIDTH * 0.15)  # 15% מרוחב המסך
    player_size = int(box_size * 0.8)    # 80% מגודל הריבוע
    spacing = int(WINDOW_WIDTH * 0.03)    # 3% מרוחב המסך
    side_margin = int(WINDOW_WIDTH * 0.1)
    total_width = (box_size * 4) + (spacing * 3)
    start_x = (WINDOW_WIDTH - total_width) // 2

    players = [
         pygame.transform.scale(player1_img, (player_size, player_size)),
         pygame.transform.scale(player2_img, (player_size, player_size)),
         pygame.transform.scale(player3_img, (player_size, player_size)),
         pygame.transform.scale(custom_img, (player_size, player_size))
    ]
    selected = None
    while True:
        # רקע מדורג
        for y in range(WINDOW_HEIGHT):
            color = (
                min(255, int(100 + y/5)),
                min(255, int(150 + y/5)),
                255
            )
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))
            
        # כותרת עם צל
        title = title_font.render("Choose Your Hero!", True, TITLE_COLOR)
        title_shadow = title_font.render("Choose Your Hero!", True, (50, 50, 50))
        screen.blit(title_shadow, (WINDOW_WIDTH//2 - 195, 55))
        screen.blit(title, (WINDOW_WIDTH//2 - 200, 50))

        # ציור הריבועים והדמויות
        for i, player in enumerate(players):
            x = start_x + (i * (box_size + spacing))
            y = WINDOW_HEIGHT//2 - box_size//2
            
            # מסגרת חיצונית
            pygame.draw.rect(screen, (200, 200, 200), (x, y, box_size, box_size))
            pygame.draw.rect(screen, (255, 255, 255), (x+5, y+5, box_size-10, box_size-10))
            
            if i == 3:  # הריבוע הרביעי - אפשרות העלאת תמונה
                if isinstance(player, pygame.Surface):  # בודק אם כבר נבחרה תמונה
                    player_x = x + (box_size - player_size)//2
                    player_y = y + (box_size - player_size)//2
                    screen.blit(player, (player_x, player_y))
                
            else:
                player_x = x + (box_size - player_size)//2
                player_y = y + (box_size - player_size)//2
                screen.blit(player, (player_x, player_y))
                
            if selected == i:
                pygame.draw.rect(screen, (255, 215, 0), (x, y, box_size, box_size), 4)


        # כפתורי START ו-Instructions
        mouse_pos = pygame.mouse.get_pos()
        
        start_rect = None
        if selected is not None:
            start_rect = pygame.Rect(WINDOW_WIDTH//2 - 70, WINDOW_HEIGHT - 120, 140, 50)
            start_color = HOVER_COLOR if start_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, start_color, start_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), start_rect, 3, border_radius=10)
            
            start_text = button_font.render("START", True, (255, 255, 255))
            screen.blit(start_text, (WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 110))

        inst_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 180, 200, 40)
        inst_color = HOVER_COLOR if inst_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, inst_color, inst_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), inst_rect, 3, border_radius=10)
        
        inst_text = font.render("Instructions", True, (255, 255, 255))
        screen.blit(inst_text, (WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT - 170))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                # בדיקת בחירת דמות
                for i in range(4):
                    x = start_x + (i * (box_size + spacing))
                    y = WINDOW_HEIGHT//2 - box_size//2
                    if (x < mouse_pos[0] < x + box_size and 
                        y < mouse_pos[1] < y + box_size):
                        if i == 3:  # לחיצה על ריבוע העלאת תמונה
                            from tkinter import filedialog
                            import tkinter as tk
                            root = tk.Tk()
                            root.withdraw()
                            file_path = filedialog.askopenfilename(
                                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
                            )
                            if file_path:
                                custom_player = pygame.image.load(file_path)
                                players[3] = pygame.transform.scale(custom_player, (150, 150))
                        selected = i
                
                # בדיקת לחיצה על כפתורים
                if selected is not None and start_rect and start_rect.collidepoint(mouse_pos):
                    return players[selected]
                    
                if inst_rect.collidepoint(mouse_pos):
                    if not show_instructions_screen():
                        return None




def show_instructions_screen():
    TITLE_COLOR = (70, 130, 180)
    BUTTON_COLOR = (46, 139, 87)
    HOVER_COLOR = (60, 179, 113)
    
    scroll_y = 0
    scroll_speed = 20
    
    instructions = [
        "Controls:",
        "→ Right Arrow: Move right",
        "SPACE: Jump",
        "ENTER: Shoot",
        "",
        "Goal:",
        "Reach the end of the level while avoiding or shooting obstacles",
        "",
        "Obstacles:",
        "Butterflies - Flying enemies",
        "Mushrooms - Ground obstacles",
        "Snails - Slow moving enemies",
        "",
        "Score: +10 points for each destroyed obstacle",
        "Lives: You have 3 lives - Don't touch the obstacles!"
    ]
    
    # Calculate total content height
    content_height = len(instructions) * 30 + 200
    max_scroll = max(0, content_height - (WINDOW_HEIGHT - 200))
    
    while True:
        for y in range(WINDOW_HEIGHT):
            color = (
                min(255, int(100 + y/5)),
                min(255, int(150 + y/5)),
                255
            )
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))
            
        # Title
        title = font.render("Game Instructions", True, TITLE_COLOR)
        screen.blit(title, (WINDOW_WIDTH//2 - 100, 50))
        
        # Content area with clipping
        content_surface = pygame.Surface((WINDOW_WIDTH-100, WINDOW_HEIGHT-200))
        content_surface.fill((255, 255, 255))
        
        # Draw instructions on content surface
        for i, line in enumerate(instructions):
            text = font.render(line, True, (0, 0, 0))
            content_surface.blit(text, (20, i * 30 - scroll_y))
        
        # Draw content area with border
        pygame.draw.rect(screen, (200, 200, 200), (50, 100, WINDOW_WIDTH-100, WINDOW_HEIGHT-200))
        screen.blit(content_surface, (50, 100))
        
        # Back button
        back_rect = pygame.Rect(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 60, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        back_color = HOVER_COLOR if back_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (WINDOW_WIDTH//2 - 25, WINDOW_HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse_pos):
                    return True
                if event.button == 4:  # Mouse wheel up
                    scroll_y = max(0, scroll_y - scroll_speed)
                if event.button == 5:  # Mouse wheel down
                    scroll_y = min(max_scroll, scroll_y + scroll_speed)


def add_obstacle_to_map(x, y, type):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        game_map[x][y] = {'type': type, 'alive': True}

# נעדכן את פונקציית draw_butterfly כדי להוסיף צבע כפרמטר
def draw_butterfly(surface, x, y, is_moving=False):
    color = (147, 112, 219) if is_moving else (255, 192, 203)  # סגול לזזים, ורוד לעומדים
    pygame.draw.circle(surface, color, (x-10, y), 10)
    pygame.draw.circle(surface, color, (x+10, y), 10)
    pygame.draw.line(surface, (0, 0, 0), (x, y-5), (x, y+5), 2)

def draw_snail(surface, x, y, direction):
    if direction > 0:
        pygame.draw.ellipse(surface, (150, 75, 0), (x, y, 40, 30))
        pygame.draw.circle(surface, (165, 42, 42), (x+10, y+10), 20)
        pygame.draw.circle(surface, (139, 69, 19), (x+10, y+10), 15)
        pygame.draw.line(surface, (150, 75, 0), (x+35, y+10), (x+45, y-5), 3)
        pygame.draw.line(surface, (150, 75, 0), (x+35, y+10), (x+45, y+5), 3)
        pygame.draw.circle(surface, (0, 0, 0), (x+38, y+8), 3)
    else:
        pygame.draw.ellipse(surface, (150, 75, 0), (x, y, 40, 30))
        pygame.draw.circle(surface, (165, 42, 42), (x+30, y+10), 20)
        pygame.draw.circle(surface, (139, 69, 19), (x+30, y+10), 15)
        pygame.draw.line(surface, (150, 75, 0), (x+5, y+10), (x-5, y-5), 3)
        pygame.draw.line(surface, (150, 75, 0), (x+5, y+10), (x-5, y+5), 3)
        pygame.draw.circle(surface, (0, 0, 0), (x+2, y+8), 3)

def draw_mushroom(surface, x, y):
    pygame.draw.rect(surface, (255, 255, 255), (x+10, y+20, 20, 30))
    pygame.draw.circle(surface, (255, 0, 0), (x+20, y+20), 25)
    pygame.draw.circle(surface, (255, 255, 255), (x+10, y+15), 5)
    pygame.draw.circle(surface, (255, 255, 255), (x+30, y+15), 5)
    pygame.draw.circle(surface, (255, 255, 255), (x+20, y+25), 5)


# הוספת מטבעות
coins = []
for x in range(SAFE_ZONE, 5000, 100):
    if random.random() > 0.5:
        coins.append({
            'x': x,
            'y': random.randint(WINDOW_HEIGHT - 300, WINDOW_HEIGHT - GROUND_HEIGHT - 50),
            'collected': False
        })


def draw_coin(surface, x, y):
    pygame.draw.circle(surface, (255, 215, 0), (x, y), 12)  # מטבע זהב מבריק
    pygame.draw.circle(surface, YELLOW, (x, y), 10)


# Create background
background = pygame.Surface((MAP_WIDTH, WINDOW_HEIGHT))

# שכבת שמיים עם גוונים משתנים
for x in range(0, MAP_WIDTH, 50):
    r = min(255, 100 + x//40)
    g = min(255, 180 + x//60)
    b = 255
    color = (r, g, b)
    pygame.draw.rect(background, color, (x, 0, 50, WINDOW_HEIGHT))

# הוספת עננים
for i in range(30):
    cloud_x = random.randint(0, MAP_WIDTH-200)
    cloud_y = random.randint(50, 200)
    pygame.draw.ellipse(background, WHITE, (cloud_x, cloud_y, 200, 60))

# הוספת הרים
for i in range(20):
    mountain_x = random.randint(0, MAP_WIDTH-400)
    pygame.draw.polygon(background, (100, 100, 100), 
                       [(mountain_x, WINDOW_HEIGHT-100), 
                        (mountain_x + 200, 100), 
                        (mountain_x + 400, WINDOW_HEIGHT-100)])

# הוספת פרפרים (רק אחרי אזור בטוח)
butterflies = []
for i in range(40):
    butterfly_x = random.randint(SAFE_ZONE, 4800)
    butterfly_y = random.randint(100, 400)
    butterflies.append(Butterfly(butterfly_x, butterfly_y))
    obstacles.append({
        'x': butterfly_x,
        'y': butterfly_y,
        'width': 15,
        'height': 15,
        'type': 'butterfly'
    })

# בתחילת המשחק, אחרי הוספת הפרפרים
# הוספת פטריות
for x in range(SAFE_ZONE, MAP_WIDTH-100, 120):
    if random.random() > 0.3:
        mushroom_y = WINDOW_HEIGHT - GROUND_HEIGHT - 50
        obstacles.append({
            'x': x,
            'y': mushroom_y,
            'width': 40,
            'height': 50,
            'type': 'mushroom'
        })

# הוספת חלזונות
for x in range(SAFE_ZONE, MAP_WIDTH-100, 180):
    if random.random() > 0.4:
        snail_y = WINDOW_HEIGHT - GROUND_HEIGHT - 30
        obstacles.append({
            'x': x,
            'y': snail_y,
            'width': 40,
            'height': 30,
            'type': 'snail'
        })


# הוספה אחרי יצירת הפרפרים
coins = []
for x in range(SAFE_ZONE, 5000, 100):
    if random.random() > 0.5:
        coin_y = random.randint(WINDOW_HEIGHT - 300, WINDOW_HEIGHT - GROUND_HEIGHT - 50)
        coins.append({'x': x, 'y': coin_y, 'collected': False})


# קרקע
pygame.draw.rect(background, (34, 139, 34), (0, WINDOW_HEIGHT-GROUND_HEIGHT, MAP_WIDTH, GROUND_HEIGHT))
for x in range(0, MAP_WIDTH, 30):
    pygame.draw.line(background, (28, 120, 28), 
                    (x, WINDOW_HEIGHT-GROUND_HEIGHT), 
                    (x+15, WINDOW_HEIGHT-GROUND_HEIGHT+10), 2)

# הוספת מכשולים למפה
for i in range(40):
    butterfly_x = random.randint(SAFE_ZONE, MAP_WIDTH-200)
    butterfly_y = random.randint(100, 400)
    add_obstacle_to_map(butterfly_x, butterfly_y, 'butterfly')

# בתחילת המשחק, כשמוסיפים מכשולים
for x in range(SAFE_ZONE, MAP_WIDTH-100, 120):
    if random.random() > 0.3:
        y = WINDOW_HEIGHT - GROUND_HEIGHT - 50
        obstacles.append({
            'x': x,
            'y': y,
            'width': 40,
            'height': 50,
            'type': 'mushroom'
        })

for x in range(SAFE_ZONE, MAP_WIDTH-100, 180):
    if random.random() > 0.4:
        y = WINDOW_HEIGHT - GROUND_HEIGHT - 30
        obstacles.append({
            'x': x,
            'y': y,
            'width': 40,
            'height': 30,
            'type': 'snail'
        })


# Bullets
bullets = []
BULLET_SPEED = 10
BULLET_SIZE = 15

# Score and Lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

def draw_map_obstacles(screen, bg_x):
    start_x = max(0, int(bg_x))
    end_x = min(MAP_WIDTH, int(bg_x + WINDOW_WIDTH))
    
    for x in range(start_x, end_x):
        for y in range(MAP_HEIGHT):
            obstacle = game_map[x][y]
            if obstacle and obstacle['alive']:
                screen_x = x - bg_x
                if obstacle['type'] == 'butterfly':
                    draw_butterfly(screen, screen_x, y)
                elif obstacle['type'] == 'mushroom':
                    draw_mushroom(screen, screen_x, y)
                elif obstacle['type'] == 'snail':
                    draw_snail(screen, screen_x, y, 1)

def check_bullet_hit(bullet_x, bullet_y):
    # הגדלת טווח הבדיקה
    for dx in range(-40, 41):
        for dy in range(-40, 41):
            check_x = int(bullet_x + dx)
            check_y = int(bullet_y + dy)
            if 0 <= check_x < MAP_WIDTH and 0 <= check_y < MAP_HEIGHT:
                obstacle = game_map[check_x][check_y]
                if obstacle and obstacle['alive']:
                    obstacle['alive'] = False
                    hit_sound.play()
                    return True
    return False


def adjust_background_volume(volume):
    background_sound.set_volume(volume)


# def check_bullet_hit(bullet_x, bullet_y):
#     bullet_rect = pygame.Rect(bullet_x, bullet_y, BULLET_SIZE, BULLET_SIZE)
#     for obstacle in obstacles[:]:
#         obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], 
#                                   obstacle['width'], obstacle['height'])
#         if bullet_rect.colliderect(obstacle_rect):
#             obstacles.remove(obstacle)
#             return True
#     return False


running = True
clock = pygame.time.Clock()

def main():

    pygame.init()
    pygame.display.init()
    # Get selected player image
    player_image = show_start_screen()
    if player_image is None:
        return
    
        # אתחול המשחק
    initialize_game()
    # Game variables
    bg_width = 5000
    bg_x = 0
    player_width = 150
    player_height = 150
    player_x = 50
    player_world_x = 50
    player_y = WINDOW_HEIGHT - GROUND_HEIGHT - player_height + 20
    player_speed = 5
    player_jump = -15
    player_velocity = 0
    gravity = 0.8
    immunity_time = 0
    score = 0
    lives = 3
    bullets = []
    running = True
    clock = pygame.time.Clock()

    # def check_player_collision(player_world_x, player_y):
    #     # מיקום מדויק יותר של מרכז השחקן
    #     center_x = player_world_x + player_width // 2
    #     center_y = player_y + player_height // 2
        
    #     # בדיקה במרחב סביב מרכז השחקן
    #     for dx in range(-35, 36):
    #         for dy in range(-35, 36):
    #             check_x = int(center_x + dx)
    #             check_y = int(center_y + dy)
    #             if 0 <= check_x < MAP_WIDTH and 0 <= check_y < MAP_HEIGHT:
    #                 obstacle = game_map[check_x][check_y]
    #                 if obstacle and obstacle['alive']:
    #                     return True
    #     return False
    # def check_player_collision(x, y):
    #     player_rect = pygame.Rect(x, y, player_width-80, player_height-80)
    #     for obstacle in obstacles:
    #         obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], 
    #                                   obstacle['width'], obstacle['height'])
    #         if player_rect.colliderect(obstacle_rect):
    #             return True
    #     return False

    def check_player_collision(x, y):
        player_rect = pygame.Rect(x + 40, y + 40, player_width-80, player_height-80)
    
    # בדיקת התנגשות עם כל סוגי המכשולים
        for obstacle in obstacles:
            if obstacle['type'] in ['mushroom', 'snail']:
                obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], 
                                          obstacle['width'], obstacle['height'])
                if player_rect.colliderect(obstacle_rect):
                    return True
        return False

   
    def shoot():
        background_sound.stop()  # עוצר את מוזיקת הרקע
        hit_sound.play()       # משמיע את צליל הירייה
        bullet = {
         'x': player_x + player_width - 20,
        'y': player_y + player_height-40,
         'world_x': player_world_x + player_width,
         'rect': pygame.Rect(player_x + player_width - 20, 
                           player_y + player_height-40, 
                           BULLET_SIZE, BULLET_SIZE)
        }
        bullets.append(bullet)
        pygame.time.set_timer(pygame.USEREVENT + 1, 300)  # טיימר להחזרת הווליום

    while running:
        background_sound.play()
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE and player_y >= WINDOW_HEIGHT - GROUND_HEIGHT - player_height + 20:
        #             adjust_background_volume(0.1)  # הנמכת הווליום
        #             player_velocity = player_jump
        #             jump_sound.play()
        #             pygame.time.set_timer(pygame.USEREVENT + 1, 500) 
        #         if event.key == pygame.K_RETURN:
        #             shoot()    
        # In your main game loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_y >= WINDOW_HEIGHT - GROUND_HEIGHT - player_height + 20:
                    background_sound.stop()  # Stop background music
                    player_velocity = player_jump
                    jump_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Timer to resume music
                if event.key == pygame.K_RETURN:
                    background_sound.stop()  # Stop background music
                    shoot()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Timer to resume music
            elif event.type == pygame.USEREVENT + 2:
                background_sound.set_volume(0.3)  # Resume background music
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Cancel timer


        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player_world_x < bg_width - player_width:
            player_world_x += player_speed
            if player_x < WINDOW_WIDTH * 0.4:
                player_x += player_speed
            else:
                bg_x += player_speed

        # Gravity
        player_velocity += gravity
        player_y += player_velocity
        if player_y > WINDOW_HEIGHT - GROUND_HEIGHT - player_height + 20:
            player_y = WINDOW_HEIGHT - GROUND_HEIGHT - player_height + 20
            player_velocity = 0

        # #     # Update bullets
        # for bullet in bullets[:]:
        #     bullet['x'] += BULLET_SPEED
        #     bullet['world_x'] += BULLET_SPEED
        #     bullet['rect'].x = bullet['x']
                  
        #     if check_bullet_hit(bullet['world_x'], bullet['y']):
        #         bullets.remove(bullet)
        #         score += 10
        #     elif bullet['x'] > WINDOW_WIDTH:
        #         bullets.remove(bullet)

        # Update bullets
    # Update bullets
        for bullet in bullets[:]:
            bullet['x'] += BULLET_SPEED
            bullet['world_x'] += BULLET_SPEED
            bullet['rect'].x = bullet['x']
                   
            if check_bullet_hit(bullet['world_x'], bullet['y']):
                bullets.remove(bullet)
                score += 10
            elif bullet['x'] > WINDOW_WIDTH:
                bullets.remove(bullet)

            
            # בדיקת פגיעה במכשולים
            for obstacle in obstacles[:]:
                obstacle_rect = pygame.Rect(obstacle['x'] - bg_x, obstacle['y'], 
                                      obstacle['width'], obstacle['height'])
                if bullet['rect'].colliderect(obstacle_rect):
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)
                    score += 10
                    break



         # Update butterflies position
        for butterfly in butterflies:
            draw_butterfly(screen, butterfly.x - bg_x, butterfly.y, True)
            butterfly.update()
            for obstacle in obstacles:
                if obstacle['type'] == 'butterfly' and obstacle['x'] == butterfly.x:
                    obstacle['y'] = butterfly.y
        

        # בדיקת איסוף מטבעות
        for coin in coins[:]:
            if not coin['collected']:
                coin_rect = pygame.Rect(coin['x'] - bg_x, coin['y'], 20, 20)
                player_rect = pygame.Rect(player_x + 40, player_y + 40, 
                                          player_width - 80, player_height - 80)
                if player_rect.colliderect(coin_rect):
                    coin['collected'] = True
                    score += 5
                    background_sound.stop()
                    coin_sound.play()
                    background_sound.play()
        # # Collision detection
        # if immunity_time <= 0:
        #     if check_player_collision(player_world_x, player_y):
        #         lives -= 1
        #         immunity_time = 60
        #         if lives <= 0:
        #             show_end_screen(False)
        #             running = False
        # else:
        #     immunity_time -= 1
      # Collision detection
        # בבדיקת ההתנגשויות
        # בבדיקת ההתנגשויות
        # בבדיקת ההתנגשויות בלולאת המשחק
        # בלולאת המשחק, נשנה את בדיקת ההתנגשות
        if immunity_time <= 0:
            player_rect = pygame.Rect(player_x + 40, player_y + 40,
                                    player_width - 80, player_height - 80)
            
            for obstacle in obstacles:
                screen_x = obstacle['x'] - bg_x
                if 0 <= screen_x <= WINDOW_WIDTH:
                    obstacle_rect = pygame.Rect(screen_x, obstacle['y'],
                                              obstacle['width'], obstacle['height'])
                    if player_rect.colliderect(obstacle_rect):
                        lives -= 1
                        immunity_time = 60
                        hit_sound.play()
                        show_hit_message()
                        show_lives_screen(lives, player_image)
                        initialize_game()  # מאתחל את המשחק
                        player_world_x = 50
                        player_x = 50
                        bg_x = 0
                        if lives <= 0:
                            show_end_screen(False)
                            running = False
                        break
        else:
            immunity_time -= 1

        # Check for victory
        if player_world_x >= MAP_WIDTH - player_width:
            show_end_screen(True)
            running = False

         # Drawing
         # חלק הציור בלולאת המשחק
        screen.blit(background, (-bg_x, 0))
        
        # ציור כל המכשולים
        for obstacle in obstacles:
            screen_x = obstacle['x'] - bg_x
            if 0 <= screen_x <= WINDOW_WIDTH:  # מציירים רק אם המכשול נראה במסך
                if obstacle['type'] == 'butterfly':
                    draw_butterfly(screen, screen_x, obstacle['y'], True)
                elif obstacle['type'] == 'mushroom':
                    draw_mushroom(screen, screen_x, obstacle['y'])
                elif obstacle['type'] == 'snail':
                    draw_snail(screen, screen_x, obstacle['y'], 1)
        

        # Draw player and bullets
        if immunity_time % 4 < 2 or immunity_time == 0:
            screen.blit(player_image, (player_x, player_y))
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet['rect'])
# בלולאת המשחק, בחלק של הציור
        for coin in coins:
            if not coin['collected']:
                draw_coin(screen, coin['x'] - bg_x, coin['y'])

        # Display score and lives
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        lives_text = font.render(f'Lives: {lives}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if lives <= 0 or player_world_x >= MAP_WIDTH - player_width:
            if show_end_screen(player_world_x >= MAP_WIDTH - player_width):
                main()  # התחל משחק חדש
            else:
                running = False  # צא מהמשחק

        pygame.display.flip()
        clock.tick(60)

    create_shortcut()
    pygame.quit()


if __name__ == "__main__":
    main()
    try:
        create_shortcut()
    except:
        pass
    pygame.quit()
