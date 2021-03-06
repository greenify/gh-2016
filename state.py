# -*- coding: utf-8 -*-


from utils import dist_ceil


class State:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def next_free_drone(self):
        """ returns the next free drone """
        next_drone = self.drones[0]
        for drone in self.drones:
            if drone.busy_time < next_drone.busy_time:
                next_drone = drone
        return next_drone

    def closest_warehouse(self, drone, offer):
        potential_warehouse = None
        current_dist = None
        for w in self.warehouses:
            if w.has_product(offer["product"], offer["count"]):
                    if potential_warehouse is None or dist_ceil(w.pos, drone.pos) < current_dist:
                        potential_warehouse = w
                        current_dist = dist_ceil(w.pos, drone.pos)

        assert potential_warehouse.has_product(offer["product"], offer["count"])
        assert potential_warehouse is not None
        return potential_warehouse

    def next_offer(self):
        """ looks at all drones and gives the nearest offer """
        next_drone = self.next_free_drone()
        next_order = None
        current_dist = None
        for order in self.orders:
            if order.has_unreserved_items():
                if next_order is None or dist_ceil(next_drone, order) < current_dist:
                    next_order = order
                    current_dist = dist_ceil(next_drone.pos, order.pos)

        if next_order is None:
            return None
        item, count = next_order.best_unreserved_item(self.max_payload)
        count = min(int(self.max_payload / self.products[item]), count)
        offer = {"product": item, "order": next_order, "count": count}
        return offer
