# AlgoritmoTorres
Scripts gráficos y no gráficos.

En ambos archivos se describe el algoritmo de simulación.
En grafico.py se con ayuda de Matplotlib de aprecia gráficamente el performance de los nodos, mientras que en script.py unicamente se despliegan las instrucciones necesarias en consola.
Dado que se trata de proyectos son salidas diferentes, se requieren dos ambientes virtuales diferentes, los mismos que están descritos en los archivos .yml correspondientes a cada script.

Para desplegar un ambiente virtual a partir de su correspondiente .yml se utiliza el siguiente comando:

conda env create --file name.yml

Para los casos serán:

conda env create --file enviroment_grafico.yml 
conda env create --file enviroment_script.yml

Cada archivo .py solo podrá ser compilado en su respectivo ambiente virtual. Dicho de paso, es necesario Anaconda3 para poder trabajar con ambientes virtuales.
