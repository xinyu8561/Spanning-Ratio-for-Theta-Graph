import random as rd
import math as math
import copy as cp


# how to deal with the points on the line of the cone???
# when k >= 7 won't be a cycle
# I directly use the distance, I didn't use project


def dataset_generator(number, seed):
    dataset = []
    for item in range(number):
        dataset.append([rd.randint(0, seed), rd.randint(0, seed)])
    f.write(str(dataset) + '\n')
    return dataset


def cone_check(point1, point2, k):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    angle = 0.0
    dy = float(y2 - y1)
    dx = float(x2 - x1)
    if dy == 0 and dx > 0: angle = 0.0
    if dy == 0 and dx < 0: angle = math.pi
    if dx == 0 and dy > 0: angle = math.pi / 2
    if dx == 0 and dy < 0: angle = 3.0 * math.pi / 2.0
    if dx > 0 and dy > 0: angle = math.atan(dy / dx)
    elif dx < 0 and dy > 0: angle = math.pi - math.atan(math.fabs(dy / dx))
    elif dx < 0 and dy < 0: angle = math.pi + math.atan(dy / dx)
    elif dx > 0 and dy < 0:  angle = 2.0 * math.pi - math.atan(math.fabs(dy / dx))
    cn = math.ceil((angle * float(k)) / (2.0 * math.pi))
    return cn if cn > 0 else 1

def t_cal(point_1, point_2, ds, k, dis):
    if point_1[0] == point_2[0] and point_1[1] == point_2[1]: return dis
    cone = cone_check(point_1, point_2, k)
    temp_len = len(ds)
    res = float('inf')
    point = ()
    for item in range(temp_len):
        point_temp = (ds[item][0], ds[item][1])
        if cone_check(point_1, point_temp, k) == cone:
            tmp1, tmp2 = point_temp[0], point_temp[1]
            x1, y1 = point_1[0], point_1[1]
            # tan, b = ort_line(cone, x1, y1, k)
            e_dis = math.sqrt((tmp1 - x1) * (tmp1 - x1) + (tmp2 - y1) * (tmp2 - y1))
            # not much difference in the results after project
            # (sometime this part is wrong because of precise loss)
            # e_dis = project_dis(tmp1, tmp2, tan, b, x1, y1, e_dis)
            if e_dis != 0 and res > e_dis:
                point = point_temp
                res = e_dis
    return t_cal(point, point_2, ds, k, dis + res)

def ort_line(cone, x1, y1, k):
    tan = 2.0 * math.pi * (cone - 1.0) + math.pi / (k + 0.0001)
    b = y1 / (tan * x1 + 0.0001)
    return tan, b

def project_dis(pnt_x, pnt_y, line_tan, line_b, x1, y1, e_dis):
    tan1 = (y1 - pnt_y) / (x1 - pnt_x)
    tan2 = line_tan
    angle = math.fabs(math.atan(tan1) - math.atan(tan2))
    return e_dis * math.cos(angle)

def spanner(ds, k):
    cnt = 1
    len_ds = len(ds)
    point = ()
    res = 0.0
    for i in range(len_ds):
        for j in range(i + 1, len_ds):
            if ds[i][0] != ds[j][0] or ds[i][1] != ds[j][1]:
                point1 = (ds[i][0], ds[i][1])
                point2 = (ds[j][0], ds[j][1])

                total_distance = t_cal(point1[:], point2[:], ds[:], k, 0.0)
                t_spanner = total_distance / math.sqrt(
                    (point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (
                                point1[1] - point2[1]))
                if res < t_spanner:
                    res = t_spanner
                    point = (point1, point2)
                cnt = cnt + 1
    return point, res


f = open("test.txt", "w")
k = 7.0
for i in range(200):
    f.write("Dataset " + str(i) + ":\n")
    ds = dataset_generator(100, 1000)
    f.write("k: " + str(k) + '\n')
    f.write("Worst Case:\n")
    points, t = spanner(ds, k)
    theta = 2.0 * math.pi / k
    f.write("Point1: " + str(points[0]) + " Point2: " + str(points[1]) + '\n')
    f.write("1 / (cos(theta) - sin(theta)) : " + str(1.0 / (math.cos(theta) - math.sin(theta))) + "\n")
    f.write("1 / (1 - 2sin(theta/2)) : " + str(1.0 / (1.0 - 2.0 * math.sin(theta / 2.0))) + '\n')
    f.write("t: " + str(t) + '\n\n')


f.close()
