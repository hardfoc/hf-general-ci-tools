#ifndef GEOMETRY_H
#define GEOMETRY_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @file geometry.h
 * @brief Geometry utility helpers that exercise the C pipeline.
 *
 * The functions in this header are intentionally simple so they can be used
 * for smoke-testing compilers, linters, and static analysis tools in CI.
 */

/**
 * @brief Compute the area of a rectangle.
 *
 * @param width  Width of the rectangle, must be non-negative.
 * @param height Height of the rectangle, must be non-negative.
 * @return The computed area.
 */
double geometry_rectangle_area(double width, double height);

/**
 * @brief Compute the perimeter of a rectangle.
 *
 * @param width  Width of the rectangle, must be non-negative.
 * @param height Height of the rectangle, must be non-negative.
 * @return The computed perimeter.
 */
double geometry_rectangle_perimeter(double width, double height);

/**
 * @brief Compute the length of the hypotenuse using the Pythagorean theorem.
 *
 * @param leg_a Length of the first leg.
 * @param leg_b Length of the second leg.
 * @return The length of the hypotenuse.
 */
double geometry_hypotenuse(double leg_a, double leg_b);

#ifdef __cplusplus
}
#endif

#endif /* GEOMETRY_H */
