import csv
import os
import sys


class WrongCarDataException(BaseException):
    pass


class BaseCar:
    def __init__(self, brand, photo_file_name, carrying):
        self.car_type = None  # car, truck, spec_machine
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(BaseCar):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = passenger_seats_count


class Truck(BaseCar):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        self._body_whl = body_whl
        self._parse_body_whl()

    def _parse_body_whl(self):
        params = str.split(self._body_whl, sep='x')

        if len(params) == 1 and params[0] == '':
            self.body_width = 0.0
            self.body_height = 0.0
            self.body_length = 0.0
            return

        if len(params) < 3:
            raise WrongCarDataException('Error: body_whl')

        try:
            self.body_width = float(params[0])
            self.body_height = float(params[1])
            self.body_length = float(params[2])
        except ValueError:
            raise WrongCarDataException('Error: body_whl')

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(BaseCar):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car(row):
    csv_struct = {'car_type': 0, 'brand': 1, 'passenger_seats_count': 2, 'photo_file_name': 3, 'body_whl': 4,
                  'carrying': 5, 'extra': 6}

    if len(row) < 6:
        raise WrongCarDataException('Error: some cells are empty')

    car_type = row[csv_struct['car_type']]
    brand = row[csv_struct['brand']]
    photo_file_name = row[csv_struct['photo_file_name']]

    try:
        carrying = float(row[csv_struct['carrying']])
    except ValueError:
        raise WrongCarDataException('Error: carrying')

    if car_type == 'car':
        try:
            passenger_seats_count = int(row[csv_struct['passenger_seats_count']])
        except ValueError:
            raise WrongCarDataException('Error: passenger_seats_count')

        new_car = Car(brand, photo_file_name, carrying, passenger_seats_count)

    elif car_type == 'truck':
        body_whl = row[csv_struct['body_whl']]
        new_car = Truck(brand, photo_file_name, carrying, body_whl)

    elif car_type == 'spec_machine':
        extra = row[csv_struct['extra']]
        new_car = SpecMachine(brand, photo_file_name, carrying, extra)
    else:
        raise WrongCarDataException('Error: car_type')

    return new_car


# return list of cars
def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename, 'r') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                new_car = get_car(row)
                car_list.append(new_car)
            except WrongCarDataException:
                continue

    return car_list


if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))
