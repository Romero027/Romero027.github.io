import gurobipy as gp
from gurobipy import GRB



def lp_solver(datas, systems, budget, cost, preference, bw, data_trans_size):

    num_of_clients = len(datas)
    num_of_class = len(datas[0])

    # Create a new model
    m = gp.Model("client_selection")


        
    qlist = []
    for idx, _ in enumerate(datas):
        for i in range(len(datas[0])):
            qlist.append((idx, i))
    quantity = 

    slowest = m.addVar(vtype=GRB.CONTINUOUS, name="slowest", lb = 0.0)
    quantity = m.addVar(vtype=GRB.INTEGER, name="quantity", lb = 0)

    time_list = [((sum([quantity[(i, j)] for j in range(num_of_class)])/systems[i]) + data_trans_size/bw[i]) for i in range(num_of_clients)]



    # The objective is to minimize the slowest
    m.setObjective(slowest, GRB.MINIMIZE)


datas = [[10, 20, 10, 1], [0, 19, 1, 5], [7, 0, 10, 9], [0, 0, 1, 10]]
system = [14, 10, 17, 10]
bw = [2, 5, 5, 10]
data_trans_size = 5
cost = [1, 1, 1, 1]
budget = 2
preference = [10, 20, 15, 20]
lp_solver(datas, system, budget, cost, preference, bw, data_trans_size)
