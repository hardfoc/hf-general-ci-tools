/**
 * @file greeter.cpp
 * @brief Implementation for the sample C++ greeter.
 */

#include "../include/greeter.hpp"

#include <sstream>
#include <utility>

namespace ci_demo {

Greeter::Greeter(std::string salutation) : salutation_(std::move(salutation)) {}

Greeter::Greeter() : salutation_("Hello") {}

std::string Greeter::greet(const std::string& name) const {
  std::ostringstream stream;
  stream << salutation_;
  if (!salutation_.empty() && !name.empty()) {
    stream << ", ";
  }
  stream << name;
  if (!name.empty()) {
    stream << "!";
  }
  return stream.str();
}

void Greeter::set_salutation(std::string salutation) { salutation_ = std::move(salutation); }

const std::string& Greeter::salutation() const noexcept { return salutation_; }

}  // namespace ci_demo
