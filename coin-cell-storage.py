#! /usr/bin/env python

from solid import *
from solid.utils import *

SEGMENTS = 48

storage_unit_def = {
    "types": {
        "default": {
            "battery_clearance": 0.5,
            "battery_protrusion": .2,
            "grabby_slot_diameter": 15,
            "grabby_slot_offset": 5,
            "slot_margin": 2,
            "slot_angle": -15,
            "tower_bottom_margin": 2.5,
        },
        "CR1632": {
            "label": "CR1632",
            "battery_count": 10,
            "battery_height": 3,
            "battery_diameter": 15.8,
        },
        "CR2025": {
            "label": "CR2025",
            "battery_count": 11,
            "battery_height": 2.5,
            "battery_diameter": 19.8,
        },
    },
    "order": [
        "CR1632",
        "CR2025",
    ],
}

# -----------------------

class ButtonCellStorageConfig():
    def __init__(self, config):
        self.config = config

    def get(self, i):
        cell_type = self.config["order"][i]
        return {**self.config["types"]["default"], **self.config["types"][cell_type]}

    def len(self):
        return len(self.config["order"])
    
class ButtonCellTower():
    def __init__(self, config):
        self.definition = config

        self.label_text = config['label']

        self.battery_diameter = config["battery_diameter"]
        self.battery_count = config["battery_count"]
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
        self.tower_height = (self.battery_height+self.battery_clearance*2+self.slot_margin) * self.battery_count + self.slot_margin + self.tower_bottom_margin

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
        for i in range(0, self.battery_count):
            t -= self.slot(i, [self.slot_width, self.slot_depth, self.slot_height])
        t -= self.grabby_slot()
        t -= self.label()
        return t

    def width(self):
        return self.tower_width

class ButtonCellStorage():
    def __init__(self, config):
        self.config = config

    def assemble(self):
        u = None

        max_tower_height = 0
        max_tower_depth = 0
        towers = []
        for i in range(0, self.config.len()):
            tower = ButtonCellTower(self.config.get(i))
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

if __name__ == '__main__':
    config = ButtonCellStorageConfig(storage_unit_def)
    a = ButtonCellStorage(config).assemble()
    scad_render_to_file(a, "button-cell-holder.scad", file_header=f'$fn = {SEGMENTS};', include_orig_code=True)