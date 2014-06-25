

OMERO.HPC
=========

This is a HPC implementation of [Weka environment] Fast Random Forest that uses a pre-OMERO.fs OMERO server as the front-end.

System Dependencies
-------------------

  - [OMERO] server
  - [RabbitMQ]
  - [xvfb]
  
Python Dependencies
-------------------

  - [Pika]
  
Sample
------
  - ```sample/images/```: A set of image files that will work with the given classifier
  - ```sample/classifiers/```: Weka .model file with 5 classes

How it works
------------
![alt tag](https://raw.github.com/jjcorreao/OMERO.HPC/master/readme/architecture.png)
OMERO/SCRIPT/JOB/TaskFarmerMQ/TFMQ_Client/ImageJ_JOBS


Installation
------------
  - Stop OMERO.server and OMERO.web

    ```sh
    $OMERO_HOME/bin/omero admin stop
    $OMERO_HOME/bin/omero web stop
    ```

  - Clone repository
  
    ```sh
    cd $OMERO_HOME/lib/scripts
    git clone https://github.com/jjcorreao/OMERO.HPC.git
    ```

  - Install [xvfb]
  
  - Install [Pika]
  
    ```sh
    pip install pika
    ```
  
    or:

    ```sh
    easy_install pika
    ```

  - Install [RabbitMQ]

  - Start OMERO.server and OMERO.web

    ```sh  
    $OMERO_HOME/bin/omero admin start
    $OMERO_HOME/bin/omero web start
    ```

Configuration
-------------

  - Edit ```weka_tfmq.py``` to include ```OMERO_HOME```, ```GSCRATCH```, ```cache_dir``` and path to ```qsub```
  
    ```py
    OMERO_HOME="/usr/local/"
    GSCRATCH = "/global/scratch2/sd/jcorrea"
    cache_dir = "/global/scratch2/sd/jcorrea/ngbi/tmp"
    qsub_path="/usr/syscom/opt/torque/4.2.6/bin/qsub"
    ```

  - Edit ```resources/taskfarmermq/Config.py``` to include your RabbitMQ configuration:

    ```py
    RMQ_HOST = ''
    RMQ_USER = ''
    RMQ_PASS = ''
    RMQ_VHOST = ''
    RMQ_PORT = ''
    ```
    
  - Edit the template generator ```resources/scripts/pbsgen_tfmq.sh``` to include username, system, env, among other
  parameters you may require to successfully execute ```$OMERO_HOME/bin/omero import```
   
    ```sh
    ssh jcorrea@sgn02 'source ~/.bashrc; . /usr/share/Modules/init/bash; source ${OMERO_ENV}; omero import -s sgn02 -d ${dataset} -n ${name} ${outpath}/segmented_map.tif -k ${uuid}'
    ```
  
Acknowledgements
----------------
  - This work was supported by the Laboratory Directed Research and Development Program of Lawrence Berkeley National Laboratory under U.S. Department of Energy Contract No. DE-AC02-05CH11231
  - [Shreyas Cholia]
  - [David Skinner]
  - [Seung-Jin Sul]


[Seung-Jin Sul]:https://github.com/sulsj
[OMERO]:https://www.openmicroscopy.org/
[RabbitMQ]:http://www.rabbitmq.com/
[ImageJ]:http://fiji.sc
[Weka environment]:http://www.cs.waikato.ac.nz/ml/weka/
[TaskFarmerMQ]:https://github.com/jjcorreao/OMERO.HPC/tree/master/resources/taskfarmermq
[xvfb]:http://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml
[Shreyas Cholia]:https://github.com/shreddd
[David Skinner]:https://github.com/deskinner
[Pika]:http://pika.readthedocs.org/en/latest/