Requerimientos:
- Python 2.7
	* scipy (1.9.0)
	* scikit-learn (0.16.1)
	* numpy (1.9.2)
- OpenCV 2.4.10

Instrucciones:
1) Calcular descriptores locales.

$ python CalcSift <folder> <out_folder>

<folder> : Carpeta desde la cual se obtendrán las imágenes
<out_folder> : Carpeta en la cual se guardarán los descriptores

2) Generar BOVW:

$ python BOVWcalculator.py <number_of_clusters> <out_folder> <descriptors_folder_1> <class_name1> [<descriptors_folder_2> <class_name_2> ...]

<number_of_clusters> : Número de clusters o palabras visuales que se generarán
<out_folder> : Carpeta en la cual se guardarán las palabras visuales
<descriptors_folder_X> : Carpeta desde la cual se leerán descriptores de una clase determinada
<class_nameX> : Nombre de la clase para la carpeta X

3) Clasificar un conjunto de imágenes

$ python Classifier.py <kernel_args> <bovw_folder> <img_folder1> <class_name1> [<img_folder2> <class_name2>...]
<kernel_args> : Tipo de kernel para el SVM.
	Puede ser:
		linear : Se usa un kernel lineal
		rbf_<gamma>_<c> : Se usa un kernel rbf con parámetros gamma y c
<bovw_folder> : Carpeta donde se encuentran las palabras visuales
<img_folderX> : Carpeta que contiene imágenes de consulta de una clase determinada
<class_nameX> : Nombre de la clase de las imágenes de la carpeta X.



ADICIONALES:
Imprimir matriz de confusión.
	El script Classifier genera sus resultados en el par de archivos results y results.vindex.npy y son sobreescritos al realizarse otras clasificaciones.
	
	$ python ConfusionMatrix <results_file> <file_out>
	
	<results_file> : Archivo de resultados de clasificación (típicamente 'results')