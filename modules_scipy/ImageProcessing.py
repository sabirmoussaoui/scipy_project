from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import io
import urllib, base64

def convertGraphToimage(fig):
    # convert graph into string buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

class ImageProcessing():
    def __init__(self, chemin_img):
        self.chemin_img = chemin_img
      
    def importer_img(self):
        # importer l'image avec pyplot
        image = plt.imread(self.chemin_img)
        image = image[:, :, 0]  # réduire l'image en 2D
        fig, ax = plt.subplots()
        ax.imshow(image, cmap='gray')  # afficher l'image
        print("l'importation est terminée")
        return (convertGraphToimage(fig),image)

    def copy_img_cree_hist(self, image_2D):
        # copy de l'image, puis création d'un histogramme
        image_2 = np.copy(image_2D)
        fig, ax = plt.subplots()
        #L’histogramme d’une image est une fonction discrète. Elle représente le nombre de pixels en fonction du niveau de gris.
        ax.hist(image_2.ravel(), bins=255)
        return (convertGraphToimage(fig))

    def cree_image_binaire(self, image_2D):
        # boolean indexing: création d'une image binaire
        image_binaire = image_2D <0.6
        fig, ax = plt.subplots()
        ax.imshow(image_binaire)
        return (convertGraphToimage(fig),image_binaire)

    def enlever_artefacts(self, image_binaire):
        # morphologie utilisée pour enlever les artefacts
        open_image = ndimage.binary_opening(image_binaire)
        fig, ax = plt.subplots()
        ax.imshow(open_image)
        return (convertGraphToimage(fig),open_image)

    def segmenter_image(self, open_image):
        # Segmentation de l'image: label_image contient les différents labels et n_labels est le nombre de labels
        label_image, n_labels = ndimage.label(open_image)
        return (label_image, n_labels)

    def show_image_etiquete(self, label_image):
        # Visualisation de l'image étiquetée
        fig, ax = plt.subplots()
        ax.imshow(label_image)
        return convertGraphToimage(fig)

    def mesurer_taille(self, open_image, label_image, n_labels):
        # Mesure de la taille de chaque groupes de label_images (fait la somme des pixels)
        sizes = ndimage.sum(open_image, label_image, range(n_labels))
        print(type(sizes))
        return sizes

    def show_result(self, sizes, n_labels):
        # Visualisation des résultats
        fig, ax = plt.subplots()
        ax.scatter(range(n_labels), sizes)
        plt.xlabel('bactérie ID')
        plt.ylabel('taille relative')
        return convertGraphToimage(fig)
