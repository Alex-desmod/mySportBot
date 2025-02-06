from enum import Enum

class Sports(Enum):
    BASKET = "баскетбол 🏀"
    CYCLING = "велоспорт 🚴"
    ATHLETICS = "бега и прочая легкая атлетика 🏃‍♀️🏃"

class Basket(Enum):
    EURO = "Евролига"
    NBA = "НБА"

class Euro(Enum):
    PAST_EURO_GAMES = "Последние результаты"
    FUTURE_EURO_GAMES = "Ближайшие игры"
    STANDINGS_EURO = "Положение команд"

