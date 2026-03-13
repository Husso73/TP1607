import random
import numpy as np

Q = 1
C = 0.7
a = 1
b = 1

# ── Init ─────────────────────────────────────────────────────────────────────

def init_distance(N=10):
    mat = []
    for i in range(N):
        row = []
        for j in range(N):
            if j < i:
                row.append(mat[j][i])
            elif i == j:
                row.append(0)
            else:
                row.append(random.randint(1, 19))
        mat.append(row)
    return mat



def init_mat(N=10):
    mat = []
    for i in range(N):
        row = []
        for j in range(N):
            if i != j:
                row.append(1)
            else:
                row.append(0)
        mat.append(row)
    return mat

# ── Probabilités ─────────────────────────────────────────────────────────────

def get_phermone(c1, c2, pheromone):
    return (pheromone[c1][c2]) ** a

def get_distance_prob(c1, c2, distance):
    return (1 / distance[c1][c2]) ** b

def desire(c1, c2, pheromone, distance):
    return get_phermone(c1, c2, pheromone) * get_distance_prob(c1, c2, distance)

def sum_desire(c1, villes_restantes, pheromone, distance):
    total = 0
    for i in villes_restantes:
        total += desire(c1, i, pheromone, distance)
    return total

def prob(c1, c2, villes_restantes, pheromone, distance):
    d = desire(c1, c2, pheromone, distance)
    s = sum_desire(c1, villes_restantes, pheromone, distance)
    return d / s

def get_probas(c1, villes_restantes, pheromone, distance):
    probas = []
    for v in villes_restantes:
        probas.append(prob(c1, v, villes_restantes, pheromone, distance))
    total = sum(probas)
    for i in range(len(probas)):
        probas[i] = probas[i] / total
    return probas

def prob_tir_au_sort(c1, villes_restantes, pheromone, distance):
    probas = get_probas(c1, villes_restantes, pheromone, distance)
    res = int(np.random.choice(villes_restantes, p=probas))
    return res

# ── Route ────────────────────────────────────────────────────────────────────

def route(depart, pheromone, distance, N=10):
    visite = [depart]
    non_visite = list(range(N))
    non_visite.remove(depart)
    while non_visite:
        ville_actuelle = visite[-1]
        suivante = prob_tir_au_sort(ville_actuelle, non_visite, pheromone, distance)
        visite.append(suivante)
        non_visite.remove(suivante)
    return visite

# ── Longueur ─────────────────────────────────────────────────────────────────

def longueur_route(visite, distance, retour=False):
    total = 0
    for i in range(len(visite) - 1):
        total += distance[visite[i]][visite[i + 1]]
    if retour:
        total += distance[visite[-1]][visite[0]]
    return total

# ── Phéromones ───────────────────────────────────────────────────────────────

def evaporer(pheromone, N):
    for i in range(N):
        for j in range(N):
            pheromone[i][j] *= (1 - C)

def depot_pheromone(c1, c2, pheromone, longueur):
    pheromone[c1][c2] += Q / longueur
    pheromone[c2][c1] += Q / longueur

def deposer_pheromones(visite, pheromone, distance, retour=False):
    L = longueur_route(visite, distance, retour)
    for i in range(len(visite) - 1):
        depot_pheromone(visite[i], visite[i + 1], pheromone, L)
    if retour:
        depot_pheromone(visite[-1], visite[0], pheromone, L)

# ── ACO ───────────────────────────────────────────────────────────────────────

def aco(N, nb_iterations, distance, retour=False):
    pheromone          = init_mat(N)
    meilleure_route    = None
    meilleure_longueur = float('inf')
    historique         = []

    for i in range(nb_iterations):
        # répartition aléatoire des fourmis sur le graphe (spec du cours)
       
        #Départs aléatoires
        departs = []
        for j in range(N):
            departs.append(random.randint(0, N - 1))

        routes = []
        for depart in departs:
            routes.append(route(depart, pheromone, distance, N))


        #Évaporation
        evaporer(pheromone, N)


        #Dépôt 
        for r in routes:
            deposer_pheromones(r, pheromone, distance, retour)


        for r in routes:
            L = longueur_route(r, distance, retour)
            if L < meilleure_longueur:
                meilleure_longueur = L
                meilleure_route = []
                for ville in r:
                    meilleure_route.append(ville)
        historique.append(meilleure_longueur)

    return meilleure_route, meilleure_longueur, historique, pheromone




# ── Tests question 2 : variation du nombre de villes ─────────────────────────
 
def test_variation_villes():
    nb_iterations = 60
    valeurs_N = [5, 10, 15, 20, 30]
 
    print("Question 2 - variation du nombre de villes")
    print("nb_iterations =", nb_iterations)
    print()
 
    for N in valeurs_N:
        print("--- N =", N, "villes ---")
 
        random.seed(42)
        distance = init_distance(N)
 
        #random.seed(41)
        meilleure_route_sr, meilleure_longueur_sr,_,_ = aco(N, nb_iterations, distance, retour=False)
 
        #random.seed(40)
        meilleure_route_ar, meilleure_longueur_ar,_, _ = aco(N, nb_iterations, distance, retour=True)
 
        print("  sans retour :")
        print("    meilleure route    :", meilleure_route_sr)
        print("    meilleure longueur :", meilleure_longueur_sr)
 
        print("  avec retour :")
        print("    meilleure route    :", meilleure_route_ar)
        print("    meilleure longueur :", meilleure_longueur_ar)
 
 
if __name__ == "__main__":
    test_variation_villes()