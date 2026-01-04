#!/bin/bash
#
# Bash script that creates a single ZIP file containing the full code of
# Skybrush Studio for Blender so it can simply be extracted in the
# Blender addons folder.
#
# It also creates standalone executables for Blender if the Skybrush Studio
# bootloader is accessible on your system.
#
# You need to install Python 3 and uv in order to use this script; both
# of them must be accessible on the system path in order for the script to
# succeed.

VENV_DIR=".venv-`uname`"
OUTPUT_DIR="./dist"
MINIFY=1

###############################################################################

set -e

SCRIPT_ROOT=$(dirname $0)
REPO_ROOT="${SCRIPT_ROOT}/../.."

cd "${REPO_ROOT}"

# Extract the name of the project and the version number from pyproject.toml
PROJECT_NAME=$(cat pyproject.toml | grep ^name | head -1 | cut -d '"' -f 2)
VERSION=$(cat pyproject.toml | grep ^version | head -1 | cut -d '"' -f 2)

# Remove all requirements.txt files, we don't use them, only uv
rm -f requirements*.txt

# Generate requirements.txt from uv
uv export --no-hashes --no-emit-project --format requirements-txt >requirements.txt
trap "rm -f requirements.txt" EXIT

# Log requirements for debugging purposes
echo "[>] List of requirements"
cat requirements.txt
echo ""

# Create virtual environment if it doesn't exist yet
if [ ! -d ${VENV_DIR} ]; then
  echo -n "--> Creating virtual environment... "
  python3 -m venv ${VENV_DIR}
  echo "done."
fi

# Create build folder
BUILD_DIR="${OUTPUT_DIR}/build"
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/vendor/skybrush"

echo "[>] Installing dependencies"
${VENV_DIR}/bin/pip install -q -U pip wheel pyclean
${VENV_DIR}/bin/pip install -r requirements.txt -t "${BUILD_DIR}/vendor/skybrush"
rm -rf "${BUILD_DIR}/vendor/skybrush/bin"
echo ""

# Copy our code as well
echo -n "--> Copying addon code... "
cp -r src/modules/sbstudio ${BUILD_DIR}/vendor/skybrush
cp src/addons/ui_skybrush_studio.py ${BUILD_DIR}
echo "done."

# Compile cython modules
if [ "$OSTYPE" == "cygwin" ]; then
  pythin_exe="C:\Users\goalizc\AppData\Local\Programs\Python\Python311\python.exe"
  cython_files=(
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/algorithm.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/base.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/console.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/calculate_safe_path.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/custom_color.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/export_to_hh.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/hhang_operators.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/import_image.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/validate_trajectories.py"
  )
  for pyfile in ${cython_files[*]}; do
    echo "--> Compiling cython module: $pyfile"
    pydir=${pyfile}.cython
    mkdir ${pydir} && mv ${pyfile} ${pydir} && cd ${pydir}
    ${pythin_exe} -c "from distutils.core import setup; from Cython.Build import cythonize; setup(ext_modules=cythonize('`basename ${pyfile}`', compiler_directives={'language_level': '3'}))" build_ext -b .. > /dev/null 2>&1
    cd - > /dev/null
  done
  find ${BUILD_DIR}/vendor/skybrush -type f -name "*.pyd" | xargs upx
  find ${BUILD_DIR}/vendor/skybrush -type d -name "*.cython" | xargs rm -rf
fi

# Clean any __pycache__ and *.dist-info files
echo -n "--> Cleaning up and minifying code... "
${VENV_DIR}/bin/pyclean -q ${BUILD_DIR}
rm -rf ${BUILD_DIR}/vendor/skybrush/*.dist-info

# Strip the comments from the source code
if [ "x${MINIFY}" = x1 ]; then
  for file in $(find ${BUILD_DIR}/vendor/skybrush/sbstudio -name "*.py"); do
    if [ -s "$file" ]; then
      ${VENV_DIR}/bin/python etc/scripts/_strip_comments.py -o ${BUILD_DIR}/tmp.py > /dev/null 2>&1 $file && mv ${BUILD_DIR}/tmp.py $file
    fi
  done
fi
echo "done."

# Create a single ZIP
echo -n "--> Creating ZIP addon... "
ZIP_STEM="${PROJECT_NAME}-${VERSION}"
rm -rf "${OUTPUT_DIR}/${ZIP_STEM}"
mkdir -p "${OUTPUT_DIR}/${ZIP_STEM}"
cp -r "${BUILD_DIR}"/* "${OUTPUT_DIR}/${ZIP_STEM}"
(
  cd "${OUTPUT_DIR}/${ZIP_STEM}"
  rm -f "../${ZIP_STEM}.zip" && zip -q -r "../${ZIP_STEM}.zip" *
)
mv "${OUTPUT_DIR}/${ZIP_STEM}.zip" "${OUTPUT_DIR}"
rm -rf "${OUTPUT_DIR}/${ZIP_STEM}"
echo "done."

# Clean up after ourselves
rm -rf "${BUILD_DIR}"

echo ""
echo "------------------------------------------------------------------------"
echo ""
echo "Bundle created successfully in ${OUTPUT_DIR}/${ZIP_STEM}.zip"
