from tkinter import PROJECTING
from webbrowser import get
import tile_error
import tile_error_recognition
from sympy import Plane, Point3D, Line3D, geometry ,symbols 
import numpy as np
def point_to_plane_z_projection(plane:Plane,point:Point3D):
    """
    projects a given point on the given plane along z direction

    Args:
        plane (Plane): [plane which the point is projected on]
        point (Point3D): [point we want its projection]
    Returns:
        [Point]: [the projected point]
    """
    [x_0,y_0,z_0] = list(plane.p1)
    [n_1,n_2,n_3] = list(plane.normal_vector)
    z1=-n_1/n_3*(point.x-x_0)-n_2/n_3*(point.y-y_0)+z_0
    projected_point= Point3D(point.x, point.y , z1)
    ax.scatter(projected_point.x,projected_point.y,projected_point.z)
    return projected_point

if __name__ == '__main__':
    offset_list = [987, 1076, 1131, 1148, 1186]
    sample_file = []
    with open(f'tile_1.json') as f:
        sample_file = tile_error_recognition.json.loads(f.read())
    for setting, data in sample_file.items():
        print(f'setting {setting}')
        for sample in data:
            t_id = data[sample]['tile_id']
            sensor_data = data[sample]['data']
            tile = tile_error_recognition.Tile_Geo(sensor_data, offset_list)
            print(tile.get_grade())
            if tile.is_data_valid:

                x = tile_error.np.arange(0,tile.max_sensor_samples,1)
                y = tile_error.np.arange(0,tile.sensor_count,1)
                xx ,yy =tile_error.np.meshgrid(x,y)

                errored_tile = tile_error.Tile([y , x, np.flipud(np.array(tile.sensors_array,np.float64))])
                print(errored_tile.array[2])
                print(tile.sensors_data)
                # errored_tile.corner_pyramid(1000,3,[3,3])
                
                prepared_errored_tile = np.hstack((np.zeros((y.size,1)),errored_tile.array[2],np.zeros((y.size,1))))

                tile2 = tile_error_recognition.Tile_Geo(prepared_errored_tile, [0,0,0,0,0])
                print(tile2.get_grade())
                fig = tile_error.plt.figure(figsize=tile_error.plt.figaspect(1))  
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(yy, xx, (np.array(tile2.sensors_array,np.float64)),  rstride=4, cstride=4, color='r')
                i=0
                neighbourhood_points_list = []
                for point_name in tile2._special_corner_point_list:
                    if i<10:
                        point = getattr(tile2,point_name)
                        ax.scatter(point.x,point.y,point.z)
                        plane = getattr(tile2,f'plane_{point_name}')
                        projected_point =point_to_plane_z_projection(plane,point)
                        [x_0,y_0,z_0] = list(plane.p1)
                        [n_1,n_2,n_3] = list(plane.normal_vector)
                        z = -n_1/n_3*(yy-x_0)-n_2/n_3*(xx-y_0)+z_0 
                        ax.plot_surface(yy, xx, z, alpha=0.2)
                        distance = abs(point.z-projected_point.z)
                        l2=geometry.Segment3D(point, projected_point)
                        ax.plot([l2.p1.x,l2.p2.x],[l2.p1.y,l2.p2.y],[l2.p1.z,l2.p2.z], color='black')
                        ax.text(l2.midpoint.x, l2.midpoint.y, l2.midpoint.z, "{:.2f}".format(float(distance)), l2.direction_ratio)
                        i+=1
                tile_error.plt.show()