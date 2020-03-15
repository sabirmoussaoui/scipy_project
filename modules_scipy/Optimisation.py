import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import io
import urllib, base64
import random

def generateNuage(x):
    list = [1,2,3,4,5,6]
    print("haaaahya random : {}".format(random.choice(list)))
    return 1 / (random.choice(list)) * x ** 3 - 3 / 5 * x ** 2 + 2 + np.random.randn(x.shape[0]) / 20

 # les modéles dyawlna
def f_linear(x, a, b):
    return a * x  + b
def f_quadratic (x, a, b,c):
    return a * x ** 2 + b * x  + c
def f_cubic(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d
def f_logarithmic (x, a, b):
    return a  + b*(np.log(x,where=x > 0))


def convertGraphTimage(fig):
    # convert graph into string buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

class Optimisation():
    def __init__(self):
        #permet d’obtenir un tableau 1D allant d’une valeur de départ à une valeur de fin avec un nombre donné d’éléments.
        self.x = np.linspace(0, 2, 100)
        self.y = generateNuage(self.x)
    
    def show_nuage(self):
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y)
        return convertGraphTimage(fig)

    # Définition d'un modele statistique sensé "coller" au dataset ci-dessus
    def getParam(self):
        params_linear, param_cov = optimize.curve_fit(f_linear, self.x, self.y)
        params_quadratic , param_cov1 = optimize.curve_fit(f_quadratic, self.x, self.y)
        params_cubic , param_cov2 = optimize.curve_fit(f_cubic, self.x, self.y)
        params_logarithmic , param_cov3 = optimize.curve_fit(f_logarithmic, self.x, self.y, maxfev=1000000)

        return (params_linear,params_quadratic,params_cubic,params_logarithmic)
    
    def showResult(self,params_linear,params_quadratic,params_cubic,params_logarithmic):
        fig, ax = plt.subplots()
        ax.scatter(self.x,self.y)
        if params_linear[0]!=False :
           ax.plot(self.x, f_linear(self.x, params_linear[0], params_linear[1]), c='g', lw=3)
        if params_quadratic[0] !=False :
           ax.plot(self.x, f_quadratic(self.x, params_quadratic[0], params_quadratic[1], params_quadratic[2]), c='c', lw=3)
        if params_cubic[0] !=False :
           ax.plot(self.x, f_cubic(self.x, params_cubic[0], params_cubic[1], params_cubic[2], params_cubic[3]), c='r', lw=3)
        if params_logarithmic[0] !=False  :
           ax.plot(self.x, f_logarithmic(self.x, params_logarithmic[0], params_logarithmic[1]), c='y', lw=3)
        return  convertGraphTimage(fig)

""""
def main():
    # Création d'un Dataset avec du bruit "normal"
    opt = Optimisation()
    opt.show_nuage()
    # curve_fit permet de trouver les parametres du modele f grace a la méthode des moindres carrés
    params_linear,params_quadratic,params_cubic,params_logarithmic = opt.getParam()
    print(params_linear)
    print(params_quadratic)
    print(params_cubic)
    print(params_logarithmic)

    # Visualisation des résultats.
    opt.showResult(params_linear,params_quadratic,params_cubic,params_logarithmic)


if __name__ == '__main__':
    main()
"""