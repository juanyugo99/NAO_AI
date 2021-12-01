# NAO_AI

Imitación del movimiento humano en robot humanoide NAO mediante inteligencia artificial, tesis de grado desarrollada por Jeimmy A. Cuitiva y Juan Pablo Guerrero, estudiantes de ingenieria electrónica en la Pontificia Universidad javeriana, Bogota-Colombia.

------------------------------

![Demo de proyecto](https://www.youtube.com/watch?v=o3aseUNGSXI)
 
 
## Proceso de reproducción 

Se recomienda correr los codigos necesarios en un sistema operativo Linux, Ubuntu 14.04

1. Configuración inicial de NAO. guía: http://doc.aldebaran.com/2-1/nao/nao-connecting.html

2. Instalación de softwares y paquetes necesarios para controlar a NAO
    * ROS Indigo: http://wiki.ros.org/indigo/Installation/Ubuntu  
    * Configuración del entorno para ROS :  http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
    * Paquetes para NAO en ROS : sudo apt-get install ros-indigo-nao-robot
    * Naoqi para el PC : 
       * antiguo sdk: https://www.softbankrobotics.com/emea/en/support/nao-6/downloads-softwares/former-versions?os=49&category=76
       * Tutorial : http://wiki.ros.org/nao/Tutorials/Installation
       * Probar la conexión con el robot: http://wiki.ros.org/nao_bringup
    * Naoqi para robot Nao (En caso de que el SO del robot deba ser actualizado) : Se encuentra en https://drive.google.com/drive/folders/1Z8o0tsE_2d0TbEYgxMoSdvvrxMmHCwuD (opennao-atom-system-image-2.1.4.13_2015-08-27)
    
    
3. Predicción de los ángulos 
    * Se debe crear un conda environment, clonar el repositorio e instalar las dependencias, para esto se deben correr los siguientes comandos desde la terminal: 
        ```shell
        conda create -n naoai python=3.6 -y
        conda activate naoai
        git clone https://github.com/juanyugo99/NAO_AI.git
        pip install -r requirtments.txt 
        ```
   
    * Para hacer la predicción de los ángulos se debe correr el codigo llamado mediapipe_keypoints.py, para correrlo se deben tener en cuenta las banderas explicadas a continuación:
        ```shell
        python mediapipe_keypoints.py -m mode: mode corresponde detección usando la cámara web, video o imagen o rep si se desea reproducir un json que contenga el movimiento
                                      -in_dir input_direction : dirección o fuente del archivo que se desea pasar al algoritmo  
                                      -out_dir output_direction : donde se desea guardar la predicción realizada
                                      -sk skip : skip corresponde al número de frames que se desean saltar en el video de detección
                                      -save_img save_image : si se desea guardar las imagenes 
                                      -save_json save_json : si se desea guardar el json que contiene los angulos predichos por el algoritmo
                                      -vel velocity : el tiempo de espera entre frames enviados al robot para los modos de imagen o rep
        ```
   * Ejemplo para correr el algoritmo por defecto: ``` python mediapipe_keypoints.py -m camera -in_dir 0 -sk 10```
        
  
4. Control de NAO 
     * Para controlar a Nao se debe correr el codigo nao_imitation.py en otra terminal, es necesario que tanto el computador, como el robot estén conectados a la misma red wifi. Se debe revisar la dirección IP del robot NAO y verificar que sea la misma dirección que se encuentra en el código, la IP del robot se encuentra en la linea 239.
     
     ```shell
     python2 nao_imitation.py
     ```
 

