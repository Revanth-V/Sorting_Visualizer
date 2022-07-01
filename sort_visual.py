import math

import pygame
import random
pygame.init()

class DrawInformation():
    # defining colors that we will be using for our rectangle bars and text
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    RED = 255, 0, 0
    YELLOW = 255, 250, 100
    PINK = 255, 192, 203
    BACKGROUND_COLOR = WHITE

    # 3 shades of grey to represent our rectangle blocks i.e. our list
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # whenever we draw something in python we use font and this is the way to set the font
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    # initialization which sets the width and the height of the instance of the object
    # lst is the list which needs to be sorted and we will store it inside of this instance
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # whenever we work with pygame we need to set up a screen or window that we're going to draw everything on
        # we use pygame.display.set_mode whenever we create a window; we are passing width and height as a tuple here
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # block_width depends on the number of items in the list
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # block_height depends on the minimum value and the maximum value in the list
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                        draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    # blit means to copy graphics from one image to another
    # A more formal definition is to copy an array of data to a bitmapped array destination
    # informally we can say blit means assigning pixels
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | Q - Quick Sort | M - Merge Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)

    # used to update the display
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        # defining only the section of the screen we want to redraw on
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # this gives the index and value of every single element in the list
    for i, val in enumerate(lst):
        # we can find the starting co-ordinates of every block
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        # color assigned among the three values of the gradients
        color = draw_info.GRADIENTS[i % 3]

        # to color the two indices we will be swapping
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# function to randomly generate the starting list
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        # this val can have any value between min_val and max_val (both inclusive)
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def quick_sort(draw_info, ascending=True):
    # use an iterative version to adjust the settings in the main function
    lst = draw_info.lst
    l, h = 0, len(lst) - 1

    stack = [0] * len(lst)
    # push initial values of l and h to stack
    top = 0
    stack[top] = l
    top += 1
    stack[top] = h
    # Keep popping from stack whenever it is not empty
    while top >= 0:
        # Pop h and l
        h = stack[top]
        top -= 1
        l = stack[top]
        top -= 1
        # Set pivot element at its correct position in
        # sorted array
        i = l - 1
        x = lst[h]
        for j in range(l, h):
            if ascending:
                if lst[j] <= x:
                    # increment index of smaller element
                    i = i + 1
                    lst[i], lst[j] = lst[j], lst[i]
            else:  # descending:
                if lst[j] >= x:
                    # increment index of larger element
                    i = i + 1
                    lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.YELLOW, l: draw_info.PINK, h: draw_info.RED}, True)
            yield True
        lst[i + 1], lst[h] = lst[h], lst[i + 1]
        p = i + 1

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    low = 0
    high = len(lst) - 1
    # sort list `lst` using lst temporlstry list `temp`
    temp = lst[:]

    # divide the list into blocks of size `m`
    # m = [1, 2, 4, 8, 16…]

    m = 1
    while m <= high - low:
        # for m = 1, i = [0, 2, 4, 6, 8…]
        # for m = 2, i = [0, 4, 8, 12…]
        # for m = 4, i = [0, 8, 16…]
        # …
        for i in range(low, high, 2 * m):
            frm = i
            mid = i + m - 1
            to = min(i + 2 * m - 1, high)
            k = frm
            i = frm
            j = mid + 1

            # loop till no elements are left in the left and right runs
            while i <= mid and j <= to:
                if ascending:
                    if lst[i] <= lst[j]:
                        temp[k] = lst[i]
                        i = i + 1
                    else:
                        temp[k] = lst[j]
                        j = j + 1
                else:  # descending
                    if lst[i] >= lst[j]:
                        temp[k] = lst[i]
                        i = i + 1
                    else:
                        temp[k] = lst[j]
                        j = j + 1
                k = k + 1
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.YELLOW, k: draw_info.RED, m: draw_info.PINK},
                          True)
                yield True
            # copy remaining elements
            while i < len(lst) and i <= mid:
                temp[k] = lst[i]
                k = k + 1
                i = i + 1
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.YELLOW, k: draw_info.RED, m: draw_info.PINK},
                          True)
                yield True
            # copy back to the original list to reflect sorted order
            for i in range(frm, to + 1):
                lst[i] = temp[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.YELLOW, k: draw_info.RED, m: draw_info.PINK},
                          True)
                yield True
        m = 2 * m
    return lst


def main():
    run = True

    # this creates a clock object which can be used to keep track of time
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    # instantiating object of class DrawInformation
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    # represents what sorting algorithm we will use
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    # generates or performs the sorting algorithm we want
    sorting_algorithm_generator = None

    # pygame event loop
    while run:

        # this regulates how quickly the application will run
        clock.tick(60)

        # if we are currently sorting, call the next(sorting_algorithm_generator) method
        # if it is not responding, which essentially means the sorting is complete
        # then raise an exception which says StopIteration and put sorting = False
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # quits the application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # key press controls
            # key 'r' is for resetting the application
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            # key 'space' is for starting the sort procedure
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            # key 'a' chooses the ascending option of sorting
            elif event.key == pygame.K_a and not sorting:
                ascending = True

            # key 'd' chooses the descending option of sorting
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            # key 'i' selects Insertion Sort
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            # key 'b' selects Bubble Sort
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            # key 'q' selects Quick Sort
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            # key 'm' selects Merge Sort
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":
    main()