# Import the necessary libraries
import os
import vtk

# Input information
input_file = os.path.join("Data", "Isabel_2D.vti")
isovalue = float(input("Enter the isovalue: "))

# Read the input image using vtkXMLImageDataReader
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(input_file)
reader.Update()

image_data = reader.GetOutput()
dims = image_data.GetDimensions()

# Initialize containers for the marching squares algorithm
contour_data = vtk.vtkPolyData()
points = vtk.vtkPoints()
lines = vtk.vtkCellArray()

point_index = 0
z_index = 25  # Fixed z-index slice for 2D contour extraction

# Marching Squares Algorithm
for i in range(dims[0] - 1):
    for j in range(dims[1] - 1):
        # Get scalar values at the four corners of the cell
        v = [image_data.GetScalarComponentAsDouble(i, j, z_index, 0),
             image_data.GetScalarComponentAsDouble(i+1, j, z_index, 0),
             image_data.GetScalarComponentAsDouble(i+1, j+1, z_index, 0),
             image_data.GetScalarComponentAsDouble(i, j+1, z_index, 0)]

        # Get the corresponding points' (i, j) indices
        p = [[i, j], [i+1, j], [i+1, j+1], [i, j+1]]

        # Determine where the contour crosses each edge of the cell
        edges = []
        for k in range(4):
            v1, v2 = v[k], v[(k+1) % 4]
            # Check if the isovalue crosses this edge
            if (v1 < isovalue and v2 >= isovalue) or (v1 <= isovalue and v2 > isovalue) or (v2 < isovalue and v1 >= isovalue) or (v2 <= isovalue and v1 > isovalue):
                # Linear interpolation to find the intersection point
                t = (isovalue - v1) / (v2 - v1)
                x = p[k][0] + t * (p[(k+1) % 4][0] - p[k][0])
                y = p[k][1] + t * (p[(k+1) % 4][1] - p[k][1])
                edges.append((x, y))

        # If exactly two intersection points, create a line segment
        if len(edges) == 2:
            p1_id = point_index
            p2_id = point_index + 1

            points.InsertNextPoint(edges[0][0], edges[0][1], z_index)
            points.InsertNextPoint(edges[1][0], edges[1][1], z_index)
            point_index += 2

            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, p1_id)
            line.GetPointIds().SetId(1, p2_id)
            lines.InsertNextCell(line)

# Set points and lines to the contour polydata
contour_data.SetPoints(points)
contour_data.SetLines(lines)

# Output information
os.makedirs("Output", exist_ok=True)
output_filename = os.path.join("Output", f"Isabel_Isocontour_{int(isovalue)}.vtp")

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(output_filename)
writer.SetInputData(contour_data)
writer.Write()

# Logging - inform the user that the process is complete
print(f"Isocontour extraction complete! Output saved to {os.path.basename(output_filename)}")
