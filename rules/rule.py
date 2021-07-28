""" rule parser """
import json


class Rule:
    """ wrapper for parsing rules """
    def __init__(self, file_path):
        with open(file_path, 'r') as rule:
            rule = json.load(rule)
        self.type = rule['type']
        self.trigger_count = rule['trigger_count']
        self.min_avg = rule['avg_min']
        self.max_avg = rule['avg_max']

    def __call__(self, value, *args, **kwargs):
        return value < self.min_avg or value > self.max_avg
