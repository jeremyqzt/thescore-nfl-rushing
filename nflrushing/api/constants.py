from stats.types import SortByTypes, SortTypes

NoneInput = "None"

SortByTypesMap = {
    "ASC": SortByTypes.ASC,
    "DESC": SortByTypes.DESC,
    NoneInput: None,
}

SortTypesMap = {
    "TOTAL_RUSHING_YARDS": SortTypes.TOTAL_RUSHING_YARDS,
    "LONGEST_RUSH": SortTypes.LONGEST_RUSH,
    "TOTAL_RUSHING_TOUCHDOWN": SortTypes.TOTAL_RUSHING_TOUCHDOWN,
    NoneInput: None,
}
