from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random


class Tile:
# in this class we assume every tile as a member of 'Tile' class we define here.
# we get an array of 3 elements to define a member
# then we define each error as a method 
    count=0
    def __init__(self , my_tile_array:list):
        """[method of defining the tile]

        Args:
            my_tile_array (np.array): [an array of 3 arguments: my_tile_array = [x ,y ,z ]]
            x : array of x cordinates of the tile (1-D array)
            y : array of y cordinates of the tile (1-D array)
            z : array of z cordinates of the tile in size of meshgrid(x,y) (2-D array)
        """ 
                
        self.array = my_tile_array.copy()
        # we copy the original array, to avoid unintended changees
#==============================================================
    def continuous_reading(self, error_magnitude:float , error_area_coordinates:list ):
        """[apply continuous reading error on the tile, it sums data on the tile with a random number within range of error magnitude.]

        Args:
            error_magnitude (float): [random number will be generated within range of (-error_magnitude,error_magnitude)]
            error_area_coordinates (list): [number of points in lenghth and width of the error area,
            [errror_width,error_length]]
        """        
        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix

        center_length, center_width = int((self.array[0].size)/2), int((self.array[1].size)/2)
        # for odd array sizes, center cordinates will be (number-1)/2

        for length in range(0,error_length):
            for width in range(0,error_width):
                self.array[2][center_width-int(error_width/2)+width+(1-error_width%2),\
                center_length-int(error_length/2)+length+(1-error_length%2)]\
                +=(random.uniform(-error_magnitude,error_magnitude)) 
#---------------------------------------------------------------
#---------------------------------------------------------------
    def center_pyramid(self, error_magnitude:float , error_area_coordinates:list):
        """[center error on the tile with the shape of pyramid]

        Args:
            error_magnitude (float): [it shows maximum pyramids height]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        
        error_width , error_length = error_area_coordinates 
        pyramid_height_step=(error_magnitude)/(int((min(error_length,error_width)/2))
            +min(error_length,error_width)%2)

        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix

        center_length, center_width = int((self.array[0].size)/2), int((self.array[1].size)/2)
        # for odd array sizes, center cordinates will be (number-1)/2

        for a in range(0,min(error_length,error_width)):

            self.array[2][center_width-int(error_width/2)+a:center_width+int(error_width/2)-a+ (error_width%2), \
            center_length-int(error_length/2)+a:center_length+int(error_length/2)-a+(error_length%2)]\
            +=pyramid_height_step            
           
#---------------------------------------------------------------
    def center_sphere(self, error_magnitude:float , error_area_coordinates:list):
        """[center error on the tile with the shape of sphere]

        Args:
            error_magnitude (float): [it shows maximum sphere height]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        
        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix
        center_length, center_width = int((self.array[0].size)/2), int((self.array[1].size)/2)
        # for odd array sizes, center cordinates will be (number-1)/2
        x=np.linspace(-0.5,0.5,error_length)
        y=np.linspace(-0.5,0.5,error_width)
        
        xx,yy= np.meshgrid(x,y)
        z= error_magnitude*np.sqrt(1-xx**2-yy**2) 
        z[xx**2 + yy**2 > 1] = 0
        

        self.array[2][center_width-int(error_width/2):center_width+int(error_width/2)+(error_width%2),\
        center_length-int(error_length/2):center_length+int(error_length/2)+(error_length%2)]\
        +=z

# #---------------------------------------------------------------
# #---------------------------------------------------------------
    def corner_pyramid(self,error_magnitude:float, point:int , error_area_coordinates:list):
        """[corner error on the corners makes them rise or fall with the shape of pyramid within 
        the cordinates]

        Args:
            error_magnitude (float): [it shows maximum pyramid height]
            point (int): [which corner to put the pyramid]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        
        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix

        pyramid_height_step=(error_magnitude/min(error_length,error_width))
        

        if point==1: # top left
            for a in range(0,min(error_length,error_width)):
                self.array[2][0:error_width-a, 0:error_length-a]\
                +=pyramid_height_step

        if point==2: # bot left
            for a in range(0,min(error_length,error_width)):
                self.array[2][self.array[0].size-(error_width-a):self.array[0].size,\
                0:error_length-a]\
                +=pyramid_height_step

        if point==3: # bot right
            for a in range(0,min(error_length,error_width)):
                self.array[2][self.array[0].size-(error_width-a):self.array[0].size,\
                self.array[1].size-(error_length-a):self.array[1].size]\
                +=pyramid_height_step

        if point==4: # bot right
            for a in range(0,min(error_length,error_width)):
                self.array[2][0:error_width-a,\
                self.array[1].size-(error_length-a):self.array[1].size]\
                +=pyramid_height_step
# #---------------------------------------------------------------

    def corner_sphere(self,error_magnitude:float, point:int , error_area_coordinates:list):
        """[corner error on the corners makes them rise or fall with the shape of sphere within 
        the cordinates]

        Args:
            error_magnitude (float): [it shows maximum sphere height]
            point (int): [which corner to put the sphere]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        
        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix

        x=np.linspace(-0.5,0.5,2*error_length)
        y=np.linspace(-0.5,0.5,2*error_width)
        xx,yy= np.meshgrid(x,y)
        z=error_magnitude*np.sqrt(1-xx**2-yy**2) 
        z[(xx**2+yy**2)>1]=0
        # make  a sphere twice as large as error cordinates and we chose one piece for each point   
        if point==1: #top left
            self.array[2][0:error_width,\
            0:error_length]\
            +=z[error_width:2*error_width,error_length:2*error_length]

        if point==2: #bot left
            self.array[2][-error_width:self.array[0].size,\
            0:error_length]\
            +=z[0:error_width,error_length:2*error_length]

        if point==3: #bot right
            self.array[2][-error_width:self.array[0].size,\
            -error_length:self.array[1].size]\
            +=z[0:error_width,0:error_length]

        if point==4: #top right
            self.array[2][0:error_width,\
            -error_length:self.array[1].size]\
            +=z[error_width:2*error_width,0:error_length]
