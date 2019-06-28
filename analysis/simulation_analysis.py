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

    def group_by_interarrival_single_nodes(self, file_list, node_number):
        """
        Group all the simulations in a list of files by seeds, computing the average of load, throughput, drop rate and
        collision rate of each node
        :param file_list: the list of simulation result files to be grouped
        :param node_number: number of nodes
        :return: a dict, with keys the inter-arrival time, and values a list of SimulationGroupResult
        """
        # group by inter-arrival time and seed
        inter_arrival_group = {}
        # key: inter-arrival, value: dict
        # 2nd dict, key: seed, value: raw data of the simulations
        for file_name in file_list:
            single_simulation = SingleNodeAnalysis(self.folder_path, file_name)
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
            nodes_throughput = [0.0 for _ in range(node_number)]
            nodes_collisions = [0.0 for _ in range(node_number)]
            nodes_drops = [0.0 for _ in range(node_number)]
            nodes_corr = [0.0 for _ in range(node_number)]
            # for each simulation with the same inter arrival, compute means of the metrics for each node
            for seed in simulations:
                simulation = simulations[seed]
                thr = simulation.node_throughput()
                coll = simulation.node_collision_rate()
                drop = simulation.node_drop_rate()
                corr = simulation.node_corruption_rate()
                for i in range(node_number):
                    nodes_throughput[i] += thr[i]
                    nodes_collisions[i] += coll[i]
                    nodes_drops[i] += drop[i]
                    nodes_corr[i] += corr[i]
                for i in range(node_number):
                    nodes_throughput[i] /= len(simulations)
                    nodes_collisions[i] /= len(simulations)
                    nodes_drops[i] /= len(simulations)
                    nodes_corr[i] /= len(simulations)
                group_results[inter_arrival] = SimulationGroupResult(
                    inter_arrival, load, nodes_throughput, nodes_collisions, nodes_drops, nodes_corr
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
        self._received = df.loc[df["event"] == Log.LOG_RECEIVED]
        self._corrupted = len(df.loc[df["event"] == Log.LOG_CORRUPTED])
        self._corrupted_by_channel = len(df.loc[df["event"] == Log.LOG_CORRUPTED_BY_CHANNEL])
        self._dropped = len(df.loc[df["event"] == Log.LOG_QUEUE_DROPPED])
        self._generated = len(df.loc[df["event"] == Log.LOG_GENERATED])
        self._incoming = len(self._received) + self._corrupted + self._corrupted_by_channel

    def offered_load(self):
        """
        Compute the offered load
        :return: the offered load
        """
        packet_size = (32 + 1500) / 2
        return self.inter_arrival * packet_size * self._n * 8 / 1024 / 1024

    def throughput(self):
        """
        Compute the throughput at the receiver
        :return: the throughput, in Mbps
        """
        return self._received["size"].sum() * 8 / self._simulation_time / 1024 / 1024

    def collision_rate(self):
        """
        #Corrupted packets / all the incoming packets
        :return: the collision rate
        """
        return self._corrupted * 1.0 / self._incoming

    def drop_rate(self):
        """
        Ratio of packets dropped at the queue over total generated
        :return: the drop rate
        """
        return self._dropped * 1.0 / self._generated

    def channel_corruption_rate(self):
        """
        Ratio of packets corrupted by the channel over total generated.
        Of course, it does not make sense with disk reception
        :return: channel corruption rate
        """
        return self._corrupted_by_channel * 1.0 / self._incoming


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
        return "(Inter-arrival: %s, Load: %s, throughput: %s, collision rate: %s, drop rate: %s)" % \
               (str(self.inter_arrival), str(self.load), str(self.throughput), str(self.collision_rate),
                str(self.drop_rate))


class NodeData:
    """
    Class to collect data of a single node, and to compute its metrics
    """

    def __init__(self, df, simulation_time):
        self.simulation_time = simulation_time
        self._received = df.loc[df["event"] == Log.LOG_RECEIVED]
        self._corrupted = len(df.loc[df["event"] == Log.LOG_CORRUPTED])
        self._corrupted_by_channel = len(df.loc[df["event"] == Log.LOG_CORRUPTED_BY_CHANNEL])
        self._dropped = len(df.loc[df["event"] == Log.LOG_QUEUE_DROPPED])
        self._generated = len(df.loc[df["event"] == Log.LOG_GENERATED])
        self._incoming = len(self._received) + self._corrupted + self._corrupted_by_channel

    def throughput(self):
        """
        Compute the throughput of a single node, at the receiver
        :return: the throughput, in Mbps
        """
        return self._received["size"].sum() * 8 / self.simulation_time / 1024 / 1024

    def collision_rate(self):
        """
        #Corrupted packets / all the incoming packets
        :return: the collision rate
        """
        return self._corrupted * 1.0 / self._incoming

    def drop_rate(self):
        """
        Ratio of packets dropped at the queue over total generated
        :return: the drop rate
        """
        return self._dropped * 1.0 / self._generated

    def channel_corruption_rate(self):
        """
        Ratio of packets corrupted by the channel over total generated.
        Of course, it does not make sense with disk reception
        :return: channel corruption rate
        """
        return self._corrupted_by_channel * 1.0 / self._incoming


class SingleNodeAnalysis:
    """
    Handle a single simulation file, computing the metrics for each single node
    """

    def __init__(self, folder_path, file_name) -> None:
        self.folder_path = folder_path
        if not self.folder_path.endswith("/"):
            self.folder_path += "/"
        self.file_name = file_name
        info = self.file_name.split("_")
        seed_format = info[2].split(".")
        self.inter_arrival = int(info[1])
        self.seed = int(seed_format[0])
        df = pd.read_csv(self.folder_path + self.file_name)
        self._n = len(df['dst'].unique())
        self._simulation_time = max(df['time'])
        self.nodes = []
        # saving the raw rows related to a single node
        for i in range(1, self._n + 1):
            self.nodes.append(NodeData(df.loc[df['dst'] == i], self._simulation_time))

    def offered_load(self):
        """
        Compute the offered load
        :return: the offered load
        """
        packet_size = (32 + 1500) / 2
        return self.inter_arrival * packet_size * self._n * 8 / 1024 / 1024

    def node_throughput(self):
        """
        All the throughputs of the nodes
        :return: list with throughput
        """
        return [n.throughput() for n in self.nodes]

    def node_collision_rate(self):
        """
        Collision rate of each node
        :return: list of collision rates
        """
        return [n.collision_rate() for n in self.nodes]

    def node_drop_rate(self):
        """
        Drop rate of each node
        :return: list of drop rates
        """
        return [n.drop_rate() for n in self.nodes]

    def node_corruption_rate(self):
        """
        Channel corruption rate at each node
        :return: list of channel corruption rates
        """
        return [n.channel_corruption_rate() for n in self.nodes]
