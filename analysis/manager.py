from plot import Plotter
from simulation_analysis import SimulationGroupFolder


class AnalysisManager:
    """
    This class handles the whole ana.
    It reads the general folder that contains all the results of the simulations, and subfolder by subfolder aggregates
    the results and creates the plots.
    """
    ALOHA_DISK_FOLDER = "aloha_disk/"
    ALOHA_PROB_FOLDER = "aloha_prob/"
    TRIVIAL_DISK_FOLDER = "trivial_disk/"
    TRIVIAL_PROB_FOLDER = "trivial_prob/"

    def __init__(self, base_folder="raw_data/"):
        self.base_folder = base_folder
        if not self.base_folder.endswith("/"):
            self.base_folder += "/"

    def _analyze_sub_folder(self, raw_data_sub_folder):
        folder_manager = SimulationGroupFolder(self.base_folder + raw_data_sub_folder)
        file_list = folder_manager.get_file_list()
        # results of a single type of simulaton, grouped by inter-arrival
        results_by_inter_arrival = folder_manager.group_by_inter_arrival(file_list)
        ordered_keys = sorted(results_by_inter_arrival.keys())
        loads = []
        throughputs = []
        coll_rate = []
        drop_rate = []
        for k in ordered_keys:
            loads.append(results_by_inter_arrival[k].load)
            throughputs.append(results_by_inter_arrival[k].throughput)
            coll_rate.append(results_by_inter_arrival[k].collision_rate)
            drop_rate.append(results_by_inter_arrival[k].drop_rate)
        return SettingResult(loads, throughputs, coll_rate, drop_rate)

    def make_plots(self):
        aloha_disk = self._analyze_sub_folder(self.ALOHA_DISK_FOLDER)
        aloha_prob = self._analyze_sub_folder(self.ALOHA_PROB_FOLDER)
        trivial_disk = self._analyze_sub_folder(self.TRIVIAL_DISK_FOLDER)
        trivial_prob = self._analyze_sub_folder(self.TRIVIAL_PROB_FOLDER)
        Plotter.plot_throughput(aloha_disk.load,
                                aloha_disk.throughput,
                                aloha_prob.throughput,
                                trivial_disk.throughput,
                                trivial_prob.throughput)
        Plotter.plot_collision_rate(aloha_disk.load,
                                    aloha_disk.collision_rate,
                                    aloha_prob.collision_rate,
                                    trivial_disk.collision_rate,
                                    trivial_prob.collision_rate)
        Plotter.plot_drop_rate(aloha_disk.load, aloha_disk.drop_rate, aloha_prob.drop_rate,
                               trivial_disk.drop_rate, trivial_prob.drop_rate)


class SettingResult:

    def __init__(self, load, throughput, collision_rate, drop_rate):
        self.load = load
        self.throughput = throughput
        self.collision_rate = collision_rate
        self.drop_rate = drop_rate

    def __repr__(self):
        return "Setting result:\nLoad: %s\nThroughput: %s\nColl. rate: %s\nDrop rate %s" % (
            str(self.load), str(self.throughput), str(self.collision_rate), str(self.drop_rate)
        )
