#!/usr/bin/env python

import random
from typing import List, Tuple, Callable, Dict
import math
import time
import argparse


class Sorter:

    def __init__(self, array: List[int]):
        self.array = array

    def __result_is_correct(self, array: List[int]) -> bool:
        return all([array[i] <= array[i + 1] for i in range(len(array) - 1)])

    def __bold(self, text: str) -> str:
        return f"\033[1m{text}\033[0m"

    def __write_results(self, algo: str, amount: int, duration: float):
        import os.path
        name_file = f"results.csv"
        output_file_existed = os.path.isfile(name_file)
        with open(name_file, "a") as f:
            if not output_file_existed:
                f.write("algorithm,amount,duration\n")
            f.write(f"{algo.strip().lower()},{amount},{duration}\n")

    def __sort(self, method: Callable[[List[int], Dict], List[int]], method_name: str, **kwargs: Dict):
        print(f"Running {self.__bold(method_name)} with {len(self.array)} elements. ", end='', flush=True)
        array_copy = self.array.copy()
        start_time = time.time()
        result = method(array_copy, **kwargs)
        end_time = time.time()
        print(f"Took {round(end_time - start_time, 4)} seconds to sort {len(self.array)} elements.")
        print(f"The final result is{' ' if self.__result_is_correct(result) else ' not '}correctly ordered")
        # self.__write_results(method_name.replace(" ", "_"), len(self.array), end_time - start_time)

    def __insertion_sort(self, array: List[int]) -> List[int]:
        for index in range(1, len(array)):
            number = array[index]
            el = index - 1
            while el >= 0 and number < array[el]:
                array[el + 1] = array[el]
                el -= 1
            array[el + 1] = number
        return array

    def __merge(self, array: List[int], middle_point: int) -> List[int]:
        left_arr = [array[i] for i in range(len(array[:middle_point]))]
        right_arr = [array[i] for i in range(middle_point, middle_point + len(array[middle_point:]))]

        i = j = 0
        k = 0
        while i < len(array[:middle_point]) and j < len(array[middle_point:]):
            if left_arr[i] <= right_arr[j]:
                array[k] = left_arr[i]
                i += 1
            else:
                array[k] = right_arr[j]
                j += 1
            k += 1
        while i < len(array[:middle_point]):
            array[k] = left_arr[i]
            i += 1
            k += 1
        while j < len(array[middle_point:]):
            array[k] = right_arr[j]
            j += 1
            k += 1
        return array

    def __merge_sort(self, array: List[int]) -> List[int]:
        if len(array) > 1:
            middle_point = len(array) // 2
            array[:middle_point] = self.__merge_sort(array[:middle_point])
            array[middle_point:] = self.__merge_sort(array[middle_point:])
            array = self.__merge(array, middle_point)
        return array

    def __timsort(self, array: List[int], **kwargs: Dict) -> List[int]:
        run_size = kwargs["run_size"] or 32
        for index in range(0, len(array), run_size):
            upper_bound = min(index + run_size, len(array))
            array[index:upper_bound] = self.__insertion_sort(array[index:upper_bound])
        size = run_size
        while size <= len(array):
            for index in range(0, len(array), size * 2):
                upper_bound = min(index + (size * 2), len(array))
                array[index:upper_bound] = self.__merge(array[index:upper_bound], size)
            size *= 2
        return array

    def __quicksort_partition(self, array: List[int]) -> Tuple[List[int], int]:
        pivot = array[-1]
        i = 0
        for j in range(len(array)):
            if array[j] < pivot:
                array[i], array[j] = array[j], array[i]
                i += 1
        array[i], array[-1] = array[-1], array[i]
        return array, i

    def __quicksort(self, array: List[int]) -> List[int]:
        if len(array) > 1:
            array, partition = self.__quicksort_partition(array)
            array[:partition] = self.__quicksort(array[:partition])
            array[partition:] = self.__quicksort(array[partition:])
        return array

    def __heapify(self, array: List[int], i: int = 0) -> List[int]:
        largest = i
        left_child = 2 * i + 1 if 2 * i + 1 < len(array) else None
        right_child = 2 * i + 2 if 2 * i + 2 < len(array) else None

        if left_child is not None and array[left_child] > array[largest]:
            largest = left_child
        if right_child is not None and array[right_child] > array[largest]:
            largest = right_child

        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            self.__heapify(array, largest)

        return array

    def __heapsort(self, array: List[int]) -> List[int]:
        for i in range(len(array) // 2 - 1, -1, -1):
            array = self.__heapify(array, i)
        for i in range(len(array) - 1, 0, -1):
            array[i], array[0] = array[0], array[i]
            array[:i] = self.__heapify(array[:i])
        return array

    def __introsort(self, array: List[int], **kwargs: Dict) -> List[int]:
        depth_limit = int(kwargs["depth_limit"])
        if len(array) < 16:
            return self.__insertion_sort(array)
        elif depth_limit == 0:
            return self.__heapsort(array)
        else:
            middle = len(array) // 2
            pivot = 0 if array[middle] >= array[0] >= array[-1] or array[middle] <= array[0] <= array[-1] else \
                middle if array[0] >= array[middle] >= array[-1] or array[0] <= array[middle] <= array[-1] else -1
            array[pivot], array[-1] = array[-1], array[pivot]
            _, partition = self.__quicksort_partition(array)
            array[:partition] = self.__introsort(array[:partition], **{"depth_limit": depth_limit - 1})
            array[partition:] = self.__introsort(array[partition:], **{"depth_limit": depth_limit - 1})
            return array

    def insertion_sort(self):
        self.__sort(self.__insertion_sort, "insertion sort")

    def merge_sort(self):
        self.__sort(self.__merge_sort, "merge sort")

    def timsort(self, run_size: int = 32):
        self.__sort(self.__timsort, f"timsort {run_size}", **{"run_size": run_size})

    def quicksort(self):
        self.__sort(self.__quicksort, "quicksort")

    def heapsort(self):
        self.__sort(self.__heapsort, "heapsort")

    def introsort(self):
        depth_limit = int(2 * math.log2(len(self.array)))
        self.__sort(self.__introsort, "introsort", **{"depth_limit": depth_limit})


def create_list(n: int) -> List[int]:
    return random.sample(range(n), n)


def create_worst_case_quicksort(n: int) -> List[int]:
    numbers = list(range(n))
    numbers[:-1] = numbers[1:]
    numbers[-1] = 0
    return numbers


def create_worst_case_insertion_sort(n: int) -> List[int]:
    return list(range(n - 1, -1, -1))


def create_best_case_insertion_sort(n: int) -> List[int]:
    return list(range(n))


def main():
    import sys
    sys.setrecursionlimit(4000)
    algorithms = ["insertion", "merge", "timsort", "quicksort", "heapsort", "introsort"]
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="Amount of elements in list", type=int, required=True)
    parser.add_argument("-a", "--algorithm", help="Sorting algorithm to run", required=True, choices=algorithms)
    parser.add_argument("--run-size", help="Size of the run, only to be used with timsort", default=32, type=int)
    args = parser.parse_args()
    numbers = create_list(args.number)
    algo = args.algorithm
    sorter = Sorter(numbers)
    if algo == "insertion":
        sorter.insertion_sort()
    elif algo == "merge":
        sorter.merge_sort()
    elif algo == "timsort":
        sorter.timsort(args.run_size)
    elif algo == "quicksort":
        sorter.quicksort()
    elif algo == "heapsort":
        sorter.heapsort()
    elif algo == "introsort":
        sorter.introsort()
    else:
        import sys
        print(f"Chosen algorithm '{algo}' is not an available option")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
