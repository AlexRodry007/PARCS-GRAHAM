from Pyro4 import expose
from random import randrange
import math


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        dots = self.read_input()
        step = int(len(dots) / len(self.workers))
        mapped = []

        for i in list(range(0, len(self.workers))):
            print("Current worker: " + str(i))
            if i < len(self.workers) - 1:
                addition = self.workers[i].mymap(dots[i * step:(i + 1) * step])
                mapped.append(addition)
            else:
                addition = self.workers[i].mymap(dots[i * step:])
                mapped.append(addition)

        result = self.myreduce(mapped)
        self.write_output(result)
        print("Job finished")

    @staticmethod
    @expose
    def mymap(list_of_dots):
        answer = convex_hull(list_of_dots)
        return answer

    @staticmethod
    @expose
    def myreduce(mapped):
        output = []
        for x in mapped:
            output += x.value
        answer = convex_hull(output)
        return answer

    def read_input(self):
        f = open(self.input_file_name, 'r')
        list_of_dots = []
        for line in f:
            list_of_dots.append([int(line.split(',')[0]), int(line.split(',')[1].rstrip('\n'))])
        f.close()
        return list_of_dots

    def write_output(self, answer):
        open(self.output_file_name, 'w').close()
        f = open(self.output_file_name, 'a')
        for dot in answer:
            f.write(str(dot[0]) + "," + str(dot[1]) + '\n')
        f.close()


def polar_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.atan2(y_diff, x_diff)


def distance(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.sqrt(x_diff**2 + y_diff**2)


def cross_product(p1, p2, p3):
    x1, y1 = p2[0] - p1[0], p2[1] - p1[1]
    x2, y2 = p3[0] - p1[0], p3[1] - p1[1]
    return x1*y2 - x2*y1

@expose
def convex_hull(points):
    points = sorted(points, key=lambda x: (x[1], x[0]))
    start_point = points[0]
    points = sorted(points, key=lambda x: polar_angle(start_point, x))
    stack = [points[0], points[1]]
    for point in points[2:]:
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], point) < 0:
            stack.pop()
        stack.append(point)
    return stack


def randomise_input(file, amount):
    open(file, 'w').close()
    f = open(file, 'a')
    for i in range(amount):
        f.write(str(randrange(10000000)) + "," + str(randrange(10000000)) + '\n')
    f.close()


if __name__ == '__main__':
    randomise_input("input.txt", 1000000)
