import time
import itertools

import numpy as np

from pivy import coin
import FreeCADGui as Gui
import FreeCAD as App
import Part


def draw_frame(target: App.Placement = App.Placement) -> coin.SoSeparator():
    frame_sep: coin.SoSeparator = coin.SoSeparator()

    frame_draw_style: coin.SoDrawStyle = coin.SoDrawStyle()
    frame_draw_style.lineWidth = 1
    frame_sep.addChild(frame_draw_style)

    x_sep: coin.SoSeparator = coin.SoSeparator()
    x_color: coin.SoBaseColor = coin.SoBaseColor()
    x_color.rgb = (1, 0, 0)
    x_sep.addChild(x_color)
    x_pts: coin.SoCoordinate3 = coin.SoCoordinate3()
    x_pts.point.setValues(0, 2, [(0, 0, 0), (10, 0, 0)])
    x_sep.addChild(x_pts)
    x_line: coin.SoLineSet = coin.SoLineSet()
    x_line.numVertices = 2
    x_sep.addChild(x_line)
    frame_sep.addChild(x_sep)

    y_sep: coin.SoSeparator = coin.SoSeparator()
    y_color: coin.SoBaseColor = coin.SoBaseColor()
    y_color.rgb = (0, 1, 0)
    y_sep.addChild(y_color)
    y_pts: coin.SoCoordinate3 = coin.SoCoordinate3()
    y_pts.point.setValues(0, 2, [(0, 0, 0), (0, 10, 0)])
    y_sep.addChild(y_pts)
    y_line: coin.SoLineSet = coin.SoLineSet()
    y_line.numVertices = 2
    y_sep.addChild(y_line)
    frame_sep.addChild(y_sep)

    z_sep: coin.SoSeparator = coin.SoSeparator()
    z_color: coin.SoBaseColor = coin.SoBaseColor()
    z_color.rgb = (0, 0, 1)
    z_sep.addChild(z_color)
    z_pts: coin.SoCoordinate3 = coin.SoCoordinate3()
    z_pts.point.setValues(0, 2, [(0, 0, 0), (0, 0, 10)])
    z_sep.addChild(z_pts)
    z_line: coin.SoLineSet = coin.SoLineSet()
    z_line.numVertices = 2
    z_sep.addChild(z_line)
    frame_sep.addChild(z_sep)

    return frame_sep


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
        fixture_align_axis_gf: App.Vector = to_spindle_axis_gf * fixture_align_axis_ff
        fixture_align_axis_sf: App.Vector = spindle_rot_gf.inverted() * fixture_align_axis_gf  # noqa
        deg_to_spindle_align_axis: float = float(np.arctan2(fixture_align_axis_sf.y, fixture_align_axis_sf.x) -
                                                 np.arctan2(spindle_align_axis_sf.y, spindle_align_axis_sf.x))
        to_spindle_x_gf: App.Rotation = App.Rotation(-spindle_axis_gf, float(np.degrees(deg_to_spindle_align_axis)))

        # Set compound placement
        fixture_frame_obj.Placement = App.Placement(
            spindle_pos_gf - target_pos_ff,
            to_spindle_x_gf * to_spindle_axis_gf,
            target_pos_ff
        )

        abc_angle: tuple[float] = (to_spindle_x_gf * to_spindle_axis_gf).getYawPitchRoll()
        print("X", round(target_pos_ff.x), ", Y", round(target_pos_ff.y), ", Z", round(target_pos_ff.z),
              ", A", round(abc_angle[0]), ", B", round(abc_angle[1]), ", C", round(abc_angle[2]))

        Gui.updateGui()
        time.sleep(sleep)

    # Reset after animation
    fixture_frame_obj.Placement = App.Placement()


doc: App.Document = App.ActiveDocument
if doc:
    sg: coin.SoSeparator = Gui.ActiveDocument.ActiveView.getSceneGraph()

    frame: coin.SoSeparator = draw_frame()
    sg.addChild(frame)
    # sg.removeChild(frame)

    # Spindle
    spindle_frame_obj: App.DocumentObject = doc.getObjectsByLabel("spindle_frame")[0]
    spindle_pos_gf: App.Vector = spindle_frame_obj.Placement.Base  # noqa
    spindle_rot_gf: App.Vector = spindle_frame_obj.Placement.Rotation  # noqa
    spindle_axis_sf: App.Vector = App.Vector(0, 0, 1)
    spindle_axis_gf: App.Vector = spindle_frame_obj.Placement.Rotation * spindle_axis_sf  # noqa
    spindle_align_axis_sf: App.Vector = App.Vector(1, 0, 0)

    # Fixture
    fixture_frame_obj: App.DocumentObject = doc.getObjectsByLabel("fixture_frame")[0]
    fixture_align_axis_ff: App.Vector = App.Vector(0, 0, 1)

    # Part
    part_frame_obj: App.DocumentObject = doc.getObjectsByLabel("part_frame")[0]
    part_pos_ff: App.Vector = part_frame_obj.Placement.Base  # noqa
    part_rot_ff: App.Vector = part_frame_obj.Placement.Rotation  # noqa

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
