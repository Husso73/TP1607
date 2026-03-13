import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx

from aco_functions import init_distance, init_mat, aco, longueur_route

# ── Graphe networkx ──────────────────────────────────────────────────────────

def build_graph(N, distances):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            G.add_edge(i, j, weight=distances[i][j])
    return G

def get_edge_widths(G, pheromone):
    max_ph = max(pheromone[i][j] for i, j in G.edges())
    return [5 * pheromone[i][j] / max_ph for i, j in G.edges()]

def get_edge_colors(G, pheromone):
    max_ph = max(pheromone[i][j] for i, j in G.edges())
    colors = []
    for i, j in G.edges():
        intensity = pheromone[i][j] / max_ph
        colors.append((0.1, 0.5, intensity, intensity * 0.8))
    return colors

def get_route_edges(visite, retour=False):
    edges = []
    for i in range(len(visite) - 1):
        c1, c2 = visite[i], visite[i + 1]
        edges.append((min(c1, c2), max(c1, c2)))
    if retour:
        c1, c2 = visite[-1], visite[0]
        edges.append((min(c1, c2), max(c1, c2)))
    return edges

# ── Affichage d'un graphe ─────────────────────────────────────────────────────

def draw_graphe(ax, G, pos, pheromone, meilleure_route, retour, titre):
    ax.clear()
    ax.set_facecolor('#1a1d27')

    edge_w = get_edge_widths(G, pheromone)
    edge_c = get_edge_colors(G, pheromone)
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_w, edge_color=edge_c)

    route_edges  = get_route_edges(meilleure_route, retour)
    autres_edges = [(i, j) for i, j in G.edges()
                    if (min(i, j), max(i, j)) not in route_edges]

    nx.draw_networkx_edges(G, pos, edgelist=autres_edges, ax=ax,
                           edge_color='#2e3347', width=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, ax=ax,
                           edge_color='#1db97a', width=3)

    depart        = meilleure_route[0]
    autres_noeuds = [n for n in G.nodes() if n != depart]
    nx.draw_networkx_nodes(G, pos, nodelist=autres_noeuds, ax=ax,
                           node_color='#7c6fcd', node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=[depart], ax=ax,
                           node_color='#f5a623', node_size=420)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color='white', font_size=8)
    ax.set_title(titre, color='white', fontsize=10, pad=6)
    ax.axis('off')

# ── Comparaison des deux modes ────────────────────────────────────────────────

def comparer(N=10, nb_iterations=60):
    random.seed(42)
    distance = init_distance(N)
    G        = build_graph(N, distance)
    pos      = nx.spring_layout(G, seed=7)

    print(f"\n=== N={N} villes, {nb_iterations} itérations ===")

    random.seed(42)
    r_sr, l_sr, hist_sr, ph_sr = aco(N, nb_iterations, distance, retour=False)
    print(f"  Sans retour : longueur = {l_sr}  |  route = {r_sr}")

    random.seed(42)
    r_ar, l_ar, hist_ar, ph_ar = aco(N, nb_iterations, distance, retour=True)
    print(f"  Avec retour : longueur = {l_ar}  |  route = {r_ar}")

    # ── figure ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor('#0f1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            left=0.05, right=0.97,
                            top=0.92, bottom=0.08,
                            hspace=0.45, wspace=0.25)

    ax_sr   = fig.add_subplot(gs[0, 0])
    ax_ar   = fig.add_subplot(gs[0, 1])
    ax_conv = fig.add_subplot(gs[1, :])

    for ax in [ax_sr, ax_ar, ax_conv]:
        ax.set_facecolor('#1a1d27')
        for spine in ax.spines.values():
            spine.set_edgecolor('#2e3347')

    draw_graphe(ax_sr, G, pos, ph_sr, r_sr, retour=False,
                titre=f'Sans retour — longueur {l_sr}')
    draw_graphe(ax_ar, G, pos, ph_ar, r_ar, retour=True,
                titre=f'Avec retour — longueur {l_ar}')

    # — courbe comparaison —
    iters = range(1, nb_iterations + 1)
    ax_conv.plot(iters, hist_sr, color='#1db97a', linewidth=2, label='Sans retour')
    ax_conv.fill_between(iters, hist_sr, alpha=0.12, color='#1db97a')
    ax_conv.plot(iters, hist_ar, color='#f5a623', linewidth=2, label='Avec retour')
    ax_conv.fill_between(iters, hist_ar, alpha=0.12, color='#f5a623')

    ax_conv.set_xlabel('Itération', color='#8899aa', fontsize=9)
    ax_conv.set_ylabel('Longueur',  color='#8899aa', fontsize=9)
    ax_conv.tick_params(colors='#8899aa')
    ax_conv.set_xlim(1, nb_iterations)
    for spine in ax_conv.spines.values():
        spine.set_edgecolor('#2e3347')
    ax_conv.legend(facecolor='#1a1d27', labelcolor='white',
                   edgecolor="#ffffff", fontsize=9)
    ax_conv.set_title('Comparaison de convergence', color='white',
                      fontsize=11, pad=8)

    diff = l_ar - l_sr
    fig.suptitle(
        f'ACO — {N} villes  |  '
        f'sans retour : {l_sr}   avec retour : {l_ar}   '
        f'(différence : {diff:+.0f})',
        color='white', fontsize=12
    )
    plt.show()


if __name__ == "__main__":
    for n in [10, 15, 20]:
        comparer(N=n, nb_iterations=60)