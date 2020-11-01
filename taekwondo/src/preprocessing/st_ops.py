import numpy as np

def adjlist_to_coo(adj_list):
    pairs = []
    for key in adj_list.keys():
        values = adj_list[key]
        for value in values:
            pairs.append([key, value])
    pairs = np.array(pairs)
    return pairs.transpose()


def create_st_graph(frames, skeleton_edges, num_nodes, add_backward=True, add_forward=True):
    edges_pattern = skeleton_edges.transpose()
    frame_links = [edges_pattern]  # Links do primeiro frame é o próprio padrão
    temporal_links = []            # Com apenas 1 frame não tenho ligações temporais
    for i in range(1, len(frames)):  # Criando ligações temporais e indices para frames ao longo do tempo
        frame_links.append(edges_pattern + (i * num_nodes))
        if add_forward:
            forward_links = np.array([np.arange(0, num_nodes) + ((i - 1) * num_nodes),
                                      np.arange(0, num_nodes) + (i * num_nodes)]).transpose()
            temporal_links.append(forward_links)

        if add_backward:
            backward_links = np.array([np.arange(0, num_nodes) + (i * num_nodes),
                                      np.arange(0, num_nodes) + ((i - 1) * num_nodes)]).transpose()
            temporal_links.append(backward_links)

    # Reestruturando os dados para que eles tenham equivalencia com os indices do grafo completo
    data_dim = frames.shape[2]
    merged_data = frames.reshape((-1, data_dim))

    merged_frame_links = np.concatenate(frame_links)

    if len(temporal_links) > 0:
        merged_temporal_links = np.concatenate(temporal_links)
        merged_links = np.concatenate([merged_frame_links, merged_temporal_links])
    else:
        merged_links = merged_frame_links
    merged_links = merged_links.transpose()
    return merged_data, merged_links