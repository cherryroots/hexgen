from tkinter import Tk, BOTH, Canvas
from typing import Tuple


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def xy(self) -> Tuple[int, int]:
        return self.x, self.y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(self.p1.xy(), self.p2.xy(), fill=fill_color, width=2)


class Window:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title("hexgen")
        self.__root.resizable(0, 0)

        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def center(self) -> Tuple[int, int]:
        return self.width / 2, self.height / 2

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def draw(self, line: Line, fill_color: str = "black") -> None:
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self) -> None:
        self.__running = True
        print("window opened")
        while self.__running:
            self.redraw()
        print("window closed")

    def close(self) -> None:
        self.__running = False
