from unittest import TestCase

from manager import AnalysisManager
from simulation_analysis import SingleSimulation, SimulationGroupFolder


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


class TestPlotter(TestCase):
    def test_plotter(self):
        analyzer = AnalysisManager()
        res = analyzer._analyze_sub_folder(AnalysisManager.ALOHA_DISK_FOLDER)
        res1 = analyzer._analyze_sub_folder(AnalysisManager.TRIVIAL_DISK_FOLDER)
        print(len(res.load))
        print(len(res.throughput))
        print(len(res.collision_rate))
        print(len(res.drop_rate))
        print(len(res1.load))
        print(len(res1.throughput))
        print(len(res1.collision_rate))
        print(len(res1.drop_rate))
