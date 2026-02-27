from random import randrange

Q = 1
C = 0.7
a = 1
b = 1

# matrice distance
def init_distance():
    mat = []
    for i in range(20):
            row = []
            for j in range(20):
                if j < i:
                    row.append(mat[j][i])
                elif i == j:
                    row.append(0)
                else:
                    r = randrange(1,20)
                    row.append(r)

            mat.append(row)
    return mat

dis = init_distance()
for ligne in dis:
    print(ligne)
# matrice pheronome
def init_mat():
    mat = []
    for i in range(20):
        row = []
        for j in range(20):
           row.append(1)
        mat.append(row)
    return mat

# print(init_mat())

# taille = len(ville)

# def visited():
#     placer = [randrange(4)][randrange(4)]
#     if 
#     for i in range()

# def random_endroite():

# def tour(phero,distance):

# #worse path to optimize becuase if they took always the good path they will never knwo if it is the best or not
# #cycle complete n ville and n formnie et ...

# def tir_de_sort():

# def 