import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import MinMaxScaler


class Genetic:
    """class for genetic optimization """
    def __init__(self, population_size, data_path, wight_name, cost_name):
        # initialize data storage and gen names
        self.wight_name = wight_name
        self.cost_name = cost_name
        self.data = pd.read_csv(data_path)
        # get hyper parameter population_size
        self.population_size = population_size
        # create begin population
        self.population = pd.DataFrame(columns=self.data.index, index=np.arange(self.population_size + 1))
        self.population = self.population.applymap(lambda x: np.random.choice([True, False]))
        # initialize new_population
        self.new_population = pd.DataFrame()
        # initialize unit_rate
        self.unit_rate = pd.Series()


    def fitness(self):
        """
        Calculates rate fore each unit in population
        :return:
        np.array with scalar rate
        """
        # get accumulative cost
        cost = self.population.apply(lambda x: sum(self.data.loc[x.values, self.cost_name]), axis=1)

        # get accumulative wight
        wight = self.population.apply(lambda x: sum(self.data.loc[x.values, self.wight_name]), axis=1)
        # result is hou many cost in one wight for the unit
        result = cost
        # if accumulative wight bigger than wight border the population unit rate equal to zero
        select = (wight > 6) | (wight == 0)
        result.loc[select] = 0
        # scaling
        self.unit_rate = result/sum(result)
        print(self.unit_rate)



    def selection(self):
        """
        puts new unit to new population by rolling method until half is full
        :return:
            pass
        """
        new_population = pd.DataFrame(columns=self.data.index,)
        while len(new_population) < self.population_size/2:
            new_population = new_population.append(
                self.population.loc[np.random.choice(self.population.index, p=self.unit_rate)], ignore_index=True)
        self.new_population = new_population


    def crossbreeding(self):
        """
        crossbreeds two roll unites and and add new units to new population until it full
        :return:
            pass
        """
        while self.population_size - len(self.new_population) > 0:
            # get slice of gen id for crossbreeding
            border_1 = np.random.random_integers(0, len(self.population.columns)+1)
            border_2 = np.random.random_integers(0, len(self.population.columns)+1)
            select_interval = self.population.columns[min(border_1, border_2): max(border_1, border_2)]
            # get parents
            first_parent = self.population.loc[np.random.choice(self.population.index, p=self.unit_rate)]
            second_parent = self.population.loc[np.random.choice(self.population.index, p=self.unit_rate)]
            # get childes and add it to the new population
            first_child = first_parent
            first_child.loc[select_interval] = second_parent.loc[select_interval]
            self.new_population = self.new_population.append(first_child, ignore_index=True)
            second_child = second_parent
            second_child.loc[select_interval] = first_parent.loc[select_interval]
            self.new_population = self.new_population.append(second_child, ignore_index=True)


    def mutation(self):
        mutation_value = np.random.random_integers(3, 20)
        mutation_unit_ids = []
        while len(mutation_unit_ids)/self.population_size*100 < mutation_value:
            mutation_unit_ids.append(np.random.choice(self.new_population.index))
        for i in mutation_unit_ids:
            mutation_count = np.random.random_integers(1, len(self.new_population.columns))
            mutation_gens = random.sample(list(self.new_population.columns), mutation_count)
            if len(mutation_gens) == 1:
                self.new_population.loc[i, mutation_gens] = np.random.choice([True, False])
            else:
                self.new_population.loc[i, mutation_gens] = self.new_population.loc[i, mutation_gens].apply(
                    lambda x: np.random.choice([True, False]))


    def elitism(self):
        self.new_population = self.new_population.append(self.population.loc[self.unit_rate.idxmax()])


    def run(self, loop_count):
        for i in range(loop_count):
            self.fitness()
            self.selection()
            self.crossbreeding()
            self.mutation()
            self.elitism()
        return self.population.loc[self.unit_rate.idxmax()]

if __name__ == '__main__':
    print(Genetic(population_size=100, data_path='data.csv', wight_name='вес', cost_name='ценность').run(50))