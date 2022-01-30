from math import dist
from threading import Semaphore
from numpy import result_type
from sympy import Plane, Point3D, Line3D, symbols
# from sympy.solvers import solve
from statistics import mean, stdev
from copy import deepcopy
import itertools
import time
import json

from sympy.core.function import Function
from sympy.geometry import plane
from sympy.geometry.util import intersection
from sympy.logic.boolalg import Boolean
from sympy.solvers.solvers import solve


def get_item_if_exists(sensor_array, sensor_index, index):
    try:
        return sensor_array[sensor_index][index]
    except IndexError:
        return None


def get_average(sensor_array: list, sensor_index: int, data_index: int) -> int:
    average_list = []
    average_list.append(get_item_if_exists(
        sensor_array, sensor_index, data_index-1))
    average_list.append(get_item_if_exists(
        sensor_array, sensor_index-1, data_index))
    average_list.append(get_item_if_exists(
        sensor_array, sensor_index+1, data_index))
    average_list = [item for item in average_list if item != None]
    return int(mean(average_list))


def point_plane_distance(point: Point3D, plane: Plane, signed: Boolean = True):
    """
    get point to plane distance along Z axis

    Args:
        point (Point3D): [description]
        plane (Plane): [description]
        signed (Boolean, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """    
    # distance = plane.distance(point)
    # if signed:
    #     x, y, z = symbols('x y z')
    #     equation = plane.equation(x, y, z)
    #     exper = equation.xreplace({x: point.x, y: point.y})
    #     solve_list = solve(exper)
    #     if solve_list:
    #         z_index = int(solve_list[0])
    #         distance = distance if point.z > z_index else -distance
    # return distance

    distance=0
    x, y, z = symbols('x y z')
    equation = plane.equation(x, y, z)
    exper = equation.xreplace({x: point.x, y: point.y})
    solve_list = solve(exper)
    if solve_list:
        z_index = int(solve_list[0])
        distance = point.z-z_index
        distance = distance if signed else abs(distance)
    return distance


def signed_max(item_list):
    return max(item_list, key=abs)


