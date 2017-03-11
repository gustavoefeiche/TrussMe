import math
import numpy as np

ke_matrix = np.array([[1,2,-1,-2],[2,3,-2,-3],[-1,-2,1,2],[-2,-3,2,3]])#matrix de rigidez no sistema global
material_value = 21#*(10**5)
coor = np.array([[0, 0],[0, 21],[21, 0],[21, 21]]) #matriz de coordenadas
inci = np.array([[0,1],[0,2],[2,3],[1,3],[1,2],[0,3]]) #Matriz de incidencia
prop = np.array([[1],[1],[1],[1],[math.sqrt(2)],[math.sqrt(2)]]) #matriz de propriedades geometricas
mater = np.array([[material_value]]*6)

def calc_distance(x1, y1, x2, y2):
    x_dist = (x2 - x1)
    y_dist = (y2 - y1)
    dist = float(math.sqrt(x_dist * x_dist + y_dist * y_dist))
    return dist

def calc_sin(y1,y2,dist):
    y_dist = (y2 - y1)
    return float(y_dist/dist)

def calc_cos(x1,x2,dist):
    x_dist = (x2 - x1)
    return float(x_dist/dist)

def calculate(item,coor):
    x1 = coor[item[0]][0]
    y1 = coor[item[0]][1]
    x2 = coor[item[1]][0]
    y2 = coor[item[1]][1]

    dist = float(calc_distance(x1,y1,x2,y2))
    sin = float(calc_sin(y1,y2,dist))
    cos = float(calc_cos(x1,x2,dist))
    return dist,cos,sin

def make_matrix(inci,coor):
    matrix = np.array([[0]*5]*6)
    new_matrix = matrix.astype(float)
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
    #retorna o elemento da matrix de rigidez global nas posicoes x e y
    s = float(geom_matrix[element_pos][3])
    c = float(geom_matrix[element_pos][4])
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


def make_fdeg_matrix(inci):
    m = np.zeros((len(inci), 4), dtype=np.int) # np.array([[0]*4]*range(len(inci)))
    for i in range(len(inci)):
        m[i] = [2*inci[i][0], 2*inci[i][0]+1, 2*inci[i][1], 2*inci[i][1]+1]
    return m

def calc_global_k():
    matrix_fdeg = make_fdeg_matrix(inci)
    max_fdeg = matrix_fdeg[-1][-1]
    k_global_matrix_pre = np.array([[0]*(max_fdeg+1)]*(max_fdeg+1))
    k_global_matrix = k_global_matrix_pre.astype(float)
    index = 0
    for degrees in matrix_fdeg:
        print(degrees)
        print(index)
        for x in range(len(degrees)):
            for y in range(len(degrees)):
                k = k_element(index,x,y)
                k *= (prop[index][0] * mater[index][0])/geom_matrix[index][2]
                k_global_matrix[degrees[x]][degrees[y]] += k
        index+=1
    return k_global_matrix

def main():
    global geom_matrix
    geom_matrix = make_matrix(inci,coor)
    print(geom_matrix);
    #print(make_matrix(inci,coor))
    print(calc_global_k())

if __name__ == '__main__':
    main()
