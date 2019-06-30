from manager import AnalysisManager
import warnings
# ignore matplotlib warnings
warnings.filterwarnings("ignore")

analyzer = AnalysisManager()
analyzer.make_plots()
analyzer.plot_single_nodes()
