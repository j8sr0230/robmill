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

        # Fixture orientation to spindle axis (z)
        uv_pf: tuple[float, float] = normal_srf_pf.parameter(target_pos_pf[i])  # noqa
        cut_normal_ff: App.Vector = part_rot_ff * normals.normalAt(uv_pf[0], uv_pf[1])
        to_spindle_axis_gf: App.Rotation = App.Rotation(cut_normal_ff, -spindle_axis_gf)

        # Fixture orientation to spindle x
        align_axis_gf: App.Vector = to_spindle_axis_gf * align_axis_ff
        align_axis_sf: App.Vector = spindle_frame_obj.Placement.Rotation.inverted() * align_axis_gf  # noqa
        deg_to_spindle_x: float = float(np.degrees(np.arctan2(align_axis_sf.y, align_axis_sf.x) -
                                                   np.arctan2(spindle_axis_sf.y, spindle_axis_sf.x)))
        to_spindle_x_gf: App.Rotation = App.Rotation(-spindle_axis_gf, deg_to_spindle_x)

        # Set compound placement
        fixture_frame_obj.Placement = App.Placement(
            spindle_pos_gf - target_pos_ff,
            to_spindle_x_gf * to_spindle_axis_gf,
            target_pos_ff
        )

        Gui.updateGui()
        time.sleep(sleep)

    # Reset after animation
    fixture_frame_obj.Placement = App.Placement()


doc: App.Document = App.ActiveDocument

# Frames
fixture_frame_obj: App.DocumentObject = doc.getObjectsByLabel("fixture_frame")[0]
part_frame_obj: App.DocumentObject = doc.getObjectsByLabel("part_frame")[0]
spindle_frame_obj: App.DocumentObject = doc.getObjectsByLabel("spindle_frame")[0]

# Vectors
align_axis_ff: App.Vector = App.Vector(0, 0, 1)
part_pos_ff: App.Vector = part_frame_obj.Placement.Base  # noqa
part_rot_ff: App.Vector = part_frame_obj.Placement.Rotation  # noqa
spindle_axis_sf: App.Vector = App.Vector(0, 0, 1)
spindle_x_sf: App.Vector = App.Vector(1, 0, 0)
spindle_pos_gf: App.Vector = spindle_frame_obj.Placement.Base  # noqa
spindle_axis_gf: App.Vector = spindle_frame_obj.Placement.Rotation * spindle_axis_sf  # noqa

#####################################
# Job: feature_1_clearing
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_clearing_path")[0]
wires_list: list[Part.Wire] = path_obj.Shape.Wires  # noqa
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_clearing_top")[0].Shape.Faces[0]  # noqa
animate_job(wires_list, normal_face, dist=3, step=3, sleep=0.0005)

# #####################################
#  Job: feature_1_hor_finishing
path_obj_1: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_1")[0]
path_obj_2: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_2")[0]
path_obj_3: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_3")[0]
path_obj_4: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_4")[0]
wires_list: list[Part.Wire] = [
    path_obj_1.Shape.Wires[0], path_obj_2.Shape.Wires[0], path_obj_3.Shape.Wires[0], path_obj_4.Shape.Wires[0]  # noqa
]
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_hor_finishing_srf")[0].Shape.Faces[0]  # noqa
animate_job(wires_list, normal_face, dist=2, step=2, sleep=0.0005)

# #####################################
# Job: feature_1_ver_finishing
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_ver_finishing_path")[0]
wires_list: list[Part.Wire] = path_obj.Shape.Wires  # noqa
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_ver_finishing_srf")[0].Shape.Faces[0]  # noqa
animate_job(wires_list, normal_face, dist=2, step=2, sleep=0.0005)
