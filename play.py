import sys

import pygame


class Pygomoku:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        # 设置棋盘大小
        self.board_size = 15
        # 棋盘
        self.board: list[list[str]] = [["空" for _ in range(self.board_size)] for _ in range(self.board_size)]
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
        # 下棋次数
        self.times = 0

    def draw_board(self):
        """ 绘制棋盘 """
        self.screen.fill((230, 189, 144))  # 棋盘颜色
        for i in range(self.board_size):
            pygame.draw.line(self.screen, self.BLACK, ((i + 1) * self.cell_size, self.cell_size), ((i + 1) * self.cell_size, self.board_size * self.cell_size))
            pygame.draw.line(self.screen, self.BLACK, (self.cell_size, (i + 1) * self.cell_size), (self.board_size * self.cell_size, (i + 1) * self.cell_size))

    def check_win(self, row: int, col: int):
        """ 判断是否有五子连珠 """

        data_left, data_right, data_up, data_down = "", "", "", ""
        for i in range(9):

            # 收集左边的棋子
            if 0 <= col - i < self.board_size:
                data_left += self.board[row][col - i]

            # 收集右边的棋子
            if 0 <= col + i < self.board_size:
                data_right += self.board[row][col + i]

            # 收集上边的棋子
            if 0 <= row - i < self.board_size:
                data_up += self.board[row][col]

            # 收集下边的棋子
            if 0 <= row + i < self.board_size:
                data_down += self.board[row][col]

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # 向一个方向搜索
            nx, ny = row + dx, col + dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny][0] == self.board[row][col][0]:
                count += 1
                nx += dx
                ny += dy
            # 向相反方向搜索
            nx, ny = row - dx, col - dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny][0] == self.board[row][col][0]:  # noqa
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False

    def show_win_popup(self):
        """ 胜利提示 """

        popup_width = self.cell_size * 4
        popup_height = self.cell_size
        popup = pygame.Surface((popup_width, popup_height))
        popup.fill((230, 189, 144))

        # 使用默认字体渲染英文
        font = pygame.font.SysFont(None, 20)
        current_player = "black" if self.current_player == "黑" else "white"
        text = font.render(f"Player {current_player} Wins!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(popup_width // 2, popup_height / 2))

        # 组合元素
        popup.blit(text, text_rect)
        x = (self.board_size + 1) * self.cell_size / 2 - (popup_width / 2)
        self.screen.blit(popup, (x, 0))
        pygame.display.flip()

    def pay(self, x: int, y: int):
        """ 落子, 并返回是否棋局结束了, false: 棋局结束了 """

        if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == "空":
            self.times += 1
            self.board[x][y] = f"{self.current_player}{self.times:03d}"
            center = ((x + 1) * self.cell_size, (15 - y) * self.cell_size)

            # 绘制棋子
            if "黑" in self.board[x][y]:
                pygame.draw.circle(self.screen, self.BLACK, center, self.cell_size // 2 - 2)
            elif "白" in self.board[x][y]:
                pygame.draw.circle(self.screen, self.WHITE, center, self.cell_size // 2 - 2)

            if self.check_win(x, y):
                self.winner = self.current_player
                self.show_win_popup()

            # 换对手下
            self.current_player = "白" if self.current_player == "黑" else "黑"

    def main(self):
        # 初始化 pygame
        pygame.init()
        # 绘制棋盘
        self.draw_board()

        # 主循环
        running = True
        while running:
            for event in pygame.event.get():
                if self.winner:
                    continue
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    # 坐标修正
                    x_pos = x_pos - 1  # noqa
                    y_pos = y_pos - 3  # noqa
                    x = round(x_pos / self.cell_size) - 1
                    y = 15 - round(y_pos / self.cell_size)
                    self.pay(x, y)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gomoku = Pygomoku()
    gomoku.main()
