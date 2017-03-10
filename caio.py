import math
import numpy as np

ke_matrix = np.array([[1,2,-1,-2],[2,3,-2,-3],[-1,-2,1,2],[-2,-3,2,3]])#matrix de rigidez no sistema global
material_value = 21*(10**5)
coor = np.array([[0, 0],[0, 21],[21, 0],[21, 21]]) #matriz de coordenadas
inci = np.array([[1,2],[1,3],[3,4],[2,4],[2,3],[1,4]]) #Matriz de inicdencia
prop = np.array([[1],[1],[1],[1],[math.sqrt(2)],[math.sqrt(2)]]) #matriz de propriedades geometricas
mater = np.array([[material_value]]*6)

def calc_distance(x1, y1, x2, y2):
    x_dist = (x2 - x1)
    y_dist = (y2 - y1)
    return math.sqrt(x_dist * x_dist + y_dist * y_dist)

def calc_sin(y1,y2,dist):
    y_dist = (y2 - y1)
    return y_dist/dist

def calc_cos(x1,x2,dist):
    x_dist = (x2 - x1)
    return x_dist/dist

def calculate(item,coor):
    x1 = coor[item[0]-1][0]
    y1 = coor[item[0]-1][1]
    x2 = coor[item[1]-1][0]
    y2 = coor[item[1]-1][1]

    dist = calc_distance(x1,y1,x2,y2)
    sin = calc_sin(y1,y2,dist)
    cos = calc_cos(x1,x2,dist)
    return dist,cos,sin

def make_matrix(inci,coor):
    new_matrix = np.array([[0]*5]*6)
    x = 0
    for item in inci:
        dist,cos,sin = calculate(item,coor)
        new_matrix[x][0] = item[0]
        new_matrix[x][1] = item[1]
        new_matrix[x][2] = dist
        new_matrix[x][3] = cos
        new_matrix[x][4] = sin
        x+=1
    return new_matrix

def k_element (element_pos, x, y):
    #retorna o elemento da matrix de rigidez global nas posições x e y
    s = geom_matrix[element_pos][3]
    c = geom_matrix[element_pos][4]
    element = ke_matrix[x][y]

    if element == 1:
        return c**2
        #print ("c2 ", end='')
    elif element == 2:
        return c*s
        #print ("cs ", end='')
    elif element == 3:
        return s**2
        #print ("s2 ", end='')
    elif element == -1:
        return -c**2
        #print ("-c2 ", end='')
    elif element == -2:
        return -c*s
        #print ("-cs ", end='')
    elif element == -3:
        return -s**2
        #print ("-s2 ", end='')


geom_matrix = make_matrix(inci, coor)
print (k_element(2, 1, 1))



#k_element(1,2,3)
#script
#print(make_matrix(inci,coor))
