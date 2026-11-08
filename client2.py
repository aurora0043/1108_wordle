# client.py
import sys
import os
import pygame
import requests

API_BASE_URL = "http://127.0.0.1:8000"

COLOR_BG = (18, 18, 19)
COLOR_TEXT = (255, 255, 255)
COLOR_EMPTY = (58, 58, 60)
COLOR_CORRECT = (83, 141, 78)
COLOR_PRESENT = (181, 159, 59)
COLOR_ABSENT = (58, 58, 60)

pygame.init()
WIDTH, HEIGHT = 500, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Wordle + FastAPI Client")
font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

class WordleGame:
    def __init__(self):
        self.game_id = None
        self.grid = [["" for _ in range(5)] for _ in range(6)]
        self.colors = [[COLOR_EMPTY for _ in range(5)] for _ in range(6)]
        self.row = 0
        self.col = 0
        self.game_over = False
        self.message = "Press ENTER to submit, R to restart"
        self.start_new_game()

    def start_new_game(self):
        try:
            res = requests.post(f"{API_BASE_URL}/api/new-game", timeout=60)
            if res.status_code == 200:
                self.game_id = res.json()["game_id"]
                self.grid = [["" for _ in range(5)] for _ in range(6)]
                self.colors = [[COLOR_EMPTY for _ in range(5)] for _ in range(6)]
                self.row = 0
                self.col = 0
                self.game_over = False
                self.message = "New game started!"
            else:
                self.message = "Server error starting new game."
        except requests.exceptions.RequestException:
            self.message = "Cannot connect to FastAPI server!"

    def submit_guess(self):
        if self.col < 5:
            self.message = "Not enough letters!"
            return

        guess_word = "".join(self.grid[self.row])
        try:
            payload = {"game_id": self.game_id, "guess": guess_word}
            res = requests.post(f"{API_BASE_URL}/api/guess", json=payload, timeout=60)
            
            if res.status_code == 200:
                data = res.json()
                feedback = data["feedback"]
                
                for i in range(5):
                    if feedback[i] == "correct":
                        self.colors[self.row][i] = COLOR_CORRECT
                    elif feedback[i] == "present":
                        self.colors[self.row][i] = COLOR_PRESENT
                    else:
                        self.colors[self.row][i] = COLOR_ABSENT

                if data["is_correct"]:
                    self.message = "Congratulations! You won! Press R to restart."
                    self.game_over = True
                else:
                    self.row += 1
                    self.col = 0
                    if self.row == 6:
                        self.message = "Game Over! Press R to restart."
                        self.game_over = True
                    else:
                        self.message = "Keep guessing!"
            else:
                self.message = res.json().get("detail", "Error processing guess")
        except requests.exceptions.RequestException:
            self.message = "Network error during guess!"

    def handle_keydown(self, event):
        # --- 防呆機制 1：遊戲結束狀態 ---
        # 如果遊戲已經結束，只允許按 R 重新開始，忽略其他按鍵
        if self.game_over:
            if event.key == pygame.K_r:
                self.start_new_game()
            return

        # --- 以下為遊戲「進行中」的狀態 ---
        
        # 處理刪除鍵 (Backspace)
        if event.key == pygame.K_BACKSPACE:
            if self.col > 0:
                self.col -= 1
                self.grid[self.row][self.col] = ""
                self.message = "Keep typing..." # 刪除後恢復提示
                
        # 處理送出鍵 (Enter)
        elif event.key == pygame.K_RETURN:
            # 防呆機制 2：確認字數是否填滿，沒填滿 5 個字不准送出，並跳出警告
            if self.col < 5:
                self.message = "Not enough letters! Need 5 letters."
            else:
                self.message = "Checking..."
                self.submit_guess()
                
        # 處理一般字母輸入 (包含 R)
        elif event.unicode.isalpha() and len(event.unicode) == 1:
            # 防呆機制 3：限制每一列只能輸入 5 個字，超過就不會有反應
            if self.col < 5:
                self.grid[self.row][self.col] = event.unicode.upper()
                self.col += 1
                
                # 如果剛好打滿 5 個字，提示玩家可以按 Enter 了
                if self.col == 5:
                    self.message = "Press ENTER to submit!"

    def draw(self, surface):
        surface.fill(COLOR_BG)
        margin_x, margin_y = 75, 50
        box_size = 60
        gap = 10
        for r in range(6):
            for c in range(5):
                x = margin_x + c * (box_size + gap)
                y = margin_y + r * (box_size + gap)
                rect = pygame.Rect(x, y, box_size, box_size)
                
                pygame.draw.rect(surface, self.colors[r][c], rect, border_radius=4)
                if self.colors[r][c] == COLOR_EMPTY:
                    pygame.draw.rect(surface, (80, 80, 80), rect, width=2, border_radius=4)

                char = self.grid[r][c]
                if char:
                    text_surface = font.render(char, True, COLOR_TEXT)
                    text_rect = text_surface.get_rect(center=rect.center)
                    surface.blit(text_surface, text_rect)

        msg_surface = small_font.render(self.message, True, COLOR_TEXT)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        surface.blit(msg_surface, msg_rect)

def main():
    clock = pygame.time.Clock()
    game = WordleGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.handle_keydown(event)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()