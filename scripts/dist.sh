#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

rye build --clean
version=$(rye version)
files=(dist/*.tar.gz)
for file in "${files[@]}"; do
  target=${file/-$version/}
  mv --no-target-directory --verbose "$file" "$target"
done
