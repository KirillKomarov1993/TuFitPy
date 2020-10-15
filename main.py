import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import loader as ld
import node as nd
import configuration as cnf
import field as fld
import numpy as np
import group as grp
import potential as ptl
import functional as fnc
import approximator as apr
import polarization as plr
import material as mt
import time as tm
import math as mth
import combination as cmb


def load_pair_group(number, colloid, amplitude):
    address = 'data/pair'
    group = grp.Group(number)
    for i in range(20):
        name = 'pair-P' + str(number) + '_' + str(i + 1)
        data = np.array(ld.load_data(address + '/' + name + '.txt'))
        node1 = nd.Node(colloid, data[0, 1:4] / colloid.get_diameter())
        node2 = nd.Node(colloid, data[1, 1:4] / colloid.get_diameter())
        group.set_configuration(cnf.Pair(i + 1, node1, node2, fld.Conical(amplitude, data[0, 5]),
                                         sum(data[:, 4])))
    return group


def load_triplet_group(number, n_theta, colloid, amplitude):
    address = 'data/triplet'
    parameters = np.array((ld.load_data("data/parameters_pair_4.txt"))).transpose()[0]
    potential = ptl.Potential('pair', parameters, 'analytic', 4)
    group = grp.Group(number)
    for i in range(1, 19):
        name = 'triplet-T' + str(number) + '-' + str(n_theta) + '_' + str(i + 1)
        data = np.array(ld.load_data(address + '/' + name + '.txt'))
        node1 = nd.Node(colloid, data[0, 1:4] / colloid.get_diameter())
        node2 = nd.Node(colloid, data[1, 1:4] / colloid.get_diameter())
        node3 = nd.Node(colloid, data[2, 1:4] / colloid.get_diameter())
        pair1 = cnf.Pair(1, node1, node2, fld.Conical(amplitude, data[0, 5]), 0)
        pair2 = cnf.Pair(2, node1, node3, fld.Conical(amplitude, data[0, 5]), 0)
        pair3 = cnf.Pair(3, node2, node3, fld.Conical(amplitude, data[0, 5]), 0)

        # group.set_configuration(cnf.Triplet(i + 1, node1, node2, node3, fld.Conical(amplitude, data[0, 5]),
        #                                    sum(data[:, 4])
        #                                    ))
        group.set_configuration(cnf.Triplet(i + 1, node1, node2, node3, fld.Conical(amplitude, data[0, 5]),
                                            sum(data[:, 4]) - potential.get_energy(pair1) -
                                            potential.get_energy(pair2) -
                                            potential.get_energy(pair3)
                                            ))
    return group


def computer_pair_part():

    task1 = True
    task2 = True
    # Parameter of the system:
    colloid = plr.Colloid(mt.SiliconDioxide(), mt.Water(), 2)
    field_amplitude = 1e3

    # Set groups:
    # group = load_pair_groups(colloid, field_amplitude)
    group = grp.Group(1)
    groups = []
    for n in range(12):
        print('Loading, P' + str(n + 1))
        groups.append(load_pair_group(n + 1, colloid, field_amplitude))
        group.set_group(groups[n])

    # Approximation:
    order = 4
    # parameters = [1, 1, 1, 1, 1, 1, 1, 1]
    parameters = np.array((ld.load_data('data/parameters_pair_' + str(order) + '.txt'))).transpose()[0]
    method_name = 'analytic'
    # method_name = 'diagrammatic'

    potential = ptl.Potential('pair', parameters, method_name, order)
    functional = fnc.Functional2(potential, group, 1)

    # Проведение аппроксимации выбранным парным потенциалом:
    if task1:
        # 'shgo', 'COBYLA'
        approximator = apr.Approximator(functional, 'Powell', 'data/parameters_pair_' + str(order) + '.txt')
        bnds_points = ((0.8, 1.2), (-200, 200), (-200, 200), (-200, 200), (-200, 200), (-200, 200), (-200, 200), (-200, 200))
        approximator.set_options(bnds_points,
                                 parameters, 100, 50, 1e-3)
        approximator.fit()
        par = np.array((ld.load_data('data/parameters_pair_' + str(order) + '.txt'))).transpose()[0]
        print(par)

    # Построение потенциалов для выбранной группы:
    if task2:
        parameters = np.array((ld.load_data('data/parameters_pair_' + str(order) + '.txt'))).transpose()[0]
        # print(np.array(parameters))
        potential.set_parameters(parameters)
        group = load_pair_group(1, colloid, field_amplitude)
        print("Figure1")
        # Data for interpolation function:
        # rs = np.linspace(r[0], r[19], num=1000, endpoint=True)

        # pot_list = []
        # for i in range(1, 14):
        #    us = interp1d(r, func.get_group_term(group[i - 1], par), kind='cubic')
        #    np.savetxt('pair_fit_potential_' + str(i) + '.txt', np.c_[rs, us(rs)])
        #    pot_list.append(us(rs))

        # Plotting of the figure:
        fig = plt.figure()
        colors = np.array(ld.load_data('colors/trend.txt')) / 256
        type(fig)
        ax = fig.add_subplot(111)
        for n in range(12):
            r = []
            u = []
            phi = []
            for i in range(20):
                configuration = groups[n].get_configuration(i)
                r.append(configuration.get_combination().get_minimum())
                u.append(configuration.get_energy())
                phi.append(potential.get_energy(configuration))
            ax.semilogx(r, u, 'o', color=colors[n, :])
            ax.semilogx(r, phi, '-', color=colors[n, :])
        # ax.semilogx(r, group[12].get_energy_array(), 'o', color='black')
        # for i in range(0, 12):
        # ax.semilogx(rs, pot_list[i], color=colors[i, :])
        # ax.semilogx(rs, pot_list[12], color='black')
        # ax.semilogx(rs, 0 * rs, color='black')
        # fig.savefig('figure/p_pot_r.pdf')
        plt.show()


