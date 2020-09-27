#! /usr/bin/env python

from solid import *
from solid.utils import *

SEGMENTS = 48

storage_unit_def = {
    "order": [
        "CR1632",
        "CR2025",
    ],
    "types": {
        "default": {
            "battery_clearance": 0.5,
            "battery_protrusion": .2,
            "grabby_slot_diameter": 15,
            "grabby_slot_offset": 5,
            "slot_margin": 2,
            "slot_angle": -15,
            "tower_bottom_margin": 2.5,
            "min_battery_count": 10,
        },
        "CR3032": {
            "label": "CR3032",
            "battery_diameter": 30,
            "battery_height": 3.2,
        },
        "CR2016": {
            "label": "CR2016",
            "battery_diameter": 20,
            "battery_height": 1.6,
        },
        "CR2330": {
            "label": "CR2330",
            "battery_diameter": 20,
            "battery_height": 3.2,
        },
        "CR2032": {
            "label": "CR2032",
            "battery_diameter": 20,
            "battery_height": 3.2,
        },
        "CR1220": {
            "label": "CR1220",
            "battery_diameter": 12.5,
            "battery_height": 2.0,
        },
        "CR1632": {
            "label": "CR1632",
            "battery_diameter": 16,
            "battery_height": 3.2,
        },
        "CR927": {
            "label": "CR927",
            "battery_diameter": 9.5,
            "battery_height": 2.7,
        },
        "CR1025": {
            "label": "CR1025",
            "battery_diameter": 10,
            "battery_height": 2.5,
        },
        "CR1130": {
            "label": "CR1130",
            "battery_diameter": 11.5,
            "battery_height": 3.0,
        },
        "CR1216": {
            "label": "CR1216",
            "battery_diameter": 12.5,
            "battery_height": 1.6,
        },
        "CR1225": {
            "label": "CR1225",
            "battery_diameter": 12.5,
            "battery_height": 2.5,
        },
        "CR1616": {
            "label": "CR1616",
            "battery_diameter": 16,
            "battery_height": 1.6,
        },
        "CR1620": {
            "label": "CR1620",
            "battery_diameter": 16,
            "battery_height": 2.0,
        },
        "CR2012": {
            "label": "CR2012",
            "battery_diameter": 20,
            "battery_height": 1.2,
        },
        "CR2020": {
            "label": "CR2020",
            "battery_diameter": 20,
            "battery_height": 2,
        },
        "CR2025": {
            "label": "CR2025",
            "battery_diameter": 20,
            "battery_height": 2.5,
        },
        "CR2040": {
            "label": "CR2040",
            "battery_diameter": 20,
            "battery_height": 4.0,
        },
        "CR2050": {
            "label": "CR2050",
            "battery_diameter":  20,
            "battery_height": 5.0,
        },
        "CR2320": {
            "label": "CR2320",
            "battery_diameter": 23,
            "battery_height": 2,
        },
        "CR2325": {
            "label": "CR2325",
            "battery_diameter": 23,
            "battery_height": 2.5,
        },
        "BR2335": {
            "label": "BR2335",
            "battery_diameter": 23,
            "battery_height": 3.5,
        },
        "CR2354": {
            "label": "CR2354",
            "battery_diameter": 23,
            "battery_height": 5.4,
        },
        "CR2412": {
            "label": "CR2412",
            "battery_diameter": 24.5,
            "battery_height": 1.2,
        },
        "CR2430": {
            "label": "CR2430",
            "battery_diameter": 24.5,
            "battery_height": 3.0,
        },
        "CR2450": {
            "label": "CR2450",
            "battery_diameter": 4.5,
            "battery_height": 5.0,
        },
        "CR2477": {
            "label": "CR2477",
            "battery_diameter": 24.5,
            "battery_height": 7.7,
        },
        "CR11108": {
            "label": "CR11108",
            "battery_diameter": 11.6,
            "battery_height": 10.8,
        },
    },
}

# -----------------------

