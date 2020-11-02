import pygame
import random
from typing import List, Tuple
import time
from abc import ABC, abstractmethod


class Element:

    def __init__(self, value: int, parent: "ElementList"):
        self.value = value
        self.parent = parent

    def __gt__(self, other: "Element"):
        return self.value > other.value

    def __str__(self):
        return str(self.value)

    def draw(self, surface: pygame.Surface, index: int, color: Tuple[int, int, int] = (255, 0, 0)):
        bar_height = self.value * surface.get_height() / max(self.parent).value
        rect = (index * self.parent.bar_width, surface.get_height() - bar_height, self.parent.bar_width, bar_height)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)
        """
        if index * self.parent.bar_width < mouse_pos[0] < (index + 1) * self.parent.bar_width:
            pygame.draw.rect(surface, (0, 255, 0), rect, 1)
        else:
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)
        """


class ElementList:

    def __init__(self):
        self.elements: List[Element] = []
        self.bar_width = 0

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def add(self, value: int):
        self.elements.append(Element(value, self))
        self.bar_width = int(screen.get_width() / len(self.elements))

    def get_hover(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        bar_width = int(screen.get_width() / len(self.elements))
        return int(mouse_pos[0] / bar_width)

    def draw(self, screen: pygame.Surface):
        for index in range(len(self.elements)):
            self.elements[index].draw(screen, index)


class AbstractSort(ABC):

    @abstractmethod
    def keep_looping(self) -> bool:
        pass

    @abstractmethod
    def draw(self, background: pygame.Surface) -> None:
        pass


class InsertionSort(AbstractSort):

    def __init__(self, numbers: ElementList):
        self.numbers = numbers
        self.index = 1
        self.el = self.index - 1
        self.number = numbers[self.index]

    def keep_looping(self) -> bool:
        return self.index < len(self.numbers)

    def draw(self, background: pygame.Surface) -> None:
        self.number.draw(background, self.index, (0, 0, 255))
        self.numbers[self.el].draw(background, self.el, (255, 255, 0))
        if self.el >= 0 and self.number < numbers[self.el]:
            numbers[self.el + 1] = numbers[self.el]
            self.el -= 1
        else:
            self.numbers[self.el].draw(background, self.el, (0, 255, 0))
            pygame.display.flip()
            time.sleep(sleeping_time)
            self.numbers[self.el + 1] = self.number
            self.index += 1
            if not self.index == len(numbers):
                self.number = numbers[self.index]
                self.el = self.index - 1


class MergeSort(AbstractSort):

    def __init__(self, numbers: ElementList):
        self.numbers = numbers
        self.shard_queue = []
        self.__populate_queue(self.numbers)

    def __populate_queue(self, array, index: int = 0):
        if len(array) > 1:
            middle_point = len(array) // 2
            self.shard_queue.append((index, middle_point))
            print(f"Adding ({index},{middle_point})")
            self.__populate_queue(array[:middle_point], index)
            self.shard_queue.append((index + middle_point, len(array) - middle_point))
            print(f"Adding ({index + middle_point},{len(array) - middle_point})")
            self.__populate_queue(array[middle_point:], middle_point)

    def keep_looping(self) -> bool:
        return len(self.shard_queue) > 0

    def draw(self, background: pygame.Surface) -> None:
        shard_index, shard_size = self.shard_queue.pop(0)
        for index in range(shard_index, shard_index + shard_size):
            self.numbers[index].draw(background, index, (255, 255, 0))


if __name__ == "__main__":
    import sys
    pygame.init()
    pygame.font.init()

    screen: pygame.Surface = pygame.display.set_mode((1200, 800))
    background = pygame.Surface(screen.get_size())
    numbers = ElementList()
    n = int(sys.argv[1])
    sleeping_time = float(sys.argv[2])
    for el in random.sample(range(1, n + 1), n):
        numbers.add(el)

    font = pygame.font.SysFont("None", 32)

    #sorter = InsertionSort(numbers)
    sorter = MergeSort(numbers)
    main_loop = True
    while sorter.keep_looping() and main_loop:
        mouse_pos = pygame.mouse.get_pos()
        background.fill((255, 255, 255))
        numbers.draw(background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    main_loop = False
                elif pygame.key.get_pressed()[pygame.K_LEFT] and sleeping_time > 0:
                    sleeping_time -= .001
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    sleeping_time += .001

        sorter.draw(background)
        background = background.convert()
        screen.blit(background, (0, 0))
        """
        hover_index = numbers.get_hover(screen)
        if hover_index is not None:
            font_surface = font.render(str(numbers[hover_index]), True, (0, 0, 0)).convert_alpha()
            pos_x = mouse_pos[0] + (10 if mouse_pos[0] + 10 < screen.get_width() - font_surface.get_width()
                                       else -font_surface.get_width())
            screen.blit(font_surface, (pos_x, mouse_pos[1] + 10))
        """
        screen.blit(font.render(f"slow down: {round(sleeping_time, 4)}", True, (0, 0, 0)).convert_alpha(), (10, 10))
        pygame.display.flip()
        time.sleep(sleeping_time)

    if main_loop:
        background.fill((255, 255, 255))
        numbers.draw(background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
        time.sleep(2)

