from datetime import datetime
from teams.exception import NegativeTitlesError
from teams.exception import InvalidYearCupError
from teams.exception import ImpossibleTitlesError


class EnsureData:
    def data_processing(data):
        all_cup = []
        current_year = datetime.now().year

        for year in range(1930, current_year + 1):
            if year == 1930 or year == 1934 or year == 1938:
                all_cup.append(year)
            elif (year - 1950) % 4 == 0 and year >= 1950:
                all_cup.append(year)

        if "titles" in data:
            if data["titles"] < 0:
                raise NegativeTitlesError("titles cannot be negative")

        if "first_cup" in data:
            request_year = datetime.strptime(data["first_cup"], "%Y-%m-%d").year
            cup_count = (current_year - request_year) / 4
            if request_year < 1930:
                raise InvalidYearCupError("there was no world cup this year")
            elif request_year not in all_cup:
                raise InvalidYearCupError("there was no world cup this year")
            if "titles" in data:
                if data["titles"] > cup_count:
                    raise ImpossibleTitlesError(
                        "impossible to have more titles than disputed cups"
                    )
