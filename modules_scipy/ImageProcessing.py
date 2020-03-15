from scipy import ndimage
import numpy as np
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
class ImageProcessing():
    def __init__(self, chemin_img):
        self.chemin_img = chemin_img

    def importer_img(self):
        image = plt.imread(self.chemin_img)
        image = image[:, :, 0]  # réduire l'image en 2D
        fig, ax = plt.subplots()
        ax.imshow(image, cmap='gray')  # afficher l'image
        print("l'importation est terminée")
        return (convertGraphTimage(fig),image)

    def copy_img_cree_hist(self, image_2D):
        image_2 = np.copy(image_2D)
        fig, ax = plt.subplots()
        ax.hist(image_2.ravel(), bins=255)
        return (convertGraphTimage(fig))

    def cree_image_binaire(self, image_2D):
        #L’histogramme d’une image est une fonction discrète. Elle représente le nombre de pixels en fonction du niveau de gris.
        image_binaire = image_2D <0.6
        fig, ax = plt.subplots()
        ax.imshow(image_binaire)
        return (convertGraphTimage(fig),image_binaire)

    def enlever_artefacts(self, image_binaire):
        open_image = ndimage.binary_opening(image_binaire)
        fig, ax = plt.subplots()
        ax.imshow(open_image)
        return (convertGraphTimage(fig),open_image)

    def segmenter_image(self, open_image):
        label_image, n_labels = ndimage.label(open_image)
        print(f'###################   il y a {n_labels} groupes   ###################')
        return (label_image, n_labels)

    def show_image_etiquete(self, label_image):
        fig, ax = plt.subplots()
        ax.imshow(label_image)
        return convertGraphTimage(fig)

    def mesurer_taille(self, open_image, label_image, n_labels):
        sizes = ndimage.sum(open_image, label_image, range(n_labels))
        print(type(sizes))
        return sizes

    def show_result(self, sizes, n_labels):
        # Visualisation des résultats
        fig, ax = plt.subplots()
        ax.scatter(range(n_labels), sizes)
        plt.xlabel('bactérie ID')
        plt.ylabel('taille relative')
        return convertGraphTimage(fig)

# def main():
#
#     """*******************************************Image Processing***************************************"""
#     # importer l'image avec pyplot
#     print("********************importer l'image avec pyplot********************")
#     chemain = input("====> Entrer le chemin de l'image : ")
#     imgp = ImageProcessing(chemain)
#     image_2D = imgp.importer_img()
#     plt.close()
#     print("******************** Plot closed")
#     # copy de l'image, puis création d'un histogramme
#     print("********************copy de l'image, puis création d'un histogramme")
#     imgp.copy_img_cree_hist(image_2D)
#     plt.close()
#     print("********************Plot closed")
#     # boolean indexing: création d'une image binaire
#     print("********************création d'une image binaire")
#     image_binaire = imgp.cree_image_binaire(image_2D)
#     plt.close()
#     print("********************Plot closed")
#     # morphologie utilisée pour enlever les artefacts
#     print("********************enlever les artefacts")
#     open_image = imgp.enlever_artefacts(image_binaire)
#     plt.close()
#     print("********************Plot closed")
#     # Segmentation de l'image: label_image contient les différents labels et n_labels est le nombre de labels
#     print("********************Segmentation de l'image")
#     label_image, n_label = imgp.segmenter_image(open_image)
#     # Visualisation de l'image étiquetée
#     print("********************Visualisation de l'image étiquetée")
#     imgp.show_image_etiquete(label_image)
#     plt.close()
#     print("********************Plot closed")
#     # Mesure de la taille de chaque groupes de label_images (fait la somme des pixels)
#     print("******************** Mesure de la taille de chaque groupes de label_images (fait la somme des pixels)")
#     sizes = imgp.mesurer_taille(open_image, label_image, n_label)
#     print(sizes)
#     print("********************Visualisation des résultats")
#     # Visualisation des résultats
#     imgp.show_result(sizes, n_label)
#     plt.close()
#
#     """*******************************************Finished***************************************"""
#
#
#
#
#
# if __name__ == '__main__':
#     main()
