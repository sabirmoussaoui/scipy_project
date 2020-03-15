from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from modules_scipy.ImageProcessing import ImageProcessing
from modules_scipy.Minimisation import Minimisation
from modules_scipy.Optimisation import Optimisation
from modules_scipy.Signal import Signal

#l'initialisation de l'objet 
opt = Optimisation()  # Création d'un Dataset avec du bruit "normal"
min = Minimisation(-20,10,100,-6)
sgn = Signal()

#page d'accueil
def index(request):
    return render(request, 'index.html')

#ProcessingImage
def processingImg(request):
    return render(request, 'processingImage/index.html')
def getProcessingImage(request):
    myfile = request.FILES['myfile']
    path_img = "modules_scipy/image/"+str(myfile)
    imgp = ImageProcessing(path_img)
    # importer l'image avec pyplot
    fig_image, image_2D = imgp.importer_img()
    # copy de l'image, puis création d'un histogramme
    fig_histogramme = imgp.copy_img_cree_hist(image_2D)
    # boolean indexing: création d'une image binaire
    fig_image_binaire,image_binaire = imgp.cree_image_binaire(image_2D)
    # morphologie utilisée pour enlever les artefacts
    fig_enlever_artefacts,image_enlever_artefacts = imgp.enlever_artefacts(image_binaire)
    # Segmentation de l'image: label_image contient les différents labels et n_labels est le nombre de labels
    label_image, n_label = imgp.segmenter_image(image_enlever_artefacts)
    # Visualisation de l'image étiquetée
    fig_image_etiquete =imgp.show_image_etiquete(label_image)
    # Mesure de la taille de chaque groupes de label_images (fait la somme des pixels)
    sizes = imgp.mesurer_taille(image_enlever_artefacts, label_image, n_label)
    # Visualisation des résultats
    fig_result=imgp.show_result(sizes, n_label)
    return render(request, 'processingImage/figure.html',
                  {'figure_image': fig_image,
                   'fig_histogramme': fig_histogramme,
                   'fig_image_binaire': fig_image_binaire,
                   'fig_enlever_artefacts': fig_enlever_artefacts,
                   'n_label': n_label,
                   'fig_image_etiquete': fig_image_etiquete,
                   'fig_result': fig_result})





#Optimisation
def showNuage(request):
    # Visualisation le nuage
    fig_nuage =opt.show_nuage()
    return render(request,'Optimisation/index.html',{'fig_nuage':fig_nuage})
def getModel(request):
    #getParam() permet de trouver les parametres du modele f grace a la méthode des moindres carrés
    params_linear, params_quadratic, params_cubic, params_logarithmic = opt.getParam()
    pl=params_linear
    pq=params_quadratic
    pc=params_cubic
    plo=params_logarithmic
    if request.method == 'POST':
        listmodeles = request.POST.getlist('modele')
        if '1' not in listmodeles:
            pl = [False]
        if '2' not in listmodeles:
            pq = [False]
        if '3' not in listmodeles:
            pc = [False]
        if '4' not in listmodeles:
            plo = [False]
    # Visualisation des résultats.
    fig_nuage_modele =opt.showResult(pl,pq,pc,plo)
    return render(request,'Optimisation/figure.html',{
        'fig_nuage_modele':fig_nuage_modele,
        'params_linear':params_linear,
        'params_quadratic':params_quadratic,
        'params_cubic':params_cubic,
        'params_logarithmic':params_logarithmic,
                                                     })

#Minimisation
def showCurve(request):
    # Visualisation de la fonction
    fig_curve = min.show_Model()
    return  render(request,'Minimisation/index.html',{'fig_curve':fig_curve})
def getMinimumValue(request):
        if request.method == 'POST':
            data_form = request.POST.dict()
            initial = data_form.get("Initial")
            debut   = data_form.get("Debut")
            final   = data_form.get("Final")
            if len(initial)==0 and len(debut)==0 and len(final)==0 :
                # résultat de la minimisation

                minimum_value = min.getResult()                 #Default(S'ils sont vides)
                fig_result_minimisation = min.showResult(minimum_value)
            else:
                if len(initial)==0:
                                 initial = -15 
                if len(debut)==0:
                                 debut = -20
                if len(final)==0:
                                 final = 100
                min1 = Minimisation(int(debut),10,int(final),int(initial))
                minimum_value = min1.getResult() # return la valeur minimum
                # résultat de la minimisation
                fig_result_minimisation  = min1.showResult(minimum_value)

        return render(request, 'Minimisation/figure.html',{
                                                       'minimum_value': minimum_value,
                                                       'fig_result_minimisation': fig_result_minimisation })
                                                       
#Signal
def getSignalTrend(request):
    # Création d'un Dataset avec une tendance linéaire
    sgn = Signal()
    fig_segnal_trend = sgn.showSignalOriginal()
    return render(request, 'Signal/index.html',{'fig_signal_trend': fig_segnal_trend })

def getSignalDetrend(request):
    # Élimination de la tendance linéaire
    new_signal = sgn.elimninerTendance()
    # Visualisation des résultats*
    fig_signal_detrend = sgn.showAllSignal(new_signal)
    return render(request, 'Signal/figure.html',{'fig_signal_detrend': fig_signal_detrend})





    

