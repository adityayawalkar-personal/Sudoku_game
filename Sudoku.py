import arcade
import random
import time
import math

# --- CONFIGURATION ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Sudoku Pro Master"

# Colors (Modern Palette)
C_BG = arcade.color.ALICE_BLUE
C_ACCENT = arcade.color.CORNFLOWER_BLUE
C_BUTTON = arcade.color.ROYAL_BLUE
C_BUTTON_HOVER = arcade.color.MIDNIGHT_BLUE
C_TEXT_MAIN = arcade.color.DARK_SLATE_GRAY
C_GRID_LINES = arcade.color.SLATE_GRAY
C_CELL_BG = arcade.color.WHITE
C_HIGHLIGHT = (200, 230, 255)
C_SELECTED = (150, 200, 255)
C_ERROR = (255, 200, 200)
C_CORRECT_TEXT = arcade.color.DARK_BLUE
C_ERROR_TEXT = arcade.color.DARK_RED

# Difficulty Settings (Removed cells count)
DIFFICULTY = {
    "Easy": 30,
    "Medium": 40,
    "Hard": 50,
    "Expert": 60,
    "Extreme": 68
}


class SudokuLogic:
    def __init__(self, size=9):
        self.size = size
        self.box_h = int(math.sqrt(size))  # 3 for 9x9, 4 for 16x16
        self.box_w = int(math.sqrt(size))
        self.board = [[0] * size for _ in range(size)]
        self.solution = [[0] * size for _ in range(size)]

    def generate(self, difficulty_name="Medium"):
        # 1. Clear Board
        self.board = [[0] * self.size for _ in range(self.size)]

        # 2. Fill Diagonal Boxes (Independent)
        for i in range(0, self.size, self.box_h):
            self._fill_box(i, i)

        # 3. Solve to generate full valid board
        self._solve_board(self.board)

        # 4. Save Solution
        for r in range(self.size):
            for c in range(self.size):
                self.solution[r][c] = self.board[r][c]

        # 5. Remove cells based on difficulty
        if self.size == 16:
            to_remove = 120  # Fixed for 16x16
        else:
            to_remove = DIFFICULTY.get(difficulty_name, 40)

        attempts = to_remove
        while attempts > 0:
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.board[r][c] != 0:
                self.board[r][c] = 0
                attempts -= 1

    def _fill_box(self, row, col):
        for i in range(self.box_h):
            for j in range(self.box_w):
                while True:
                    num = random.randint(1, self.size)
                    if self._is_safe_box(row, col, num):
                        self.board[row + i][col + j] = num
                        break

    def _is_safe_box(self, row_start, col_start, num):
        for i in range(self.box_h):
            for j in range(self.box_w):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, board, row, col, num):
        # Row
        for x in range(self.size):
            if board[row][x] == num: return False
        # Col
        for x in range(self.size):
            if board[x][col] == num: return False
        # Box
        start_row = row - row % self.box_h
        start_col = col - col % self.box_w
        for i in range(self.box_h):
            for j in range(self.box_w):
                if board[start_row + i][start_col + j] == num: return False
        return True

    def _solve_board(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self._solve_board(board): return True
                            board[i][j] = 0
                    return False
        return True


class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = C_BG

        # Game State Variables
        self.state = "MENU"  # MENU, GAME, RESULT
        self.logic = None
        self.grid_size = 9
        self.difficulty = "Medium"

        # Game Play Variables
        self.grid = []
        self.fixed_grid = []
        self.notes = []
        self.selected_row = -1
        self.selected_col = -1
        self.mistakes = 0
        self.start_time = 0
        self.end_time = 0
        self.note_mode = False

        # UI
        self.buttons = []
        self.text_objects = []  # For grid numbers

        # Initialize Menu
        self.setup_menu()

    # --- SETUP FUNCTIONS ---

    def setup_menu(self):
        self.buttons = []
        y_start = 500
        options = ["Easy", "Medium", "Hard", "Expert", "Extreme", "16x16"]

        for i, opt in enumerate(options):
            self.buttons.append({
                "id": f"dif_{opt}", "text": opt,
                "x": SCREEN_WIDTH // 2, "y": y_start - i * 70,
                "w": 200, "h": 50, "color": C_BUTTON
            })

        # Title Text
        self.title_text = arcade.Text("SUDOKU PRO", SCREEN_WIDTH // 2, 650, C_TEXT_MAIN, 40, anchor_x="center",
                                      bold=True)

    def start_game(self, mode):
        self.state = "GAME"
        self.difficulty = mode
        self.grid_size = 16 if mode == "16x16" else 9

        self.logic = SudokuLogic(self.grid_size)
        self.logic.generate(mode)

        self.grid = [row[:] for row in self.logic.board]
        self.fixed_grid = [row[:] for row in self.logic.board]
        self.notes = [[set() for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.mistakes = 0
        self.selected_row = -1
        self.selected_col = -1
        self.start_time = time.time()
        self.note_mode = False

        # Layout Calculations
        margin = 20
        available_width = SCREEN_WIDTH - 2 * margin
        self.cell_size = available_width / self.grid_size
        self.grid_origin_x = margin
        self.grid_origin_y = SCREEN_HEIGHT - margin - available_width - 80  # Offset for header

        self.setup_game_ui()
        self.refresh_grid_text()

    def setup_game_ui(self):
        self.buttons = []

        # Tool Buttons
        tools = [("Note", "note"), ("Hint", "hint"), ("Menu", "menu")]
        bw = 100
        start_x = SCREEN_WIDTH // 2 - bw - 10
        y_pos = 50

        for i, (label, action) in enumerate(tools):
            x = start_x + i * (bw + 10) - 50
            self.buttons.append({
                "id": action, "text": label,
                "x": x, "y": y_pos, "w": bw, "h": 40, "color": C_BUTTON
            })

    def setup_result_screen(self, won):
        self.state = "RESULT"
        self.end_time = time.time()
        self.won = won
        self.buttons = []

        self.buttons.append({
            "id": "replay", "text": "Play Same Level",
            "x": SCREEN_WIDTH // 2, "y": 300, "w": 250, "h": 60, "color": C_BUTTON
        })
        self.buttons.append({
            "id": "menu", "text": "New Game (Menu)",
            "x": SCREEN_WIDTH // 2, "y": 220, "w": 250, "h": 60, "color": C_BUTTON
        })
        self.buttons.append({
            "id": "exit", "text": "Exit",
            "x": SCREEN_WIDTH // 2, "y": 140, "w": 250, "h": 60, "color": C_BUTTON
        })

    def refresh_grid_text(self):
        """Creates arcade.Text objects for grid numbers to optimize rendering."""
        self.text_objects = []

        # Font size dynamic adjustment
        f_size = 20 if self.grid_size == 9 else 12

        for r in range(self.grid_size):
            row_objs = []
            for c in range(self.grid_size):
                val = self.grid[r][c]
                if val != 0:
                    x = self.grid_origin_x + c * self.cell_size + self.cell_size / 2
                    y = self.grid_origin_y + (self.grid_size - 1 - r) * self.cell_size + self.cell_size / 2

                    color = C_CORRECT_TEXT
                    if self.fixed_grid[r][c] != 0:
                        color = arcade.color.BLACK
                    elif val != self.logic.solution[r][c]:
                        color = C_ERROR_TEXT

                    txt = arcade.Text(str(val), x, y, color, f_size, anchor_x="center", anchor_y="center", bold=True)
                    row_objs.append(txt)
                else:
                    row_objs.append(None)
            self.text_objects.append(row_objs)

    # --- DRAWING ---

    def on_draw(self):
        self.clear()

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "GAME":
            self.draw_game()
        elif self.state == "RESULT":
            self.draw_result()

    def draw_menu(self):
        self.title_text.draw()
        arcade.draw_text("Select Difficulty", SCREEN_WIDTH // 2, 550, C_TEXT_MAIN, 20, anchor_x="center")
        self.draw_buttons()

    def draw_game(self):
        # Header
        elapsed = int(time.time() - self.start_time)
        t_str = f"{elapsed // 60:02}:{elapsed % 60:02}"
        arcade.draw_text(t_str, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 40, C_TEXT_MAIN, 20, anchor_x="right")
        arcade.draw_text(f"Mistakes: {self.mistakes}/3", 30, SCREEN_HEIGHT - 40,
                         C_ERROR_TEXT if self.mistakes > 0 else C_TEXT_MAIN, 20)
        arcade.draw_text(f"Mode: {self.difficulty}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, C_ACCENT, 20,
                         anchor_x="center")

        # Grid Background
        gs_px = self.grid_size * self.cell_size
        arcade.draw_rect_filled(
            arcade.XYWH(self.grid_origin_x + gs_px / 2, self.grid_origin_y + gs_px / 2, gs_px, gs_px), C_CELL_BG)

        # Highlights
        if self.selected_row != -1:
            self.draw_highlights()

        # Grid Lines
        self.draw_grid_lines()

        # Numbers
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.text_objects[r][c]:
                    self.text_objects[r][c].draw()
                # Draw Notes
                if self.grid[r][c] == 0 and self.notes[r][c]:
                    self.draw_notes(r, c)

        # UI Buttons
        self.draw_buttons()

    def draw_highlights(self):
        sr, sc = self.selected_row, self.selected_col
        val = self.grid[sr][sc]

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.grid_origin_x + c * self.cell_size + self.cell_size / 2
                y = self.grid_origin_y + (self.grid_size - 1 - r) * self.cell_size + self.cell_size / 2

                color = None

                # Logic for highlighting (Same row, col, box)
                box_h = int(math.sqrt(self.grid_size))
                in_same_box = (r // box_h == sr // box_h) and (c // box_h == sc // box_h)

                if r == sr and c == sc:
                    color = C_SELECTED
                elif val != 0 and self.grid[r][c] == val:
                    color = C_SELECTED
                elif r == sr or c == sc or in_same_box:
                    color = C_HIGHLIGHT

                if self.grid[r][c] != 0 and self.grid[r][c] != self.logic.solution[r][c]:
                    color = C_ERROR

                if color:
                    arcade.draw_rect_filled(arcade.XYWH(x, y, self.cell_size, self.cell_size), color)

    def draw_grid_lines(self):
        gs_px = self.grid_size * self.cell_size
        box_gap = int(math.sqrt(self.grid_size))

        for i in range(self.grid_size + 1):
            thickness = 3 if i % box_gap == 0 else 1
            # Vertical
            x = self.grid_origin_x + i * self.cell_size
            arcade.draw_line(x, self.grid_origin_y, x, self.grid_origin_y + gs_px, C_GRID_LINES, thickness)
            # Horizontal
            y = self.grid_origin_y + i * self.cell_size
            arcade.draw_line(self.grid_origin_x, y, self.grid_origin_x + gs_px, y, C_GRID_LINES, thickness)

    def draw_notes(self, r, c):
        x_base = self.grid_origin_x + c * self.cell_size
        y_base = self.grid_origin_y + (self.grid_size - 1 - r) * self.cell_size

        # 3x3 mini grid for notes
        sub_s = self.cell_size / 3
        for n in self.notes[r][c]:
            nx = (n - 1) % 3
            ny = (n - 1) // 3
            # adjust for larger numbers in 16x16
            if self.grid_size == 16:
                # simple listing for 16x16 notes to fit
                nx = (n - 1) % 4
                ny = (n - 1) // 4
                sub_s = self.cell_size / 4

            tx = x_base + nx * sub_s + sub_s / 2
            ty = y_base + (3 if self.grid_size == 9 else 4) * sub_s - ny * sub_s - sub_s / 2 - 10  # rough align

            arcade.draw_text(str(n), tx, ty, C_GRID_LINES, 10, anchor_x="center", anchor_y="center")

    def draw_result(self):
        title = "VICTORY!" if self.won else "GAME OVER"
        col = arcade.color.GREEN if self.won else arcade.color.RED

        arcade.draw_text(title, SCREEN_WIDTH // 2, 600, col, 50, anchor_x="center", bold=True)

        if self.won:
            total_sec = int(self.end_time - self.start_time)
            mins = total_sec // 60
            secs = total_sec % 60
            arcade.draw_text(f"Time: {mins}m {secs}s", SCREEN_WIDTH // 2, 500, C_TEXT_MAIN, 25, anchor_x="center")
            arcade.draw_text(f"Difficulty: {self.difficulty}", SCREEN_WIDTH // 2, 450, C_TEXT_MAIN, 20,
                             anchor_x="center")

        self.draw_buttons()

    def draw_buttons(self):
        for btn in self.buttons:
            # Shadow
            arcade.draw_rect_filled(arcade.XYWH(btn["x"] + 2, btn["y"] - 2, btn["w"], btn["h"]), arcade.color.GRAY)
            # Body
            color = btn["color"]
            if btn["id"] == "note" and self.note_mode: color = C_BUTTON_HOVER
            arcade.draw_rect_filled(arcade.XYWH(btn["x"], btn["y"], btn["w"], btn["h"]), color)
            # Text
            arcade.draw_text(btn["text"], btn["x"], btn["y"], arcade.color.WHITE, 14, anchor_x="center",
                             anchor_y="center", bold=True)

    # --- INPUT ---

    def on_mouse_press(self, x, y, button, modifiers):
        # Button Click Check
        for btn in self.buttons:
            if (abs(x - btn["x"]) < btn["w"] / 2 and abs(y - btn["y"]) < btn["h"] / 2):
                self.handle_button(btn["id"])
                return

        # Game Grid Click
        if self.state == "GAME":
            gs_px = self.grid_size * self.cell_size
            if (self.grid_origin_x < x < self.grid_origin_x + gs_px and
                    self.grid_origin_y < y < self.grid_origin_y + gs_px):

                c = int((x - self.grid_origin_x) // self.cell_size)
                r = self.grid_size - 1 - int((y - self.grid_origin_y) // self.cell_size)

                if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                    self.selected_row = r
                    self.selected_col = c

    def handle_button(self, btn_id):
        if btn_id.startswith("dif_"):
            mode = btn_id.split("_")[1]
            self.start_game(mode)
        elif btn_id == "note":
            self.note_mode = not self.note_mode
        elif btn_id == "hint":
            self.use_hint()
        elif btn_id == "menu":
            self.setup_menu()
            self.state = "MENU"
        elif btn_id == "replay":
            self.start_game(self.difficulty)
        elif btn_id == "exit":
            arcade.exit()

    def on_key_press(self, key, modifiers):
        if self.state != "GAME": return

        # Navigation
        if key == arcade.key.UP:
            self.move_sel(-1, 0)
        elif key == arcade.key.DOWN:
            self.move_sel(1, 0)
        elif key == arcade.key.LEFT:
            self.move_sel(0, -1)
        elif key == arcade.key.RIGHT:
            self.move_sel(0, 1)

        # Input
        num = -1
        if arcade.key.KEY_0 <= key <= arcade.key.KEY_9:
            num = key - arcade.key.KEY_0
        elif arcade.key.NUM_0 <= key <= arcade.key.NUM_9:
            num = key - arcade.key.NUM_0

        # 16x16 support (a-g keys for 10-16?) Or just rely on standard digit entry limitation.
        # For simplicity, this version supports 1-9 via keyboard. 16x16 usually requires multi-key input or mouse.
        # Adding basic A-F support for 16x16:
        if self.grid_size == 16:
            if key == arcade.key.A:
                num = 10
            elif key == arcade.key.B:
                num = 11
            elif key == arcade.key.C:
                num = 12
            elif key == arcade.key.D:
                num = 13
            elif key == arcade.key.E:
                num = 14
            elif key == arcade.key.F:
                num = 15
            elif key == arcade.key.G:
                num = 16

        if num > 0: self.input_number(num)

        if key == arcade.key.BACKSPACE or key == arcade.key.DELETE:
            self.delete_number()
        elif key == arcade.key.N:
            self.note_mode = not self.note_mode

    def move_sel(self, dr, dc):
        nr, nc = self.selected_row + dr, self.selected_col + dc
        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
            self.selected_row, self.selected_col = nr, nc

    def input_number(self, num):
        if self.selected_row == -1: return
        r, c = self.selected_row, self.selected_col
        if self.fixed_grid[r][c] != 0: return  # Immutable

        if self.note_mode:
            if num in self.notes[r][c]:
                self.notes[r][c].remove(num)
            else:
                self.notes[r][c].add(num)
        else:
            self.grid[r][c] = num
            self.notes[r][c].clear()
            self.refresh_grid_text()

            # Check correctness
            if num != self.logic.solution[r][c]:
                self.mistakes += 1
                if self.mistakes >= 3:
                    self.setup_result_screen(False)
            else:
                self.check_win()

    def delete_number(self):
        if self.selected_row == -1: return
        r, c = self.selected_row, self.selected_col
        if self.fixed_grid[r][c] == 0:
            self.grid[r][c] = 0
            self.refresh_grid_text()

    def use_hint(self):
        if self.selected_row == -1: return
        r, c = self.selected_row, self.selected_col
        if self.grid[r][c] == 0:
            self.grid[r][c] = self.logic.solution[r][c]
            self.refresh_grid_text()
            self.check_win()

    def check_win(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] != self.logic.solution[r][c]: return
        self.setup_result_screen(True)


if __name__ == "__main__":
    window = App()
    arcade.run()