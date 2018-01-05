from __future__ import print_function, absolute_import, division

from fontTools.misc.py23 import *
from fontTools.pens.recordingPen import RecordingPen
from fontTools.svgLib import parse_path

import pytest


@pytest.mark.parametrize(
    "pathdef, expected",
    [

        # Examples from the SVG spec

        (
            "M 100 100 L 300 100 L 200 300 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # for Z command behavior when there is multiple subpaths
        (
            "M 0 0 L 50 20 M 100 100 L 300 100 L 200 300 z",
            [
                ("moveTo", ((0.0, 0.0),)),
                ("lineTo", ((50.0, 20.0),)),
                ("endPath", ()),
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        (
            "M100,200 C100,100 250,100 250,200 S400,300 400,200",
            [
                ("moveTo", ((100.0, 200.0),)),
                ("curveTo", ((100.0, 100.0),
                             (250.0, 100.0),
                             (250.0, 200.0))),
                ("curveTo", ((250.0, 300.0),
                             (400.0, 300.0),
                             (400.0, 200.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M100,200 C100,100 400,100 400,200",
            [
                ("moveTo", ((100.0, 200.0),)),
                ("curveTo", ((100.0, 100.0),
                             (400.0, 100.0),
                             (400.0, 200.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M100,500 C25,400 475,400 400,500",
            [
                ("moveTo", ((100.0, 500.0),)),
                ("curveTo", ((25.0, 400.0),
                             (475.0, 400.0),
                             (400.0, 500.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M100,800 C175,700 325,700 400,800",
            [
                ("moveTo", ((100.0, 800.0),)),
                ("curveTo", ((175.0, 700.0),
                             (325.0, 700.0),
                             (400.0, 800.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M600,200 C675,100 975,100 900,200",
            [
                ("moveTo", ((600.0, 200.0),)),
                ("curveTo", ((675.0, 100.0),
                             (975.0, 100.0),
                             (900.0, 200.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M600,500 C600,350 900,650 900,500",
            [
                ("moveTo", ((600.0, 500.0),)),
                ("curveTo", ((600.0, 350.0),
                             (900.0, 650.0),
                             (900.0, 500.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M600,800 C625,700 725,700 750,800 S875,900 900,800",
            [
                ("moveTo", ((600.0, 800.0),)),
                ("curveTo", ((625.0, 700.0),
                             (725.0, 700.0),
                             (750.0, 800.0))),
                ("curveTo", ((775.0, 900.0),
                             (875.0, 900.0),
                             (900.0, 800.0))),
                ("endPath", ()),
            ]
        ),
        (
            "M200,300 Q400,50 600,300 T1000,300",
            [
                ("moveTo", ((200.0, 300.0),)),
                ("qCurveTo", ((400.0, 50.0),
                              (600.0, 300.0))),
                ("qCurveTo", ((800.0, 550.0),
                              (1000.0, 300.0))),
                ("endPath", ()),
            ]
        ),
        # End examples from SVG spec

        # Relative moveto
        (
            "M 0 0 L 50 20 m 50 80 L 300 100 L 200 300 z",
            [
                ("moveTo", ((0.0, 0.0),)),
                ("lineTo", ((50.0, 20.0),)),
                ("endPath", ()),
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # Initial smooth and relative curveTo
        (
            "M100,200 s 150,-100 150,0",
            [
                ("moveTo", ((100.0, 200.0),)),
                ("curveTo", ((100.0, 200.0),
                             (250.0, 100.0),
                             (250.0, 200.0))),
                ("endPath", ()),
            ]
        ),
        # Initial smooth and relative qCurveTo
        (
            "M100,200 t 150,0",
            [
                ("moveTo", ((100.0, 200.0),)),
                ("qCurveTo", ((100.0, 200.0),
                              (250.0, 200.0))),
                ("endPath", ()),
            ]
        ),
        # relative l command
        (
            "M 100 100 L 300 100 l -100 200 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # relative q command
        (
            "M200,300 q200,-250 400,0",
            [
                ("moveTo", ((200.0, 300.0),)),
                ("qCurveTo", ((400.0, 50.0),
                              (600.0, 300.0))),
                ("endPath", ()),
            ]
        ),
        # absolute H command
        (
            "M 100 100 H 300 L 200 300 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # relative h command
        (
            "M 100 100 h 200 L 200 300 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((300.0, 100.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # absolute V command
        (
            "M 100 100 V 300 L 200 300 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((100.0, 300.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # relative v command
        (
            "M 100 100 v 200 L 200 300 z",
            [
                ("moveTo", ((100.0, 100.0),)),
                ("lineTo", ((100.0, 300.0),)),
                ("lineTo", ((200.0, 300.0),)),
                ("lineTo", ((100.0, 100.0),)),
                ("closePath", ()),
            ]
        ),
        # absolute A command, arc 1
        (
            "M 100 100 A 150 150 0 1 0 150 -150 z",
            [
                ('moveTo', ((100.0, 100.0),)),
                ('qCurveTo', ((217.17583, 139.78681),
                              (324.37829, 77.97418),
                              (348.64695, -43.36913),
                              (273.46493, -141.65865),
                              (150.0, -150.0))),
                ('lineTo', ((100.0, 100.0),)),
                ('closePath', ()),
            ]
        ),
        # relative A command
        (
            "M 100 100 a 150 150 0 1 0 150 -150",
            [
                ('moveTo', ((100.0, 100.0),)),
                ('qCurveTo', ((161.832212, 221.352549),
                              (296.3525491, 242.6584774),
                              (392.6584774, 146.35254915),
                              (371.3525491, 11.83221215),
                              (250.0, -50.0))),
                ('endPath', ())
            ]
        ),
        # absolute A command, arc 1, sweap 1, rotation 30
        (
            "M 100 100 A 150 150 30 1 1 150 -150 z",
            [
                ('moveTo', ((100.0, 100.0),)),
                ('qCurveTo', ((-23.46493, 91.65865),
                              (-98.6469560, -6.63086811),
                              (-74.3782932, -127.97418174),
                              (32.8241612, -189.786813),
                              (150.0, -150.0))),
                ('lineTo', ((100.0, 100.0),)),
                ('closePath', ()),
            ]
        ),
        # absolute A command, arc 1, sweap 1, rotation 30, end == start
        (
            "M 100 100 A 150 150 30 1 1 100 100 z",
            [
                ('moveTo', ((100.0, 100.0),)),
                ('qCurveTo', ((-42.6584408, -3.64747653),
                              (11.832264448, -171.3525544),
                              (188.16782558, -171.352554),
                              (242.65853078, -3.647476),
                              (100.0, 100.0))),
                ('lineTo', ((100.0, 100.0),)),
                ('closePath', ()),
            ]
        ),
    ]
)

def test_parse_path(pathdef, expected):
    pen = RecordingPen()
    parse_path(pathdef, pen)

    assert len(pen.value) == len(expected)
    for (instr, coords), (exp_instr, exp_coords) in zip(pen.value, expected):
        assert instr == exp_instr
        assert len(coords) == len(exp_coords)
        for c, e in zip(coords, exp_coords):
            assert c == pytest.approx(e)

@pytest.mark.parametrize(
    "pathdef1, pathdef2",
    [
        # don't need spaces between numbers and commands
        (
            "M 100 100 L 200 200",
            "M100 100L200 200",
        ),
        # repeated implicit command
        (
            "M 100 200 L 200 100 L -100 -200",
            "M 100 200 L 200 100 -100 -200"
        ),
        # don't need spaces before a minus-sign
        (
            "M100,200c10-5,20-10,30-20",
            "M 100 200 c 10 -5 20 -10 30 -20"
        ),
        # closed paths have an implicit lineTo if they don't
        # end on the same point as the initial moveTo
        (
            "M 100 100 L 300 100 L 200 300 z",
            "M 100 100 L 300 100 L 200 300 L 100 100 z"
        )
    ]
)
def test_equivalent_paths(pathdef1, pathdef2):
    pen1 = RecordingPen()
    parse_path(pathdef1, pen1)

    pen2 = RecordingPen()
    parse_path(pathdef2, pen2)

    assert pen1.value == pen2.value


def test_exponents():
    # It can be e or E, the plus is optional, and a minimum of +/-3.4e38 must be supported.
    pen = RecordingPen()
    parse_path("M-3.4e38 3.4E+38L-3.4E-38,3.4e-38", pen)
    expected = [
        ("moveTo", ((-3.4e+38, 3.4e+38),)),
        ("lineTo", ((-3.4e-38, 3.4e-38),)),
        ("endPath", ()),
    ]

    assert pen.value == expected


def test_invalid_implicit_command():
    with pytest.raises(ValueError) as exc_info:
        parse_path("M 100 100 L 200 200 Z 100 200", RecordingPen())
    assert exc_info.match("Unallowed implicit command")
