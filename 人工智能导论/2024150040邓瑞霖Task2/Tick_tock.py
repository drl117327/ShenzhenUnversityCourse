import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time

class TicTacToe:
    def __init__(self):
        # 初始化3*3棋盘，空位用' '表示
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = 'X'  # 人类玩家标记
        self.ai = 'O'  # AI玩家标记
        self.current_player = self.human
        self.game_over = False
        self.ai_thinking = False

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("Tick_tock - Man-machine battle")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # 设置窗口居中
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 询问先手
        self.ask_first_player()
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """创建GUI界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="Tick_tock - Man-machine battle",
            font=("微软雅黑", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50')
        title_label.pack(pady=20)
        # 游戏状态显示
        self.status_label = tk.Label(
            self.root,text="You are ❌, AI is ⭕",
            font=("微软雅黑", 14),
            bg='#f0f0f0',fg='#34495e')
        
        self.status_label.pack(pady=10)
        # 棋盘框架
        board_frame = tk.Frame(self.root, bg='#34495e', padx=5, pady=5)
        board_frame.pack(pady=20)
        # 棋盘按钮
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=("微软雅黑", 24, 'bold'),
                    width=4, height=2, bg='white', fg='#2c3e50',
                    command=lambda r=i, c=j: self.human_move(r, c),
                    cursor='hand2'
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
            # 控制按钮框架
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=20)
        
        # 重新开始按钮
        self.restart_btn = tk.Button(
            control_frame,
            text="Restart",
            font=("微软雅黑", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=self.restart_game
        )
        self.restart_btn.pack(side=tk.LEFT, padx=10)
        
        # 退出按钮
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            font=("微软雅黑", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=self.root.quit
        )
        quit_btn.pack(side=tk.LEFT, padx=10)

    def ask_first_player(self):
        """询问谁先开始"""
        result = messagebox.askyesno(
            "choose first player", 
            "Do you want to go first?\n\nYes = You go first (x)\nNo = AI goes first (o)",
            icon='question'
        )
        
        if result:
            self.current_player = self.human
            self.update_status("It's your turn! Click to make a move.")
        else:
            self.current_player = self.ai
            self.update_status("AI is thinking...")
            self.root.after(1000, self.ai_move)
    
    def update_status(self, message):
        """更新状态显示"""
        self.status_label.config(text=message)
        self.root.update()

    def human_move(self, row, col):
        """处理人类玩家移动"""
        if self.game_over or self.ai_thinking or self.current_player != self.human:
            return

        if self.is_valid_move(row, col):
            # 更新棋盘和界面
            self.make_move(row, col, self.human)
            self.update_button(row, col, 'X', '#e74c3c')
            
            # 检查游戏状态
            if self.check_game_end():
                return
            
            # 切换到AI回合
            self.current_player = self.ai
            self.update_status("AI思考中...")
            self.ai_thinking = True

            # 延迟AI移动
            self.root.after(500, self.ai_move)

    def ai_move(self):
        """处理AI移动"""
        if self.game_over:
            return

        move = self.get_best_move()
        if move:
            row, col = move
            self.make_move(row, col, self.ai)
            self.update_button(row, col, 'O', '#3498db')
            # 检查游戏状态
            if self.check_game_end():
                return
            # 切换到人类回合
            self.current_player = self.human
            self.update_status("It's your turn! Click to make a move.")
        
        self.ai_thinking = False 

    
    def update_button(self, row, col, symbol, color):
        """更新按钮显示"""
        self.buttons[row][col].config(
            text=symbol,
            fg=color,
            state='disabled',
            relief='sunken'
        )

    def check_game_end(self):
        """检查游戏是否结束"""
        winner = self.check_winner()
        
        if winner:
            self.game_over = True
            if winner == self.human:
                self.update_status("you win!")
                messagebox.showinfo("game is over", "you successfully defeated AI!")
            else:
                self.update_status("AI wins!")
                messagebox.showinfo("game is over", "AI wins!\nTry again!")
            
            self.disable_all_buttons()
            return True
        
        elif self.is_board_full():
            self.game_over = True
            self.update_status("Tie game!")
            messagebox.showinfo("game is over", "Tie game!\nA hard-fought battle!")
            return True
        
        return False
    
    def disable_all_buttons(self):
        """禁用所有按钮"""
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['state'] != 'disabled':
                    self.buttons[i][j].config(state='disabled')
    
    def restart_game(self):
        """重新开始游戏"""
        # 重置游戏状态
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.ai_thinking = False
        
        # 重置按钮
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text='',
                    state='normal',
                    bg='white',
                    fg='#2c3e50',
                    relief='raised'
                )
        
        # 重新询问先手
        self.ask_first_player()

    def is_valid_move(self, row, col):
        """检查移动是否有效"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        """在指定位置下棋"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        """检查是否有获胜者"""
        # 检查行
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        # 检查列
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # 检查对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def get_empty_cells(self):
            empty_cells = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        empty_cells.append((i, j))
            return empty_cells

    def minimax(self, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        """Minimax算法实现+Alpha-Beta剪枝"""
        winner = self.check_winner()
        # 终止条件
        if winner == self.ai:
            return 1  # AI获胜
        elif winner == self.human:
            return -1  # 人类获胜
        elif self.is_board_full():
            return 0  # 平局
        
        if is_maximizing:  # AI的回合
            max_eval = -float('inf')
            for row, col in self.get_empty_cells():
                self.board[row][col] = self.ai
                eval_score = self.minimax(depth+1, False, alpha, beta)
                self.board[row][col] = ' '  # 撤销移动
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
            return max_eval
        else: # 人类回合
            min_eval = float('inf')
            for row, col in self.get_empty_cells():
                self.board[row][col] = self.human
                eval_score = self.minimax(depth+1, True, alpha, beta)
                self.board[row][col] = ' '  # 撤销移动
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
            return min_eval

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        
        for row, col in self.get_empty_cells():
            self.board[row][col] = self.ai
            score = self.minimax(0, False)
            self.board[row][col] = ' '
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move      

    def run(self):
        """运行游戏"""
        self.root.mainloop()

def main():
    """主函数"""
    game = TicTacToe()
    game.run()

if __name__ == "__main__":
    main()
