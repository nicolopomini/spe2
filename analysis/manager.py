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
    SIMPLE_DISK_75 = "simple_disk_75"
    SIMPLE_DISK_50 = "simple_disk_50"
    SIMPLE_DISK_25 = "simple_disk_25"
    SIMPLE_DISK_00 = "simple_disk_00"
    SIMPLE_PROB_75 = "simple_prob_75"
    SIMPLE_PROB_50 = "simple_prob_50"
    SIMPLE_PROB_25 = "simple_prob_25"
    SIMPLE_PROB_00 = "simple_prob_00"

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
        simple_disk = {
            0.0: self._analyze_sub_folder(self.SIMPLE_DISK_00),
            0.25: self._analyze_sub_folder(self.SIMPLE_DISK_25),
            0.5: self._analyze_sub_folder(self.SIMPLE_DISK_50),
            0.75: self._analyze_sub_folder(self.SIMPLE_DISK_75),
        }
        simple_prob = {
            0.0: self._analyze_sub_folder(self.SIMPLE_PROB_00),
            0.25: self._analyze_sub_folder(self.SIMPLE_PROB_25),
            0.5: self._analyze_sub_folder(self.SIMPLE_PROB_50),
            0.75: self._analyze_sub_folder(self.SIMPLE_PROB_75),
        }
        # plot collision rate (does not change wrt the reception model)
        Plotter.plot_collision_rate(aloha_disk.load,
                                    aloha_disk.collision_rate,
                                    trivial_disk.collision_rate,
                                    simple_disk)
        # plot drop rate (does not change wrt the reception model)
        Plotter.plot_drop_rate(aloha_disk.load, aloha_disk.drop_rate, trivial_disk.drop_rate, simple_disk)
        # plot throughput with disk reception
        Plotter.plot_throughput("Throughput with disk reception", Plotter.BASE_DIR + "throughput_disk.pdf",
                                aloha_disk.load, aloha_disk.throughput, trivial_disk.throughput, simple_disk)
        # plot throughput with prob reception
        Plotter.plot_throughput("Throughput with prob reception", Plotter.BASE_DIR + "throughput_prob.pdf",
                                aloha_prob.load, aloha_prob.throughput, trivial_prob.throughput, simple_prob)
        # plot comparison of throughput
        Plotter.plot_throughput_comparison(aloha_disk.load, aloha_disk.throughput, aloha_prob.throughput,
                                           trivial_disk.throughput, trivial_prob.throughput,
                                           simple_disk[0.0].throughput, simple_prob[0.0].throughput)


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
