import matplotlib.pyplot as plt


class Plotter:
    """
    Class that manage the creation of the various plots
    """
    BASE_DIR = "results/"
    THROUGHPUT_PLOT_NAME = "throughput.pdf"
    DROP_RATE_PLOT_NAME = "drop.pdf"
    COLLISION_RATE_PLOT_NAME = "collision.pdf"
    CORRUPTION_RATE_PLOT_NAME = "corruption.pdf"

    @staticmethod
    def plot_throughput(title, location, load, aloha_throughput, trivial_throughput, simple_throughput):
        plt.figure(figsize=(8.5, 4.8))
        sub = plt.subplot(111)
        sub.grid()
        sub.plot(load, aloha_throughput, "o-", label="Aloha")
        sub.plot(load, trivial_throughput, "o-", label="Trivial")
        for persistence in simple_throughput:
            sub.plot(load, simple_throughput[persistence].throughput, "o-", label="Simple, p = %2f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title(title)
        box = sub.get_position()
        sub.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        sub.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(location)

    @staticmethod
    def plot_drop_rate(load, aloha_drop, trivial_drop, simple_drop):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_drop, "o-", label="Aloha")
        plt.plot(load, trivial_drop, "o-", label="Trivial")
        for persistence in simple_drop:
            plt.plot(load, simple_drop[persistence].drop_rate, "o-", label="Simple with p = %.2f" % persistence)
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
            plt.plot(load, simple_coll[persistence].collision_rate, "o-", label="Simple with p = %.2f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet collision rate at the receiver")
        plt.title("Collision rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.COLLISION_RATE_PLOT_NAME)

    @staticmethod
    def plot_throughput_comparison(load, aloha_disk, aloha_prob, trivial_disk, trivial_prob, simple0_disk, simple0_prob):
        plt.figure(figsize=(9.5, 4.8))
        sub = plt.subplot(111)
        sub.grid()
        sub.plot(load, aloha_disk, "o-", label="Aloha with disk rec.")
        sub.plot(load, aloha_prob, "o-", label="Aloha with prob rec.")
        sub.plot(load, trivial_disk, "o-", label="Trivial with disk rec.")
        sub.plot(load, trivial_prob, "o-", label="Trivial with prob rec.")
        sub.plot(load, simple0_disk, "o-", label="Simple [p = 0], disk rec.")
        sub.plot(load, simple0_prob, "o-", label="Simple [p = 0], prob rec.")
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title("Throughput with different reception models")
        box = sub.get_position()
        sub.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        sub.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(Plotter.BASE_DIR + "throughput_comp.pdf")

    @staticmethod
    def plot_corruption_rate(load, aloha_corr, trivial_corr, simple_corr):
        plt.figure()
        plt.grid()
        plt.plot(load, aloha_corr, "o-", label="Aloha")
        plt.plot(load, trivial_corr, "o-", label="Trivial")
        for persistence in simple_corr:
            plt.plot(load, simple_corr[persistence].corruption_rate, "o-", label="Simple with p = %.2f" % persistence)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Channel corruption rate")
        plt.title("Channel corruption rate")
        plt.legend(loc='best')
        plt.savefig(Plotter.BASE_DIR + Plotter.CORRUPTION_RATE_PLOT_NAME)


class SingleNodePlotter:
    BASE_DIR = "results/"

    @staticmethod
    def plot_throughput(node_data, title, filename):
        plt.figure()
        nodes = plt.subplot(111)
        # change grid density
        thin_rows = [i * 1.0 / 100 for i in range(40)]
        thick_rows = [i * 1.0 / 100 for i in range(0, 41, 5)]
        nodes.set_yticks(thick_rows)
        nodes.set_yticks(thin_rows, minor=True)
        nodes.grid(which='major')
        nodes.grid(which='minor', alpha=0.2)
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Throughput at receiver [Mbps]")
        plt.title(title)
        for node in node_data:
            nodes.plot(node.loads, node.throughputs, "o-", label="Node %d" % node.node)
        box = nodes.get_position()
        nodes.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        nodes.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.savefig(SingleNodePlotter.BASE_DIR + filename)

    @staticmethod
    def plot_collision_rate(node_data, title, filename):
        plt.figure()
        nodes = plt.subplot(111)
        nodes.grid()
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet collision rate at the receiver")
        plt.title(title)
        for node in node_data:
            nodes.plot(node.loads, node.coll_rates, "o-", label="Node %d" % node.node)
        box = nodes.get_position()
        nodes.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        nodes.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.savefig(SingleNodePlotter.BASE_DIR + filename)

    @staticmethod
    def plot_drop_rate(node_data, title, filename):
        plt.figure()
        nodes = plt.subplot(111)
        nodes.grid()
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Packet drop rate at the sender")
        plt.title(title)
        for node in node_data:
            nodes.plot(node.loads, node.drop_rates, "o-", label="Node %d" % node.node)
        box = nodes.get_position()
        nodes.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        nodes.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.savefig(SingleNodePlotter.BASE_DIR + filename)

    @staticmethod
    def plot_channel_corruption_rate(node_data, title, filename):
        plt.figure()
        nodes = plt.subplot(111)
        nodes.grid()
        plt.xlabel("Total offered load [Mbps]")
        plt.ylabel("Channel corruption rate")
        plt.title(title)
        for node in node_data:
            nodes.plot(node.loads, node.corr_rates, "o-", label="Node %d" % node.node)
        box = nodes.get_position()
        nodes.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        nodes.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.savefig(SingleNodePlotter.BASE_DIR + filename)
