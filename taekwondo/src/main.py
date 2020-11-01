import preprocessing.read as r
import torch
from torch_geometric.data import Data

loader = r.TaekwondoLoader('../dataset')
athletes, labels, idx = loader.load();
print(labels)
frame = athletes[1].get('Left Kick')[1]
print(frame)

edge_index = torch.tensor([[2, 14, 0, 14, 0, 6, 6, 8, 1, 14, 1, 7, 7, 9, 3, 14, 3, 4, 4, 10, 10, 12, 3, 5, 5, 11, 11, 13],
                           [14, 2, 14, 0, 6, 0, 8, 6, 14, 1, 7, 1, 9, 7, 14, 3, 4, 3, 10, 4, 12, 10, 5, 3, 11, 5, 13, 11]], dtype=torch.long)

x = torch.tensor(frame, dtype=torch.float)
data = Data(x=x, edge_index=edge_index)
print(data)
