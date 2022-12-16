import itertools
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


class Shibuts:
    def __init__(self, my_settlements: List[Settlement], available_males: List[Soldier],
                 available_females: List[Soldier]):
        self.settlements = my_settlements
        self.available_males = male_soldiers
        self.available_females = female_soldiers
        self.settlement_dict = {}

    def remove_settlement_and_soldiers_after_recruited(self, settlement_to_remove: Settlement,
                                                       soldiers_to_remove: List[Soldier]):
        if settlement_to_remove.men:
            for s in soldiers_to_remove:
                for sol in self.available_males:
                    if s.name == sol.name:
                        self.available_males.remove(sol)
        else:
            for s in soldiers_to_remove:
                for sol in self.available_females:
                    if s.name == sol.name:
                        self.available_females.remove(sol)

        for s in self.settlements:
            if s.name == settlement_to_remove.name:
                self.settlements.remove(s)

    def calc_all_shibutsim(self):
        for settlement in self.settlements:
            if settlement.men:
                most_connected, connections = self.find_most_connected_group(settlement.capacity, True)
                self.settlement_dict[settlement.name] = self.get_names_of_soldiers(
                    most_connected) + f', with {connections} connections.'
            else:
                most_connected, connections = self.find_most_connected_group(settlement.capacity, False)
                self.settlement_dict[settlement.name] = self.get_names_of_soldiers(
                    most_connected) + f', with {connections} connections.'

            self.remove_settlement_and_soldiers_after_recruited(settlement_to_remove=settlement,
                                                                soldiers_to_remove=most_connected)

    def find_most_connected_group(self, size: int, is_men: bool) -> (List[Soldier], int):
        group_dict = {}
        if is_men:
            for subset in itertools.combinations(self.available_males, size):
                group_dict[subset] = self.calc_connection(subset)
        else:
            for subset in itertools.combinations(self.available_females, size):
                group_dict[subset] = self.calc_connection(subset)

        max_connections = max(group_dict, key=group_dict.get)
        return max_connections, group_dict[max_connections]

    def calc_connection(self, group: List[Soldier]) -> int:
        counter = 0
        for soldier1 in group:
            for soldier2 in group:
                if soldier1.pref1 == soldier2.name or soldier1.pref2 == soldier2.name:
                    counter += 1
        return counter

    def get_names_of_soldiers(self, soldiers: List[Soldier]) -> str:
        names = ''
        for i in range(len(soldiers) - 1):
            names += f' {soldiers[i].name},'
        return names + f' {soldiers[len(soldiers) - 1].name}'


if __name__ == '__main__':
    # read file of soldiers and get their preferences
    df = pd.read_excel('preferences.xlsx', sheet_name='prefs')
    all_soldiers = []
    for soldier in df.values:
        all_soldiers.append(Soldier(soldier))

    male_soldiers = []
    female_soldiers = []
    for soldier in all_soldiers:
        if soldier.gender == 'male':
            male_soldiers.append(soldier)
        else:
            female_soldiers.append(soldier)

    # for soldier in soldiers_prefs:
    #     print(soldier)

    # set settlements and their prioritization:
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
    settlements = [settlement1, settlement2, settlement3, settlement4, settlement5, settlement6, settlement7,
                   settlement8, settlement9, settlement10, settlement11, settlement12, settlement13, settlement14]

    my_shibuts = Shibuts(settlements, male_soldiers, female_soldiers)
    my_shibuts.calc_all_shibutsim()
    for key, value in my_shibuts.settlement_dict:
        print(f'settlement: {key}, soldiers: {value}')
    # most_connected, connections = my_shibuts.find_most_connected_group(5)
    # print(most_connected[0].name + '\n', most_connected[1].name + '\n', most_connected[2].name + '\n',
    #       most_connected[3].name + '\n',
    #       most_connected[4].name + '\n', connections)
