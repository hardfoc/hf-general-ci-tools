/**
 * @file geometry.c
 * @brief Implementation for the sample geometry helpers.
 */

#include "../include/geometry.h"

#include <math.h>
#include <stddef.h>

static const double PERIMETER_MULTIPLIER = 2.0;

static double clamp_non_negative(double value) { return value < 0.0 ? 0.0 : value; }

double geometry_rectangle_area(double width, double height) {
  width = clamp_non_negative(width);
  height = clamp_non_negative(height);
  return width * height;
}

double geometry_rectangle_perimeter(double width, double height) {
  width = clamp_non_negative(width);
  height = clamp_non_negative(height);
  return PERIMETER_MULTIPLIER * (width + height);
}

double geometry_hypotenuse(double leg_a, double leg_b) {
  leg_a = clamp_non_negative(leg_a);
  leg_b = clamp_non_negative(leg_b);
  return hypot(leg_a, leg_b);
}
