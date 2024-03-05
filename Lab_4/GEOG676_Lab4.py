
# Create a gdb and garage feature
import arcpy 
arcpy.env.overwriteOutput = True

folder_path = r'\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-590824\AccountSettings\Desktop\GEOG_676\Lab_4'
arcpy.env.workspace = folder_path
gdb_name = 'Test.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-590824\AccountSettings\Desktop\GEOG_676\Lab_4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', "y", garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

# Open campus gdb, copy building feature to our gdb
campus = r'\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-590824\AccountSettings\Desktop\GEOG_676\Lab_4\Campus.gdb'
#buildings_campus = campus + r'\Structures'
buildings_campus = r'\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-590824\AccountSettings\Desktop\GEOG_676\Lab_4\Campus.gdb\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# Re-Projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

# Buffer the garages
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path + '\Garage_Points_buffered', 150)

# Intersect our buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', r'\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-590824\AccountSettings\Desktop\GEOG_676\Lab_4', 'nearbyBuildings.csv')