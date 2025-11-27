import pygame
import random
import sys

# --- 상수 정의 ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
BOARD_WIDTH = GRID_WIDTH * BLOCK_SIZE
BOARD_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# 색상 (R, G, B)
BLACK = (26, 26, 46)  # 배경색 (#1a1a2e)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRID_COLOR = (40, 40, 60)
TEXT_COLOR = (255, 215, 0) # Gold (#ffd700)

# 블록 색상 (Neon Style)
COLORS = [
    (0, 0, 0),          # 0: Empty
    (0, 255, 255),      # 1: I - Neon Cyan
    (255, 255, 0),      # 2: O - Neon Yellow
    (200, 0, 255),      # 3: T - Neon Purple
    (57, 255, 20),      # 4: S - Neon Green
    (255, 0, 60),       # 5: Z - Neon Red
    (0, 100, 255),      # 6: J - Neon Blue
    (255, 100, 0)       # 7: L - Neon Orange
]

# 블록 모양
SHAPES = [
    [], # 0: Empty
    [[1, 1, 1, 1]], # I
    [[2, 2], [2, 2]], # O
    [[0, 3, 0], [3, 3, 3]], # T
    [[0, 4, 4], [4, 4, 0]], # S
    [[5, 5, 0], [0, 5, 5]], # Z
    [[6, 0, 0], [6, 6, 6]], # J
    [[0, 0, 7], [7, 7, 7]]  # L
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('malgungothic', 20)
        self.title_font = pygame.font.SysFont('malgungothic', 40, bold=True)
        
        # 키 반복 입력 설정 (딜레이 300ms, 간격 50ms)
        pygame.key.set_repeat(300, 50)
        
        self.reset_game()

    def reset_game(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines = 0
        self.hold_piece = None
        self.can_hold = True
        
        self.next_pieces = []
        self.next_pieces = [self.get_new_piece() for _ in range(5)]
        self.current_piece = self.get_new_piece()
        
        self.drop_time = 0
        self.drop_speed = 1000 # ms

    def get_new_piece(self):
        if self.next_pieces:
            piece = self.next_pieces.pop(0)
            self.next_pieces.append(self.create_random_piece())
            return piece
        return self.create_random_piece()

    def create_random_piece(self):
        shape_idx = random.randint(1, 7)
        shape = SHAPES[shape_idx]
        return {
            'shape': shape,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0,
            'color': shape_idx
        }

    def rotate_piece(self, piece):
        # 행과 열을 전치하고 각 행을 뒤집음 (시계 방향 회전)
        shape = piece['shape']
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        return rotated_shape

    def valid_move(self, piece, x, y, shape=None):
        if shape is None:
            shape = piece['shape']
        
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_x = x + c
                    new_y = y + r
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        for r, row in enumerate(self.current_piece['shape']):
            for c, val in enumerate(row):
                if val:
                    self.board[self.current_piece['y'] + r][self.current_piece['x'] + c] = self.current_piece['color']
        
        self.clear_lines()
        self.current_piece = self.get_new_piece()
        self.can_hold = True
        
        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        new_board = [row for row in self.board if any(x == 0 for x in row)]
        lines_cleared = GRID_HEIGHT - len(new_board)
        
        if lines_cleared > 0:
            for _ in range(lines_cleared):
                new_board.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.board = new_board
            self.lines += lines_cleared
            self.score += [0, 100, 300, 500, 800][lines_cleared] * self.level
            self.level = self.lines // 10 + 1
            self.drop_speed = max(100, 1000 - (self.level - 1) * 100)

    def hold(self):
        if not self.can_hold:
            return
        
        if self.hold_piece is None:
            self.hold_piece = {
                'shape': self.current_piece['shape'],
                'color': self.current_piece['color'],
                'x': 0, 'y': 0 # 위치는 나중에 재설정
            }
            self.current_piece = self.get_new_piece()
        else:
            # 현재 블록과 보관 블록 교체 (모양과 색상만)
            temp_shape = self.current_piece['shape']
            temp_color = self.current_piece['color']
            
            self.current_piece['shape'] = self.hold_piece['shape']
            self.current_piece['color'] = self.hold_piece['color']
            
            self.hold_piece['shape'] = temp_shape
            self.hold_piece['color'] = temp_color
            
            # 위치 초기화
            self.current_piece['x'] = GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2
            self.current_piece['y'] = 0
            
        self.can_hold = False

    def hard_drop(self):
        while self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
            self.current_piece['y'] += 1
            self.score += 2
        self.lock_piece()

    def draw_grid(self, surface, x_offset, y_offset):
        pygame.draw.rect(surface, BLACK, (x_offset, y_offset, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(surface, WHITE, (x_offset, y_offset, BOARD_WIDTH, BOARD_HEIGHT), 2)
        
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                val = self.board[r][c]
                if val:
                    self.draw_block(surface, x_offset + c * BLOCK_SIZE, y_offset + r * BLOCK_SIZE, val)
                else:
                    pygame.draw.rect(surface, GRID_COLOR, (x_offset + c * BLOCK_SIZE, y_offset + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # 고스트 블럭 그리기
        if self.current_piece:
            ghost_y = self.current_piece['y']
            while self.valid_move(self.current_piece, self.current_piece['x'], ghost_y + 1):
                ghost_y += 1
            
            # 고스트 블럭은 현재 블럭과 겹치지 않을 때만 그리기 (선택 사항, 여기서는 항상 그림)
            for r, row in enumerate(self.current_piece['shape']):
                for c, val in enumerate(row):
                    if val:
                        self.draw_ghost_block(surface, x_offset + (self.current_piece['x'] + c) * BLOCK_SIZE, 
                                              y_offset + (ghost_y + r) * BLOCK_SIZE, 
                                              self.current_piece['color'])

        # 현재 블록 그리기
        if self.current_piece:
            for r, row in enumerate(self.current_piece['shape']):
                for c, val in enumerate(row):
                    if val:
                        self.draw_block(surface, x_offset + (self.current_piece['x'] + c) * BLOCK_SIZE, 
                                        y_offset + (self.current_piece['y'] + r) * BLOCK_SIZE, 
                                        self.current_piece['color'])

    def draw_block(self, surface, x, y, color_idx):
        color = COLORS[color_idx]
        
        # 1. 내부 채우기 (약간 어둡게 하여 테두리가 빛나 보이게 함)
        # 색상의 밝기를 줄임
        darker_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))
        pygame.draw.rect(surface, darker_color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        
        # 2. 메인 테두리 (네온 색상) - 두껍게
        pygame.draw.rect(surface, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 3)
        
        # 3. 내부 하이라이트 (흰색) - 네온 튜브 느낌
        pygame.draw.rect(surface, (255, 255, 255), (x + 5, y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), 1)
        
        # 4. 모서리 광택 (선택 사항)
        pygame.draw.circle(surface, (255, 255, 255), (x + 3, y + 3), 1)

    def draw_ghost_block(self, surface, x, y, color_idx):
        # 고스트 블럭은 테두리만 그림 (회색)
        color = GRAY
        pygame.draw.rect(surface, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2)  # 테두리만

    def draw_preview(self, surface, x, y, title, pieces):
        pygame.draw.rect(surface, BLACK, (x, y, 150, 500))
        pygame.draw.rect(surface, WHITE, (x, y, 150, 500), 2)
        
        text = self.font.render(title, True, TEXT_COLOR)
        surface.blit(text, (x + 10, y + 10))
        
        start_y = y + 40
        for i, piece in enumerate(pieces):
            shape = piece['shape']
            color = piece['color']
            
            # 중앙 정렬 계산
            piece_width = len(shape[0]) * BLOCK_SIZE
            piece_height = len(shape) * BLOCK_SIZE
            draw_x = x + (150 - piece_width) // 2
            draw_y = start_y + i * 90 # 간격
            
            for r, row in enumerate(shape):
                for c, val in enumerate(row):
                    if val:
                        self.draw_block(surface, draw_x + c * BLOCK_SIZE, draw_y + r * BLOCK_SIZE, color)

    def draw_hold(self, surface, x, y):
        pygame.draw.rect(surface, BLACK, (x, y, 150, 150))
        pygame.draw.rect(surface, WHITE, (x, y, 150, 150), 2)
        
        text = self.font.render("보관함 (Hold)", True, TEXT_COLOR)
        surface.blit(text, (x + 10, y + 10))
        
        if self.hold_piece:
            shape = self.hold_piece['shape']
            color = self.hold_piece['color']
            
            piece_width = len(shape[0]) * BLOCK_SIZE
            draw_x = x + (150 - piece_width) // 2
            draw_y = y + 50
            
            for r, row in enumerate(shape):
                for c, val in enumerate(row):
                    if val:
                        self.draw_block(surface, draw_x + c * BLOCK_SIZE, draw_y + r * BLOCK_SIZE, color)

    def draw_info(self, surface, x, y):
        infos = [
            f"점수: {self.score}",
            f"레벨: {self.level}",
            f"라인: {self.lines}"
        ]
        
        start_y = y
        for info in infos:
            text = self.font.render(info, True, WHITE)
            surface.blit(text, (x, start_y))
            start_y += 40

    def draw_controls(self, surface, x, y):
        controls = [
            "조작법:",
            "← → : 이동",
            "↑ : 회전",
            "↓ : 빠른 낙하",
            "Space : 즉시 낙하",
            "C : 보관/교체",
            "P : 일시정지"
        ]
        start_y = y
        for line in controls:
            text = self.font.render(line, True, WHITE)
            surface.blit(text, (x, start_y))
            start_y += 30

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    
                    if not self.game_over and not self.paused:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1
                                self.score += 1
                        elif event.key == pygame.K_UP:
                            rotated = self.rotate_piece(self.current_piece)
                            if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'], rotated):
                                self.current_piece['shape'] = rotated
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()
                        elif event.key == pygame.K_c:
                            self.hold()
                    
                    if self.game_over and event.key == pygame.K_r:
                        self.reset_game()

            # 게임 로직 업데이트
            if not self.game_over and not self.paused:
                if current_time - self.drop_time > self.drop_speed:
                    if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                        self.current_piece['y'] += 1
                    else:
                        self.lock_piece()
                    self.drop_time = current_time

            # 화면 그리기
            self.screen.fill(BLACK)
            
            # 레이아웃 배치
            # 왼쪽: 보관함 + 정보
            self.draw_hold(self.screen, 50, 50)
            self.draw_info(self.screen, 50, 250)
            
            # 중앙: 게임 보드
            board_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
            self.draw_grid(self.screen, board_x, 50)
            
            # 오른쪽: 다음 블록 + 조작법
            self.draw_preview(self.screen, SCREEN_WIDTH - 200, 50, "다음 블록", self.next_pieces)
            self.draw_controls(self.screen, SCREEN_WIDTH - 200, 600)

            # 게임 오버 메시지
            if self.game_over:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
                score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
                restart_text = self.font.render("R 키를 눌러 다시 시작", True, WHITE)
                
                self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
                self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
                self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
            
            # 일시정지 메시지
            if self.paused and not self.game_over:
                pause_text = self.title_font.render("PAUSED", True, WHITE)
                self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.run()
