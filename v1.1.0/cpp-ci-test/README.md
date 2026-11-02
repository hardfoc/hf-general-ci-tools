# C/C++ Sample Sources for CI Experiments

This directory contains small, well-documented C and C++ translation units that
exercise the C/C++ related tooling showcased in this repository:

- `include/geometry.h` and `src/geometry.c` provide a handful of geometry helper
  functions written in C.
- `include/greeter.hpp` and `src/greeter.cpp` deliver a simple C++ class used to
  model basic object-oriented behaviour.

The files include Doxygen comments and are referenced by `_config/Doxyfile`,
which means they are automatically published when you run

```
doxygen _config/Doxyfile
```

The generated documentation lands under `docs/doxygen/html`. This location is
compatible with the Jekyll + GitHub Pages setup used by the Publish Docs
workflows, so you can push the rendered artefacts alongside the rest of the
documentation if desired.
