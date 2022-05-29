# Attendance Marking System Using Face Recognition

This project is to make a attendance marking system using face recognition by native desktop application.
In this project, the images are added to a particular directory and the faces are detected in the images and and encodings are obtained using face recognition library.

To find faces in an image, we’ll start by making our image black and white because we don’t need color data to find faces:


Then we’ll look at every single pixel in our image one at a time. For every single pixel, we want to look at the pixels that directly surrounding it:


Our goal is to figure out how dark the current pixel is compared to the pixels directly surrounding it. Then we want to draw an arrow showing in which direction the image is getting darker:


Looking at just this one pixel and the pixels touching it, the image is getting darker towards the upper right.
If you repeat that process for every single pixel in the image, you end up with every pixel being replaced by an arrow. These arrows are called gradients and they show the flow from light to dark across the entire image:


This might seem like a random thing to do, but there’s a really good reason for replacing the pixels with gradients. If we analyze pixels directly, really dark images and really light images of the same person will have totally different pixel values. But by only considering the direction that brightness changes, both really dark images and really bright images will end up with the same exact representation. That makes the problem a lot easier to solve!

But saving the gradient for every single pixel gives us way too much detail. We end up missing the forest for the trees. It would be better if we could just see the basic flow of lightness/darkness at a higher level so we could see the basic pattern of the image.

To do this, we’ll break up the image into small squares of 16x16 pixels each. In each square, we’ll count up how many gradients point in each major direction (how many point up, point up-right, point right, etc…). Then we’ll replace that square in the image with the arrow directions that were the strongest.

The end result is we turn the original image into a very simple representation that captures the basic structure of a face in a simple way:


The original image is turned into a HOG representation that captures the major features of the image regardless of image brightnesss.
To find faces in this HOG image, all we have to do is find the part of our image that looks the most similar to a known HOG pattern that was extracted from a bunch of other training faces:


Using this technique, we can now easily find faces in any image:


If you want to try this step out yourself using Python and dlib, we can  generate and view HOG representations of images. 

now, the current image is obtained using webcam and its face encodings are obtained and these encodings are compared with encodings of preloaded images and index of best match will be found

The name of best match will be therein added to a .csv file along with present date and time and now we can take the list of attendance from .csv file 
## Optimizations

1)A bar for the time limit upto which the attendances are accepted can be setup so that the system won't allow late markings. 
## Tech Stack

 HTML, CSS , PYTHON

**Server:** flask framework


## Appendix

Any additional information goes here

for further reading:
https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
## Run Locally

Clone the project

```bash
  git clone https://github.com/dinesh-webdesign/attendance-marking-system
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```


## Please Note

1) The title of the image to be uploaded should be the name of the student itself

