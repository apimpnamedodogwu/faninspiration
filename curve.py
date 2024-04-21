import rhinoscriptsyntax as rs

def CreatePointBelowLineCenter(line_id, distance= 0.7):
  """
  Creates a point below the center of a given line.

  Args:
      line_id (guid): The ID of the line object.
      distance (float): The distance from the line's center to the new point.

   Returns:
    tuple: A 3D tuple (x, y, z) representing the coordinates of the new point.
  """ 

  # Calculate the line's midpoint
  midPt = rs.CurveMidPoint(line_id)
  rs.AddPoint(midPt)

  # Calculate the direction vector pointing downwards (negative Y direction)
  dirVec = (0, -0.5, 0)

  # Create a scaled direction vector for the offset
  offsetVec = rs.VectorScale(dirVec, distance) 

  # Create the new point below the midpoint
  newPt = rs.PointAdd(midPt, offsetVec)

  # Add the point to the Rhino document
  rs.AddPoint(newPt) 

  return newPt

def create_first_pattern(pt_dict, i, j):
    """
    Creates a pattern of lines, points, and curves based on a point dictionary and indices.

    Args:
        pt_dict (dict): A dictionary storing point coordinates as tuples (x, y, z).
        i (int): The row index of the current point.
        j (int): The column index of the current point.
    """

    if i > 0 and j > 0 and j < 4:
        line_B = rs.AddLine(pt_dict[(i-1,j)], pt_dict[(i,j)])
        line_A = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i-1,j)])
        line_C = rs.AddLine(pt_dict[(i, j-1)], pt_dict[(i,j)])
        line_D = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i, j-1)])
        pt_A = CreatePointBelowLineCenter(line_A)
        pt_C = CreatePointBelowLineCenter(line_C)
        rs.HideObjects(line_A)
        rs.HideObject(line_C)
        line_B_centre = rs.CurveMidPoint(line_B)
        line_D_centre = rs.CurveMidPoint(line_D)
        rs.AddPoint(line_B_centre)
        rs.AddPoint(line_D_centre)
        rs.AddCurve((line_B_centre, pt_A))
        rs.AddCurve((line_B_centre, pt_C))
        rs.AddCurve((pt_A, line_D_centre, pt_C))

def create_matrix():
    pt_dict = {}
    for i in range(6):
        for j in range(5):
            x = i 
            y = j 
            z = 0
            # rs.AddPoint(x, y, z)
            pt_dict[(i,j)] = (x,y,z)
            # rs.AddTextDot((i, j), pt_dict[(i,j)])
            create_first_pattern(pt_dict, i, j)
            
               


create_matrix()



