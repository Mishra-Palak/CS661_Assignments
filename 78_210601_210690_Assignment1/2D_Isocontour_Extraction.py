# import the necessary libraries
import os
import vtk

# input information
input_file = "Input/Isabel_2D.vti"  
isovalue = float(input("Enter the isovalue: "))

# read the input image
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(input_file)
reader.Update()

image_data = reader.GetOutput()
dims = image_data.GetDimensions()

# marching squares algorithm
contour_data = vtk.vtkPolyData()
points = vtk.vtkPoints()
lines = vtk.vtkCellArray()

point_index = 0
z_index = 25  # according to the shared input image

for i in range(dims[0] - 1):
    for j in range(dims[1] - 1):
        v = [image_data.GetScalarComponentAsDouble(i, j, z_index, 0),
             image_data.GetScalarComponentAsDouble(i+1, j, z_index, 0),
             image_data.GetScalarComponentAsDouble(i+1, j+1, z_index, 0),
             image_data.GetScalarComponentAsDouble(i, j+1, z_index, 0)]
        
        p = [[i, j], [i+1, j], [i+1, j+1], [i, j+1]]

        # counter-clockwise traversal
        edges = []
        for k in range(4):
            v1, v2 = v[k], v[(k+1) % 4]
            if (v1 < isovalue and v2 >= isovalue) or (v1 <= isovalue and v2 > isovalue) or (v2 < isovalue and v1 >= isovalue) or (v2 <= isovalue and v1 > isovalue):
                t = (isovalue - v1) / (v2 - v1)
                x = p[k][0] + t * (p[(k+1) % 4][0] - p[k][0])
                y = p[k][1] + t * (p[(k+1) % 4][1] - p[k][1])
                edges.append((x, y))

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

contour_data.SetPoints(points)
contour_data.SetLines(lines)

# output image
os.makedirs("Output", exist_ok = True) # create 'Output' folder if it doesn't exist already
output_filename = os.path.join("Output", f"Isabel_Isocontour_{int(isovalue)}.vtp")

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(output_filename)
writer.SetInputData(contour_data)
writer.Write()

# logging
print(f"Isocontour extraction complete! Output saved to {os.path.basename(output_filename)}")
