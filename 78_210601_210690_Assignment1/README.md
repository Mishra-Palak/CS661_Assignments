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

### Overview

This Python script uses the Visualization Toolkit (VTK) to perform 3D volume rendering from volumetric dataset files in `.vti` format. It allows the user to enable or disable Phong shading for realistic lighting effects.

### Requirements

- Python
- VTK library (Install using `pip install vtk`)

### Usage

#### Running the Script

```sh
python render_volume.py --phong yes
```

#### Arguments

- `--phong yes` → Enables Phong shading
- `--phong no` (default) → Renders without shading

### Features

- Loads and processes 3D volumetric data (`.vti` format).
- Applies color and opacity transfer functions.
- Uses the `vtkSmartVolumeMapper` for rendering.
- Supports optional Phong shading for improved visualization.
- Generates an outline for better scene reference.
- Interactive camera controls for 3D navigation.

### Implementation Guide

#### 1. Load Volume Data

The script reads a `.vti` file using `vtkXMLImageDataReader` and retrieves the image dataset.

```python
def load_volume_data(file_path):
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()
```

#### 2. Create 

A white bounding box outline is generated using `vtkOutlineFilter` for visualization reference.

```python
def create_outline(dataset):
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(dataset)
    outline_filter.Update()
    ...
```

#### 3. Configure Color and Opacity Transfer Functions

The transfer functions define how different scalar values are mapped to colors and opacities for rendering.

```python
def configure_color_opacity():
    color_function = vtk.vtkColorTransferFunction()
    opacity_function = vtk.vtkPiecewiseFunction()
    ...
```

#### 4. Setup Volume Properties

This function sets the color, opacity, and optional Phong shading parameters.

```python
def setup_volume_properties(use_phong):
    properties = vtk.vtkVolumeProperty()
    properties.SetColor(color_tf)
    properties.SetScalarOpacity(opacity_tf)
    properties.SetInterpolationTypeToLinear()
    if use_phong:
        properties.ShadeOn()
        properties.SetAmbient(0.5)
    return properties
```

#### 5. Render the Scene

The dataset is mapped, visualized, and rendered in an interactive window.

```python
def render_scene(use_phong):
    dataset = load_volume_data(DATA_PATH)
    outline_actor = create_outline(dataset)
    ...
    render_window.Render()
    interactor.Start()
```

### Output

- A 3D interactive volume rendering window.
- The scene includes color-mapped scalar values and an outline.

### Notes

- Ensure the `.vti` file path is correctly set in `DATA_PATH`.
- The output can be used in medical imaging, scientific visualization, and simulation data analysis.
- Adjust color and opacity transfer functions for better results depending on the dataset.


## Author

Md Rahbar | 210601 | mdrahbar21@iitk.ac.in <br/>
Palak Mishra | 210690 | palakm21@iitk.ac.in