# #---------------------------------------------------------------
    def corner_ramp(self, error_magnitude:float, point:int , error_area_coordinates:list):
        """[corner error on the corners makes them rise or fall with the shape of ramp within 
        the cordinates]

        Args:
            error_magnitude (float): [it shows maximum ramp height]
            point (int): [which corner to put the ramp]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        
        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix
        x=np.linspace(-1,1,error_length+1)
        y=np.linspace(-1,1,error_width+1)
        xx,yy= np.meshgrid(x,y)

        if point==1: #top left
            z=(-xx-yy)*(error_magnitude/2)
            z[z<0]=0
            self.array[2][0:error_width+1,0:error_length+1]+=z

        if point==2: #bot left
            z=(-xx+yy)*(error_magnitude/2)
            z[z<0]=0
            self.array[2][-error_width-1:self.array[0].size,0:error_length+1]+=z

        if point==3: #bot right
            z=(xx+yy)*(error_magnitude/2)
            z[z<0]=0
            self.array[2][-error_width-1:self.array[0].size+1,-error_length-1:self.array[1].size]+=z

        if point==4: #top right
            z=(xx-yy)*(error_magnitude/2)
            z[z<0]=0
            self.array[2][0:error_width+1,-error_length-1:self.array[1].size]+=z

# #---------------------------------------------------------------
# #---------------------------------------------------------------

    def side_pyramid(self,error_magnitude:float, point:int , error_area_coordinates:list):
        """[side error on the sides makes them rise or fall with the shape of pyramid within 
        the cordinates]

        Args:
            error_magnitude (float): [it shows maximum pyramid height]
            point (int): [which side to put the pyramid]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        

        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix        

        if point==1: #b1

            pyramid_height_step=(error_magnitude/min(error_length,(int(error_width/2)+(error_width%2))))
            
            for a in range(0,min(error_length,error_width)):
                self.array[2][int(self.array[0].size/2)-int(error_width/2)+a:int(self.array[0].size/2)+int(error_width/2)-a+(error_width%2),\
                0:error_length-a]\
                +=pyramid_height_step

        if point==2: #a2

            pyramid_height_step=(error_magnitude/min((int(error_length/2)+(error_length%2),error_width)))

            for a in range(0,min(error_length,error_width)):
                self.array[2][-error_width+a:self.array[0].size,\
                int(self.array[1].size/2)-int(error_length/2)+a:int(self.array[1].size/2)+int(error_length/2)-a+(error_length%2)]\
                +=pyramid_height_step

        if point==3: #b2

            pyramid_height_step=(error_magnitude/min(error_length,(int(error_width/2)+(error_width%2))))

            for a in range(0,min(error_length,error_width)):
                self.array[2][int(self.array[0].size/2)-int(error_width/2)+a:int(self.array[0].size/2)+int(error_width/2)-a+(error_width%2),\
                -error_length+a:self.array[1].size]\
                +=pyramid_height_step

        if point==4: #a1

            pyramid_height_step=(error_magnitude/min((int(error_length/2)+(error_length%2),error_width)))

            for a in range(0,min(error_length,error_width)):
                self.array[2][0:error_width-a,\
                int(self.array[1].size/2)-int(error_length/2)+a:int(self.array[1].size/2)+int(error_length/2)-a+(error_length%2)]\
                +=pyramid_height_step
