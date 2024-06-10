import enum
from graphics import (
    Window,
    Point,
    Line,
)


class Cell:
    def __init__(self, win: Window) -> None:
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.__x1, self.__y1 = 0, 0  # top left
        self.__x2, self.__y2 = 0, 0  # bottom right
        self.__win = win

    def draw(self, x1, y1, x2, y2) -> None:
        self.__x1, self.__y1 = x1, y1  # top left
        self.__x2, self.__y2 = x2, y2  # bottom right

        corners = [
            Point(self.__x1, self.__y1),
            Point(self.__x2, self.__y1),
            Point(self.__x2, self.__y2),
            Point(self.__x1, self.__y2),
        ]

        # connect each point together
        lines = list(
            map(lambda i: Line(corners[i], corners[i + 1]), range(len(corners) - 1))
        )
        # connect the tail to the head
        lines.append(Line(corners[-1], corners[0]))

        if self.has_top_wall:
            self.__win.draw(lines[0])
        if self.has_right_wall:
            self.__win.draw(lines[1])
        if self.has_bottom_wall:
            self.__win.draw(lines[2])
        if self.has_left_wall:
            self.__win.draw(lines[3])
