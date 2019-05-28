import os
from typing import List
import pandas as pd

from simulator.log import Log


class SimulationGroupFolder:
    """
    Handle a series of simulations.
    Each group of simulations in contained in the same folder.
    This class provides the method to handle the folder and to get results
    """
    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def get_file_list(self, format: str = ".csv") -> List[str]:
        """
        Get all the files in the simulation group folder
        :param format: format of the files. By default is '.csv'
        :return: list of filenames, each of them containing a single simulation
        """
        files_list = []
        for f in os.listdir(self.folder_path):
            if f.endswith(format):
                files_list.append(f)
        return files_list


class SingleSimulation:
    """
    Handle a single csv file coming from one single simulation.
    A single simulation has well defined seed and inter arrival rate
    """
    def __init__(self, folder_path: str, file_name: str) -> None:
        self.folder_path = folder_path
        self.file_name = file_name
        info = self.file_name.split("_")
        seed_format = info[2].split(".")
        self.inter_arrival = int(info[1])
        self.seed = int(seed_format[0])
        df = pd.read_csv(self.folder_path + "/" + self.file_name)
        # pre compute all the information needed for the evaluation
        self._n = len(df['dst'].unique())
        self._simulation_time = max(df['time'])
        self._received = len(df.loc[df["event"] == Log.LOG_RECEIVED])
        self._corrupted = len(df.loc[df["event"] == Log.LOG_CORRUPTED])
        self._dropped = len(df.loc[df["event"] == Log.LOG_QUEUE_DROPPED])
        self._generated = len(df.loc[df["event"] == Log.LOG_GENERATED])

    def offered_load(self) -> float:
        """
        Compute the offered load
        :return: the offered load
        """
        return self.inter_arrival * (32 + 1500) / 2 * self._n * 8 / 1024 / 1024

    def throughput(self) -> float:
        """
        Compute the throughput at the receiver
        :return: the throughput, in Mbps
        """
        return self._received / self._simulation_time

    def collision_rate(self) -> float:
        """
        #Corrupted packets / all the incoming packets
        :return: the collision rate
        """
        return self._corrupted / (self._corrupted + self._received)

    def drop_rate(self) -> float:
        """
        Ratio of packets dropped at the queue over total generated
        :return: the drop rate
        """
        return self._dropped / self._generated


class SimulationGroupResult:
    """
    Container for aggregated results of a simulation.
    Inter arrival rate is fixed, while all the attributes are the average of multiple simulations with different seeds
    """
    def __init__(self, load: float, throughput: float, collision_rate: float, drop_rate: float) -> None:
        self.load = load
        self.throughput = throughput
        self.collision_rate = collision_rate
        self.drop_rate = drop_rate
