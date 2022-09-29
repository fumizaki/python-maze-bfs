# python standard library
import random

class Maze:

    def __init__(self, length=11, maze=None):
        """
        length * lengthの正方形(迷路)を作成する
        """
        self.__length = length
        self.__maze = [[0]*self.__length for _ in range(self.__length)] if maze is None else maze

    def create_maze(self):

        def _make_inside_walls():
            """
            約30%を壁とし、迷路を作成する
            """
            for i in range(len(self.__maze)):
                for j in range(len(self.__maze[i])):
                    # 約30%を壁にする
                    num = random.randint(1, 10)
                    if num % 3 == 0:
                        self.__maze[i][j] = -1


        def _make_outside_walls():
            """
            迷路の外側に壁を作成する
            底はすべてゴールとする
            """
            top = [[-1]*(self.__length) for _ in range(self.__length)]
            bottom = [[-2]*(self.__length) for _ in range(self.__length)]
            # 上辺
            self.__maze.insert(0, top[0])
            # 下辺
            self.__maze.append(bottom[0])
            # 両側
            for i in range(len(self.__maze)):
                # 左端
                self.__maze[i].insert(0, -1)
                # 右端
                self.__maze[i].append(-1)

        def _set_entry_point():
            """
            上辺の中央を探索開始地点にする
            """
            self.__maze[0][len(self.__maze[0])//2] = 1
            # エントリーポイントの左右は未探索にしておく
            self.__maze[0][(len(self.__maze[0])//2) - 1] = 0
            self.__maze[0][(len(self.__maze[0])//2) + 1] = 0

        _make_inside_walls()
        _make_outside_walls()
        _set_entry_point()


    def get_entry_point(self):
        """
        探索開始地点の位置情報を取得する
        """
        for i in range(len(self.__maze[0])):
            if self.__maze[0][i] == 1:
                return [[0, i, self.__maze[0][i]]]


    def get_goal_point(self):
        """
        ゴール地点の位置情報を取得する
        """
        for i in range(len(self.__maze[len(self.__maze)-1])):
            if self.__maze[len(self.__maze)-1][i] > 0:
                return [[len(self.__maze)-1, i]]


    def draw_route(self, route):
        """
        迷路の探索結果とゴールまでのルートを描画する
        """
        draw = ''
        for i in range(len(self.__maze)):
            for j in range(len(self.__maze[i])):
                # 探索開始地点
                if self.__maze[i][j] == 1:
                    draw += ' S '
                # 壁
                elif self.__maze[i][j] == -1:
                    draw += ' ■ '
                # 未探索
                elif self.__maze[i][j] == 0:
                    draw += ' o '
                # ゴール(未到達)
                elif self.__maze[i][j] == -2:
                    draw += ' - '
                # ルート
                elif [i, j] in route:
                    draw += ' $ '
                # 探索済み
                else:
                    draw += ' + '
            draw += '\n'
        print(draw)


    def get_route(self):
        """
        探索開始地点からゴールまでのルートを取得する
        """
        point = self.get_goal_point()
        route = []
        while len(point) > 0:
            route.append(point[0])
            x, y = point.pop(0)

            # 左側
            if self.__maze[x][y-1] == self.__maze[x][y] - 1:
                point.append([x, y-1])
            # 右側
            elif self.__maze[x][y+1] == self.__maze[x][y] - 1:
                point.append([x, y+1])
            # 上側
            elif self.__maze[x-1][y] == self.__maze[x][y] - 1:
                point.append([x-1, y])

        return route[::-1]



    def bfs(self):
        """
        幅優先探索
        """
        point = self.get_entry_point()

        while len(point) > 0:
            x, y, depth = point.pop(0)

            # 下側がゴールの場合
            if self.__maze[x+1][y] == -2:
                self.__maze[x+1][y] = depth + 1
                return True

            # 左側
            if self.__maze[x][y-1] == 0:
                self.__maze[x][y-1] = depth+1
                point.append([x, y-1, depth+1])

            # 右側
            if self.__maze[x][y+1] == 0:
                self.__maze[x][y+1] = depth+1
                point.append([x, y+1, depth+1])

            # 下側
            if self.__maze[x+1][y] == 0:
                self.__maze[x+1][y] = depth+1
                point.append([x+1, y, depth+1])

        print('No Goal')
        return False



if __name__ == '__main__':
    maze = Maze(31)
    maze.create_maze()
    flg = maze.bfs()
    if flg:
        maze.draw_route(maze.get_route())
