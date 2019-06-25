import os
import pandas as pd

from simulator.log import Log


class SimulationGroupFolder:
    """
    Handle a series of simulations.
    Each group of simulations in contained in the same folder.
    This class provides the method to handle the folder and to get results
    """
    def __init__(self, folder_path) -> None:
        self.folder_path = folder_path
        if not self.folder_path.endswith("/"):
            self.folder_path += "/"

    def get_file_list(self, file_format=".csv"):
        """
        Get all the files in the simulation group folder
        :param file_format: format of the files. By default is '.csv'
        :return: list of filenames, each of them containing a single simulation
        """
        files_list = []
        for f in os.listdir(self.folder_path):
            if f.endswith(file_format):
                files_list.append(f)
        return files_list

    def group_by_inter_arrival(self, file_list):
        """
        Group all the simulations in a list of files by seeds, computing the average of load, throughput, drop rate and
        collision rate
        :param file_list: the list of simulation result files to be grouped
        :return: a dict, with keys the inter-arrival time, and values a list of SimulationGroupResult
        """
        # group by inter-arrival time and seed
        inter_arrival_group = {}
        # key: inter-arrival, value: dict
        # 2nd dict, key: seed, value: raw data of the simulations
        for file_name in file_list:
            single_simulation = SingleSimulation(self.folder_path, file_name)
            # inter arrival
            if single_simulation.inter_arrival not in inter_arrival_group:
                inter_arrival_group[single_simulation.inter_arrival] = {}
            # seed
            inter_arrival_group[single_simulation.inter_arrival][single_simulation.seed] = single_simulation
        # create and fill a dictionary, with keys the inter-arrival times,
        # and values the aggregation over seeds of the simulations
        group_results = {}
        for inter_arrival in inter_arrival_group:
            simulations = inter_arrival_group[inter_arrival]
            load = simulations[next(iter(simulations))].offered_load()
            avg_throughput = sum([simulations[s].throughput() for s in simulations]) / len(simulations)
            avg_collisions = sum([simulations[s].collision_rate() for s in simulations]) / len(simulations)
            avg_drop = sum([simulations[s].drop_rate() for s in simulations]) / len(simulations)
            avg_corr = sum([simulations[s].channel_corruption_rate() for s in simulations]) / len(simulations)
            group_results[inter_arrival] = SimulationGroupResult(
                inter_arrival, load, avg_throughput, avg_collisions, avg_drop, avg_corr
            )
        return group_results


class SingleSimulation:
    """
    Handle a single csv file coming from one single simulation.
    A single simulation has well defined seed and inter arrival rate
    """
    def __init__(self, folder_path, file_name):
        self.folder_path = folder_path
        if not self.folder_path.endswith("/"):
            self.folder_path += "/"
        self.file_name = file_name
        info = self.file_name.split("_")
        seed_format = info[2].split(".")
        self.inter_arrival = int(info[1])
        self.seed = int(seed_format[0])
        df = pd.read_csv(self.folder_path + self.file_name)
        #  pre compute all the information needed for the evaluation
        self._n = len(df['dst'].unique())
        self._simulation_time = max(df['time'])
        self._received = len(df.loc[df["event"] == Log.LOG_RECEIVED])
        self._corrupted = len(df.loc[df["event"] == Log.LOG_CORRUPTED])
        self._corrupted_by_channel = len(df.loc[df["event"] == Log.LOG_CORRUPTED_BY_CHANNEL])
        self._dropped = len(df.loc[df["event"] == Log.LOG_QUEUE_DROPPED])
        self._generated = len(df.loc[df["event"] == Log.LOG_GENERATED])

    def offered_load(self):
        """
        Compute the offered load
        :return: the offered load
        """
        return self.inter_arrival * (32 + 1500) / 2 * self._n * 8 / 1024 / 1024

    def throughput(self):
        """
        Compute the throughput at the receiver
        :return: the throughput, in Mbps
        """
        return self._received / self._simulation_time

    def collision_rate(self):
        """
        #Corrupted packets / all the incoming packets
        :return: the collision rate
        """
        return self._corrupted / (self._corrupted + self._received + self._corrupted_by_channel)

    def drop_rate(self):
        """
        Ratio of packets dropped at the queue over total generated
        :return: the drop rate
        """
        return self._dropped / self._generated

    def channel_corruption_rate(self):
        """
        Ratio of packets corrupted by the channel over total generated.
        Of course, it does not make sense with disk reception
        :return: channel corruption rate
        """
        return self._corrupted_by_channel / (self._corrupted + self._received + self._corrupted_by_channel)


class SimulationGroupResult:
    """
    Container for aggregated results of a simulation.
    Inter arrival rate is fixed, while all the attributes are the average of multiple simulations with different seeds
    """
    def __init__(self, inter_arrival, load, throughput, collision_rate, drop_rate, corruption_rate):
        self.inter_arrival = inter_arrival
        self.load = load
        self.throughput = throughput
        self.collision_rate = collision_rate
        self.drop_rate = drop_rate
        self.corruption_rate = corruption_rate

    def __repr__(self):
        return "(Inter-arrival: %f, Load: %f, throughput: %f, collision rate: %f, drop rate: %f)" % \
               (self.inter_arrival, self.load, self.throughput, self.collision_rate, self.drop_rate)
