import vtk
import argparse
import os
import faulthandler

faulthandler.enable()

DATA_PATH = os.path.join("Data", "Isabel_3D.vti")

def load_volume_data(file_path):
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()

def create_outline(dataset):
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(dataset)
    outline_filter.Update()
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outline_filter.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)
    
    return actor

def configure_color_opacity():
    color_function = vtk.vtkColorTransferFunction()
    color_points = [
        (-4931.54, (0.0, 1.0, 1.0)),
        (-2508.95, (0.0, 0.0, 1.0)),
        (-1873.9,  (0.0, 0.0, 0.5)),
        (-1027.16, (1.0, 0.0, 0.0)),
        (-298.031, (1.0, 0.4, 0.0)),
        (2594.97,  (1.0, 1.0, 0.0))
    ]
    for val, color in color_points:
        color_function.AddRGBPoint(val, *color)
    
    opacity_function = vtk.vtkPiecewiseFunction()
    opacity_points = [
        (-4931.54, 1.0),
        (101.815, 0.002),
        (2594.97, 0.0)
    ]
    for val, opacity in opacity_points:
        opacity_function.AddPoint(val, opacity)
    
    return color_function, opacity_function

def setup_volume_properties(use_phong):
    color_tf, opacity_tf = configure_color_opacity()
    properties = vtk.vtkVolumeProperty()
    properties.SetColor(color_tf)
    properties.SetScalarOpacity(opacity_tf)
    properties.SetInterpolationTypeToLinear()
    
    if use_phong:
        properties.ShadeOn()
        properties.SetAmbient(0.5)
        properties.SetDiffuse(0.5)
        properties.SetSpecular(0.5)
        properties.SetSpecularPower(10)
    
    return properties

def setup_renderer(volume, outline):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.5, 0.5, 0.5)
    renderer.AddVolume(volume)
    renderer.AddActor(outline)
    
    return renderer

def render_scene(use_phong):
    dataset = load_volume_data(DATA_PATH)
    outline_actor = create_outline(dataset)
    
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputData(dataset)
    
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(setup_volume_properties(use_phong))
    
    renderer = setup_renderer(volume, outline_actor)
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)
    
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    interactor.SetRenderWindow(render_window)
    
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3D Volume Rendering with Phong Shading Option")
    parser.add_argument("--phong", choices=["yes", "no"], default="no", help="Enable Phong shading (yes or no). Default is no.")
    args = parser.parse_args()
    
    render_scene(args.phong == "yes")
