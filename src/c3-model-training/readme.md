# Model (vgg16): model training

## Executive Summary on Model Training
Previously, the model has been trained with more image samples, with knowledge distillation for model compression, and TF records for efficient file I/O. It has also been demonstrated how to launch custom job in Vertex AI platform successfully. Detail instructions can be found in the <a href="https://github.com/mleung5/AC215_rehab_image_detection_ai/tree/milestone5#readme">readme of MS5</a>.

In this final milestone, we have attempted to address and provide insights on the following areas:

* Demonstration of the capability of a distillation technique - Online Distillation (aka. Deep Mutual Learning)

* The importance of having quality data as training input. 

* Exploration of various ways to improve accuracy performance, including: pre-trained models (EfficientNet-B0, EfficientNet-B7), and data augmentation.

In conclusion,
we have confirmed the technique of online distillation as published in the original paper, that:
    
    1) No prior powerful teacher model is necessary – mutual learning of a collection of simple student models works.

    2) Student outperforms distillation from a more powerful yet static teacher.

With that, we used the identical architecture of the student models, and applied the online distillation (no teacher) to both the weather dataset and the fixer dataset, as a simple way to benchmark the datasets.
    
    1) For the weather dataset, online distillation improves the accuracy performance from 79% (baseline model) to 93%. 

    2) For the fixer dataset, online distillation is at par with the baseline model (~69%). 

    It further indicates that our fixer dataset may be noisy.


Also, 
   
    1) Data Augmentation is proven helpful and has been incorporated into all model (teacher) trainings.

    2) Both EfficientNet-B0 & EfficientNet-B7 underperform VGG16.


## Table of Contents
1) Online Distillation (Deep Mutual Learning)
2) Results of Online Distillation
    * Weather dataset
    * Fixer dataset
3) Further Enhancement on Online Distillation
4) Data Augmentation Implementation
5) Appendix

    (a) Configuration on Colab Notebook
    * Vertex AI
    * Distillation (teacher-student)
    * Distillation (student-student 2x)
    * Distillation (student-student 10x)
    
    (b) Prepare secrets folder & json file

    (c) Authenticate login to WandB

    (d) Notebooks for developing the python codes


## 1) Online Distillation (Deep Mutual Learning)
Online Distillation has only 2 student models. Both are untrained and are used to distill knowedge to help each other. The advantage is that it does not require any prior training of any teacher model, which is time consuming. The much smaller size of a student model is also preferable to the large model size of a teacher model for inference. The result is surprisingly good.

Original paper by: <b>[Zhang 2018](https://openaccess.thecvf.com/content_cvpr_2018/papers/Zhang_Deep_Mutual_Learning_CVPR_2018_paper.pdf)</b>

Key idea is captured by the diagram below.
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/ff53e423-6f42-46f2-96e1-51295959c75a)



## 2) Results of Online Distillation
### Fixer Dataset

#### <b>Teacher-Student Distillation (result of MS5)</b>
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/6d1f7dd3-6663-4507-861f-ae8099841b6a)
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/6225e0c9-b784-42eb-993e-786b88b125f6)


#### <b>Student-Student Distillation </b>
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/ea553f69-3874-4a53-a865-1c31630a77f0)
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/8106056d-ffda-4185-82d6-b82cc836fd0e)
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/86554f1a-a519-417f-a036-15012b3cb158)

All performance achieved by either distillation methods is just as bad as the baseline. The capability of online distillation is dwarfed by the noisy dataset. Once again Garbage-in; Garbage-out. The importance of data quality is crucial as a good start point to successful training.

### Weather Dataset
This weather dataset comes from the class tutorial (lecture 9 - model compression techniques).

<img width="640" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/65c54944-a73a-4ee5-b14b-068ab6961e45">


<img width="640" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/a3b10dd5-4b9a-469f-abc5-8d864f6ec83c">


#### <b>Teacher-Student Distillation</b>
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/18bdd3c0-c9ef-4dd5-9367-69e81802e065)
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/b8370e65-226a-41b9-b239-07d1902beb3e)

#### <b>Student-Student Distillation</b>
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/7614aac3-4eae-475c-aa86-e01fc736c830)
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/9479683d-ffd8-4e16-bb2b-36bbeb51baa7)

<img width="1329" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/45a7f1ac-667b-4277-86e9-ec79f437c61d">


Without any prior training effort, 2 student models are able to accomplish comparable results (92.4%) as teacher-student distillaion(92.9%). This is great compression technique for fast tiny ML.

## 3) Further Enhancement on Online Distillation
This idea of naive students spawned my curiosity. What if I have more students than only 2. Most likely it should boost performance. But by how much? Hence, the following experiment is resulted.

#### Conceptual Diagram 
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/56885cd2-c968-450c-aecd-7b5f3a2b4f45)

<img width="600" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/6d476ed9-6a2d-43e2-a11f-19667026014e">

#### <b>Student-Student distillation (by 10)</b>
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/a6c8476d-4e56-4b3c-9e83-a3c9f4dccf32)

![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/97ca6110-f967-4151-9e69-fdebbbc62171)

<img width="1317" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/0e7bcde1-14fb-4e92-a88e-ac05f130afeb">


Accuracy performance for 10 students is one percentage point above the 2-student distillation method. And it's even better than the teacher-student distillation method. 

10 students studing together would gain more knowledge than learning from a knowledgeable teacher! Did human learn something from this AI experiment, or vice versa?


## 4) Data Augmentation Implementation
This is an example code from Keras that we borrowed for quick augmentation implementation. It's proven to show immediate improvement on overfitting.

<img width="500" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/8bd00e40-0bd2-48d7-8ca1-7757ea9711c6">

Using the augmentation is rather straight forward.

<img width="600" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/f89bab97-b26c-46a6-b190-088277092b45">


## 5) Appendix
#### (a) Configuration on Colab Notebook
* Vertex AI
<img width="500" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/919bbbc2-c5ae-4dfd-b7f3-131824bd4713">

* Distillation (teacher-student)
<img width="500" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/d33b66a0-5c4d-4c3d-874e-78319bfd6bc2">

* Distillation (student-student 2x)
<img width="500" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/992255af-85f8-4cf1-97f4-477300532ceb">

* Distillation (student-student 10x)
<img width="500" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/2a2fe4bb-c72a-463c-984d-242010bd5c77">

 (same configuratoin as Distillation student-student 2x above)

#### (b) Prepare secrets folder and json file
<img width="417" alt="image" src="https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/ff8d8f11-57f8-4220-93fb-37a7f5957b9b">

#### (c) Authenticate login to WandB
![image](https://github.com/mleung5/AC215_rehab_image_detection_ai/assets/140679896/2ef99baa-324c-420b-b2af-94808183b375)

key for rehab-ai: <b>6c8cXXXXXXXXXXa784</b>

#### (c) Notebooks for developing the python codes:
* [Fixer upper identification (model for MS6)](https://github.com/mleung5/AC215_rehab_image_detection_ai/blob/main/src/c3-model-training/Fixer_upper_identification_(model_for_MS6).ipynb)
<br><br>

* [(ac215 demo) online distillation](https://github.com/mleung5/AC215_rehab_image_detection_ai/blob/main/src/c3-model-training/(ac215_demo)_distillation_online.ipynb)



