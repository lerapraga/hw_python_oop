

class InfoMessage:
    """Это самостоятельный класс для создания объектов сообщений."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки.
    Содержит все основные свойства и методы для тренировок."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах)."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Возвращает значение средней скорости"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:  # type: ignore
        """Возвращает количество килокалорийи"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращает объект класса сообщения."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    LEN_STEP = 0.65
    KMH_IN_MS = 0.278
    MIN_IN_H = 60

    def get_spent_calories(self) -> float:
        '''Расчёт количества калорий'''
        # Проверьте формулу расчёта потраченных калорий в классе `Running`
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CM_IN_M: float = 100
    KMH_IN_MSEC: float = 0.278
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        '''Расчёт количества калорий,
        израсходованных за тренировку.'''

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP: float = 1.38
    M_IN_KM = 1000
    CALORIES_SWIMMING: float = 1.1
    CALORIES_MEAN_SWIMMING: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SWIMMING)
                * self.weight * self.duration
                * self.CALORIES_MEAN_SWIMMING)


def read_package(workout_type: str, data: list) -> Training:
    """Должна принимать на вход код тренировки
    и список её параметров."""

    type_of_training: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in type_of_training:
        class_training: Training = type_of_training[workout_type](*data)
        return class_training
    else:
        raise ValueError('Тренировки нет!')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training)
    print(info.get_message())

    #  return(f'Тип тренировки: {self.training_type}')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
