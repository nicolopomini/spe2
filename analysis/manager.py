from analysis.simulation_analysis import SimulationGroupFolder


class AnalysisManager:
    ALOHA_DISK_FOLDER = "aloha_disk/"
    ALOHA_PROB_FOLDER = "aloha_prob/"
    TRIVIAL_DISK_FOLDER = "trivial_disk/"
    TRIVIAL_PROB_FOLDER = "trivial_prob/"

    def __init__(self, base_folder: str = "../raw_data/") -> None:
        self.base_folder = base_folder
        if not self.base_folder.endswith("/"):
            self.base_folder += "/"

    def _analyze(self, raw_data_folder: str):
        folder_manager = SimulationGroupFolder(raw_data_folder)
        for file_name in folder_manager.get_file_list():
            pass
