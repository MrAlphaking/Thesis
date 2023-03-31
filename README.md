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
 
    # Create training and evaluation dataset
    # OCR data collection
    #   - Collect corrected texts for various time periods
    #   - Data preprocessing (only use sentences with a certain amount of words)        (DataCleaner class)
    #   - (Optional) assess the quality of the OCR to make sure the quality is sufficient https://journal.dhbenelux.org/wp-content/uploads/2022/07/jdhbenelux4_07-Cuper.pdf
    # Style detection
    # - For each time period identify the style of the text:
    #   - Font
    #   - Font size
    #   - Opacity of the letters
    #   - Paper
    # - For each text in the dataset:
    #   - Create an image with the identified style                                     (ImageCreation)
    #   - Run the image through an OCR engine                                           (OCR class)
    #   - The output is now the given output of the ocr text
    # Use the training dataset to train the T5 text-to-text model based on https://huggingface.co/yhavinga/t5-base-dutch
    # Retrieve OCR data from Delpher, and run it through the model
    # Find existing solutions, and compare results
 
 https://sites.google.com/view/icdar2019-postcorrectionocr/evaluation
 https://zenodo.org/record/3515403#.Y_8xfNLMJki
 https://gitlab.univ-lr.fr/crigau02/icdar2019-post-ocr-text-correction-competition/-/tree/master/
