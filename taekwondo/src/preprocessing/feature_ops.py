import numpy as np
from scipy.spatial.transform import Rotation as R


def rotate(frames, degree):
    r = R.from_rotvec(np.deg2rad(degree) * np.array([0, 1, 0]))
    num_frames = frames.shape[0]
    num_nodes = frames.shape[1]
    temp = frames.reshape((num_frames * num_nodes, 3))
    temp = r.apply(temp)
    temp = temp.reshape(num_frames, num_nodes, 3)
    return temp


def apply_noise(frames, sigma):
    mu = 0
    noise = np.random.normal(mu, sigma, frames.shape)
    return frames + noise

def scale_noise(base_sample, noise_intensity):
    return base_sample * (1 + noise_intensity)


def unfold_features(frames):
    num_frames = frames.shape[0]
    num_nodes = frames.shape[1]
    num_dim = frames.shape[2]
    res = np.zeros((num_frames, num_nodes*num_dim))
    for frame_idx in range(num_frames):
        for node_idx in range(num_nodes):
            res[frame_idx, num_dim*node_idx:num_dim*(node_idx+1)] = frames[frame_idx, node_idx]
    return res