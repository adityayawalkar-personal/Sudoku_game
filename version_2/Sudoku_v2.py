"""
Sudoku Pro Master - Enhanced Arcade Sudoku Game
A polished, professional Sudoku game with Sudoku.com-style interface.

Features:
- Vertical layout (600x900) with four sections
- Top Header: Difficulty, Mistakes, Score, Timer, Pause, Hints badge
- Grid: 9x9 and 16x16 support with proper highlighting
- Action Bar: Undo, Redo, Erase, Notes toggle, Hint
- Number Pad: Clickable 1-9 buttons at bottom
- Undo/Redo functionality (Ctrl+Z/Ctrl+Y) with history stack (max 200)
- Enhanced highlighting: selected cell, same-number, row/col/box, conflicts
- Auto-update notes when placing numbers in peer cells
- Notes rendering: 3x3 mini-grid for 9x9, comma-separated for 16x16
- Pause/Resume with timer freeze
- Flash effect when hints place numbers
- Dynamic font sizing based on cell size
- Color-coded numbers: black (given), blue (correct), red (incorrect)
- Game over at 3 mistakes, win on completion
"""

import arcade
import random
import time
import math

# ============================================================================
# CONFIGURATION
# ============================================================================

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Sudoku Pro"

# Layout Constants - will be recalculated for 16x16
HEADER_HEIGHT = 90
GRID_MARGIN = 20
ACTION_BAR_HEIGHT = 60
NUMBER_PAD_HEIGHT = 80
BOTTOM_MARGIN = 20

# Colors - Modern Sudoku.com Style Palette
C_BG = (245, 247, 250)  # Light grey-blue background
C_WHITE = (255, 255, 255)
C_GRID_THIN = (200, 200, 210)
C_GRID_THICK = (50, 55, 65)

C_FIXED_NUMBER = (30, 30, 35)  # Black for puzzle numbers
C_USER_CORRECT = (30, 100, 200)  # Dark blue for correct user input
C_USER_ERROR = (220, 50, 50)  # Red for errors
C_NOTES = (100, 130, 180)  # Blue-grey for pencil marks

C_SELECTED = (173, 216, 255)  # Blue for selected cell
C_PEERS = (225, 235, 245)  # Light blue for row/col/box
C_SAME_NUMBER = (200, 225, 255)  # Darker blue for same numbers
C_CONFLICT = (255, 200, 200)  # Light red for conflicts
C_FLASH = (150, 255, 200)  # Green flash for hints

C_BUTTON = (66, 133, 244)  # Google blue
C_BUTTON_HOVER = (25, 103, 210)
C_BUTTON_ACTIVE = (21, 101, 192)
C_BUTTON_TEXT = (255, 255, 255)
C_BUTTON_SHADOW = (150, 150, 160)

C_HEADER_BG = (235, 240, 248)
C_HEADER_TEXT = (50, 55, 65)
C_ACCENT = (100, 150, 255)  # Accent color
C_MISTAKE_TEXT = (220, 50, 50)

# Difficulty settings (cells to remove)
DIFFICULTY_LEVELS = {
    "Easy": 30,
    "Medium": 40,
    "Hard": 50,
    "Expert": 58,
    "Extreme": 64
}


# ============================================================================
# SUDOKU LOGIC CLASS
# ============================================================================

