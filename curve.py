import rhinoscriptsyntax as rs


def create_point_offset_from_line_centre(line_id, distance=0.7, direction="down"):
  
  """
  Creates a point at a specified distance from the center of a given line, in either the 
  positive or negative Y direction.

  Args:
      line_id (guid): The ID of the line object.
      distance (float): The distance from the line's center to the new point.
      direction (str):  Specifies the direction of the offset. Can be either "down" or "up". 
                        Defaults to "down".

  Returns:
      tuple: A 3D tuple (x, y, z) representing the coordinates of the new point.
  """ 

  # Calculate the line's midpoint
  midPt = rs.CurveMidPoint(line_id)

  # Calculate the direction vector 
  if direction.lower() == "down":
      dirVec = (0, -0.5, 0)
  elif direction.lower() == "up":
      dirVec = (0, 0.5, 0)  # Positive Y direction
  else:
      raise ValueError("Invalid direction. Must be either 'down' or 'up'")
  

  # Create a scaled direction vector for the offset
  offsetVec = rs.VectorScale(dirVec, distance) 

  # Create the new point 
  newPt = rs.PointAdd(midPt, offsetVec)

  return newPt 


def create_first_pattern(pt_dict, i, j):

    """
    Creates a pattern of lines, points, and curves based on a point dictionary and indices.

    Args:
        pt_dict (dict): A dictionary storing point coordinates as tuples (x, y, z).
        i (int): The row index of the current point.
        j (int): The column index of the current point.
    """

    if i > 0 and j > 0:

        rs.EnableRedraw(False)

        line_B = rs.AddLine(pt_dict[(i-1,j)], pt_dict[(i,j)])
        line_A = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i-1,j)])
        line_C = rs.AddLine(pt_dict[(i, j-1)], pt_dict[(i,j)])
        line_D = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i, j-1)])

        rs.HideObject(line_B)
        rs.HideObject(line_D)
        rs.HideObjects(line_A)
        rs.HideObject(line_C)


        pt_A = create_point_offset_from_line_centre(line_A)
        pt_C = create_point_offset_from_line_centre(line_C)
        
        line_B_centre = rs.CurveMidPoint(line_B)
        line_D_centre = rs.CurveMidPoint(line_D)
        
    
        left_curve = rs.AddCurve((line_B_centre, pt_A))
        right_curve = rs.AddCurve((line_B_centre, pt_C))
        bottom_curve = rs.AddCurve((pt_A, line_D_centre, pt_C))

        left_curve_mid = rs.CurveMidPoint(left_curve)
        right_curve_mid = rs.CurveMidPoint(right_curve)
        bottom_curve_mid = rs.CurveMidPoint(bottom_curve)

        inner_left_curve = rs.AddCurve((bottom_curve_mid, left_curve_mid))
        inner_left_curve_mid = rs.CurveMidPoint(inner_left_curve)
        inner_right_curve = rs.AddCurve((bottom_curve_mid, right_curve_mid))
        inner_right_curve_mid = rs.CurveMidPoint(inner_right_curve)
        rs.AddCurve((bottom_curve_mid, left_curve_mid, line_B_centre))
        rs.AddCurve((bottom_curve_mid, right_curve_mid, line_B_centre))

        rs.AddCurve((bottom_curve_mid, left_curve_mid, right_curve_mid, line_B_centre))
        rs.AddCurve((pt_A, inner_left_curve_mid,left_curve_mid))
        rs.AddCurve((pt_C, inner_right_curve_mid, right_curve_mid))

        rs.EnableRedraw()

def create_second_pattern(pt_dict, i, j):

    """
    Creates a pattern of lines, points, and curves based on a point dictionary and indices.

    Args:
        pt_dict (dict): A dictionary storing point coordinates as tuples (x, y, z).
        i (int): The row index of the current point.
        j (int): The column index of the current point.
    """

    if i > 0 and j > 0:
                
                rs.EnableRedraw(False)

                line_B = rs.AddLine(pt_dict[(i-1,j)], pt_dict[(i,j)])
                line_A = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i-1,j)])
                line_C = rs.AddLine(pt_dict[(i, j-1)], pt_dict[(i,j)])
                line_D = rs.AddLine(pt_dict[(i-1, j-1)], pt_dict[(i, j-1)])

                rs.HideObject(line_B)
                rs.HideObject(line_A)
                rs.HideObjects(line_D)
                rs.HideObject(line_C)


                pt_A = create_point_offset_from_line_centre(line_A, direction="up")
                pt_C = create_point_offset_from_line_centre(line_C, direction="up")
                
                line_B_centre = rs.CurveMidPoint(line_B)
                line_D_centre = rs.CurveMidPoint(line_D)
                
               
                left_curve = rs.AddCurve((line_D_centre, pt_A))
                right_curve = rs.AddCurve((line_D_centre, pt_C))
                bottom_curve = rs.AddCurve((pt_A, line_B_centre, pt_C))

                left_curve_mid = rs.CurveMidPoint(left_curve)
                right_curve_mid = rs.CurveMidPoint(right_curve)
                bottom_curve_mid = rs.CurveMidPoint(bottom_curve)

                inner_left_curve = rs.AddCurve((bottom_curve_mid, left_curve_mid))
                inner_left_curve_mid = rs.CurveMidPoint(inner_left_curve)
                inner_right_curve = rs.AddCurve((bottom_curve_mid, right_curve_mid))
                inner_right_curve_mid = rs.CurveMidPoint(inner_right_curve)
                rs.AddCurve((bottom_curve_mid, left_curve_mid, line_D_centre))
                rs.AddCurve((bottom_curve_mid, right_curve_mid, line_D_centre))

                rs.AddCurve((bottom_curve_mid, left_curve_mid, right_curve_mid, line_D_centre))
                rs.AddCurve((pt_A, inner_left_curve_mid, left_curve_mid))
                rs.AddCurve((pt_C, inner_right_curve_mid, right_curve_mid))

                rs.EnableRedraw()
        

def create_matrix():
    pt_dict = {}
    for i in range(10):
        for j in range(11):
            x = i 
            y = j 
            z = 0
            pt_dict[(i,j)] = (x,y,z)
            
            if j % 2 == 0: 
                create_second_pattern(pt_dict, i, j)
                
            else:   
                create_first_pattern(pt_dict, i, j)



create_matrix()



