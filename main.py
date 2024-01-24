import numpy as np

import FreeCAD as App
# import Part

doc: App.Document = App.ActiveDocument
obj_list: list[App.DocumentObject] = doc.getObjectsByLabel("discretized_clearing_path_1")
obj: App.DocumentObject = obj_list[0]

# noinspection PyUnresolvedReferences
pts: list[App.Vector] = obj.Points
print(np.array(pts))
