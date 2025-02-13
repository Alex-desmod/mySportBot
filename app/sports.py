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


class Cycling(Enum):
    CLASSICS = "Монументы и другие крутые классики"
    GT = "Гранд-туры 🇮🇹🇫🇷🇪🇸"
    CYCLING_WC = "Чемпионат мира"


class Classics(Enum):
    SB = "17336"
    MSR = "17339"
    RVV = "17345"
    PR = "17347"
    AGR = "17348"
    FW = "17349"
    LBL = "17350"
    IL = "17363"


class GT(Enum):
    GIRO = "17365"
    TDF = "17366"
    VUELTA = "17367"


CYCLING_WC = 17469
MAJORS = 327
DIAMONDS = 240
ATHLETICS_WC = 109


class Athletics(Enum):
    MAJORS = "Марафоны-мейджоры"
    DIAMOND_LEAGUE = "Бриллиантовая лига 💎"
    ATHLETICS_WC = "Чемпионат мира"


class Countries(Enum):
    AU = "🇦🇺"
    BE = "🇧🇪"
    CN = "🇨🇳"
    CH = "🇨🇭"
    ES = "🇪🇸"
    DE = "🇩🇪"
    FR = "🇫🇷"
    GB = "🇬🇧"
    JP = "🇯🇵"
    IT = "🇮🇹"
    MA = "🇲🇦"
    MC = "🇲🇨"
    NL = "🇳🇱"
    NO = "🇳🇴"
    QA = "🇶🇦"
    PL = "🇵🇱"
    RW = "🇷🇼"
    SE = "🇸🇪"
    US = "🇺🇸"

class NBA_teams(Enum):
    CLE = "Кливленд"
    BOS = "Бостон"
    NY = "Нью-Йорк"
    IND = "Индиана"
    MIL = "Милуоки"
    DET = "Детройт"
    ORL = "Орландо"
    MIA = "Майами"
    ATL = "Атланта"
    CHI = "Чикаго"
    BKN = "Бруклин"
    PHI = "Филадельфия"
    TOR = "Торонто"
    CHA = "Шарлотт"
    WAS = "Вашингтон"
    OKC = "Оклахома"
    MEM = "Мемфис"
    DEN = "Денвер"
    HOU = "Хьюстон"
    LAL = "Лейкерс"
    LAC = "Клипперс"
    MIN = "Миннесота"
    DAL = "Даллас"
    SAC = "Сакраменто"
    GS = "Голден Стейт"
    PHO = "Финикс"
    SA = "Сан-Антонио"
    POR = "Портленд"
    UTA = "Юта"
    NO = "Новый Орлеан"

