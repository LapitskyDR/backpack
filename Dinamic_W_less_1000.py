import pandas as pd
import numpy as np


def run_optimization(data, w_border, cost_name, wight_name):
    """

    :param data:
    pd.DataFrame should includes
        cost of items
        wight of items
    :param w_border:
        w_border - wight limit
    :param cost_name: str column name of cost
    :param wight_name: str column name of wight
    :return:
    """
    # get cost as v
    try:
        v = data[cost_name]
    except KeyError:
        print(f'data not include {cost_name}')
    # get wight as w
    try:
        w = data[wight_name]
    except KeyError:
        print(f'data not include {wight_name}')
    # initial result table
    result_cost_table = pd.DataFrame(columns=np.arange(w_border, step=0.1), index=['no_one'] + list(data.index))
    result_scoup_table = pd.DataFrame(columns=np.arange(w_border, step=0.1), index=['no_one'] + list(data.index))
    result_cost_table = result_cost_table.applymap(lambda x: 0)
    print(result_cost_table)
    for i, name in enumerate(result_cost_table.index):
        if name == 'no_one':
            continue
        else:
            selected = result_cost_table.columns < data.loc[name, wight_name]
            result_cost_table.loc[name, selected] = result_cost_table.loc[result_cost_table.index[i-1], selected]
            result_scoup_table.loc[name, selected] = result_scoup_table.loc[result_scoup_table.index[i - 1], selected]
            result_cost_table.loc[name, ~selected] = np.maximum(result_cost_table.loc[result_cost_table.index[i - 1], ~selected], result_cost_table.loc[result_cost_table.index[i - 1], ~selected] + data.loc[name, cost_name])
    return result_cost_table

if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    data.set_index('id', inplace=True)
    print(data.head())
    print(run_optimization(data, 6, 'ценность', 'вес'))
