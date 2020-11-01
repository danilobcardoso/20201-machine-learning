from pythreejs import *


class ActivityGraphRendererBuilder(object):
    def __init__(self, num_nodes, frame_spacing=1, node_scale=1, node_colors=None):
        self.num_nodes = num_nodes
        self.frame_spacing = frame_spacing
        self.node_scale = node_scale
        self.scene_children = []
        self.camera = self.create_camera()
        self.add_light()
        self.scene_children.append(self.camera)
        if node_colors:
            self.colors = node_colors
        else:
            self.colors = ['#27AE60', '#3498DB', '#E74C3C',
                           '#6C3483', '#2874A6', '#1E8449', '#B7950B', '#A04000', '#F1C40F',
                           '#D2B4DE', '#A3E4D7', '#AED6F1', '#F9E79F', '#E6B0AA', '#922B21',
                           '#27AE60', '#3498DB', '#E74C3C',
                           '#6C3483', '#2874A6', '#1E8449', '#B7950B', '#A04000', '#F1C40F',
                           '#D2B4DE', '#A3E4D7', '#AED6F1', '#F9E79F', '#E6B0AA', '#922B21']

    def add_data(self, data, edges):
        nodes = data
        # edges = a.to_geometric_data()['edge_index']
        self.add_nodes(nodes)
        self.add_edges(edges, nodes)

    def add_nodes(self, nodes):
        for i in range(len(nodes)):
            frame = int(i / self.num_nodes)
            color = self.colors[(i % self.num_nodes)]
            self.scene_children.append(self.add_ball(nodes[i].tolist(), frame, color))

    def add_edges(self, edges, nodes):
        e = edges.transpose()
        for i in range(len(e)):
            idxs = e[i]
            s = idxs[0]
            t = idxs[1]
            pos_s = nodes[s]
            pos_t = nodes[t]
            frame_s = int(s / self.num_nodes) * self.frame_spacing
            frame_t = int(t / self.num_nodes) * self.frame_spacing
            g2 = LineSegmentsGeometry(positions=[[[pos_s[0], pos_s[1], frame_s], [pos_t[0], pos_t[1], frame_t]]], )
            m2 = LineMaterial(linewidth=1, color='black')
            line = LineSegments2(g2, m2)
            self.scene_children.append(line)

    def add_ball(self, pos, frame, color):
        ball = Mesh(geometry=SphereGeometry(),
                    material=MeshLambertMaterial(color=color),
                    position=[pos[0], pos[1], frame * self.frame_spacing],
                    scale=[self.node_scale, self.node_scale, self.node_scale])
        return ball

    def add_light(self):
        self.scene_children.append(AmbientLight(color='#777777'))

    def create_camera(self):
        key_light = DirectionalLight(color='white', position=[3, 5, 1], intensity=0.5)
        c = PerspectiveCamera(position=[0, 5, 5], up=[0, 1, 0], children=[key_light])
        return c

    def build_renderer(self):
        scene = Scene(children=self.scene_children, background=None)

        return Renderer(camera=self.camera,
                        scene=scene,
                        alpha=True,
                        clearOpacity=0,
                        controls=[OrbitControls(controlling=self.camera)],
                        width=800,
                        height=600)