class Tile_Geo():
    _valid_diffrence_reading = 1
    _valid_value = 0
    _special_corner_point_list = ['pa1b1', 'pa1b2', 'pa2b1', 'pa2b2']
    _special_point_neighbourhood_list = ['na1b1', 'na1b2', 'na2b1', 'na2b2']
    _special_side_point_list = ['sa1', 'sa2', 'sb1', 'sb2']
    _special_side_a = ['sa1', 'sa2']
    _special_side_b = ['sb1', 'sb2']
    _special_center_point = 'cp'
    _static_reading = 'sr'

    def __init__(self, sensors_array: list, offset_list: list, special_points_coordinate_dict: dict = None, deep_copy: bool = False) -> None:
        self.offset_list = offset_list
        # reverse sensor arrays order to match coardinates
        sensors_array = list(reversed(sensors_array))
        self.sensors_array = deepcopy(
            sensors_array) if deep_copy else sensors_array
        self.is_data_valid = True
        self.max_sensor_samples = 0
        self.special_points_coordinate_dict = special_points_coordinate_dict
        self.filter_sensor_data()
        self.validate_sensor_data()
        self.repair_sensor_data()
        if not special_points_coordinate_dict:
            self.default_special_points_coordinate()

    def filter_sensor_data(self):
        self.sensor_count = len(self.sensors_array)

        for sensor_id in range(self.sensor_count):
            offset = self.offset_list[sensor_id]
            sensor = [
                item - offset if item > self._valid_value else 0 for item in self.sensors_array[sensor_id]]
            if sensor[0] == 0 and sensor[-1] == 0:
                sensor = [item for item in sensor if item != 0]
            else:
                sensor = None
                self.is_data_valid = False
                # todo log here
                print('no valid data')
            self.sensors_array[sensor_id] = sensor

    def validate_sensor_data(self):
        sensor_data_count_list = [len(sensor) for sensor in self.sensors_array]
        self.max_sensor_samples = max(sensor_data_count_list)
        self.is_data_valid &= max(
            sensor_data_count_list) - min(sensor_data_count_list) <= self._valid_diffrence_reading

    def repair_sensor_data(self):
        if self.is_data_valid:
            tmp_sensor_array = [list(reversed(sensor))
                                for sensor in self.sensors_array]
            for sensor_id in range(self.sensor_count):
                sensor = tmp_sensor_array[sensor_id]
                while len(sensor) < self.max_sensor_samples:
                    sensor.append(get_average(
                        tmp_sensor_array, sensor_id, len(sensor)-1))
            self.sensors_array = [list(reversed(sensor))
                                  for sensor in tmp_sensor_array]

    def default_special_points_coordinate(self) -> None:
        if self.is_data_valid:
            end_x = self.sensor_count-1
            end_y = self.max_sensor_samples-1
            self.special_points_coordinate_dict = {'pa1b1': [(end_x, end_y)], 'pa1b2': [(end_x, 0)], 'pa2b1': [(0, end_y)], 'pa2b2': [(0, 0)], 'na1b1': [(end_x-1, end_y), (end_x-1, end_y-1), (end_x, end_y-1)], 'na1b2': [(end_x-1, 0), (end_x-1, 1), (end_x, 1)], 'na2b1': [
                (0, end_y-1), (1, end_y-1), (1, end_y)], 'na2b2': [(1, 0), (1, 1), (0, 1)], 'sa1': [(end_x, int(end_y/2))], 'sa2': [(0, int(end_y/2))], 'sb1': [(int(end_x/2), end_y)], 'sb2': [(int(end_x/2), 0)], 'cp': [(int(end_x/2), int(end_y/2))]}
            self.special_points_coordinate_dict['sr'] = list(itertools.product(
                range(1, end_x), range(1, end_y)))

    def calculate_special_points(self, map_function_list: list) -> None:
        # calculate points
        for point_name in self._special_corner_point_list + self._special_side_point_list+[self._special_center_point]:
            coordinate_list = self.special_points_coordinate_dict[point_name]
            x_list = []
            y_list = []
            z_list = []

            for x, y in coordinate_list:
                x_list.append(x)
                y_list.append(y)
                z_list.append(self.sensors_array[x][y])

            x = map_function_list[0](x_list)
            y = map_function_list[1](y_list)
            z = map_function_list[2](z_list)

            setattr(self, point_name, Point3D(x, y, z))

        # calculate neighbourhoods
        for point_name in self._special_point_neighbourhood_list:
            coordinate_list = self.special_points_coordinate_dict[point_name]
            same_x_list = []
            same_y_list = []
            unsame_list = []

            for x, y in coordinate_list:
                if x in [self.sensor_count-1, 0]:
                    same_x_list.append((x, y))
                elif y in [self.max_sensor_samples-1, 0]:
                    same_y_list.append((x, y))
                else:
                    unsame_list.append((x, y))

            neighbourhood_list = []
            for neighbourhood in [same_x_list, same_y_list, unsame_list]:
                x_list = []
                y_list = []
                z_list = []

                for x, y in neighbourhood:
                    x_list.append(x)
                    y_list.append(y)
                    z_list.append(self.sensors_array[x][y])

                x = map_function_list[0](x_list)
                y = map_function_list[1](y_list)
                z = map_function_list[2](z_list)
                neighbourhood_list.append(Point3D(x, y, z))

            setattr(self, point_name, neighbourhood_list)

    def calculate_special_planes(self) -> None:
        self.corner_plane_list = []
        for point in self._special_corner_point_list:
            point_list = [getattr(
                self, item) for item in self._special_corner_point_list if item != point]
            plane = Plane(*point_list)
            setattr(self, f'plane_{point}', plane)
            self.corner_plane_list.append(plane)

        for point in self._special_point_neighbourhood_list:
            neighbourhood_point_list = getattr(self, point)
            setattr(self, f'plane_{point}', Plane(*neighbourhood_point_list))

    def calculate_continuous_reading_points(self) -> None:
        # todo remove offset from all date mabye
        coordinate_list = self.special_points_coordinate_dict[self._static_reading]
        self.static_reading_list = []
        for index in set(map(lambda item: item[0], coordinate_list)):
            sample_list = [self.sensors_array[x][y]
                           for x, y in coordinate_list if x == index]
            self.static_reading_list.append(sample_list)

    def curve_center(self, result_map_function: Function) -> int:
        result_list = [point_plane_distance(getattr(
            self, self._special_center_point), plane) for plane in self.corner_plane_list]
        return int(result_map_function(result_list))

    def curve_side_a(self, result_map_function: Function) -> int:
        result_list = []
        for side in self._special_side_a:
            result_list += [point_plane_distance(getattr(self, side), plane)
                            for plane in self.corner_plane_list]
        return int(result_map_function(result_list))

    def curve_side_b(self, result_map_function: Function) -> int:
        result_list = []
        for side in self._special_side_b:
            result_list += [point_plane_distance(getattr(self, side), plane)
                            for plane in self.corner_plane_list]
        return int(result_map_function(result_list))

    def warpage(self, result_map_function: Function) -> int:
        result_list = []
        for point in self._special_corner_point_list:
            plane = getattr(self, f'plane_{point}')
            result_list.append(point_plane_distance(
                getattr(self, point), plane, signed=False))
        return int(result_map_function(result_list))

    def continuous_reading(self, sensor_array_map_function: Function, result_map_function: Function) -> int:
        result_list = [sensor_array_map_function(
            item) for item in self.static_reading_list]
        return int(result_map_function(result_list))

    def corner(self, result_map_function: Function) -> int:
        result_list = []
        for point in self._special_point_neighbourhood_list:
            plane = getattr(self, f'plane_{point}')
            result_list.append(point_plane_distance(
                getattr(self, f'p{point[1:]}'), plane))
        return int(result_map_function(result_list))

    def get_grade(self) -> dict:
        result = {}
        if self.is_data_valid:
            self.calculate_special_points([mean, mean, mean])
            self.calculate_special_planes()
            self.calculate_continuous_reading_points()
            result['curve_center'] = self.curve_center(signed_max)
            result['curve_side_a'] = self.curve_side_a(signed_max)
            result['curve_side_b'] = self.curve_side_b(signed_max)
            result['warpage'] = self.warpage(signed_max)
            result['continuous_reading'] = self.continuous_reading(
                stdev, signed_max)
            result['corner'] = self.corner(signed_max)
        return result


def time_it(fn):
    start = time.time()
    result = fn()
    end = time.time()
    print(f'{fn.__name__} >>>> {end-start}')
    return result


def file_test(file_id):
    offset_list = [987, 1076, 1131, 1148, 1186]
    sample_file = []
    with open(f'tile_{file_id}.json') as f:
        sample_file = json.loads(f.read())
    for setting, data in sample_file.items():
        print(f'setting {setting}')
        for sample in data:
            t_id = data[sample]['tile_id']
            sensor_data = data[sample]['data']
            # print(sensor_data)
            tile = Tile_Geo(sensor_data, offset_list)
            print(f't_id:{t_id}', tile.get_grade())


if __name__ == '__main__':
    file_test(1)
    # sensor_data = [[0,1,2,3,0],[0,4,5,6,0],[0,7,8,9,0],[0,10,11,12,0]]
    # tile = Tile_Geo(sensor_data, [0,0,0,0])
    # print(tile.get_grade())

