from ImageCreation import *
from OCR import *

if __name__ == "__main__":
    # image_path = "../images/background.jpeg"
    # output_path = "../images/background-edited.jpeg"

    image_path = "../images/white.png"
    output_path = "../images/white-edited.png"
    ImageCreation = ImageCreation(image_path, output_path)

    sentences = ["Ik loop hier alleen", "In een te stille stad", "Ik heb eigenlijk nooit last", "Van heimwee gehad"]
    ocr = OCR()
    for sentence in sentences:
        ImageCreation.getImage(sentence)
        output = ocr.get_ocr(output_path).strip("\n")
        print(f"{sentence} -> {output}")


    # Create training and evaluation dataset
    # - Collect corrected texts for various time periods
    # - For each time period identify the style of the text:
    #   - Font
    #   - Font size
    #   - Opacity of the letters
    #   - Paper
    # - For each text in the dataset:
    #   - Create an image with the identified style
    #   - Run the image through an OCR engine
    #   - The output is now the given output of the ocr text
    # Use the training dataset to train the T5 text-to-text model based on https://huggingface.co/yhavinga/t5-base-dutch
    # Retrieve OCR data from Delpher, and run it through the model
    # Find existing solutions, and compare results

