import os
from typing import List
import pandas as pd

from simulator.events import Events


class FolderManager:
    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def get_file_list(self, format: str = ".csv") -> List[str]:
        files_list = []
        for f in os.listdir(self.folder_path):
            if f.endswith(format):
                files_list.append(f)
        return files_list


class FileManager:
    def __init__(self, folder_path: str, file_name: str) -> None:
        self.folder_path = folder_path
        self.file_name = file_name
        info = self.file_name.split("_")
        seed_format = info[2].split(".")
        self.inter_arrival = int(info[1])
        self.seed = int(seed_format[0])
        self.df = pd.read_csv(self.folder_path + "/" + self.file_name)
        self._n = len(self.df['dst'].unique())
        self._simulation_time = max(self.df['time'])

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
        return len(self.df.loc[self.df["event"] == Events.END_RX]) / self._simulation_time

    def collision_rate(self) -> float:
        """
        #Corrupted packets / all the incoming packets
        :return: the collision rate
        """
        #corrupted = self.df.loc[self.df["event"] == Events.]
        return 0
