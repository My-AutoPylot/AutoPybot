
# https://github.com/topics/document-image-processing
import os

# Let's pick the desired backend
os.environ['USE_TF'] = '1'
# os.environ['USE_TORCH'] = '1'

import matplotlib.pyplot as plt

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
    

# Read the file
doc = DocumentFile.from_pdf(r"C:\Users\mrmay\OneDrive\Desktop\Cash-Payment-Receipt-Template.pdf")
print(f"Number of pages: {len(doc)}")

predictor = ocr_predictor(pretrained=True)

# Display the architecture
# print(predictor)

result = predictor(doc)

# result.show(doc)

synthetic_pages = result.synthesize()
# plt.imshow(synthetic_pages[0]); plt.axis('off'); plt.show()

# JSON export
json_export = result.export()
print(json_export)


