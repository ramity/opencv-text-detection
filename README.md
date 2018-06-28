# ocr

- Current approach:
  - Load image
  - Threshold
  - Median
  - Contours
  - Merge sibling contours recursively
  - Output image
  
- Future approach:
  - Load image
  - Threshold
  - for z in range(1, 9, 2):
    - Median(z, threshold)
    - Contours
    - Merge sibling contours recursively
  - Merge outputs from each iteration into a final data obj
  - Output image
