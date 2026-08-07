#!/bin/bash

echo "Removing remnants from previous builds..."

rm -rf submodules/*/build
rm -rf submodules/*/*egg-info

echo "Remove successed!"

bash update_submodules.sh