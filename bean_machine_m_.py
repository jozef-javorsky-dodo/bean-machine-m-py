import random
from typing import Tuple, List
from PIL import Image, ImageDraw

class GaltonBoard:
    DEFAULT_NUM_ROWS: int = 12
    DEFAULT_NUM_BALLS: int = 50_000
    DEFAULT_BOARD_WIDTH: int = 1000
    DEFAULT_BOARD_HEIGHT: int = 600
    PEG_RADIUS: int = 8
    BACKGROUND_COLOR: Tuple[int, int, int] = (102, 51, 153)
    LEFT_HALF_COLOR: Tuple[int, int, int] = (122, 122, 244)
    RIGHT_HALF_COLOR: Tuple[int, int, int] = (122, 244, 122)

    def __init__(self, num_rows: int = DEFAULT_NUM_ROWS, num_balls: int = DEFAULT_NUM_BALLS, board_width: int = DEFAULT_BOARD_WIDTH, board_height: int = DEFAULT_BOARD_HEIGHT) -> None:
        self.num_rows: int = num_rows
        self._num_balls: int = num_balls
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.slot_counts: List[int] = [0] * self.board_width
        self.image: Image.Image = Image.new("RGB", (self.board_width, self.board_height), self.BACKGROUND_COLOR)
        self.draw: ImageDraw.Draw = ImageDraw.Draw(self.image)

    @property
    def num_balls(self) -> int:
        return self._num_balls

    @num_balls.setter
    def num_balls(self, num_balls: int) -> None:
        self._num_balls = num_balls

    def simulate(self) -> None:
        for i in range(self.num_balls):
            self.slot_counts[self.calculate_bin_index()] += 1
            if (i + 1) % 10000 == 0:
                print(f"Simulated {i + 1}/{self.num_balls} balls")

    def generate_image(self) -> Image.Image:
        self.draw_histogram()
        return self.image

    def save_image(self, filename: str = 'galton_board.png') -> None:
        self.generate_image().save(filename)

    def calculate_bin_index(self) -> int:
        bin_index: int = self.board_width // 2
        for _ in range(self.board_height):
            try:
                random_direction: int = random.choice([-1, 1])
                bin_index += random_direction
            except Exception:
                bin_index += 1
        return max(0, min(bin_index, self.board_width - 1))

    def draw_histogram(self) -> None:
        max_frequency: int = max(self.slot_counts)
        bar_width: int = self.board_width // len(self.slot_counts)

        for bin_index, frequency in enumerate(self.slot_counts):
            self.draw_bar(frequency, bin_index, max_frequency, bar_width)

    def draw_bar(self, frequency: int, bin_index: int, max_frequency: int, bar_width: int) -> None:
        bar_height: int = self.calculate_bar_height(frequency, max_frequency)
        x0: int = bin_index * bar_width
        y0: int = self.board_height - bar_height
        x1: int = x0 + bar_width
        y1: int = self.board_height

        color: Tuple[int, int, int] = self.LEFT_HALF_COLOR if x0 < self.board_width // 2 else self.RIGHT_HALF_COLOR
        self.draw.rectangle([x0, y0, x1, y1], fill=color)

    def calculate_bar_height(self, frequency: int, max_frequency: int) -> int:
        return 0 if max_frequency == 0 else int(frequency / max_frequency * self.board_height)

def generate_galton_board() -> None:
    board: GaltonBoard = GaltonBoard()
    board.simulate()
    board.save_image()

if __name__ == "__main__":
    generate_galton_board()