def computer_triplet_part():

    task1 = True
    task2 = True
    # Parameter of the system:
    colloid = plr.Colloid(mt.SiliconDioxide(), mt.Water(), 2)
    field_amplitude = 1e3

    # Set groups:
    # group = load_pair_groups(colloid, field_amplitude)
    group = grp.Group(1)
    groups1 = []
    groups2 = []
    groups3 = []
    for n in range(9):
        print('Loading, T' + str(n + 1))
        groups1.append(load_triplet_group(n + 1, 1, colloid, field_amplitude))
        group.set_group(groups1[n])

    for n in range(12):
        print('Loading, T' + str(1))
        groups2.append(load_triplet_group(1, n + 1, colloid, field_amplitude))
        group.set_group(groups2[-1])

    for n in range(12):
        print('Loading, T' + str(9))
        groups3.append(load_triplet_group(9, n + 1, colloid, field_amplitude))
        group.set_group(groups3[-1])

    # Approximation:
    parameters = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    method_name = 'analytic'
    # method_name = 'diagrammatic'
    # potential = ptl.PairPotential(parameters, method_name)
    potential = ptl.Potential('triplet', parameters, method_name, 3)
    functional = fnc.Functional(potential, group, 1)

    # Проведение аппроксимации выбранным парным потенциалом:
    if task1:
        approximator = apr.Approximator(functional, 'COBYLA', 'data/parameters_triplet.txt')
        bnds_points = ((-200, 200), (-200, 200), (-200, 200), (-200, 200),
                       (-200, 200), (-200, 200), (-200, 200), (-200, 200), (-200, 200))
        approximator.set_options(bnds_points,
                                 parameters, 100, 100, 1e-3)
        approximator.fit()
        par = np.array((ld.load_data("data/parameters_triplet.txt"))).transpose()[0]
        print(par)

    # Построение потенциалов для выбранной группы:
    if task2:
        parameters = np.array((ld.load_data("data/parameters_triplet.txt"))).transpose()[0]
        potential.set_parameters(parameters)
        group = load_pair_group(11, colloid, field_amplitude)
        print("Figure1")
        # Data for interpolation function:
        # rs = np.linspace(r[0], r[19], num=1000, endpoint=True)

        # pot_list = []
        # for i in range(1, 14):
        #    us = interp1d(r, func.get_group_term(group[i - 1], par), kind='cubic')
        #    np.savetxt('pair_fit_potential_' + str(i) + '.txt', np.c_[rs, us(rs)])
        #    pot_list.append(us(rs))

        # Plotting of the figure:
        fig = plt.figure()
        colors = np.array(ld.load_data('colors/trend.txt')) / 256
        type(fig)
        ax = fig.add_subplot(111)
        for n in range(12):
            r = []
            u = []
            phi = []
            for i in range(1, 18):
                configuration = groups3[n].get_configuration(i)
                r.append(configuration.get_combination().get_minimum())
                u.append(configuration.get_energy() / (2 * groups3[n].get_configuration(0).get_null_energy()))
                phi.append(potential.get_energy(configuration) / (2 * groups3[n].get_configuration(0).get_null_energy()))
            ax.semilogx(r, u, 'o', color=colors[n, :])
            ax.semilogx(r, phi, '-', color=colors[n, :])
            np.savetxt('data/triplet_bem_T9_' + str(n + 1) + '.txt', np.c_[r, u])
            np.savetxt('data/triplet_pdm_T9_' + str(n + 1) + '.txt', np.c_[r, phi])
        # ax.semilogx(r, group[12].get_energy_array(), 'o', color='black')
        # for i in range(0, 12):
        # ax.semilogx(rs, pot_list[i], color=colors[i, :])
        # ax.semilogx(rs, pot_list[12], color='black')
        # ax.semilogx(rs, 0 * rs, color='black')
        # fig.savefig('figure/p_pot_r.pdf')
        plt.show()


def main():

    computer_pair_part()
    # computer_triplet_part()


if __name__ == "__main__":
    main()
