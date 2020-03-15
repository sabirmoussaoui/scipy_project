import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import io
import urllib, base64

# Définition d'une fonction a 1 Dimension
def f (x):
    return x**2 + 5*np.sin(x)
def convertGraphTimage(fig):
    # convert graph into string buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
class Minimisation():
    def __init__(self,debut,nbv,final,initial):
        self.x = np.linspace(debut,nbv,final)
        self.x0 = initial

    def show_Model(self):
        fig, ax = plt.subplots()
        ax.plot(self.x, f(self.x))
        return convertGraphTimage(fig)

    def getResult(self):
        # Définition d'un point x0 pour l'algorithme de minimisation
        result = optimize.minimize(f, x0=self.x0).x  # résultat de la minimisation
        return  result

    # Visualisation du résultat
    def showResult(self,result):
        fig, ax = plt.subplots()
        ax.plot(self.x, f(self.x), lw=3, zorder=-1)  # Courbe de la fonction
        ax.scatter(self.x0, f(self.x0), s=200, marker='+', c='g', zorder=1, label='initial')  # point initial
        ax.scatter(result, f(result), s=100, c='r', zorder=1, label='final')  # point final
        ax.legend()
        return convertGraphTimage(fig)


def main():
    """*****************************************Minimisation*****************************************"""

    print("******************** Creation de la fonction suivant (f(x) = x**2 + 5*sin(x)")
    min = Minimisation()
    # Visualisation de la fonction
    print("******************** Visualisation de la fonction f(x)")
    min.show_Model()
    # Définition d'un point x0 pour l'algorithme de minimisation et faire la minimisation
    plt.close()
    print("******************** Définition d'un point x0 pour l'algorithme de minimisation et faire la minimisation")
    result = min.getResult()
    # Visualisation du résultatzd
    print("******************** Visualisation du résultat")
    min.showResult(result)
    plt.close(2)




if __name__ == '__main__':
     main()






