import sys

import pygame


class Pygomoku:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        # 设置棋盘大小
        self.board_size = 15
        # 棋盘
        self.board: list[list[str]] = [[u"　  " for _ in range(self.board_size)] for _ in range(self.board_size)]
        # 设置棋格大小
        self.cell_size = 40
        # 创建五子棋游戏界面
        size = self.cell_size * (self.board_size + 1)
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption("五子棋")
        pygame.display.flip()
        # 当前玩家: 黑
        self.current_player = "黑"
        # 最终赢家
        self.winner = None

    def draw_board(self):
        """ 绘制棋盘 """
        self.screen.fill((230, 189, 144))  # 棋盘颜色
        for i in range(self.board_size):
            pygame.draw.line(self.screen, self.BLACK, ((i + 1) * self.cell_size, self.cell_size), ((i + 1) * self.cell_size, self.board_size * self.cell_size))
            pygame.draw.line(self.screen, self.BLACK, (self.cell_size, (i + 1) * self.cell_size), (self.board_size * self.cell_size, (i + 1) * self.cell_size))

    def check_win(self, row: int, col: int):
        """ 判断是否有五子连珠 """

        # print(f'{row=}; {col=}')

        data_left, data_right, data_up, data_down = "", "", "", ""
        for i in range(9):

            # 收集左边的棋子
            if 0 <= col - i < self.board_size:
                # print(f'0000 {row=}; {col - i=}')
                data_left += self.board[row][col - i]

            # 收集右边的棋子
            if 0 <= col + i < self.board_size:
                # print(f'0000 {row=}; {col - i=}')
                data_right += self.board[row][col + i]

            # 收集上边的棋子
            if 0 <= row - i < self.board_size:
                data_up += self.board[row - 1][col]

            # 收集下边的棋子
            if 0 <= row + i < self.board_size:
                data_down += self.board[row + 1][col]

            # print(f'{data_left=}')
            # print(f'{data_right=}')
            # print(f'{data_up=}')
            # print(f'{data_down=}')

        # print(f'1111  {row=}; {col=}')
        # print("#" * 40)

        # for b in self.board:
        #     print(b)
        #     print("\n")

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # 向一个方向搜索
            nx, ny = row + dx, col + dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == self.board[row][col]:
                count += 1
                nx += dx
                ny += dy
            # 向相反方向搜索
            nx, ny = row - dx, col - dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == self.board[row][col]:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False

    def play(self):
        # 初始化 pygame
        pygame.init()
        # 绘制棋盘
        self.draw_board()

        # 主循环
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    # 坐标修正
                    x_pos = x_pos - 1  # noqa
                    y_pos = y_pos - 3  # noqa
                    print(f'{x_pos=};{y_pos=}')
                    i = round(x_pos / self.cell_size) - 1
                    j = round(y_pos / self.cell_size) - 1
                    if 0 <= i < self.board_size and 0 <= j < self.board_size and self.board[j][i] == u"　  ":
                        print(f"{i=};{j=};{self.current_player=};{self.board[i][j]}")
                        self.board[j][i] = self.current_player

                        # 绘制棋子
                        if "黑" in self.board[j][i]:
                            pygame.draw.circle(self.screen, self.BLACK, ((i + 1) * self.cell_size, (j + 1) * self.cell_size), self.cell_size // 2 - 2)
                        elif "白" in self.board[j][i]:
                            pygame.draw.circle(self.screen, self.WHITE, ((i + 1) * self.cell_size, (j + 1) * self.cell_size), self.cell_size // 2 - 2)

                        # print(1, f'{i=};{j=}; ')  # todo delete
                        if self.check_win(j, i):
                            # print(f"玩家 {self.current_player} 获胜！")
                            running = False
                        # 换对手下
                        self.current_player = "白" if self.current_player == "黑" else "黑"

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gomoku = Pygomoku()
    gomoku.play()
