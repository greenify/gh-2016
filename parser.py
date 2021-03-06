#!/usr/bin/env python
# encoding: utf-8

from drone import Drone
from state import State
from order import Order
from warehouse import Warehouse


def parse(inFileName):

    with open(inFileName, "r") as inFile:

        header = inFile.readline()
        rows, columns, nr_drones, nr_turns, max_payload = list(map(int, header.strip().split(" ")))

        # read product types
        nr_products = int(inFile.readline())
        products = list(map(int, inFile.readline().strip().split(" ")))
        assert len(products) == nr_products

        # read warehouses
        nr_warehouses = int(inFile.readline())
        warehouses = []
        for i in range(nr_warehouses):
            pos = tuple(map(int, inFile.readline().strip().split(" ")))
            items = list(map(int, inFile.readline().strip().split(" ")))
            assert len(items) == nr_products
            warehouses.append(Warehouse(i, pos, items))

        assert len(warehouses) == nr_warehouses

        # read orders
        nr_orders = int(inFile.readline())
        orders = []
        lines = inFile.readlines()
        for i, (pos, nr_items, items) in enumerate(zip(lines[::3], lines[1::3], lines[2::3])):
            pos = tuple(map(int, pos.split(" ")))
            items = list(map(int, items.strip().split(" ")))
            assert int(nr_items) == len(items)
            orders.append(Order(id=i, pos=pos, items=items))

        assert len(orders) == nr_orders

        # init drones to simulate
        drones = []
        first_warehouse = warehouses[0]
        for i in range(nr_drones):
            drone = Drone(pos=first_warehouse.pos, id=i, max_payload=max_payload)
            drones.append(drone)

        return State(
            rows = rows,
            columns = columns,
            nr_turns = nr_turns,
            max_payload = max_payload,
            products = products,
            warehouses = warehouses,
            orders = orders,
            drones = drones
        )
