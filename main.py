import time
import itertools

import numpy as np

import FreeCAD as App
import FreeCADGui as Gui
import Part


def animate_job(wires: list[Part.Wire], normals: Part.Face, dist: int = 1, step: int = 1) -> None:
    # noinspection PyUnresolvedReferences
    target_pos: list[App.Vector] = list(
        itertools.chain.from_iterable([w.discretize(Distance=dist) for w in wires])
    )

    # noinspection PyUnresolvedReferences
    normal_srf: Part.Face.Surface = normals.Surface
    target_placement: App.Placement = App.Placement()
    for i in np.arange(0, len(target_pos), step):
        # noinspection PyUnresolvedReferences
        uv: tuple[float, float] = normal_srf.parameter(target_pos[i])
        # noinspection PyUnresolvedReferences
        normal: App.Vector = normal_face.normalAt(uv[0], uv[1])

        target_placement.Base = target_pos[i]
        target_placement.Rotation = App.Rotation(tool_normal, -normal)
        tool_obj.Placement = target_placement
        Gui.updateGui()
        time.sleep(0.0005)


doc: App.Document = App.ActiveDocument

# tool
tool_obj: App.DocumentObject = doc.getObjectsByLabel("5mm_endmill")[0]
tool_normal: App.Vector = App.Vector(0, 0, -1)
tool_x: App.Vector = App.Vector(1, 0, 0)

#####################################
# feature_1_clearing job
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_clearing_path")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = path_obj.Shape.Wires
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_clearing_top")[0].Shape.Faces[0]

animate_job(wires_list, normal_face, dist=2, step=2)

#####################################
# feature_1_hor_finishing job
path_obj_1: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_1")[0]
path_obj_2: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_2")[0]
path_obj_3: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_3")[0]
path_obj_4: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_4")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = [
    path_obj_1.Shape.Wires[0], path_obj_2.Shape.Wires[0], path_obj_3.Shape.Wires[0], path_obj_4.Shape.Wires[0]
]
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_hor_finishing_srf")[0].Shape.Faces[0]

animate_job(wires_list, normal_face, dist=1, step=1)

#####################################
# feature_1_ver_finishing job
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_ver_finishing_path")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = path_obj.Shape.Wires
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_ver_finishing_srf")[0].Shape.Faces[0]

animate_job(wires_list, normal_face, dist=1, step=1)
