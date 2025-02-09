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


class NBA(Enum):
    PAST_NBA_GAMES = "Последние результаты"
    FUTURE_NBA_GAMES = "Ближайшие игры"
    STANDINGS_NBA = "Положение команд"

