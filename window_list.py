import pyautogui as pyg
import time
from python_imagesearch.imagesearch import imagesearch_loop


def get_windows_titles():
    for x in pyg.getAllWindows():
        print(x.title)


def is_window_open(title: str) -> bool:
    res = False
    for x in pyg.getAllWindows():
        if title == x.title:
            res = True
            break
    return res


def main():
    print(is_window_open('АСТРА-ГАЗ'))


if __name__ == '__main__':
    # pyg.useImageNotFoundException()
    main()
