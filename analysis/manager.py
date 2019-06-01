from typing import Dict, List

from analysis.simulation_analysis import SimulationGroupFolder, SimulationGroupResult


class AnalysisManager:
    """
    This class handles the whole analysis.
    It reads the general folder that contains all the results of the simulations, and subfolder by subfolder aggregates
    the results and creates the plots.
    """
    ALOHA_DISK_FOLDER = "aloha_disk/"
    ALOHA_PROB_FOLDER = "aloha_prob/"
    TRIVIAL_DISK_FOLDER = "trivial_disk/"
    TRIVIAL_PROB_FOLDER = "trivial_prob/"

    def __init__(self, base_folder: str = "../raw_data/") -> None:
        self.base_folder = base_folder
        if not self.base_folder.endswith("/"):
            self.base_folder += "/"

    def _analyze_sub_folder(self, raw_data_sub_folder: str):
        folder_manager = SimulationGroupFolder(self.base_folder + raw_data_sub_folder)
        file_list = folder_manager.get_file_list()
        # results of a single type of simulaton, grouped by inter-arrival
        results_by_inter_arrival: Dict[int, List[SimulationGroupResult]] = folder_manager.group_by_inter_arrival(file_list)

