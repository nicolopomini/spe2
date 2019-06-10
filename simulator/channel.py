# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2016 Michele Segata <segata@ccs-labs.org>
from __future__ import absolute_import
import math
import copy
from module import Module
from event import Event
from events import Events


class Channel(Module):
    """
    This class takes care of simulating the channel, signaling the beginning of
    reception to nodes within the communication range. For the sake of
    simplicity, the end of reception is automatically scheduled by the receiving
    node.
    """

    # communication range parameter in config file
    PAR_RANGE = "range"
    # speed of light in m/s, used to compute propagation delay
    SOL = 299792458.0

    def __init__(self, config, use_realistic_propagation):
        """
        Constructor.
        :param config: the set of configs loaded by the simu to obtain, for
        example, the communication range. The parameter is an instance of the
        Config class
        :param use_realistic_propagation: True to use the realistic propagation
        """
        # call superclass constructor
        Module.__init__(self)
        # get transmission range from configuration parameters
        self.range = config.get_param(self.PAR_RANGE)
        # list of all communication nodes in the simulation
        self.nodes = []
        # map of neighbors that maps each node id to the list of its neighbors
        self.neighbors = {}
        # set propagation model
        self.use_realistic_propagation = use_realistic_propagation

    def register_node(self, node):
        """
        Registers a node participating to the simulation. This way the channel
        knows who is participating and can notify them when transmissions start
        or end
        :param node: the node to register, an instance of the Node class
        """
        self.nodes.append(node)
        # recompute the neighbors of all nodes considering the new node as well
        self.recompute_neighbors(node)

    def distance(self, a, b):
        """
        Computes the two-dimensional Euclidean distance between nodes a and b
        :param a: first node
        :param b: second node
        """
        return math.sqrt(math.pow(a.get_posx() - b.get_posx(), 2) +
                         math.pow(a.get_posy() - b.get_posy(), 2))

    def recompute_neighbors(self, new_node):
        """
        Updates the map of neighbors, i.e., for each node it computes the list
        of nodes within communication range and stores such list
        :param new_node: the node just added to the simulation
        """
        # neighbors for the newest node
        new_node_neighbors = []
        for n in self.nodes:
            # if the node n is within communication range of the newest node
            if n.get_id() != new_node.get_id() and \
               self.distance(n, new_node) < self.range:
                # add n to the neighbors of the new node and vice versa
                new_node_neighbors.append(n)
                self.neighbors[n.get_id()].append(new_node)
        # save neighbors for the new node in the map
        self.neighbors[new_node.get_id()] = new_node_neighbors

    def start_transmission(self, source_node, packet):
        """
        Begins transmission of a frame on the channel, notifying all neighbors
        about such event
        :param source_node: node that starts the transmission
        :param packet: packet being transmitted
        """
        for neighbor in self.neighbors[source_node.get_id()]:
            # compute propagation delay: distance / speed of light
            propagation_delay = self.distance(source_node, neighbor) /\
                                Channel.SOL
            if self.use_realistic_propagation:
                distance = self.distance(source_node, neighbor)
                packet.correct_reception_probability = 1 - pow(distance / self.range, 1.0 / 3.0)
            # generate and schedule START_RX event at receiver
            # be sure to make a copy of the packet and not pass the same
            # reference to multiple nodes, as they will process the packet in
            # different ways. one node might be able to receive it, one node
            # might not
            event = Event(self.sim.get_time() + propagation_delay,
                          Events.START_RX, neighbor, source_node,
                          copy.deepcopy(packet))
            self.sim.schedule_event(event)
