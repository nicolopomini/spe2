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
    def plot_throughput(title, location, load, aloha_throughput, trivial_throughput, simple_throughput):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_throughput, "o-", label="Aloha")
        plt.plot(load, trivial_throughput, "o-", label="Trivial")
        for persistence in simple_throughput:
            plt.plot(load, simple_throughput[persistence].throughput, "o-", label="Simple with p = %f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title(title)
        plt.legend(loc='best')
        plt.savefig(location)

    @staticmethod
    def plot_drop_rate(load, aloha_drop, trivial_drop, simple_drop):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_drop, "o-", label="Aloha")
        plt.plot(load, trivial_drop, "o-", label="Trivial")
        for persistence in simple_drop:
            plt.plot(load, simple_drop[persistence].drop_rate, "o-", label="Simple with p = %f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet drop rate at the sender")
        plt.title("Packet drop rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.DROP_RATE_PLOT_NAME)

    @staticmethod
    def plot_collision_rate(load, aloha_coll, trivial_coll, simple_coll):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_coll, "o-", label="Aloha")
        plt.plot(load, trivial_coll, "o-", label="Trivial")
        for persistence in simple_coll:
            plt.plot(load, simple_coll[persistence].collision_rate, "o-", label="Simple with p = %f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet collision rate at the receiver")
        plt.title("Collision rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.COLLISION_RATE_PLOT_NAME)

    @staticmethod
    def plot_throughput_comparison(load, aloha_disk, aloha_prob, trivial_disk, trivial_prob, simple0_disk, simple0_prob):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_disk, "o-", label="Aloha with disk rec.")
        plt.plot(load, aloha_prob, "o-", label="Aloha with prob rec.")
        plt.plot(load, trivial_disk, "o-", label="Trivial with disk rec.")
        plt.plot(load, trivial_prob, "o-", label="Trivial with prob rec.")
        plt.plot(load, simple0_disk, "o-", label="Simple [p = 0] with disk rec.")
        plt.plot(load, simple0_prob, "o-", label="Simple [p = 0] with prob rec.")
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title("Throughput with different reception models")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + "throughput_comp.pdf")
