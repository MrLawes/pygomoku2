import sys

import pygame


class Pygomoku:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self):
        # 设置棋盘大小
        self.board_size = 15
        # 设置棋格大小
        self.cell_size = 40
        # 创建五子棋游戏界面
        size = self.cell_size * (self.board_size + 1)
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption("五子棋")
        pygame.display.flip()

        # 绘制重启按钮
        self.restart_btn = pygame.Rect(
            (self.board_size - 2) * self.cell_size,  # X坐标
            10,  # Y坐标
            self.cell_size * 2,  # 宽度
            self.cell_size // 1.5  # 高度
        )

        # 重置游戏数据
        self.reset_game()

    def draw_board(self):
        """ 绘制棋盘 """

        pygame.init()

        # 棋盘颜色
        self.screen.fill((230, 189, 144))

        # 画横线竖线
        for i in range(self.board_size):
            pygame.draw.line(self.screen, self.BLACK, ((i + 1) * self.cell_size, self.cell_size), ((i + 1) * self.cell_size, self.board_size * self.cell_size))
            pygame.draw.line(self.screen, self.BLACK, (self.cell_size, (i + 1) * self.cell_size), (self.board_size * self.cell_size, (i + 1) * self.cell_size))

        # 画中元和星位
        for x, y in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7), ]:
            center = ((x + 1) * self.cell_size, (15 - y) * self.cell_size)
            pygame.draw.circle(self.screen, (139, 69, 19), center, self.cell_size // 2 - 14)

        # 画重置按钮
        pygame.draw.rect(self.screen, (34, 139, 34), self.restart_btn)  # 绿色按钮
        font = pygame.font.SysFont(None, 24)
        text = font.render("Restart", True, self.WHITE)
        text_rect = text.get_rect(center=self.restart_btn.center)
        self.screen.blit(text, text_rect)

    def check_win(self, row: int, col: int):
        """ 判断是否有五子连珠 """

        data_left, data_right, data_up, data_down = "", "", "", ""
        for i in range(9):

            # 收集左边的棋子
            if 0 <= col - i < self.board_size:
                data_left += self.data["board"][row][col - i]

            # 收集右边的棋子
            if 0 <= col + i < self.board_size:
                data_right += self.data["board"][row][col + i]

            # 收集上边的棋子
            if 0 <= row - i < self.board_size:
                data_up += self.data["board"][row][col]

            # 收集下边的棋子
            if 0 <= row + i < self.board_size:
                data_down += self.data["board"][row][col]

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # 向一个方向搜索
            nx, ny = row + dx, col + dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.data["board"][nx][ny][0] == self.data["board"][row][col][0]:  # noqa
                count += 1
                nx += dx
                ny += dy
            # 向相反方向搜索
            nx, ny = row - dx, col - dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.data["board"][nx][ny][0] == self.data["board"][row][col][0]:  # noqa
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
        current_player = "black" if self.data["current_player"] == "黑" else "white"
        text = font.render(f"Player {current_player} Wins!", True, self.RED)
        text_rect = text.get_rect(center=(popup_width // 2, popup_height / 2))

        # 组合元素
        popup.blit(text, text_rect)
        x = (self.board_size + 1) * self.cell_size / 2 - (popup_width / 2)
        self.screen.blit(popup, (x, 0))
        pygame.display.flip()

    def draw_piece_to_notation(self, x, y, color):
        """ 画一个棋子到棋谱 """
        pygame.draw.circle(self.screen, color, ((x + 1) * self.cell_size, (15 - y) * self.cell_size), self.cell_size // 2 - 2)

    def pay(self, x: int, y: int):
        """ 落子, 并返回是否棋局结束了, false: 棋局结束了 """

        if 0 <= x < self.board_size and 0 <= y < self.board_size and self.data["board"][x][y] == "空":
            self.data["times"] += 1
            self.data["board"][x][y] = f"{self.data["current_player"]}{self.data["times"]:03d}"
            center = ((x + 1) * self.cell_size, (15 - y) * self.cell_size)

            # 绘制棋子
            if "黑" in self.data["board"][x][y]:
                self.draw_piece_to_notation(x, y, self.BLACK)
            elif "白" in self.data["board"][x][y]:
                self.draw_piece_to_notation(x, y, self.WHITE)

            # 当前棋位画上小红点
            pygame.draw.circle(self.screen, self.RED, center, self.cell_size // 2 - 14)

            # 去掉之前棋子的红点
            if self.data["times"] > 1:
                for search_x, row in enumerate(self.data["board"]):
                    for search_y, record in enumerate(row):
                        if f"{self.data["times"] - 1:03d}" in record:
                            if "黑" in record:
                                self.draw_piece_to_notation(search_x, search_y, self.BLACK)
                            elif "白" in record:
                                self.draw_piece_to_notation(search_x, search_y, self.WHITE)

            if self.check_win(x, y):
                self.data["winner"] = self.data["current_player"]
                self.show_win_popup()

            # 换对手下
            self.data["current_player"] = "白" if self.data["current_player"] == "黑" else "黑"

    def reset_game(self):
        self.data = {  # noqa
            "board": [["空" for _ in range(self.board_size)] for _ in range(self.board_size)],  # 初始化棋盘
            "current_player": "黑",  # 先手黑
            "winner": "",  # 重置赢家
            "times": 0,  # 重置当前下棋第几手
        }
        self.draw_board()

    def search_notation(self):
        """ 搜索棋盘 """
        # todo
        pass

    def main(self):

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
                    x = round(x_pos / self.cell_size) - 1
                    y = 15 - round(y_pos / self.cell_size)

                    # 点击重置按钮
                    if self.restart_btn.collidepoint(event.pos):
                        self.reset_game()
                        continue

                    if not self.data["winner"]:
                        self.pay(x, y)
                        if self.data["current_player"] == "黑":
                            print("尝试自动下棋")
                        # todo 匹配棋盘, 自动下棋

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gomoku = Pygomoku()
    gomoku.main()
