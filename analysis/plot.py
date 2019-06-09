import matplotlib.pyplot as plt


class Plotter:
    """
    Class that manage the creation of the various plots
    """
    BASE_DIR = "results/"
    THROUGHPUT_PLOT_NAME = "throughput.pdf"
    DROP_RATE_PLOT_NAME = "drop.pdf"
    COLLISION_RATE_PLOT_NAME = "collision.pdf"

    @staticmethod
    def plot_throughput(load, aloha_disk_throughput, aloha_prob_throughput, carrier_disk_throughput,
                        carrier_prob_throughput):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_disk_throughput, "o-", label="Aloha with disk reception", color="r")
        plt.plot(load, aloha_prob_throughput, "o-", label="Aloha with prob reception", color="g")
        plt.plot(load, carrier_disk_throughput, "o-", label="Trivial carrier sensing with disk reception", color="b")
        plt.plot(load, carrier_prob_throughput, "o-", label="Trivial carrier sensing with prob reception", color="c")
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title("Throughput")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.THROUGHPUT_PLOT_NAME)

    @staticmethod
    def plot_drop_rate(load, aloha_disk_drop, aloha_prob_drop, carrier_disk_drop, carrier_prob_drop):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_disk_drop, "o-", label="Aloha with disk reception", color="r")
        plt.plot(load, aloha_prob_drop, "o-", label="Aloha with prob reception", color="g")
        plt.plot(load, carrier_disk_drop, "o-", label="Trivial carrier sensing with disk reception", color="b")
        plt.plot(load, carrier_prob_drop, "o-", label="Trivial carrier sensing with prob reception", color="c")
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet drop rate at the sender")
        plt.title("Packet drop rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.DROP_RATE_PLOT_NAME)

    @staticmethod
    def plot_collision_rate(load, aloha_disk_coll, aloha_prob_coll, carrier_disk_coll, carrier_prob_coll):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_disk_coll, "o-", label="Aloha with disk reception", color="r")
        plt.plot(load, aloha_prob_coll, "o-", label="Aloha with prob reception", color="g")
        plt.plot(load, carrier_disk_coll, "o-", label="Trivial carrier sensing with disk reception", color="b")
        plt.plot(load, carrier_prob_coll, "o-", label="Trivial carrier sensing with prob reception", color="c")
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet collision rate at the receiver")
        plt.title("Collision rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.COLLISION_RATE_PLOT_NAME)
