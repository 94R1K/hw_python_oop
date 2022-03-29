from decimal import Decimal


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = Decimal(duration)
        self.distance = Decimal(distance)
        self.speed = Decimal(speed)
        self.calories = Decimal(calories)

    def get_message(self) -> str:
        """"Получить сообщение о выполненной тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=workout_type,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        average_speed: float = self.get_mean_speed()
        return ((coeff_calorie_1 * average_speed - coeff_calorie_2)
                * self.weight / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        average_speed: float = self.get_mean_speed()
        return ((coeff_calorie_1 * self.weight
                 + (average_speed**2 // self.height)
                 * coeff_calorie_2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 1.38
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        average_speed: float = self.get_mean_speed()
        return ((average_speed + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict = {workout_type: data}
    for workout, information in dictionary.items():
        if workout == 'RUN':
            return Running(action=information[0],
                           duration=information[1],
                           weight=information[2])
        elif workout == 'WLK':
            return SportsWalking(action=information[0],
                                 duration=information[1],
                                 weight=information[2],
                                 height=information[3])
        elif workout == 'SWM':
            return Swimming(action=information[0],
                            duration=information[1],
                            weight=information[2],
                            length_pool=information[3],
                            count_pool=information[4])


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
