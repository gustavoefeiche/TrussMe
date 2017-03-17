import math
import numpy as np

ke_matrix = np.array([[1,2,-1,-2],[2,3,-2,-3],[-1,-2,1,2],[-2,-3,2,3]])#matrix de rigidez no sistema global
strain_stress_calc_matrix = np.array([["-c","-s","c","s"]])
material_value = 21#*(10**5)
coor = np.array([[0, 0],[0, 21],[21, 0],[21, 21]]) #matriz de coordenadas
inci = np.array([[0,1],[0,2],[2,3],[1,3],[1,2],[0,3]]) #Matriz de incidencia
prop = np.array([[1],[1],[1],[1],[math.sqrt(2)],[math.sqrt(2)]]) #matriz de propriedades geometricas
mater = np.array([[material_value]]*6)
bc_nodes = np.array([1,1,1,1,0,0,0,0])
force_matrix = np.array([[0]]*8)
#adicionando forcas
force_matrix[7] = -1000;

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

def calc_element (element_pos, y, x = 0 , matrix = ke_matrix):
    #retorna o elemento da matrix de rigidez global nas posicoes x e y
    s = float(geom_matrix[element_pos][3])
    c = float(geom_matrix[element_pos][4])
    element = matrix[x][y]

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
    elif element == "-c":
        return -c
        #print ("-s2 ", end='')
    elif element == "-s":
        return -s
        #print ("-s2 ", end='')
    elif element == "c":
        return c
        #print ("-s2 ", end='')
    elif element == "s":
        return s
        #print ("-s2 ", end='')

def make_fdeg_matrix(inci):
    m = np.zeros((len(inci), 4), dtype=np.int) # np.array([[0]*4]*range(len(inci)))
    for i in range(len(inci)):
        m[i] = [2*inci[i][0], 2*inci[i][0]+1, 2*inci[i][1], 2*inci[i][1]+1]
    return m

def matrix_boundaries_conditions(matrix, bound = bc_nodes):
    deleted = 0
    for i in range(len(bound)):
        if(bound[i] == 1):
            matrix = np.delete(matrix, (i - deleted), 0)
            matrix = np.delete(matrix, (i - deleted), 1)
            deleted += 1
    return matrix

def matrix_boundaries_conditions_strain(matrix, bound):
    deleted = 0
    for item in bound:
        matrix = np.delete(matrix, item - deleted)
        deleted += 1
    return matrix

def matrix_reaction_node_boundaries_conditions(matrix):
    deleted = 0
    for i in range(len(bc_nodes)):
        if(bc_nodes[i] == 1):
            matrix = np.delete(matrix, (i - deleted), 1)
            matrix = np.delete(matrix, (-1), 0)
            deleted += 1
    return matrix

def force_boundaries_conditions(force_matrix):
    deleted = 0
    for i in range(len(bc_nodes)):
        if(bc_nodes[i] == 1):
            force_matrix = np.delete(force_matrix, (i - deleted), 0)
            deleted += 1
    return force_matrix

def calc_global_k():
    max_fdeg = matrix_fdeg[-1][-1]
    k_global_matrix_pre = np.array([[0]*(max_fdeg+1)]*(max_fdeg+1))
    k_global_matrix = k_global_matrix_pre.astype(float)
    index = 0
    for degrees in matrix_fdeg:
        for x in range(len(degrees)):
            for y in range(len(degrees)):
                k = calc_element(index,y,x)
                k *= (prop[index][0] * mater[index][0])/geom_matrix[index][2]
                k_global_matrix[degrees[x]][degrees[y]] += k*(10**5)
        index+=1
    k_global_matrix = np.array(k_global_matrix)
    k_global_matrix = np.fliplr(k_global_matrix)
    k_global_matrix = np.flipud(k_global_matrix)
    return k_global_matrix

def fill_displacement_matrix(displacement_matrix):
    for i in range(len(bc_nodes)):
        if bc_nodes[i] == 1:
            displacement_matrix = np.insert(displacement_matrix, i, 0)
    return displacement_matrix

def calc_displacement(k_global_matrix, force_matrix):
    k_global_matrix = matrix_boundaries_conditions(k_global_matrix)
    k_global_matrix = np.linalg.inv(k_global_matrix)
    displacement_matrix = k_global_matrix.dot(force_matrix)
    return displacement_matrix

def calc_reaction_node_matrix(k_global_matrix,matrix):
    k_global_matrix = matrix_reaction_node_boundaries_conditions(k_global_matrix)
    k_global_matrix = k_global_matrix.dot(matrix)
    return k_global_matrix

def calc_strain(d_matrix):
    print(geom_matrix)
    for element in range(len(geom_matrix)):
        strain = []
        U = []
        sin_cos_matrix = []
        for i in range(4):
            sin_cos_matrix.append(calc_element(element, i, 0, matrix = strain_stress_calc_matrix))

        u = matrix_boundaries_conditions_strain(d_matrix,matrix_fdeg[element])
        for y in range(len(u)):
            U.append([u[y]])

        U = np.array(U)
        sin_cos_matrix = np.array([sin_cos_matrix])
        print(U)
        print(sin_cos_matrix)
        m = U.dot(sin_cos_matrix)
        break
        a_strain = (1 / geom_matrix[element][2]) * m[0]
        strain.append(a_strain)
    return strain

def main():
    global geom_matrix
    global force_matrix
    global matrix_fdeg
    matrix_fdeg = make_fdeg_matrix(inci)
    geom_matrix = make_matrix(inci,coor)
    k_global_matrix = calc_global_k()
    force_matrix = force_boundaries_conditions(force_matrix)
    displacement_matrix = calc_displacement(k_global_matrix, force_matrix)
    reaction_node_matrix = calc_reaction_node_matrix(k_global_matrix, displacement_matrix)
    displacement_matrix = fill_displacement_matrix(displacement_matrix)
    strain = calc_strain(displacement_matrix)
    print(strain)

if __name__ == '__main__':
    main()
