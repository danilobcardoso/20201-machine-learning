import os
import numpy as np

class TaekwondoLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.prefix = 'Athlete'
        self.data_file = 'Filtered Joints.txt'
        # self.data_file = 'All Frames Joints.txt'

    def load(self):
        athletes = []
        labels = set()
        for folder in os.listdir(self.data_path):
            if self.prefix in folder:
                athlete_id = folder.replace(self.prefix, '')
                athlete_path = '{}/{}'.format(self.data_path, folder)
                athlete = TaekwondoAthlete(athlete_id)
                for label_folder in os.listdir(athlete_path):
                    label = label_folder
                    data_path = '{}/{}/{}'.format(athlete_path, label_folder, self.data_file)
                    data = self.read_activity_file(data_path)
                    athlete.add(label, data)
                    labels.add(label)
                athletes.append(athlete)
        label_idx = {key: idx for (idx, key) in enumerate(labels)}
        return athletes, labels, label_idx

    def read_activity_file(self, data_path):
        # print(data_path)
        invalid_nodes = [11, 12, 17, 18]
        with open(data_path, "r") as data_file:
            param = data_file.readline().split(',')
            lines = int(param[0].rstrip()) - 2 # Duas primeiras linhas são parametros
            frames = int(param[1].rstrip())
            dunno = data_file.readline()
            data = [[[0, 0, 0] for j in range(20-len(invalid_nodes))] for i in range(frames)]

            jumps = 0
            for i in range(lines):
                line = data_file.readline().split(',')
                if int(i / 3) in invalid_nodes:
                    if int(i % 3) == 0:
                        jumps = jumps + 1;
                    continue;

                node = int(i / 3) - jumps
                axis = int(i % 3)

                # print("node: {} / axis: {}".format(node, axis))
                for frame in range(frames):
                    data[frame][node][axis] = float(line[frame])
            return np.array(data)


class TaekwondoAthlete:
    def __init__(self, ident, parent = None):
        self.ident = ident
        self.parent = parent
        self.activities = {}

    def __str__(self):
        val = 'Athlete {}\n'.format(self.ident)
        for key in self.activities.keys():
            data = self.activities[key]
            val = "{}\t{} -> {} frames\n".format(val, key, len(data[0]))
        return val

    def add(self, label, data):
        if label not in self.activities: ## Declaration
            self.activities[label] = []
            
        self.activities[label].append(data)

    def get(self, label, idx=0):
        return self.activities[label][idx]
        