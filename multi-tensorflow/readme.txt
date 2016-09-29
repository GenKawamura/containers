## Generating TensorFlow cluster
## http://www.intellilink.co.jp/article/column/bigdata-tf01.html

## Making TensorFlow 0.8.0 Container
 $ docker pull gcr.io/tensorflow/tensorflow:0.8.0

## Make a workarea
 $ mkdir workarea

## Run parameter server
 $ docker run -it --name tf_paramserver --rm --cpuset-cpus 0 -h tf_paramserver -w /root -v $PWD/workarea:/root gcr.io/tensorflow/tensorflow:0.8.0 /bin/bash

## Run worker_1 server
 $ docker run -it --name tf_worker_1 --rm --cpuset-cpus 1 -h tf_worker_1 -w /root -v $PWD/workarea:/root gcr.io/tensorflow/tensorflow:0.8.0 /bin/bash

## Run worker_2 server
 $ docker run -it --name tf_worker_2 --rm --cpuset-cpus 2 -h tf_worker_2 -w /root -v $PWD/workarea:/root gcr.io/tensorflow/tensorflow:0.8.0 /bin/bash


## Run docker paramter server 
 $ docker exec -it tf_paramserver /bin/bash
 [in docker container]$ cp /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/cifar10/cifar10_multi_gpu_train.py .

cifar10_standalone_train.patch
------------------------------------------------------------------------
--- cifar10_multi_gpu_train.py  2016-04-13 00:00:00.000000000 +0000
+++ cifar10_standalone_train.py    2016-04-13 00:00:00.000000000 +0000
@@ -54,7 +54,7 @@ FLAGS = tf.app.flags.FLAGS
 tf.app.flags.DEFINE_string('train_dir', '/tmp/cifar10_train',
                            """Directory where to write event logs """
                            """and checkpoint.""")
-tf.app.flags.DEFINE_integer('max_steps', 1000000,
+tf.app.flags.DEFINE_integer('max_steps', 1000,
                             """Number of batches to run.""")
 tf.app.flags.DEFINE_integer('num_gpus', 1,
                             """How many GPUs to use.""")
------------------------------------------------------------------------


cifar10_cluster_train.patch
------------------------------------------------------------------------
--- cifar10_multi_gpu_train.py  2016-04-13 00:00:00.000000000 +0000
+++ cifar10_cluster_train.py    2016-04-13 00:00:00.000000000 +0000
@@ -49,14 +49,16 @@ from six.moves import xrange  # pylint:
 import tensorflow as tf
 from tensorflow.models.image.cifar10 import cifar10
 
+PS_NODE = "<IP of Paramter server>"
+
 FLAGS = tf.app.flags.FLAGS
 
 tf.app.flags.DEFINE_string('train_dir', '/tmp/cifar10_train',
                            """Directory where to write event logs """
                            """and checkpoint.""")
-tf.app.flags.DEFINE_integer('max_steps', 1000000,
+tf.app.flags.DEFINE_integer('max_steps', 1000,
                             """Number of batches to run.""")
-tf.app.flags.DEFINE_integer('num_gpus', 1,
+tf.app.flags.DEFINE_integer('num_workers', 2,
                             """How many GPUs to use.""")
 tf.app.flags.DEFINE_boolean('log_device_placement', False,
                             """Whether to log device placement.""")
@@ -147,7 +149,7 @@ def average_gradients(tower_grads):
 
 def train():
   """Train CIFAR-10 for a number of steps."""
-  with tf.Graph().as_default(), tf.device('/cpu:0'):
+  with tf.Graph().as_default(), tf.device('/job:ps/task:0/cpu:0'):
     # Create a variable to count the number of train() calls. This equals the
     # number of batches processed * FLAGS.num_gpus.
     global_step = tf.get_variable(
@@ -171,8 +173,8 @@ def train():
 
     # Calculate the gradients for each model tower.
     tower_grads = [] 
-    for i in xrange(FLAGS.num_gpus):
-      with tf.device('/gpu:%d' % i):
+    for i in xrange(FLAGS.num_workers):
+      with tf.device('/job:worker/task:%d/cpu:0' % i):
         with tf.name_scope('%s_%d' % (cifar10.TOWER_NAME, i)) as scope:
           # Calculate the loss for one tower of the CIFAR model. This function
           # constructs the entire CIFAR model but shares the variables across
@@ -231,9 +233,7 @@ def train():
     # Start running operations on the Graph. allow_soft_placement must be set to
     # True to build towers on GPU, as some of the ops do not have GPU
     # implementations.
-    sess = tf.Session(config=tf.ConfigProto(
-        allow_soft_placement=True,
-        log_device_placement=FLAGS.log_device_placement))
+    sess = tf.Session("grpc://%s:2222" % PS_NODE)
     sess.run(init)
 
     # Start the queue runners.
@@ -249,9 +249,9 @@ def train():
       assert not np.isnan(loss_value), 'Model diverged with loss = NaN'
 
       if step % 10 == 0:
-        num_examples_per_step = FLAGS.batch_size * FLAGS.num_gpus
+        num_examples_per_step = FLAGS.batch_size * FLAGS.num_workers
         examples_per_sec = num_examples_per_step / duration
-        sec_per_batch = duration / FLAGS.num_gpus
+        sec_per_batch = duration / FLAGS.num_workers
 
         format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                       'sec/batch)')
------------------------------------------------------------------------


#--------------------------------------------
# Patching files
#--------------------------------------------
root@tf_paramserver:/notebooks# cp ./cifar10_multi_gpu_train.py ./cifar10_standalone_train.py
root@tf_paramserver:/notebooks# cp ./cifar10_multi_gpu_train.py ./cifar10_cluster_train.py
root@tf_paramserver:/notebooks# patch ./cifar10_standalone_train.py ./cifar10_standalone_train.patch
patching file cifar10_standalone_train.py
root@tf_paramserver:/notebooks# patch ./cifar10_cluster_train.py ./cifar10_cluster_train.patch
patching file cifar10_cluster_train.py



#--------------------------------------------
# Instances
#--------------------------------------------

## For parameter server instance
# The follwoing python code will be inputted in interactive python shell
import tensorflow as tf
 
cluster = tf.train.ClusterSpec({
    "ps": [
        "<Paramter server IP>:2222"
    ],
    "worker": [
        "<ワーカー・ホスト1のIP>:2222",
        "<ワーカー・ホスト2のIP>:2222"
    ]})
server = tf.train.Server(cluster, job_name="ps", task_index=0)


## For TF1
import tensorflow as tf    # 以下は起動したPythonのインタラクティブシェル上で実行
 
cluster = tf.train.ClusterSpec({
    "ps": [
        "<パラメーター・サーバーのIP>:2222"
    ],
    "worker": [
        "<ワーカー・ホスト1のIP>:2222",
        "<ワーカー・ホスト2のIP>:2222"
    ]})
server = tf.train.Server(cluster, job_name="worker", task_index=0)


## For TF2
import tensorflow as tf    # 以下は起動したPythonのインタラクティブシェル上で実行
 
cluster = tf.train.ClusterSpec({
    "ps": [
        "<パラメーター・サーバーのIP>:2222"
    ],
    "worker": [
        "<ワーカー・ホスト1のIP>:2222",
        "<ワーカー・ホスト2のIP>:2222"
    ]})
server = tf.train.Server(cluster, job_name="worker", task_index=1)


## In paramter server
root@tf_paramserver:/notebooks# python cifar10_cluster_train.py

