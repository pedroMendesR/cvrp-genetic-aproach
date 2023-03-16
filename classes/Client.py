from matplotlib.axes import Axes
from classes.Point import Point

show_point_id_subtitle = False
show_point_weight_subtitle = False

class Client(Point):

    def __init__(self, x_position: float, y_position: float, packet_weight: float=0):
        super().__init__(x_position, y_position)
        self.packet_weight = packet_weight
    
    def set_packet_weight(self, packet_weight):
        self.packet_weight = packet_weight

    def __str__(self, index=-1):
        return f'[{index}]  ({self.x_position}, {self.y_position}) com peso {self.packet_weight} e id {self.id}'


    def plot_client(self, axes_plot:Axes, color:str='r', reference:str='-1'):
        axes_plot.plot(self.x_position, self.y_position, marker="o", color=color)
        if reference != '-1':
            axes_plot.text(self.x_position, self.y_position, reference)
            axes_plot.text(self.x_position+0.35, self.y_position+0.35, self.packet_weight, color='#FF8000') if show_point_weight_subtitle else None
            axes_plot.text(self.x_position-0.35, self.y_position+0.35, self.id, color='#FF007F') if show_point_id_subtitle else None
