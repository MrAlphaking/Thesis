from src.ImageProcessing.ImageCreation import *
from OCR import *
import DataCreator


if __name__ == "__main__":
    image_path = "../images/white.jpg"
    output_path = "../images/white-edited2.jpg"
    imagecreator = ImageCreation(image_path=image_path, output_path=output_path)
    ocr = OCR()
    imagecreator.getImage("Lorem ipsum is een opvultekst die drukkers, zetters, grafisch ontwerpers en dergelijken gebruiken om te kijken hoe een opmaak er grafisch uitziet. De eerste woorden van de tekst luiden doorgaans Lorem ipsum")
    source = ocr.get_ocr(output_path).strip("\n")
    print(source)
    # df = DataCreator.get_dataframe()



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