# #---------------------------------------------------------------

    def side_sphere(self, error_magnitude:float, p:int , error_area_coordinates:list):
        """[side error on the sides makes them rise or fall with the shape of sphere within 
        the cordinates]

        Args:
            error_magnitude (float): [it shows maximum sphere height]
            point (int): [which side to put the sphere]
            error_area_coordinates (list): [number of points in length and width of the error area]
            [errror_width,error_length]
        """        

        error_width , error_length = error_area_coordinates
        # error length is the number of columns in the tile matrix
        # error width is the number of rows in the tile matrix  
        center_length,center_width=int(self.array[1].size/2),int(self.array[0].size/2)

        if p==1: #b1
            x=np.linspace(-0.5, 0.5, 2*error_length)
            y=np.linspace(-0.5, 0.5, error_width)
            xx,yy= np.meshgrid(x,y)
            z=error_magnitude*np.sqrt(1-xx**2-yy**2) #Use np.sqrt like you had before
            z[(xx**2+yy**2)>1]=0

            self.array[2][int(self.array[0].size/2)-int(error_width/2):int(self.array[0].size/2)+int(error_width/2)+(error_width%2),\
                0:error_length]\
            =+z[0:error_width,error_length:error_length*2]
            


        if p==2: #a2
            x=np.linspace(-0.5,0.5,error_length)
            y=np.linspace(-0.5,0.5,2*error_width)
            xx,yy= np.meshgrid(x,y)
            z=error_magnitude*np.sqrt(1-xx**2-yy**2) #Use np.sqrt like you had before
            z[(xx**2+yy**2)>1]=0

            self.array[2][-error_width:self.array[0].size,\
            center_length-int(error_length/2):center_length+int(error_length/2)+(error_length%2)]\
            +=z[0:error_width,0:error_length]

        if p==3: #b2

            x=np.linspace(-0.5,0.5,2*error_length)
            y=np.linspace(-0.5,0.5,error_width)
            xx,yy= np.meshgrid(x,y)
            z=error_magnitude*np.sqrt(1-xx**2-yy**2) #Use np.sqrt like you had before
            z[(xx**2+yy**2)>1]=0 

            self.array[2][center_width-int(error_width/2):center_width+int(error_width/2)+(error_width%2),\
            -error_length:self.array[1].size]\
            +=z[0:error_width,0:error_length]

        if p==4: #a1
            x=np.linspace(-0.5,0.5,error_length)
            y=np.linspace(-0.5,0.5,2*error_width)
            xx,yy= np.meshgrid(x,y)
            z=error_magnitude*np.sqrt(1-xx**2-yy**2) #Use np.sqrt like you had before
            z[(xx**2+yy**2)>1]=0

            self.array[2][0:error_width,\
            center_length-int(error_length/2):center_length+int(error_length/2)+(error_length%2)]\
            +=z[error_width:2*error_width,0:error_length]
#---------------------------------------------------------------
#---------------------------------------------------------------
#==================================================================
    def show_plot(self,ax,xx,yy):
        ax.plot_surface(xx, yy, self.array[2],  rstride=4, cstride=4, color='r')
        plt.show()



if __name__ == '__main__':
    


    x0=np.linspace(0,9,50)
    y0=np.linspace(0,9,11)
    xx0,yy0=np.meshgrid(x0,y0)
    z0=np.zeros(xx0.shape)
    plane=[x0,y0,z0]
    fig = plt.figure(figsize=plt.figaspect(1))
    ax = fig.add_subplot(111, projection='3d')

    t=Tile(plane)
    # t.continuous_reading(5,[3,4])
    # t.center_pyramid (6,[5,5] )
    # t.center_sphere (3,[3,3] )
    t.corner_pyramid(6 ,1,[4,3] )
    t.corner_pyramid(6 ,2,[4,3] )
    t.corner_pyramid(6 ,3,[4,3] )
    t.corner_pyramid(6 ,4,[4,3] )

    # t.corner_sphere(6 ,1,[1,1] )
    # t.corner_sphere(6 ,2,[1,1] )
    # t.corner_sphere(6 ,3,[1,1] )
    # t.corner_sphere(6 ,4,[1,1] )

    # t.corner_ramp(6 ,1,[3,3] )
    # t.corner_ramp(6 ,2,[3,3] )
    # t.corner_ramp(6 ,3,[3,3] )
    # t.corner_ramp(6 ,4,[3,3] )

    # t.side_pyramid(6 ,1,[4,2])
    # t.side_pyramid(6 ,2,[2,3] )
    # t.side_pyramid(6 ,3,[3,3] )
    # t.side_pyramid(6 ,4,[3,3] )

    # t.side_sphere(6 ,1,[3,3])
    # t.side_sphere(6 ,2,[2,4] )
    # t.side_sphere(6 ,3,[2,3] )
    # t.side_sphere(6 ,4,[2,3] )    


    t.show_plot(ax,xx0, yy0)
    print(t.array[2])