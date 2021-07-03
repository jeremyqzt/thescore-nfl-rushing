from stats.types import SortByTypes, SortTypes

NoneInput = "None"

SortByTypesMap = {
    "ASC": SortByTypes.ASC,
    "DESC": SortByTypes.DESC,

    # Assuming some reasonable Defaults (Since we page)
    NoneInput: SortByTypes.ASC,
}

SortTypesMap = {
    "TOTAL_RUSHING_YARDS": SortTypes.TOTAL_RUSHING_YARDS,
    "LONGEST_RUSH": SortTypes.LONGEST_RUSH,
    "TOTAL_RUSHING_TOUCHDOWN": SortTypes.TOTAL_RUSHING_TOUCHDOWN,

    # Assuming some reasonable Defaults (Since we page)
    NoneInput: SortTypes.TOTAL_RUSHING_YARDS,
}
