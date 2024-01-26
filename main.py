import time
import itertools

import numpy as np

import FreeCADGui as Gui
import FreeCAD as App
import Part


def animate_job(wires: list[Part.Wire], normals: Part.Face, dist: int = 1, step: int = 1, sleep: float = .0005) -> None:
    target_pos: list[App.Vector] = list(
        itertools.chain.from_iterable([w.discretize(Distance=dist) for w in wires])
    )
    normal_srf: Part.Face.Surface = normals.Surface
    for i in np.arange(0, len(target_pos), step):
        # Fixture position
        target_offset: App.Vector = part_pos + part_rot * target_pos[i]
        fixture_placement: App.Placement = App.Placement()
        fixture_placement.Base = spindle_pos - target_offset

        # Fixture orientation
        uv: tuple[float, float] = normal_srf.parameter(target_pos[i])  # noqa
        normal: App.Vector = part_rot * normal_face.normalAt(uv[0], uv[1])
        rot_to_spindle: App.Rotation = App.Rotation(spindle_axis, -normal)
        fixture_placement.rotate(target_offset, rot_to_spindle.Axis, float(np.degrees(-rot_to_spindle.Angle)))  # noqa
        fixture_frame_obj.Placement = fixture_placement

        # print(target_offset, normal)
        Gui.updateGui()
        time.sleep(sleep)

    # Reset after animation
    fixture_placement: App.Placement = App.Placement()
    fixture_frame_obj.Placement = fixture_placement


doc: App.Document = App.ActiveDocument

# Frames
fixture_frame_obj: App.DocumentObject = doc.getObjectsByLabel("fixture_frame")[0]
part_frame_obj: App.DocumentObject = doc.getObjectsByLabel("part_frame")[0]
spindle_frame_obj: App.DocumentObject = doc.getObjectsByLabel("spindle_frame")[0]

# Vectors
part_pos: App.Vector = part_frame_obj.Placement.Base  # noqa
part_rot: App.Vector = part_frame_obj.Placement.Rotation  # noqa
spindle_pos: App.Vector = spindle_frame_obj.Placement.Base  # noqa
spindle_axis: App.Vector = spindle_frame_obj.Placement.Rotation * App.Vector(0, 0, 1)  # noqa

#####################################
# Job: feature_1_clearing
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_clearing_path")[0]
wires_list: list[Part.Wire] = path_obj.Shape.Wires  # noqa
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_clearing_top")[0].Shape.Faces[0]   # noqa

animate_job(wires_list, normal_face, dist=3, step=3, sleep=0.0005)

# #####################################
# # feature_1_hor_finishing job
# path_obj_1: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_1")[0]
# path_obj_2: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_2")[0]
# path_obj_3: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_3")[0]
# path_obj_4: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_4")[0]
# # noinspection PyUnresolvedReferences
# wires_list: list[Part.Wire] = [
#     path_obj_1.Shape.Wires[0], path_obj_2.Shape.Wires[0], path_obj_3.Shape.Wires[0], path_obj_4.Shape.Wires[0]
# ]
# # noinspection PyUnresolvedReferences
# normal_face: Part.Face = doc.getObjectsByLabel("feature_1_hor_finishing_srf")[0].Shape.Faces[0]
#
# # animate_fixture(wires_list, normal_face, dist=2, step=2)
#
# #####################################
# # feature_1_ver_finishing job
# path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_ver_finishing_path")[0]
# # noinspection PyUnresolvedReferences
# wires_list: list[Part.Wire] = path_obj.Shape.Wires
# # noinspection PyUnresolvedReferences
# normal_face: Part.Face = doc.getObjectsByLabel("feature_1_ver_finishing_srf")[0].Shape.Faces[0]
#
# # animate_fixture(wires_list, normal_face, dist=2, step=2)