class CoinCellStorageConfig():
    def __init__(self, config):
        self.config = config

    def get(self, i):
        cell_type = self.config["order"][i]
        return {**self.config["types"]["default"], **self.config["types"][cell_type]}

    def len(self):
        return len(self.config["order"])

class CoinCellTower():
    def __init__(self, config):
        self.definition = config

        self.label_text = config['label']

        self.battery_diameter = config["battery_diameter"]
        self.min_battery_count = config["min_battery_count"]
        self.battery_height = config["battery_height"]
        self.battery_clearance = config["battery_clearance"]
        self.battery_protrusion = config["battery_protrusion"]

        self.slot_angle = config["slot_angle"]
        self.slot_margin = config["slot_margin"]

        self.grabby_slot_offset = config["grabby_slot_offset"]
        self.grabby_slot_diameter = config["grabby_slot_diameter"]

        self.tower_bottom_margin = config["tower_bottom_margin"]

        self.slot_width = self.battery_diameter+self.battery_clearance*2
        self.slot_depth = self.battery_diameter * (1-self.battery_protrusion)
        self.slot_height = self.battery_height+self.battery_clearance*2

        self.tower_width = self.battery_diameter+self.battery_clearance*2+self.slot_margin*2
        self.tower_depth = self.slot_depth+self.slot_margin
        self.tower_height = (self.battery_height+self.battery_clearance*2+self.slot_margin) * self.min_battery_count + self.slot_margin + self.tower_bottom_margin

    def slot(self, i, dim):
        slot_cut_depth=50
        slot_z = ((dim[2] + self.slot_margin) * i) + self.slot_margin
        return translate([self.tower_width/2 - dim[0]/2, 0, slot_z+self.tower_bottom_margin])(
            rotate([self.slot_angle, 0, 0])(
                translate([0, -slot_cut_depth, 0])(
                    cube([dim[0], dim[1]+slot_cut_depth, dim[2]])
                )
            )
        )

    def grabby_slot(self):
        return translate([self.tower_width/2, -self.grabby_slot_offset, -5])(
            cylinder(h = self.tower_height+10, d=self.grabby_slot_diameter)
        )

    def label(self):
        return translate([self.tower_width/2, self.tower_depth/2, self.tower_height - self.slot_margin/2 + 0.1])(
            linear_extrude(self.slot_margin)(
                text(self.label_text, size=3.5, halign="center", valign="center")
            )
        )

    def assemble(self):
        t = cube([self.tower_width, self.tower_depth, self.tower_height])
        for i in range(0, self.min_battery_count):
            t -= self.slot(i, [self.slot_width, self.slot_depth, self.slot_height])
        t -= self.grabby_slot()
        t -= self.label()
        return t

    def width(self):
        return self.tower_width

class CoinCellStorage():
    def __init__(self, config):
        self.config = config

    def assemble(self):
        u = None

        max_tower_height = 0
        max_tower_depth = 0
        towers = []
        for i in range(0, self.config.len()):
            tower = CoinCellTower(self.config.get(i))
            towers.append(tower)
            if max_tower_height < tower.tower_height:
                max_tower_height = tower.tower_height
            if max_tower_depth < tower.tower_depth:
                max_tower_depth = tower.tower_depth

        assembly_width = 0
        for tower in towers:
            tower.tower_height = max_tower_height
            tower.tower_depth = max_tower_depth

            su = translate([assembly_width, 0, 0])(
                tower.assemble()
            )
            u = union()(u, su) if u else su
            assembly_width += tower.width()
        return u

def fileName(config):
    labels = []
    for i in range(0, config.len()):
        labels.append(config.get(i)['label'])
    return "_".join(labels) + ".scad"

if __name__ == '__main__':
    config = CoinCellStorageConfig(storage_unit_def)
    a = CoinCellStorage(config).assemble()
    scad_render_to_file(a, fileName(config), file_header='$fn = {SEGMENTS};', include_orig_code=True)
    print("Wrote file: " + fileName(config))
