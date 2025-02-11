# Assignment 1

## Part I - 2D Isocontour Extraction

This script extracts isocontours from a 2D uniform grid dataset stored in VTKImageData format. The extracted isocontour is saved as a VTKPolyData file (`.vtp`), which can be visualized in ParaView.

### Requirements

Ensure that the following dependencies are installed before running the script:

- Python 3.x (the latest version is preferable)
- VTK (`pip install vtk`)

### Implementation

Ensure that the working directory is set to the current folder before running the script.


Run the script from the command line:

```bash
python 2D_Isocontour_Extraction.py
```

Upon execution, the script will prompt for an **isovalue**:

```plaintext
Enter the isovalue: <your_value>
```

Provide a floating-point value in the range **(-1438, 630)** (as specified in the assignment).

### Input

- The script reads the dataset from `Isabel_2D.vti`, which is present in the **Input** folder.

### Output

- The script creates an **Output** folder in the working directory if it does not already exist.
- The extracted isocontour is saved as a `.vtp` file in the **Output** folder:
  
  ```plaintext
  Isabel_Isocontour_<isovalue>.vtp
  ```
  
  The `<isovalue>` field depends on the input isovalue.
- This `.vtp` file can be loaded into **ParaView** for visualization.

### Visualization in Paraview

- For visualization, follow these steps in **ParaView**:

1. First, **load the original dataset (`Isabel_2D.vti`)** to see the scalar field.
2. Then, **load the extracted isocontour (`Isabel_Isocontour_<isovalue>.vtp`)** stored in the **Output** folder.
3. Adjust the **color and opacity settings** for better contrast.
4. If using a **white background**, change the contour color to a visible shade (as mentioned in the assignment).

### Example Run

```bash
python 2D_Isocontour_Extraction.py
```

```plaintext
Enter the isovalue: -500
Isocontour extraction complete! Output saved to Isabel_Isocontour_-500.vtp
```

## Part II - VTK Volume Rendering and Transfer Function