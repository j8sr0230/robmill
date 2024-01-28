import time
import itertools

import numpy as np

import FreeCADGui as Gui
import FreeCAD as App
import Part


def animate_job(wires: list[Part.Wire], normals: Part.Face, dist: int = 1, step: int = 1, sleep: float = .0005) -> None:
    target_pos_pf: list[App.Vector] = list(
        itertools.chain.from_iterable([w.discretize(Distance=dist) for w in wires])
    )
    normal_srf_pf: Part.Face.Surface = normals.Surface
    for i in np.arange(0, len(target_pos_pf), step):

        # Fixture position
        target_pos_ff: App.Vector = part_pos_ff + part_rot_ff * target_pos_pf[i]

        # Fixture orientation to spindle axis
        uv_pf: tuple[float, float] = normal_srf_pf.parameter(target_pos_pf[i])  # noqa
        cut_normal_ff: App.Vector = part_rot_ff * normals.normalAt(uv_pf[0], uv_pf[1])
        rot_to_spindle_axis_gf: App.Rotation = App.Rotation(cut_normal_ff, -spindle_axis_gf)
        ff_placement: App.Placement = App.Placement(spindle_pos_gf - target_pos_ff, rot_to_spindle_axis_gf,
                                                    target_pos_ff)
        fixture_frame_obj.Placement = ff_placement

        # Fixture orientation to spindle x
        spindle_axis_ff: App.Vector = ff_placement.Rotation.inverted() * spindle_axis_gf
        # spindle_x_ff: App.Vector = ff_placement.Rotation.inverted() * spindle_x_gf
        # spindle_x_ff_proj: App.Vector = App.Vector(0, spindle_x_ff.y, spindle_x_ff.z)

        # angle_diff = np.degrees(
        #     np.arctan2(alignment_axis_ff.y, alignment_axis_ff.z) -
        #     np.arctan2(spindle_x_ff_proj.y, spindle_x_ff_proj.z)
        # )
        # print(angle_diff)

        alignment_axis_sf: App.Vector = (
                spindle_frame_obj.Placement.Rotation.inverted() * rot_to_spindle_axis_gf * alignment_axis_ff  # noqa
        )
        # print(alignment_axis_sf)
        angle_diff = np.degrees(
            np.arctan2(alignment_axis_sf.y, alignment_axis_sf.x) -
            np.arctan2(0, 1)
        )
        # print(angle_diff)

        fixture_frame_obj.Placement.rotate(target_pos_ff, - spindle_axis_ff, angle_diff)  # noqa

        Gui.updateGui()
        time.sleep(sleep)

    # Reset after animation
    # ff_placement: App.Placement = App.Placement()
    # fixture_frame_obj.Placement = ff_placement


doc: App.Document = App.ActiveDocument

# Frames
fixture_frame_obj: App.DocumentObject = doc.getObjectsByLabel("fixture_frame")[0]
part_frame_obj: App.DocumentObject = doc.getObjectsByLabel("part_frame")[0]
spindle_frame_obj: App.DocumentObject = doc.getObjectsByLabel("spindle_frame")[0]

# Vectors
part_pos_ff: App.Vector = part_frame_obj.Placement.Base  # noqa
part_rot_ff: App.Vector = part_frame_obj.Placement.Rotation  # noqa

spindle_pos_gf: App.Vector = spindle_frame_obj.Placement.Base  # noqa
spindle_axis_gf: App.Vector = spindle_frame_obj.Placement.Rotation * App.Vector(0, 0, 1)  # noqa
spindle_x_gf: App.Vector = spindle_frame_obj.Placement.Rotation * App.Vector(1, 0, 0)  # noqa

alignment_axis_ff: App.Vector = App.Vector(0, 1, 0)

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
