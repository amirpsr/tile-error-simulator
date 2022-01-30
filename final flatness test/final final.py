import tile_error_recognition
import tile_error
import numpy as np

if __name__ == '__main__':
    data_x_lines = 10
    data_y_lines = 6
    x0=np.linspace(0,9,data_x_lines)
    y0=np.linspace(0,5,data_y_lines)
    xx0,yy0=np.meshgrid(x0,y0)
    z0=tile_error.np.ones(xx0.shape)
    plane=[x0,y0,z0]
    # plane which shows sample tile
    fig = tile_error.plt.figure(figsize=tile_error.plt.figaspect(1))  
    ax = fig.add_subplot(111, projection='3d')

    t=tile_error.Tile(plane)
    # make a tile object
    t.corner_pyramid(6,1,[2,2])
    t.corner_pyramid(5,2,[2,2])
    t.corner_pyramid(4,3,[2,2])
    t.corner_pyramid(1,4,[2,2])
    # make an error
    ax.plot_surface(yy0, xx0, t.array[2],  rstride=4, cstride=4, color='r')
    
    offset_list = [0 for i in range(data_y_lines)]

    new_arr=np.append(t.array[2],np.zeros((data_y_lines,1)),axis=1)
    new_arr=np.insert(new_arr,0,np.zeros(data_y_lines),axis=1)
    new_arr=new_arr.tolist()
    # prepare data for Tile_Geo class
    tile = tile_error_recognition.Tile_Geo(new_arr, offset_list)
    print(tile.get_grade())
    print(t.array[2])
    # 
    ax.scatter(tile.pa1b1.x,tile.pa1b1.y,tile.pa1b1.z)
    ax.scatter(tile.pa1b2.x,tile.pa1b2.y,tile.pa1b2.z)
    ax.scatter(tile.pa2b1.x,tile.pa2b1.y,tile.pa2b1.z)
    ax.scatter(tile.pa2b2.x,tile.pa2b2.y,tile.pa2b2.z)
    
    print(tile.pa1b1.x,tile.pa1b1.y,tile.pa1b1.z)
    print(tile.pa1b2.x,tile.pa1b2.y,tile.pa1b2.z)
    print(tile.pa2b1.x,tile.pa2b1.y,tile.pa2b1.z)
    print(tile.pa2b2.x,tile.pa2b2.y,tile.pa2b2.z)
    i=0
    for plane in tile.corner_plane_list :
        if i<1:
            [x_0,y_0,z_0] = list(plane.p1)
            [n_1,n_2,n_3] = list(plane.normal_vector)
            z = -n_1/n_3*(yy0-x_0)-n_2/n_3*(xx0-y_0)+z_0 
            ax.plot_surface(yy0, xx0, z, alpha=0.2)
            print(plane)
            i=i+1

    # desired_name = ['pa1b1','pa1b2','pa2b1','pa2b2']
    # for point_name in tile.special_points_coordinate_dict:
    #     if point_name in desired_name:
    #         for points_cordinates in tile.special_points_coordinate_dict[point_name]:
    #         # x = tile.special_points_coordinate_dict[point_name][points_cordinates]
    #         # y = tile.special_points_coordinate_dict[point_name][0][1]
    #             x,y = points_cordinates
            
    #             ax.scatter(x,y,tile.sensors_array[x][y])
 
    # t.show_plot(ax,xx0, yy0)

tile_error.plt.show()
