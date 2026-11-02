// Known findings, built only with HOST_CI_SEED_FINDINGS=ON.
#include <string>

// performance-unnecessary-value-param (clang-tidy)
std::size_t seeded_length(std::string text) { return text.size(); }

// arrayIndexOutOfBounds (cppcheck)
int seeded_read() {
  int values[2] = {1, 2};
  return values[2];
}