class SudokuLogic:
    """Handles Sudoku puzzle generation, validation, and solving."""

    def __init__(self, size=9):
        self.size = size
        self.box_size = int(math.sqrt(size))  # 3 for 9x9, 4 for 16x16
        self.board = [[0] * size for _ in range(size)]
        self.solution = [[0] * size for _ in range(size)]

    def generate(self, difficulty="Medium"):
        """Generate a new Sudoku puzzle with the given difficulty."""
        # Clear board
        self.board = [[0] * self.size for _ in range(self.size)]

        # Fill diagonal boxes first (they are independent)
        for box in range(0, self.size, self.box_size):
            self._fill_box(box, box)

        # Solve the rest of the board
        self._solve(self.board)

        # Save the complete solution
        self.solution = [row[:] for row in self.board]

        # Remove cells based on difficulty
        if self.size == 16:
            cells_to_remove = 120  # Fixed for 16x16
        else:
            cells_to_remove = DIFFICULTY_LEVELS.get(difficulty, 40)

        self._remove_cells(cells_to_remove)

    def _fill_box(self, row_start, col_start):
        """Fill a box with random valid numbers."""
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        idx = 0
        for i in range(self.box_size):
            for j in range(self.box_size):
                self.board[row_start + i][col_start + j] = nums[idx]
                idx += 1

    def _solve(self, board):
        """Solve the Sudoku board using backtracking."""
        empty = self._find_empty(board)
        if not empty:
            return True

        row, col = empty
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)  # Randomize for variety

        for num in nums:
            if self._is_valid(board, row, col, num):
                board[row][col] = num
                if self._solve(board):
                    return True
                board[row][col] = 0
        return False

    def _find_empty(self, board):
        """Find the next empty cell."""
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def _is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in board[row]:
            return False

        # Check column
        for r in range(self.size):
            if board[r][col] == num:
                return False

        # Check box
        box_row = self.box_size * (row // self.box_size)
        box_col = self.box_size * (col // self.box_size)
        for i in range(self.box_size):
            for j in range(self.box_size):
                if board[box_row + i][box_col + j] == num:
                    return False

        return True

    def _remove_cells(self, count):
        """Remove cells to create the puzzle."""
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        removed = 0
        for r, c in cells:
            if removed >= count:
                break
            if self.board[r][c] != 0:
                self.board[r][c] = 0
                removed += 1

    def get_solution_value(self, row, col):
        """Get the correct value for a cell."""
        return self.solution[row][col]


# ============================================================================
# MAIN GAME CLASS
# ============================================================================

class SudokuGame(arcade.Window):
    """Main Sudoku game window with modern interface."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.background_color = C_BG

        # Game state
        self.state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, WIN
        self.difficulty = "Medium"
        self.grid_size = 9

        # Game data
        self.logic = None
        self.grid = []
        self.fixed = []
        self.notes = []
        self.errors = []

        # Selection
        self.selected_row = -1
        self.selected_col = -1

        # Game stats
        self.mistakes = 0
        self.score = 0
        self.hints_remaining = 3
        self.start_time = 0
        self.elapsed_time = 0
        self.pause_start = 0

        # Modes
        self.note_mode = False
        self.paused = False

        # Undo/Redo history
        self.history = []
        self.redo_stack = []

        # UI state
        self.hovered_button = None
        self.flash_cell = None  # (row, col, start_time)

        # Layout values (calculated in setup)
        self.cell_size = 0
        self.grid_origin_x = 0
        self.grid_origin_y = 0
        self.grid_pixel_size = 0

        # Buttons
        self.menu_buttons = []
        self.game_buttons = []
        self.number_buttons = []

        # Text objects for performance
        self.title_text = None
        self.grid_texts = []

        self._setup_menu()

    # ========================================================================
    # SETUP METHODS
    # ========================================================================

    def _setup_menu(self):
        """Setup the menu screen."""
        self.state = "MENU"
        self.menu_buttons = []

        button_width = 220
        button_height = 50
        start_y = 580
        gap = 65

        difficulties = ["Easy", "Medium", "Hard", "Expert", "Extreme", "16x16"]

        for i, diff in enumerate(difficulties):
            self.menu_buttons.append({
                "id": f"dif_{diff}",
                "text": diff,
                "x": SCREEN_WIDTH // 2,
                "y": start_y - i * gap,
                "w": button_width,
                "h": button_height
            })

        # Create title text object
        self.title_text = arcade.Text(
            "SUDOKU PRO",
            SCREEN_WIDTH // 2, 720,
            C_HEADER_TEXT, 44,
            anchor_x="center", bold=True
        )

    def _start_game(self, mode):
        """Start a new game with the given mode/difficulty."""
        self.state = "PLAYING"
        self.difficulty = mode
        self.grid_size = 16 if mode == "16x16" else 9

        # Generate puzzle
        self.logic = SudokuLogic(self.grid_size)
        self.logic.generate(mode if mode != "16x16" else "Medium")

        # Initialize game data
        self.grid = [row[:] for row in self.logic.board]
        self.fixed = [[self.grid[r][c] != 0 for c in range(self.grid_size)]
                      for r in range(self.grid_size)]
        self.notes = [[set() for _ in range(self.grid_size)]
                      for _ in range(self.grid_size)]
        self.errors = [[False] * self.grid_size for _ in range(self.grid_size)]

        # Reset game state
        self.selected_row = -1
        self.selected_col = -1
        self.mistakes = 0
        self.score = 0
        self.hints_remaining = 3
        self.start_time = time.time()
        self.elapsed_time = 0
        self.note_mode = False
        self.paused = False
        self.history = []
        self.redo_stack = []
        self.flash_cell = None

        # Calculate layout
        self._calculate_layout()
        self._setup_game_buttons()
        self._setup_number_pad()
        self._refresh_grid_texts()

    def _calculate_layout(self):
        """Calculate grid layout based on grid size."""
        # Available space for grid
        available_height = (SCREEN_HEIGHT - HEADER_HEIGHT - ACTION_BAR_HEIGHT -
                            NUMBER_PAD_HEIGHT - BOTTOM_MARGIN - 40)
        available_width = SCREEN_WIDTH - 2 * GRID_MARGIN

        # Cell size (use minimum to ensure square cells fit)
        max_cell_size = min(available_width, available_height) / self.grid_size
        self.cell_size = max_cell_size
        self.grid_pixel_size = self.cell_size * self.grid_size

        # Center grid horizontally
        self.grid_origin_x = (SCREEN_WIDTH - self.grid_pixel_size) / 2

        # Position grid below header
        self.grid_origin_y = (SCREEN_HEIGHT - HEADER_HEIGHT - 20 - self.grid_pixel_size)

    def _setup_game_buttons(self):
        """Setup action bar buttons."""
        self.game_buttons = []

        buttons = [
            ("undo", "Undo"),
            ("erase", "Erase"),
            ("notes", "Notes"),
            ("hint", "Hint"),
            ("redo", "Redo"),
            ("menu", "Menu")
        ]

        button_width = 70
        button_height = 40
        gap = 12
        total_width = len(buttons) * button_width + (len(buttons) - 1) * gap
        start_x = (SCREEN_WIDTH - total_width) / 2 + button_width / 2
        y_pos = self.grid_origin_y - 50

        for i, (btn_id, text) in enumerate(buttons):
            self.game_buttons.append({
                "id": btn_id,
                "text": text,
                "x": start_x + i * (button_width + gap),
                "y": y_pos,
                "w": button_width,
                "h": button_height
            })

    def _setup_number_pad(self):
        """Setup the bottom number pad."""
        self.number_buttons = []

        # For 16x16, we need more buttons but keep them smaller
        num_count = self.grid_size
        button_size = min(55, (SCREEN_WIDTH - 40) / num_count - 5)
        gap = 5
        total_width = num_count * button_size + (num_count - 1) * gap
        start_x = (SCREEN_WIDTH - total_width) / 2 + button_size / 2
        y_pos = 55

        for i in range(1, num_count + 1):
            self.number_buttons.append({
                "id": f"num_{i}",
                "value": i,
                "x": start_x + (i - 1) * (button_size + gap),
                "y": y_pos,
                "w": button_size,
                "h": button_size
            })

    def _refresh_grid_texts(self):
        """Create text objects for grid numbers with dynamic sizing and colors."""
        self.grid_texts = []

        # Font size based on cell size
        font_size = max(int(self.cell_size * 0.45), 10)
        if self.grid_size == 16:
            font_size = max(int(self.cell_size * 0.35), 8)

        for r in range(self.grid_size):
            row_texts = []
            for c in range(self.grid_size):
                val = self.grid[r][c]
                if val != 0:
                    x, y = self._grid_to_screen(r, c)

                    # Color coding
                    if self.fixed[r][c]:
                        color = C_FIXED_NUMBER
                    elif val != self.logic.solution[r][c]:
                        color = C_USER_ERROR
                    else:
                        color = C_USER_CORRECT

                    # Display value (hex for 16x16 values > 9)
                    display = str(val) if val <= 9 else hex(val)[2:].upper()

                    txt = arcade.Text(
                        display, x, y, color, font_size,
                        anchor_x="center", anchor_y="center", bold=True
                    )
                    row_texts.append(txt)
                else:
                    row_texts.append(None)
            self.grid_texts.append(row_texts)

    def _setup_result_screen(self, won):
        """Setup the result screen."""
        self.state = "WIN" if won else "GAME_OVER"
        self.elapsed_time = time.time() - self.start_time

    # ========================================================================
    # COORDINATE CONVERSION
    # ========================================================================

    def _screen_to_grid(self, x, y):
        """Convert screen coordinates to grid row/col. Returns (-1, -1) if outside."""
        if not (self.grid_origin_x <= x <= self.grid_origin_x + self.grid_pixel_size):
            return -1, -1
        if not (self.grid_origin_y <= y <= self.grid_origin_y + self.grid_pixel_size):
            return -1, -1

        col = int((x - self.grid_origin_x) / self.cell_size)
        # Y is inverted: top of grid is row 0
        row = int((self.grid_origin_y + self.grid_pixel_size - y) / self.cell_size)

        col = max(0, min(self.grid_size - 1, col))
        row = max(0, min(self.grid_size - 1, row))

        return row, col

    def _grid_to_screen(self, row, col):
        """Convert grid row/col to screen coordinates (center of cell)."""
        x = self.grid_origin_x + col * self.cell_size + self.cell_size / 2
        # Y is inverted: row 0 is at top of grid
        y = self.grid_origin_y + self.grid_pixel_size - row * self.cell_size - self.cell_size / 2
        return x, y

    # ========================================================================
    # UNDO/REDO
    # ========================================================================

    def _push_history(self, r, c, prev_val, prev_notes, prev_error):
        """Push current state to history stack."""
        self.history.append((r, c, prev_val, set(prev_notes), prev_error))
        if len(self.history) > 200:
            self.history.pop(0)
        self.redo_stack = []

    def _undo(self):
        """Undo last action."""
        if not self.history:
            return

        r, c, prev_val, prev_notes, prev_error = self.history.pop()

        # Save current to redo
        self.redo_stack.append((r, c, self.grid[r][c], set(self.notes[r][c]), self.errors[r][c]))

        # Restore
        self.grid[r][c] = prev_val
        self.notes[r][c] = prev_notes
        self.errors[r][c] = prev_error
        self._refresh_grid_texts()

    def _redo(self):
        """Redo last undone action."""
        if not self.redo_stack:
            return

        r, c, val, notes, error = self.redo_stack.pop()

        # Save current to history
        self.history.append((r, c, self.grid[r][c], set(self.notes[r][c]), self.errors[r][c]))

        # Restore
        self.grid[r][c] = val
        self.notes[r][c] = notes
        self.errors[r][c] = error
        self._refresh_grid_texts()

    # ========================================================================
    # AUTO-UPDATE NOTES
    # ========================================================================

    def _update_notes_after_place(self, r, c, num):
        """Remove placed number from notes in all peer cells."""
        # Row
        for col in range(self.grid_size):
            self.notes[r][col].discard(num)

        # Column
        for row in range(self.grid_size):
            self.notes[row][c].discard(num)

        # Box
        box_row = self.logic.box_size * (r // self.logic.box_size)
        box_col = self.logic.box_size * (c // self.logic.box_size)
        for i in range(self.logic.box_size):
            for j in range(self.logic.box_size):
                self.notes[box_row + i][box_col + j].discard(num)

    # ========================================================================
    # DRAWING
    # ========================================================================

    def on_draw(self):
        """Main draw method."""
        self.clear()

        if self.state == "MENU":
            self._draw_menu()
        elif self.state in ("PLAYING", "PAUSED"):
            self._draw_game()
            if self.state == "PAUSED":
                self._draw_pause_overlay()
        elif self.state == "GAME_OVER":
            self._draw_game()
            self._draw_game_over_overlay()
        elif self.state == "WIN":
            self._draw_game()
            self._draw_win_overlay()

    def _draw_menu(self):
        """Draw the menu screen."""
        # Title
        if self.title_text:
            self.title_text.draw()

        arcade.draw_text(
            "Select Difficulty",
            SCREEN_WIDTH // 2, 650,
            C_HEADER_TEXT, 20,
            anchor_x="center"
        )

        # Buttons
        for btn in self.menu_buttons:
            color = C_BUTTON_HOVER if self.hovered_button == btn["id"] else C_BUTTON
            self._draw_button(btn, color)

    def _draw_game(self):
        """Draw the main game screen."""
        self._draw_header()
        self._draw_grid()
        self._draw_action_bar()
        self._draw_number_pad()

    def _draw_header(self):
        """Draw the top header."""
        # Header background
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT - HEADER_HEIGHT / 2,
                        SCREEN_WIDTH, HEADER_HEIGHT),
            C_HEADER_BG
        )

        # Difficulty label (left)
        arcade.draw_text(
            self.difficulty,
            25, SCREEN_HEIGHT - 35,
            C_ACCENT, 18, bold=True
        )

        # Mistakes (center-left)
        mistake_color = C_MISTAKE_TEXT if self.mistakes > 0 else C_HEADER_TEXT
        arcade.draw_text(
            f"Mistakes: {self.mistakes}/3",
            25, SCREEN_HEIGHT - 60,
            mistake_color, 15
        )

        # Score (below mistakes)
        arcade.draw_text(
            f"Score: {self.score}",
            25, SCREEN_HEIGHT - 82,
            C_HEADER_TEXT, 14
        )

        # Hints badge (center)
        hint_x = SCREEN_WIDTH // 2 - 40
        hint_y = SCREEN_HEIGHT - 50
        arcade.draw_text("Hints:", hint_x - 35, hint_y, C_HEADER_TEXT, 14, anchor_y="center")
        arcade.draw_circle_filled(hint_x + 10, hint_y, 16, C_ACCENT)
        arcade.draw_text(
            str(self.hints_remaining),
            hint_x + 10, hint_y,
            C_WHITE, 14, anchor_x="center", anchor_y="center", bold=True
        )

        # Timer (right)
        if self.state == "PLAYING":
            self.elapsed_time = time.time() - self.start_time
        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        arcade.draw_text(
            f"{mins:02}:{secs:02}",
            SCREEN_WIDTH - 120, SCREEN_HEIGHT - 35,
            C_HEADER_TEXT, 22, bold=True
        )

        # Pause button
        pause_x = SCREEN_WIDTH - 55
        pause_y = SCREEN_HEIGHT - 60
        pause_w = 80
        pause_h = 32

        pause_color = C_BUTTON_HOVER if self.hovered_button == "pause" else C_BUTTON
        arcade.draw_rect_filled(
            arcade.XYWH(pause_x, pause_y, pause_w, pause_h),
            pause_color
        )

        pause_text = "Resume" if self.paused else "Pause"
        arcade.draw_text(
            pause_text, pause_x, pause_y,
            C_WHITE, 12, anchor_x="center", anchor_y="center", bold=True
        )

    def _draw_grid(self):
        """Draw the Sudoku grid with highlights and numbers."""
        # Grid background
        arcade.draw_rect_filled(
            arcade.XYWH(self.grid_origin_x + self.grid_pixel_size / 2,
                        self.grid_origin_y + self.grid_pixel_size / 2,
                        self.grid_pixel_size, self.grid_pixel_size),
            C_WHITE
        )

        # Draw highlights
        self._draw_highlights()

        # Draw flash effect
        if self.flash_cell:
            r, c, start_time = self.flash_cell
            elapsed = time.time() - start_time
            if elapsed < 0.6:
                x, y = self._grid_to_screen(r, c)
                alpha = int(200 * (1 - elapsed / 0.6))
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, self.cell_size - 2, self.cell_size - 2),
                    (*C_FLASH, alpha)
                )
            else:
                self.flash_cell = None

        # Draw grid lines
        self._draw_grid_lines()

        # Draw numbers and notes
        self._draw_numbers()

    def _draw_highlights(self):
        """Draw cell highlighting."""
        if self.selected_row < 0 or self.selected_col < 0:
            return

        sr, sc = self.selected_row, self.selected_col
        selected_value = self.grid[sr][sc]
        box_size = self.logic.box_size if self.logic else 3
        selected_box_row = sr // box_size
        selected_box_col = sc // box_size

        # Compute conflicts
        conflicts = self._compute_conflicts()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x, y = self._grid_to_screen(row, col)
                color = None

                in_same_box = (row // box_size == selected_box_row and
                               col // box_size == selected_box_col)

                # Priority: selected > same number > peers
                if row == sr and col == sc:
                    color = C_SELECTED
                elif selected_value != 0 and self.grid[row][col] == selected_value:
                    color = C_SAME_NUMBER
                elif row == sr or col == sc or in_same_box:
                    color = C_PEERS

                # Conflict overlay (highest priority visual)
                if conflicts[row][col]:
                    color = C_CONFLICT

                if color:
                    arcade.draw_rect_filled(
                        arcade.XYWH(x, y, self.cell_size - 1, self.cell_size - 1),
                        color
                    )

    def _compute_conflicts(self):
        """Compute cells with conflicts (duplicates in row/col/box)."""
        conflicts = [[False] * self.grid_size for _ in range(self.grid_size)]
        box_size = self.logic.box_size if self.logic else 3

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    continue
                num = self.grid[r][c]

                # Check row
                for col in range(self.grid_size):
                    if col != c and self.grid[r][col] == num:
                        conflicts[r][c] = True
                        conflicts[r][col] = True

                # Check column
                for row in range(self.grid_size):
                    if row != r and self.grid[row][c] == num:
                        conflicts[r][c] = True
                        conflicts[row][c] = True

                # Check box
                box_r = box_size * (r // box_size)
                box_c = box_size * (c // box_size)
                for i in range(box_size):
                    for j in range(box_size):
                        rr, cc = box_r + i, box_c + j
                        if (rr != r or cc != c) and self.grid[rr][cc] == num:
                            conflicts[r][c] = True
                            conflicts[rr][cc] = True

        return conflicts

    def _draw_grid_lines(self):
        """Draw grid lines with thick borders for boxes."""
        box_size = self.logic.box_size if self.logic else 3

        for i in range(self.grid_size + 1):
            thickness = 3 if i % box_size == 0 else 1
            color = C_GRID_THICK if i % box_size == 0 else C_GRID_THIN

            # Vertical line
            x = self.grid_origin_x + i * self.cell_size
            arcade.draw_line(
                x, self.grid_origin_y,
                x, self.grid_origin_y + self.grid_pixel_size,
                color, thickness
            )

            # Horizontal line
            y = self.grid_origin_y + i * self.cell_size
            arcade.draw_line(
                self.grid_origin_x, y,
                self.grid_origin_x + self.grid_pixel_size, y,
                color, thickness
            )

    def _draw_numbers(self):
        """Draw numbers and notes in the grid."""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                # Draw number text object
                if self.grid_texts[r][c]:
                    self.grid_texts[r][c].draw()
                # Draw notes if cell is empty
                elif self.notes[r][c]:
                    self._draw_notes(r, c)

    def _draw_notes(self, row, col):
        """Draw pencil marks in a cell."""
        x, y = self._grid_to_screen(row, col)

        if self.grid_size == 9:
            # 3x3 mini-grid for 9x9
            sub_size = self.cell_size / 3
            font_size = max(int(self.cell_size * 0.2), 8)

            for note in sorted(self.notes[row][col]):
                note_row = (note - 1) // 3
                note_col = (note - 1) % 3

                nx = x + (note_col - 1) * sub_size
                ny = y + (1 - note_row) * sub_size

                arcade.draw_text(
                    str(note), nx, ny,
                    C_NOTES, font_size,
                    anchor_x="center", anchor_y="center"
                )
        else:
            # Comma-separated for 16x16
            font_size = max(int(self.cell_size * 0.15), 6)
            notes_str = ",".join([hex(n)[2:].upper() for n in sorted(self.notes[row][col])])

            arcade.draw_text(
                notes_str, x, y,
                C_NOTES, font_size,
                anchor_x="center", anchor_y="center"
            )

    def _draw_action_bar(self):
        """Draw the action buttons."""
        for btn in self.game_buttons:
            # Special state for notes button
            if btn["id"] == "notes":
                color = C_BUTTON_ACTIVE if self.note_mode else C_BUTTON
                if self.hovered_button == btn["id"]:
                    color = C_BUTTON_HOVER
            else:
                color = C_BUTTON_HOVER if self.hovered_button == btn["id"] else C_BUTTON

            self._draw_button(btn, color)

            # Hint count badge
            if btn["id"] == "hint" and self.hints_remaining > 0:
                badge_x = btn["x"] + btn["w"] / 2 - 5
                badge_y = btn["y"] + btn["h"] / 2 - 5
                arcade.draw_circle_filled(badge_x, badge_y, 9, (255, 193, 7))
                arcade.draw_text(
                    str(self.hints_remaining),
                    badge_x, badge_y,
                    (0, 0, 0), 9,
                    anchor_x="center", anchor_y="center", bold=True
                )

    def _draw_number_pad(self):
        """Draw the bottom number pad."""
        for btn in self.number_buttons:
            is_hovered = self.hovered_button == btn["id"]
            color = C_BUTTON_HOVER if is_hovered else C_BUTTON

            # Draw button
            arcade.draw_rect_filled(
                arcade.XYWH(btn["x"], btn["y"], btn["w"], btn["h"]),
                color
            )

            # Draw number (hex for > 9)
            val = btn["value"]
            display = str(val) if val <= 9 else hex(val)[2:].upper()
            font_size = 20 if self.grid_size == 9 else 14

            arcade.draw_text(
                display, btn["x"], btn["y"],
                C_WHITE, font_size,
                anchor_x="center", anchor_y="center", bold=True
            )

    def _draw_button(self, btn, color):
        """Draw a generic button with shadow."""
        # Shadow
        arcade.draw_rect_filled(
            arcade.XYWH(btn["x"] + 2, btn["y"] - 2, btn["w"], btn["h"]),
            C_BUTTON_SHADOW
        )

        # Button body
        arcade.draw_rect_filled(
            arcade.XYWH(btn["x"], btn["y"], btn["w"], btn["h"]),
            color
        )

        # Text
        arcade.draw_text(
            btn["text"], btn["x"], btn["y"],
            C_WHITE, 13,
            anchor_x="center", anchor_y="center", bold=True
        )

    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 180)
        )

        arcade.draw_text(
            "PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            C_WHITE, 50, anchor_x="center", anchor_y="center", bold=True
        )

        arcade.draw_text(
            "Click 'Resume' to continue",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
            (200, 200, 200), 18,
            anchor_x="center", anchor_y="center"
        )

    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            C_MISTAKE_TEXT, 48, anchor_x="center", anchor_y="center", bold=True
        )

        arcade.draw_text(
            "Too many mistakes!",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10,
            (200, 200, 200), 20, anchor_x="center", anchor_y="center"
        )

        arcade.draw_text(
            "Press ENTER for new game or ESC for menu",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
            (150, 150, 150), 16, anchor_x="center", anchor_y="center"
        )

    def _draw_win_overlay(self):
        """Draw win overlay."""
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "CONGRATULATIONS!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
            (100, 200, 100), 40, anchor_x="center", anchor_y="center", bold=True
        )

        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        arcade.draw_text(
            f"Time: {mins:02}:{secs:02}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
            C_WHITE, 24, anchor_x="center", anchor_y="center"
        )

        arcade.draw_text(
            f"Score: {self.score}  |  Difficulty: {self.difficulty}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30,
            (200, 200, 200), 18, anchor_x="center", anchor_y="center"
        )

        arcade.draw_text(
            "Press ENTER for new game or ESC for menu",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80,
            (150, 150, 150), 16, anchor_x="center", anchor_y="center"
        )

    # ========================================================================
    # INPUT HANDLING
    # ========================================================================

    def on_mouse_motion(self, x, y, dx, dy):
        """Track hovered buttons."""
        self.hovered_button = None

        if self.state == "MENU":
            for btn in self.menu_buttons:
                if self._point_in_button(x, y, btn):
                    self.hovered_button = btn["id"]
                    return

        elif self.state in ("PLAYING", "PAUSED"):
            # Check pause button
            pause_x = SCREEN_WIDTH - 55
            pause_y = SCREEN_HEIGHT - 60
            if abs(x - pause_x) < 40 and abs(y - pause_y) < 16:
                self.hovered_button = "pause"
                return

            if self.state == "PLAYING":
                # Check action buttons
                for btn in self.game_buttons:
                    if self._point_in_button(x, y, btn):
                        self.hovered_button = btn["id"]
                        return

                # Check number pad
                for btn in self.number_buttons:
                    if self._point_in_button(x, y, btn):
                        self.hovered_button = btn["id"]
                        return

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks."""
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.state == "MENU":
            for btn in self.menu_buttons:
                if self._point_in_button(x, y, btn):
                    mode = btn["id"].replace("dif_", "")
                    self._start_game(mode)
                    return

        elif self.state in ("PLAYING", "PAUSED"):
            # Check pause button
            pause_x = SCREEN_WIDTH - 55
            pause_y = SCREEN_HEIGHT - 60
            if abs(x - pause_x) < 40 and abs(y - pause_y) < 16:
                self._toggle_pause()
                return

            if self.paused:
                return

            # Check action buttons
            for btn in self.game_buttons:
                if self._point_in_button(x, y, btn):
                    self._handle_action_button(btn["id"])
                    return

            # Check number pad
            for btn in self.number_buttons:
                if self._point_in_button(x, y, btn):
                    self._input_number(btn["value"])
                    return

            # Check grid click
            row, col = self._screen_to_grid(x, y)
            if row >= 0 and col >= 0:
                self.selected_row = row
                self.selected_col = col

    def on_key_press(self, key, modifiers):
        """Handle keyboard input."""
        # Global: ESC to menu
        if key == arcade.key.ESCAPE:
            if self.state in ("PLAYING", "PAUSED", "GAME_OVER", "WIN"):
                self._setup_menu()
            return

        # ENTER for new game on result screens
        if key == arcade.key.ENTER and self.state in ("GAME_OVER", "WIN"):
            self._start_game(self.difficulty)
            return

        if self.state != "PLAYING":
            return

        if self.paused:
            if key in (arcade.key.P, arcade.key.SPACE):
                self._toggle_pause()
            return

        # Undo/Redo shortcuts
        if modifiers & arcade.key.MOD_CTRL:
            if key == arcade.key.Z:
                self._undo()
                return
            elif key == arcade.key.Y:
                self._redo()
                return

        # Navigation
        if key == arcade.key.UP:
            self._move_selection(-1, 0)
        elif key == arcade.key.DOWN:
            self._move_selection(1, 0)
        elif key == arcade.key.LEFT:
            self._move_selection(0, -1)
        elif key == arcade.key.RIGHT:
            self._move_selection(0, 1)

        # Number input (1-9)
        num = -1
        if arcade.key.KEY_1 <= key <= arcade.key.KEY_9:
            num = key - arcade.key.KEY_0
        elif arcade.key.NUM_1 <= key <= arcade.key.NUM_9:
            num = key - arcade.key.NUM_0

        # 16x16 support (A-G for 10-16)
        if self.grid_size == 16:
            hex_keys = {
                arcade.key.A: 10, arcade.key.B: 11, arcade.key.C: 12,
                arcade.key.D: 13, arcade.key.E: 14, arcade.key.F: 15,
                arcade.key.G: 16
            }
            if key in hex_keys:
                num = hex_keys[key]

        if num > 0:
            self._input_number(num)

        # Delete/Erase
        if key in (arcade.key.BACKSPACE, arcade.key.DELETE, arcade.key.KEY_0):
            self._erase_cell()

        # Toggle note mode
        if key == arcade.key.N:
            self.note_mode = not self.note_mode

        # Pause
        if key in (arcade.key.P, arcade.key.SPACE):
            self._toggle_pause()

    def _point_in_button(self, x, y, btn):
        """Check if point is inside button."""
        half_w = btn["w"] / 2
        half_h = btn["h"] / 2
        return (btn["x"] - half_w <= x <= btn["x"] + half_w and
                btn["y"] - half_h <= y <= btn["y"] + half_h)

    def _move_selection(self, dr, dc):
        """Move selection by delta row/col."""
        if self.selected_row < 0:
            self.selected_row = 0
            self.selected_col = 0
        else:
            new_row = self.selected_row + dr
            new_col = self.selected_col + dc
            if 0 <= new_row < self.grid_size and 0 <= new_col < self.grid_size:
                self.selected_row = new_row
                self.selected_col = new_col

    # ========================================================================
    # GAME ACTIONS
    # ========================================================================

    def _handle_action_button(self, btn_id):
        """Handle action bar button clicks."""
        if btn_id == "undo":
            self._undo()
        elif btn_id == "redo":
            self._redo()
        elif btn_id == "erase":
            self._erase_cell()
        elif btn_id == "notes":
            self.note_mode = not self.note_mode
        elif btn_id == "hint":
            self._use_hint()
        elif btn_id == "menu":
            self._setup_menu()

    def _input_number(self, num):
        """Input a number into the selected cell."""
        if self.selected_row < 0 or self.selected_col < 0:
            return

        r, c = self.selected_row, self.selected_col

        # Can't modify fixed cells
        if self.fixed[r][c]:
            return

        # Save state for undo
        self._push_history(r, c, self.grid[r][c], self.notes[r][c], self.errors[r][c])

        if self.note_mode:
            # Toggle note (only in empty cells)
            if self.grid[r][c] == 0:
                if num in self.notes[r][c]:
                    self.notes[r][c].remove(num)
                else:
                    self.notes[r][c].add(num)
        else:
            # Place number
            self.grid[r][c] = num
            self.notes[r][c].clear()

            # Check if correct
            correct = self.logic.get_solution_value(r, c)
            if num != correct:
                self.errors[r][c] = True
                self.mistakes += 1

                if self.mistakes >= 3:
                    self._setup_result_screen(False)
            else:
                self.errors[r][c] = False
                self.score += 10

                # Auto-erase notes from peers
                self._update_notes_after_place(r, c, num)

                # Check win
                if self._check_win():
                    self._setup_result_screen(True)

            self._refresh_grid_texts()

    def _erase_cell(self):
        """Erase the selected cell."""
        if self.selected_row < 0 or self.selected_col < 0:
            return

        r, c = self.selected_row, self.selected_col

        if self.fixed[r][c]:
            return

        if self.grid[r][c] != 0 or self.notes[r][c]:
            self._push_history(r, c, self.grid[r][c], self.notes[r][c], self.errors[r][c])
            self.grid[r][c] = 0
            self.notes[r][c].clear()
            self.errors[r][c] = False
            self._refresh_grid_texts()

    def _use_hint(self):
        """Use a hint to fill the selected cell."""
        if self.hints_remaining <= 0:
            return

        if self.selected_row < 0 or self.selected_col < 0:
            return

        r, c = self.selected_row, self.selected_col

        if self.fixed[r][c]:
            return

        # Don't use hint on already correct cells
        if self.grid[r][c] == self.logic.solution[r][c]:
            return

        # Save for undo
        self._push_history(r, c, self.grid[r][c], self.notes[r][c], self.errors[r][c])

        # Place correct value
        correct = self.logic.get_solution_value(r, c)
        self.grid[r][c] = correct
        self.notes[r][c].clear()
        self.errors[r][c] = False

        # Flash effect
        self.flash_cell = (r, c, time.time())

        self.hints_remaining -= 1
        self.score += 5  # Less points for hints

        # Auto-erase notes
        self._update_notes_after_place(r, c, correct)

        self._refresh_grid_texts()

        # Check win
        if self._check_win():
            self._setup_result_screen(True)

    def _toggle_pause(self):
        """Toggle pause state."""
        if self.state == "PLAYING":
            self.state = "PAUSED"
            self.paused = True
            self.pause_start = time.time()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            self.paused = False
            # Adjust timer
            pause_duration = time.time() - self.pause_start
            self.start_time += pause_duration

    def _check_win(self):
        """Check if the puzzle is solved."""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] != self.logic.solution[r][c]:
                    return False
        return True

    def on_update(self, delta_time):
        """Update loop."""
        pass


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    game = SudokuGame()
    arcade.run()


if __name__ == "__main__":
    main()