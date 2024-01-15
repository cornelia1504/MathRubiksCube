import numpy as np
#!pip install colored
import colored
import itertools
COULEURS = {'o':214, 'r':1, 'b':4, 'g':2, 'w':255, 'y':226}
LETTRES  = ('R','U','L','F','B','D','M')


import numpy as np

class RubiksCube(object):

    def __init__(self):
        """
    Initializes a Rubik's Cube with the solved state.
    """
        # Initialisation par l'Identité (état résolu)
        # Orientation: Front=Blue, Up=White.
        self.up = np.array([['w'] * 3] * 3)
        self.down = np.array([['y'] * 3] * 3)
        self.front = np.array([['b'] * 3] * 3)
        self.back = np.array([['g'] * 3] * 3)
        self.left = np.array([['r'] * 3] * 3)
        self.right = np.array([['o'] * 3] * 3)
        self.nb_moves = 0  # le nombre de mouvements appliqués sur le cube
        self.shuffled = False  # si le cube est mélangé
        self.previous = ""  # le dernier mouvement appliqué sur le cube

    def set_configuration(self, up, front, down, left, right, back):
        """
        Soumission d'un état, lequel peut ensuite être résolu.
        Les couleurs sont à renseigner au sein de numpy array 3x3, de la gauche vers la droite,
        du haut vers le bas en regardant chaque face... de face.
        """
        self.up, self.down, self.front, self.back, self.left, self.right = up, down, front, back, left, right

    def inverse_moves(self, moves):
        """
        Inverse la suite de mouvements passée en paramètre.
        """
        moves = self.convert_mélange(moves)
        l = [(x + "'") for x in moves]
        l.reverse()
        l = "".join(l)
        return l

    def R_L_F_D(self, face):
        """
        Effectue une rotation sur les coins et arêtes de la face spécifiée.
        """
        # Coins
        a, b, c, d = face[0, 0], face[0, 2], face[2, 2], face[2, 0]
        face[0, 0], face[0, 2], face[2, 2], face[2, 0] = d, a, b, c
        # Arêtes :
        a, b, c, d = face[0, 1], face[1, 2], face[2, 1], face[1, 0]
        face[0, 1], face[1, 2], face[2, 1], face[1, 0] = d, a, b, c

    def U(self):
        """
        Effectue la rotation de la face supérieure dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.up)
        a = self.front[0].copy()
        self.front[0], self.right[0], self.back[0], self.left[0] = self.right[0], self.back[0], self.left[0], a
        if self.shuffled and self.previous != 'U':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'U'

    def D(self):
        """
        Effectue la rotation de la face inférieure dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.down)
        a = self.front[2].copy()
        self.front[2], self.left[2], self.back[2], self.right[2] = self.left[2], self.back[2], self.right[2], a
        if self.shuffled and self.previous != 'D':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'D'

    def R(self):
        """
        Effectue la rotation de la face droite dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.right)
        swip = self.up[:, 2].copy()
        self.up[:, 2] = self.front[:, 2]
        self.front[:, 2] = self.down[:, 2]
        self.down[:, 2] = np.flip(self.back[:, 0], axis=0)
        self.back[:, 0] = np.flip(swip, axis=0)
        if self.shuffled and self.previous != 'R':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'R'

    def L(self):
        """
        Effectue la rotation de la face gauche dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.left)
        swip = self.up[:, 0].copy()
        self.up[:, 0] = np.flip(self.back[:, 2], axis=0)
        self.back[:, 2] = np.flip(self.down[:, 0], axis=0)
        self.down[:, 0] = self.front[:, 0]
        self.front[:, 0] = swip
        if self.shuffled and self.previous != 'L':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'L'

    def F(self):
        """
        Effectue la rotation de la face avant dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.front)
        swip = self.up[2, :].copy()
        self.up[2, :] = np.flip(self.left[:, 2], axis=0)
        self.left[:, 2] = self.down[0, :]
        self.down[0, :] = np.flip(self.right[:, 0], axis=0)
        self.right[:, 0] = swip
        if self.shuffled and self.previous != 'F':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'F'

    def B(self):
        """
        Effectue la rotation de la face arrière dans le sens des aiguilles d'une montre.
        """
        self.R_L_F_D(self.back)
        swip = self.up[0, :].copy()
        self.up[0, :] = self.right[:, 2]
        self.right[:, 2] = np.flip(self.down[2, :], axis=0)
        self.down[2, :] = self.left[:, 0]
        self.left[:, 0] = np.flip(swip, axis=0)
        if (self.shuffled) and (self.previous != 'B'):
            self.nb_moves += 1
        if self.shuffled: self.previous = 'B'

    def M(self):
        """
        Effectue la rotation de la tranche du milieu dans le sens des aiguilles d'une montre.
        """
        swip = self.up[:, 1].copy()
        self.up[:, 1] = np.flip(self.back[:, 1], axis=0)
        self.back[:, 1] = np.flip(self.down[:, 1], axis=0)
        self.down[:, 1] = self.front[:, 1]
        self.front[:, 1] = swip
        if self.shuffled and self.previous != 'M':
            self.nb_moves += 1
        if self.shuffled: self.previous = 'M'

    def print_me(self, en_couleur=True):
        """
        Affiche l'état du cube à l'écran. Chaque gommette est représentée
        sous forme d'un espace surligné d'une couleur.
        """
        if en_couleur:
            tab = "print(colored.attr('reset'), '           ', end='')"
            for row in self.up:
                eval(tab)
                for c in row:
                    print(colored.bg(COULEURS["{}".format(c)]), ' ', colored.attr('reset'), end='')
                print()
            print()

            for face in [self.left[0], self.front[0], self.right[0], self.back[0]]:
                for c in face:
                    print(colored.bg(COULEURS["{}".format(c)]), ' ', colored.attr('reset'), end='')
                print('   ', end='')
            print()

            for face in [self.left[1], self.front[1], self.right[1], self.back[1]]:
                for c in face:
                    print(colored.bg(COULEURS["{}".format(c)]), ' ', colored.attr('reset'), end='')
                print('   ', end='')
            print()

            for face in [self.left[2], self.front[2], self.right[2], self.back[2]]:
                for c in face:
                    print(colored.bg(COULEURS["{}".format(c)]), ' ', colored.attr('reset'), end='')
                print('   ', end='')
            print('\n')

            for row in self.down:
                eval(tab)
                for c in row:
                    print(colored.bg(COULEURS["{}".format(c)]), ' ', colored.attr('reset'), end='')
                print()
        else:
            tab = '               '
            print(tab, self.up[0], '\n' + tab, self.up[1], '\n' + tab, self.up[2], '\n')
            print(self.left[0], ' ', self.front[0], ' ', self.right[0], ' ', self.back[0])
            print(self.left[1], ' ', self.front[1], ' ', self.right[1], ' ', self.back[1])
            print(self.left[2], ' ', self.front[2], ' ', self.right[2], ' ', self.back[2], '\n')
            print(tab, self.down[0], '\n' + tab, self.down[1], '\n' + tab, self.down[2])

    def convert_mélange(self, mélange, reversed=False):
        """
        Convertit une chaîne de caractères représentant une séquence de mouvements en une forme standard.
        Permet de traiter les mouvements comme 'R', 'L', 'U', 'D', 'F', 'B', 'M', ainsi que les notations '2' et "'".
        """
        mélange = mélange.replace(" ", "")
        for lettre in LETTRES:
            if not reversed:
                mélange = mélange.replace(lettre + '2', lettre * 2)
                mélange = mélange.replace(lettre + "'", lettre * 3)
            elif reversed:
                mélange = mélange.replace(lettre * 3, lettre + "'")
                mélange = mélange.replace(lettre + lettre, lettre + '2')
        return mélange

    def apply_moves(self, mélange):
        """
        Applique une séquence de mouvements sur le Rubik's Cube en utilisant les méthodes correspondantes.
        La séquence de mouvements est fournie sous forme de chaîne de caractères.
        """
        mélange = self.convert_mélange(mélange)
        for lettre in mélange:
            eval("self." + lettre + "()")

    ##########################
    ######### ARÊTES #########
    ##########################
    def get_target_edge(self, key='', verbose=False):
        """
        Retourne, pour la pièce en position DF, la suite de mouvements nécessaires pour l'amener en UB.
        key : par défaut, la pièce en DF. Si renseigné,
        """
        mapping = {'wg': "M2", 'wo': "RUR'U'", 'wb': "F2", 'wr': "L'U'LU",
                   'gw': "M2", 'ow': "B'RB", 'bw': "bw", 'rw': "BL'B'",
                   'br': "U'L'U", 'bo': "URU'", 'go': "UR'U'", 'gr': "U'LU",
                   'rb': "BL2B'", 'ob': "B'R2B", 'og': "RB'R'B", 'rg': "L'BLB'",
                   'yb': "buffer", 'yo': "UR2U'", 'yg': "D2", 'yr': "U'L2U",
                   'by': "buffer", 'oy': "B'R'B", 'gy': "gy", 'ry': "BLB'"}
        if key == '':
            key = self.down[0][1] + self.front[2][1]
        # Prise en compte de la tranche centrale inversée
        if (key == 'yg') and (self.front[1][1] == 'g'):
            key = 'wb'
            if verbose: print("Cible =", mapping[key])
            return mapping[key]
        if (key == 'gy') and (self.front[1][1] == 'g'):
            key = 'bw'
            if verbose: print("Cible =", mapping[key])
            return mapping[key]
        if (key == 'wb') and (self.front[1][1] == 'g'):
            key = 'yg'
            if verbose: print("Cible =", mapping[key])
            return mapping[key]
        if (key == 'bw') and (self.front[1][1] == 'g'):
            key = 'gy'
            if verbose: print("Cible =", mapping[key])
            return mapping[key]
        if verbose: print("Cible =", mapping[key])
        return mapping[key]

    def tranche_M_inversée(self):
        return self.front[1][1] == 'g'  # True si la tranche M est inversée

    def fix_BU(self):
        moves = 'F2' + "M'U'M'U'M'U'M'U2M'U'M'U'M'U'M'" + 'F2'
        print("Moves =", moves)
        self.apply_moves(moves)

    def get_unsolved_edge(self):
        """
        Le cas où le buffer est résolu mais le cube non complété,
        trouve la prochaine pièce non résolue vers laquelle envoyer le buffer
        """
        # Tranche M en priorité :
        if not self.tranche_M_inversée():
            if (self.up[2][1] != "w") or (self.front[0][1] != "b"):
                return "wb"
            if (self.down[2][1] != "y") or (self.back[2][1] != "g"):
                return "yg"
        else:
            if (self.up[2][1] != "y") or (self.front[0][1] != "g"):
                return "yg"
            if (self.down[2][1] != "w") or (self.back[2][1] != "b"):
                return "wb"
        # Face orange
        for pièce, c in zip([self.right[0][1], self.right[1][2], self.right[2][1], self.right[1][0]],
                            ['w', 'g', 'y', 'b']):
            if pièce != 'o':
                return c + 'o'
        # Face rouge
        for pièce, c in zip([self.left[0][1], self.left[1][2], self.left[2][1], self.left[1][0]], ['w', 'b', 'y', 'g']):
            if pièce != 'r':
                return c + 'r'
        # Face jaune
        for pièce, c in zip([self.down[1][2], self.down[1][0]], ['o', 'r']):
            if pièce != 'y':
                return c + 'y'
        return "fin arêtes"

    def solve_edges(self, verbose=True):

        for i in range(16):
            A = self.get_target_edge(verbose=verbose)
            B = "M2"
            if A == "buffer":  # cas du buffer
                if self.get_unsolved_edge() == "fin arêtes":
                    if self.up[0][1] == 'g':
                        self.fix_BU()
                    if self.tranche_M_inversée():
                        # Gestion de la parité arêtes
                        A = "U'F2U"
                        A_prime = self.inverse_moves(A)
                        moves = (A + ' ' + B + ' ' + A_prime)
                        print("Moves =", moves)
                        self.apply_moves(moves.replace(' ', ''))
                    self.print_me()
                    print("Arêtes terminées !\n")
                    break
                A = self.get_target_edge(key=self.get_unsolved_edge())
                A_prime = self.inverse_moves(A)
                moves = (A + ' ' + B + ' ' + A_prime)
            if A == 'F2':
                moves = "U2M'U2M'"
            elif A == 'D2':
                moves = "MU2MU2"
            elif A == "gy":
                moves = "M2DR'UR'U'M'URU'MRD'"
            elif A == "bw":
                moves = "DM'R'UR'U'MURU'RD'"
            else:
                A_prime = self.inverse_moves(A)
                moves = (A + ' ' + B + ' ' + A_prime)

            print("Moves =", moves)
            self.apply_moves(moves.replace(' ', ''))
            if verbose:
                self.print_me()

    ###########################
    ########## COINS ##########
    ###########################
    def get_unsolved_corner(self):
        # Retourne le prochain coin à résoudre quand le coin actif correspond au buffer
        # Face orange
        for pièce, c in zip([self.right[0][0], self.right[0][2], self.right[2][2], self.right[2][0]],
                            ['wb', 'wg', 'yg', 'yb']):
            if pièce != 'o':
                return 'o' + c
        # Face jaune
        for pièce, c in zip([self.down[0][0], self.down[0][2], self.down[2][2], self.down[2][0]],
                            ['rb', 'bo', 'go', 'gr']):
            if pièce != 'y':
                return 'y' + c
        # Face bleue
        for pièce, c in zip([self.front[0][0], self.front[0][2], self.front[2][2], self.front[2][0]],
                            ['rb', 'bo', 'go', 'gr']):
            if pièce != 'y':
                return 'y' + c

    def get_target_corner(self):
        # Retourne le prochain coin à résoudre
        mapping = {'w': 'u', 'y': 'd', 'o': 'r', 'r': 'l', 'g': 'b', 'b': 'f'}
        key = mapping[self.up[0, 0]] + mapping[self.back[0, 2]] + mapping[self.left[0, 0]]

        setups = {'ubr': '', 'ufl': "F2R2", 'ufr': '',  # face blanche
                  'bdr': "R'", 'bur': "R'", 'bdl': 'D2R',  # face verte
                  'luf': 'F', 'ldf': 'DR', 'lbd': "D2F'",  # face rouge
                  'ful': 'F2R', 'fur': 'R', 'fdr': 'R', 'fdl': "DF'",  # face bleue
                  'dbr': "D'R2", 'dbl': 'D2R2', 'dfl': 'DR2', 'dfr': 'R2',  # face jaune
                  'rub': "R2F'", 'ruf': "R'F'", 'rbd': "D'R", 'rfd': "F'"}  # face orange

        if key in setups:
            setup = setups[key]
        else:
            key = key[0] + key[2] + key[1]
            if key in setups:
                setup = setups[key]
            else:  # cas du buffer
                key = mapping[self.get_unsolved_corner()[0]] + \
                      mapping[self.get_unsolved_corner()[1]] + \
                      mapping[self.get_unsolved_corner()[2]]
                setup = setups[key] if key in setups else setups[key[0] + key[2] + key[1]]

        liste1 = ['ubr', 'ufl', 'bdr', 'fur', 'dbr', 'dbl', 'dfl', 'dfr']
        liste2 = ['urb', 'ulf', 'brd', 'fru', 'drb', 'dlb', 'dlf', 'dfr']
        if (key in liste1) or (key in liste2):
            pll = "UR'L'U2RUR'U2LU'R"
        else:
            pll = "FRU'R'U'RUR'F'RUR'U'R'FRF'"
        return [setup, pll]

    def corners_solved(self):
        # Retourne True si tous les coins sont résolus
        res = all([self.up[0, 0] == 'w', self.up[0, 2] == 'w', self.up[2, 2] == 'w', self.up[2, 0] == 'w'])
        res = res and all(
            [self.left[0, 0] == 'r', self.left[0, 2] == 'r', self.left[2, 2] == 'r', self.left[2, 0] == 'r'])
        res = res and all(
            [self.down[0, 0] == 'y', self.down[0, 2] == 'y', self.down[2, 2] == 'y', self.down[2, 0] == 'y'])
        return res

    def solve_corners(self, verbose=True):
        for i in range(10):
            A, B = self.get_target_corner()[0], self.get_target_corner()[1]
            A_prime = self.inverse_moves(A)
            print("Moves =", A, B, A_prime)
            self.apply_moves(A + B + A_prime)
            if verbose: self.print_me()
            if self.corners_solved():
                print("Cube résolu en %d mouvements !" % self.nb_moves)
                self.print_me()
                break

    def solve(self, verbose=False):
        self.shuffled = True  # permet l'incrémentation du compteur de mouvements
        self.solve_edges(verbose)
        self.solve_corners(verbose)



#Utilisation
B = np.array([['o','g','g'], ['g','g','g'], ['g','g','g']]) # face derrière
D = np.array([['y','y','y'], ['y','y','y'], ['y','y','y']]) # face dessous
F = np.array([['b','b','o'], ['b','b','b'], ['b','b','b']]) # face devant
L = np.array([['r','o','r'], ['r','r','r'], ['r','r','r']]) # face gauche
R = np.array([['g','r','b'], ['o','o','o'], ['o','o','o']]) # face droite
U = np.array([['w','w','w'], ['w','w','w'], ['w','w','w']]) # face dessus

mon_cube = RubiksCube()
mon_cube.set_configuration(back=B, down=D, front=F, left=L, right=R, up=U)
mon_cube.print_me()


mon_cube.solve()

'''Résolution d'un mélange connu'''



mélange = "RUR'U'R'FR2U'R'U'RUR'F'"
mon_cube = RubiksCube()
mon_cube.apply_moves(mélange)
mon_cube.print_me(en_couleur=True)

mon_cube.solve(verbose=False)


