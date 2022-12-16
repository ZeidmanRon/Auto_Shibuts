from typing import List

import pandas as pd


class Soldier:
    def __init__(self, s: List[str]):
        (self.name, self.pref1, self.pref2, self.gender) = (s[0].strip(), s[1].strip(), s[2].strip(), s[3].strip())

    def __str__(self):
        return f"{self.name}, {self.gender} ({self.pref1}, {self.pref2})"


class Settlement:
    def __init__(self, name: str, capacity: int, priority: int, men: bool):
        (self.name, self.capacity, self.priority, self.men) = (name, capacity, priority, men)
        self.soldiers = []

    def add_soldiers(self, soldier_list: List[Soldier]):
        if len(self.soldiers) >= self.capacity:
            print('Settlement class, add_soldiers: this list of soldiers is bigger then the max capacity')
            return
        self.soldiers = soldier_list

    def add_soldier(self, soldier_to_add: Soldier):
        if len(self.soldiers) >= self.capacity:
            print('Settlement class, add_soldier: cant add more soldiers -> reached max capacity')
            return
        self.soldiers.append(soldier_to_add)

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
    # for soldier in soldiers_prefs:
    #     print(soldier)
    settlement1 = Settlement(name='אחיה', capacity=4, priority=1, men=True)
    settlement2 = Settlement(name='אש קודש', capacity=4, priority=2, men=True)
    settlement3 = Settlement(name='גבעת אסף', capacity=5, priority=3, men=True)
    settlement4 = Settlement(name='נווה אח"י', capacity=5, priority=4, men=True)
    settlement5 = Settlement(name='קידה', capacity=5, priority=5, men=False)
    settlement6 = Settlement(name='עמיחי', capacity=3, priority=6, men=False)
    settlement7 = Settlement(name='גבעת הראל', capacity=5, priority=7, men=False)
    settlement8 = Settlement(name='גבעת הרואה', capacity=5, priority=8, men=False)
    settlement9 = Settlement(name='מצפה דני', capacity=4, priority=9, men=False)
    settlement10 = Settlement(name='מגרון', capacity=4, priority=10, men=False)
    settlement11 = Settlement(name='כרם רעים', capacity=5, priority=10, men=False)
    settlement12 = Settlement(name='חרשה', capacity=2, priority=10, men=True)
    settlement13 = Settlement(name='אלוני שילה', capacity=2, priority=10, men=True)
    settlement14 = Settlement(name='אל מתן', capacity=3, priority=10, men=False)

    # set settlements and their prioritization:

    # yeshuv1 = Settlement('aria', [temp1, temp2])
    # print(yeshuv1)
