# Thesis

### Datasets
The datasets used in this program are the following:

| Name                 | Description                                                                                | Source                                                           |
|----------------------|--------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| DBNL                 | Containing 220 books                                                                       | https://lab.kb.nl/dataset/dbnl-ocr-data-set                      |
| Historical Newspaper | 2000 pages of ground-truth data of newspapers                                              | https://lab.kb.nl/dataset/historical-newspapers-ocr-ground-truth |
| IMPACT project       | 2055 book pages, 1024 newspaper pages, 1179 parliamentary proceedings, 205 radio bulletins | https://lab.kb.nl/dataset/ground-truth-impact-project            |
| 17th_century         | Around 30000, 17th century articles                                                        |                                                                  |
| Bible                | The 'Statenvertaling' bible from 1637                                                      |                                                                  |

### Overview of folders

## data_loader
This folder contains all code needed to import the various data sources mentioned in the table above.

## ImageProcessing
This folder contains all code related to the image creation process. This includes creating the building blocks, and using the building blocks for creating the images with text.

## utils
Includes a delpher class, used for extracting information from Delpher. The settings class contains application global parameters. Util class contains global functions used throughout the application. 

### Overview of classes in src folder

## Analyze.py and AnalyzeIndividual.py
Not important, purely used for creating my thesis report.

## DataCreator.py
Probably on of the most important classes. Used to create images, and run those images through an OCR application using OCR.py. This class is called from create_training_dataset.py.

## create_training_dataset.py
Used to call Datacreator.py

## finetune_trainer.py
Used to train the actual models.

## OCR.py
Used extract the text from the images. 


