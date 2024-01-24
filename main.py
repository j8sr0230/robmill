import numpy as np

import FreeCAD as App
# import Part


doc: App.Document = App.ActiveDocument

# tools
tool_obj: App.DocumentObject = doc.getObjectsByLabel("5mm_endmill")[0]
tool_normal: App.Vector = App.Vector(0, 0, -1)
tool_x: App.Vector = App.Vector(1, 0, 0)

# feature_1_clearing
doc: App.Document = App.ActiveDocument
path_obj: App.DocumentObject = doc.getObjectsByLabel("discretized_clearing_path_1")[0]
# noinspection PyUnresolvedReferences
target_pos: list[App.Vector] = path_obj.Points
print("Target size", len(np.array(target_pos)))

normal_srf_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_clearing_top")[0]
# noinspection PyUnresolvedReferences
clearing_normal: App.Vector = normal_srf_obj.Shape.normalAt(0, 0)
print("Clearing normal:", clearing_normal)

target_rot: App.Rotation = App.Rotation(tool_normal, -clearing_normal)
print("Target orientation (quaternion)", target_rot)
print("Target orientation (axis, angle)", target_rot.Axis, np.degrees(target_rot.Angle))

target_placement: App.Placement = App.Placement()
target_placement.translate(target_pos[0])
target_placement.rotate((0, 0, 0), target_rot.Axis, float(np.degrees(target_rot.Angle)))
print("Target orientation (placement)", target_placement)

tool_obj.Placement = target_placement
doc.recompute()
