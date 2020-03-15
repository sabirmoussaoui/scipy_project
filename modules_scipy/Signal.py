import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import io
import urllib, base64
def convertGraphTimage(fig):
    # convert graph into string buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

class Signal:
    def __init__(self):
        # Création d'un Dataset avec une tendance linéaire
        self.x = np.linspace(0, 20, 100)
        self.y = self.x + 2 * np.sin(self.x) + np.random.randn(self.x.shape[0])

    def showSignalOriginal(self):
        fig, ax = plt.subplots()
        ax.plot(self.x,self.y)
        return convertGraphTimage(fig)

    def elimninerTendance(self):
         # Élimination de la tendance linéaire
         detrend_signal = signal.detrend(self.y)
         return detrend_signal
    def showAllSignal(self,detrend_signal):
         # Visualisation des résultats*
         fig, ax = plt.subplots()
         ax.plot(self.x, self.y, label='Original')
         ax.plot(self.x, detrend_signal, label='Detrend')
         ax.legend()
         return convertGraphTimage(fig)



def main():

    """*****************************************Traitement de Signal*****************************************"""


    print("Générer un signal aléatoire avec une tendance")
    # Création d'un Dataset avec une tendance linéaire
    sgn = Signal()
    print("Visualisation du signal ")
    sgn.showSignalOriginal()
    plt.close()
    print("Élimination de la tendance linéaire")
    new_signal = sgn.elimninerTendance()
    sgn.showAllSignal(new_signal)
    plt.close()

if __name__ == '__main__':
          main()
