# NAO_AI

Imitación del movimiento humano en robot humanoide NAO mediante inteligencia artificial, tesis de grado desarrollada por Jeimmy A. Cuitiva y Juan Pablo Guerrero, estudiantes de ingenieria electrónica en la Pontificia Universidad javeriana, Bogota-Colombia.

------------------------------
 
Se recomienda correr los codigos necesarios en un sistema operativo Linux, Ubuntu 14.04
1. Instalación de paquetes necesarios para controlar a NAO
   * En  simulación :
      * ROS Indigo: http://wiki.ros.org/indigo/Installation/Ubuntu
      * NAO_DESCRIPTION :  
    
    * Para el robot físico: 
      * Naoqi para Nao (Versión actualizada) : Este corresponde al archivo llamado "opennao-atom-system-image-2.1.4.13_2015-08-27"
      * Naoqi para el PC : 
                          * antiguo sdk: https://www.softbankrobotics.com/emea/en/support/nao-6/downloads-softwares/former-versions?os=49&category=76
                          * Tutorial : http://wiki.ros.org/nao/Tutorials/Installation
                          * Probar la conexión con el robot: http://wiki.ros.org/nao_bringup
                          
2. Predicción de los ángulos 
    * Se debe crear un conda environment y una vez creado, se debe correr el siguiente comandos desde la terminal: 
        * pip install -r requirtments.txt 
    
    * Archivos para la red de predicción de angulos (deben de estar en la misma carpeta donde se encuentra el archivo .py
        * checkpoint.pth
        * x_scaler.pkl
   
    * Para hacer la predicción de los ángulos se debe correr el codigo llamado mediapipe_keypoints.py, para correrlo se deben tener en cuenta las banderas explicadas a continuación
        *  python mediapipe_keypoints.py -m mode: mode corresponde detección usando la cámara web, video o imagen 
        *  python mediapipe_keypoints.py -in_dir input_direction : dirección o fuente del archivo que se desea pasar al algoritmo  
        *  python mediapipe_keypoints.py -out_dir output_direction : donde se desea guardar la predicción realizada
        *  python mediapipe_keypoints.py -sk skip : skip corresponde al número de frames que se desean saltar en el video de detección
        *  python mediapipe_keypoints.py -save_img save_image : si se desea guardar las imagenes 
        *  python mediapipe_keypoints.py -save_json save_json : si se desea guardar el json que contiene los angulos predichos por el algoritmo
  
3. Control de NAO 
     * Para controlar a nao se debe correr el codigo nao_imitation.py, es necesario que tanto el computador, como el robot estén conectados a la misma red wifi, adicionalmente, se debe revisar la dirección IP del robot NAO y verificar que sea la misma dirección que se encuentra en el código. 
