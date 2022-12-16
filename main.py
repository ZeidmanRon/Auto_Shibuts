from typing import List

import pandas as pd


class Soldier:
    def __init__(self, s: List[str]):
        (self.name, self.pref1, self.pref2, self.gender) = (s[0].strip(), s[1].strip(), s[2].strip(), s[3].strip())

    def __str__(self):
        return f"{self.name}, {self.gender} ({self.pref1}, {self.pref2})"


class Settlement:
    def __init__(self, name: str, soldiers: List[Soldier], priority: int):
        (self.name, self.soldiers, self.priority) = (name, soldiers, priority)

    def __str__(self):
        names = []
        for s in self.soldiers:
            names.append(s.__str__())
        return f"{self.name} ({names})"


if __name__ == '__main__':
    # read file of soldiers and get their preferences
    df = pd.read_excel('preferences.xlsx', sheet_name='prefs')
    soldiers_prefs = []
    for soldier in df.values:
        soldiers_prefs.append(Soldier(soldier))
    for soldier in soldiers_prefs:
        print(soldier)
    # set settlements and their prioritization:

    # yeshuv1 = Settlement('aria', [temp1, temp2])
    # print(yeshuv1)
