#!/usr/bin/env python3

import click
import decimal
import drawSvg as draw
import math


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--diameter",
    "-d",
    help="Outer diameter (in inches)",
    type=click.FLOAT,
    required=True,
)
@click.option(
    "--with-dots/--without-dots", help="Include light-scattering dots.", default=False
)
def main(diameter, with_dots):
    """Generate laser-cuttable lenses for edge-lit LED lights."""
    MARGIN_IN = 0.1
    DIMPLE_SPACING_IN = "0.08" # suggest using "0.04"
    DIMPLE_RADIUS_IN = 0.02 # suggest using 0.01

    d = draw.Drawing(diameter, diameter, origin="center", displayInline=False)

    # Draw a circle
    d.append(
        draw.Circle(
            0, 0, (diameter / 2), fill="none", stroke_width=0.005, stroke="blue"
        )
    )

    if with_dots:
        for x in drange(-math.ceil(diameter), math.ceil(diameter), DIMPLE_SPACING_IN):
            for y in drange(
                -math.ceil(diameter), math.ceil(diameter), DIMPLE_SPACING_IN
            ):
                if (x ** 2 + y ** 2) < (((diameter / 2) - MARGIN_IN) ** 2):
                    # point is inside circle
                    d.append(
                        draw.Circle(x, y, DIMPLE_RADIUS_IN, fill="black", stroke="none")
                    )

    d.setPixelScale(72)  # Set number of pixels per geometry unit
    d.saveSvg("output.svg")


if __name__ == "__main__":
    main()
