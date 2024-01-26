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
        target_offset: App.Vector = locale_part_pos + locale_part_rot * target_pos[i]
        fixture_placement: App.Placement = App.Placement()
        fixture_placement.Base = globale_spindle_pos - target_offset

        # Fixture orientation to spindle axis
        uv: tuple[float, float] = normal_srf.parameter(target_pos[i])  # noqa
        globale_part_normal: App.Vector = locale_part_rot * normal_face.normalAt(uv[0], uv[1])
        rot_to_spindle_axis: App.Rotation = App.Rotation(globale_part_normal, -globale_spindle_axis)

        fixture_placement.rotate(
            target_offset, rot_to_spindle_axis.Axis, float(np.degrees(rot_to_spindle_axis.Angle))  # noqa
        )
        fixture_frame_obj.Placement = fixture_placement

        proj_spindle_x: App.Vector = globale_spindle_x.projectToPlane(
            globale_spindle_pos, fixture_frame_obj.Placement.Rotation * App.Vector(1, 0, 0)  # noqa
        )

        # Fixture orientation to spindle x
        print(proj_spindle_x)
        proj_fixture_z: App.Vector = fixture_placement.Rotation * App.Vector(0, 1, 0).projectToPlane(
            spindle_frame_obj.Placement.Base, globale_spindle_axis  # noqa
        )
        #print(proj_fixture_z)
        rot_to_spindle_x: App.Rotation = App.Rotation(proj_fixture_z, globale_spindle_x)

        #print(np.degrees(rot_to_spindle_x.Angle))

        fixture_frame_obj.Placement.rotate(
            target_offset, fixture_placement.Rotation.inverted() * -globale_spindle_axis,  # noqa
            float(np.degrees(rot_to_spindle_x.Angle))
        )

        Gui.updateGui()
        time.sleep(sleep)

    # Reset after animation
    # fixture_placement: App.Placement = App.Placement()
    # fixture_frame_obj.Placement = fixture_placement


doc: App.Document = App.ActiveDocument

# Frames
fixture_frame_obj: App.DocumentObject = doc.getObjectsByLabel("fixture_frame")[0]
part_frame_obj: App.DocumentObject = doc.getObjectsByLabel("part_frame")[0]
spindle_frame_obj: App.DocumentObject = doc.getObjectsByLabel("spindle_frame")[0]

# Vectors
locale_part_pos: App.Vector = part_frame_obj.Placement.Base  # noqa
locale_part_rot: App.Vector = part_frame_obj.Placement.Rotation  # noqa

globale_spindle_pos: App.Vector = spindle_frame_obj.Placement.Base  # noqa
globale_spindle_axis: App.Vector = spindle_frame_obj.Placement.Rotation * App.Vector(0, 0, 1)  # noqa
globale_spindle_x: App.Vector = spindle_frame_obj.Placement.Rotation * App.Vector(1, 0, 0)  # noqa
#spindle_x_inv: App.Vector = App.Vector(1, 0, 0)  # noqa

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
