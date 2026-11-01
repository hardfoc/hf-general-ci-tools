#ifndef GREETER_HPP
#define GREETER_HPP

#include <string>

/**
 * @file greeter.hpp
 * @brief Sample C++ class that demonstrates basic documentation coverage.
 */

namespace ci_demo {

/**
 * @brief A simple greeter that can generate salutations for arbitrary names.
 */
class Greeter {
public:
  /**
   * @brief Construct the greeter with a salutation prefix.
   *
   * @param salutation Phrase that appears at the beginning of each greeting.
   */
  explicit Greeter(std::string salutation);

  /**
   * @brief Construct the greeter with default "Hello" salutation.
   */
  Greeter();

  /**
   * @brief Produce a greeting for the provided name.
   *
   * @param name Recipient of the greeting.
   * @return A formatted greeting.
   */
  [[nodiscard]] std::string greet(const std::string& name) const;

  /**
   * @brief Update the salutation prefix used in greetings.
   *
   * @param salutation New salutation to use.
   */
  void set_salutation(std::string salutation);

  /**
   * @brief Access the current salutation prefix.
   *
   * @return Reference to the underlying salutation string.
   */
  [[nodiscard]] const std::string& salutation() const noexcept;

private:
  std::string salutation_;
};

}  // namespace ci_demo

#endif /* GREETER_HPP */
