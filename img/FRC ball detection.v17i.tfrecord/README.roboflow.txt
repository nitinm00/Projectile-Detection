
FRC ball detection - v17 2022-02-08 6:35pm
==============================

This dataset was exported via roboflow.com on September 4, 2022 at 10:24 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

It includes 5287 images.
Balls are annotated in Tensorflow TFRecord (raccoon) format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x360 (Fit (reflect edges))

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Random brigthness adjustment of between -20 and +20 percent
* Salt and pepper noise was applied to 1 percent of pixels


