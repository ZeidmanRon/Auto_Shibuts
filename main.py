import itertools
import random
from typing import List

import pandas as pd

class Soldier:
    def __init__(self, s: List[str]):
        self.name, self.pref1, self.pref2, self.gender = map(str.strip, s)

    def __str__(self):
        return f"{self.name}, {self.gender} ({self.pref1}, {self.pref2})"


class Settlement:
    def __init__(self, name: str, capacity: int, priority: int, men: bool):
        (self.name, self.capacity, self.priority, self.men) = (name, capacity, priority, men)
        self.soldiers = []

    def add_soldiers(self, soldier_list: List[Soldier]):
        if len(self.soldiers) + len(soldier_list) > self.capacity:
            print(f'{self.name} cannot accommodate all soldiers.')
            return
        self.soldiers.extend(soldier_list)

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
        self.settlements.remove(settlement_to_remove)
        for sol in soldiers_to_remove:
            settlement_to_remove.add_soldier(sol)
            if settlement_to_remove.men:
                self.available_males.remove(sol)
            else:
                self.available_females.remove(sol)

    def calc_all_shibutsim(self):
        # while len(self.settlements) > 0:
        for i in range(len(self.settlements)):
            if self.settlements[i].men:
                most_connected, connections = self.find_most_connected_group(self.settlements[i].capacity, True)
                self.settlement_dict[self.settlements[i].name] = self.get_names_of_soldiers(
                    most_connected) + f', with {connections} connections.'
            else:
                most_connected, connections = self.find_most_connected_group(self.settlements[i].capacity, False)
                self.settlement_dict[self.settlements[i].name] = self.get_names_of_soldiers(
                    most_connected) + f', with {connections} connections.'

            self.remove_settlement_and_soldiers_after_recruited(settlement_to_remove=self.settlements[i],
                                                                soldiers_to_remove=most_connected)

    def find_most_connected_group(self, size: int, is_men: bool) -> (List[Soldier], int):
        group_dict = {}
        if is_men:
            if size <= len(self.available_males):
                for subset in itertools.combinations(self.available_males, size):
                    group_dict[subset] = self.calc_connection(subset)
            else:
                print('no male soldiers left')
                pass
        else:
            if size <= len(self.available_females):
                for subset in itertools.combinations(self.available_females, size):
                    group_dict[subset] = self.calc_connection(subset)
            else:
                print('no female soldiers left')
                pass

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


def main():
    df = pd.read_excel('preferences.xlsx', sheet_name='prefs')
    all_soldiers = [Soldier(soldier) for soldier in df.values]

    male_soldiers = [soldier for soldier in all_soldiers if soldier.gender == 'זכר']
    female_soldiers = [soldier for soldier in all_soldiers if soldier.gender != 'זכר']

    random.shuffle(male_soldiers)
    random.shuffle(female_soldiers)

    settlement_data = [
        ('אחיה', 4, 1, True),  # Add other settlement data similarly
    ]

    main_settlements = [
        Settlement(name, capacity, priority, men) for name, capacity, priority, men in settlement_data
    ]
    random.shuffle(main_settlements)

    my_shibuts = Shibuts(main_settlements, male_soldiers, female_soldiers)
    my_shibuts.calc_all_shibutsim()

    for key, value in my_shibuts.settlement_dict.items():
        print(f'settlement: {key}, soldiers: {value}')

if __name__ == '__main__':
    main()
    print('Done!')
