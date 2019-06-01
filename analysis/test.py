from unittest import TestCase

from analysis.simulation_analysis import SingleSimulation, SimulationGroupFolder


class TestSingleSimulation(TestCase):
    def test_single_file(self):
        m = SingleSimulation("../raw_data", "output_110_0.csv")
        print(m.offered_load())
        print(m.throughput())
        print(m.drop_rate())
        print(m.collision_rate())


class TestSimulationGroupFolder(TestCase):
    def test_folder(self):
        f = SimulationGroupFolder("../raw_data")
        file_list = f.get_file_list()
        print(file_list)
        res = f.group_by_inter_arrival(file_list)
        for inter_arrival in res:
            print(inter_arrival)
            print(res[inter_arrival])
