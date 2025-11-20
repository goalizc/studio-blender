#!/bin/bash
#
# Bash script that creates a single ZIP file containing the full code of
# Skybrush Studio for Blender so it can simply be extracted in the
# Blender addons folder.
#
# It also creates standalone executables for Blender if the Skybrush Studio
# bootloader is accessible on your system.
#
# You need to install Python 3 and poetry in order to use this script; both
# of them must be accessible on the system path in order for the script to
# succeed.

VENV_DIR=".venv-`uname`"
OUTPUT_DIR="./dist"
MINIFY=1
SKIP_BOOTLOADER=1

###############################################################################

set -e

SCRIPT_ROOT=`dirname $0`
REPO_ROOT="${SCRIPT_ROOT}/../.."

cd "${REPO_ROOT}"

# Check whether the bootloader is present on the system
BOOTLOADER_DIR=${BOOTLOADER_DIR:-"${REPO_ROOT}/../sbstudio-bootloader/dist"}
if [ "x${SKIP_BOOTLOADER}" = x1 -o ! -d "${BOOTLOADER_DIR}" -o ! -f "${BOOTLOADER_DIR}/sbstudio-bootloader-linux" ]; then
    BOOTLOADER_DIR=
fi

# Extract the name of the project and the version number from pyproject.toml
PROJECT_NAME=`cat pyproject.toml|grep ^name|head -1|cut -d '"' -f 2`
VERSION=`cat pyproject.toml|grep ^version|head -1|cut -d '"' -f 2`

# Remove all requirements.txt files, we don't use them, only poetry
rm -f requirements*.txt

# Generate requirements.txt from poetry
poetry export -f requirements.txt -o requirements.txt --without-hashes
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
  cython_files=(
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/algorithm.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/base.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/api/console.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/calculate_safe_path.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/create_real_frame_data.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/custom_color.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/export_to_hh.py"
    "${BUILD_DIR}/vendor/skybrush/sbstudio/plugin/operators/validate_trajectories.py"
  )
  export INCLUDE="C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\VS\include;C:\Program Files (x86)\Windows Kits\10\include\10.0.20348.0\ucrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.20348.0\um;C:\Program Files (x86)\Windows Kits\10\include\10.0.20348.0\shared;C:\Program Files (x86)\Windows Kits\10\include\10.0.20348.0\winrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.20348.0\cppwinrt;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\include\um"
  export LIB="C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\lib\x64;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\lib\um\x64;C:\Program Files (x86)\Windows Kits\10\lib\10.0.20348.0\ucrt\x64;C:\Program Files (x86)\Windows Kits\10\lib\10.0.20348.0\um\x64"
  export LIBPATH="C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\lib\x64;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\lib\x86\store\references;C:\Program Files (x86)\Windows Kits\10\UnionMetadata\10.0.20348.0;C:\Program Files (x86)\Windows Kits\10\References\10.0.20348.0;C:\Windows\Microsoft.NET\Framework\v4.0.30319"
  export Path="C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\HostX86\x64;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\HostX86\x86;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\VC\VCPackages;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TestWindow;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer;C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\bin\Roslyn;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Common\VSPerfCollectionTools\vs2019\\x64;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Common\VSPerfCollectionTools\vs2019\;C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\FSharp\Tools;C:\Program Files\Microsoft Visual Studio\2022\Community\Team Tools\DiagnosticsHub\Collector;C:\Program Files (x86)\Windows Kits\10\bin\10.0.20348.0\\x86;C:\Program Files (x86)\Windows Kits\10\bin\\x86;C:\Program Files\Microsoft Visual Studio\2022\Community\\MSBuild\Current\Bin\amd64;C:\Windows\Microsoft.NET\Framework\v4.0.30319;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\Bandizip\;C:\Program Files\Common Files\Autodesk Shared\;C:\Program Files\dotnet\;C:\Users\goalizc\AppData\Local\Programs\Python\Python311\Scripts\;C:\Users\goalizc\AppData\Local\Programs\Python\Python311\;C:\Users\goalizc\AppData\Local\Programs\Python\Python310\Scripts\;C:\Users\goalizc\AppData\Local\Programs\Python\Python310\;C:\Users\goalizc\AppData\Local\Microsoft\WindowsApps;C:\Users\goalizc\.dotnet\tools;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\VC\Linux\bin\ConnectionManagerExe"
  for pyfile in ${cython_files[*]}; do
    echo "--> Compiling cython module: $pyfile"
    pydir=${pyfile}.cython
    mkdir ${pydir} && mv ${pyfile} ${pydir} && cd ${pydir}
  # "C:\Users\goalizc\AppData\Local\Programs\Python\Python310\python.exe" -c "from distutils.core import setup; from Cython.Build import cythonize; setup(ext_modules=cythonize('`basename ${pyfile}`', compiler_directives={'language_level': '3'}))" build_ext -b .. > /dev/null 2>&1
    "C:\Users\goalizc\AppData\Local\Programs\Python\Python311\python.exe" -c "from distutils.core import setup; from Cython.Build import cythonize; setup(ext_modules=cythonize('`basename ${pyfile}`', compiler_directives={'language_level': '3'}))" build_ext -b .. > /dev/null 2>&1
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
  for file in `find ${BUILD_DIR}/vendor/skybrush/sbstudio -name "*.py"`; do
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
( cd "${OUTPUT_DIR}/${ZIP_STEM}"; rm -f "../${ZIP_STEM}.zip" && zip -q -r "../${ZIP_STEM}.zip" * )
rm -rf "${OUTPUT_DIR}/${ZIP_STEM}"
echo "done."

if [ "x${BOOTLOADER_DIR}" != x ]; then
    echo -n "--> Creating executables... "

    # pyminifier only needed here, but we need our patched version that works
    # with Python 3
    ${VENV_DIR}/bin/pip install -q -U pyminifier>=3.0.0

    # Create a single-file Python entry point
    cat ${BUILD_DIR}/ui_skybrush_studio.py | sed -n '/BLENDER ADD-ON INFO ENDS HERE/,$p' >${BUILD_DIR}/entrypoint.py
    cat >>${BUILD_DIR}/entrypoint.py <<EOF

register()

from sbstudio.plugin.api import set_fallback_api_key, get_api
set_fallback_api_key("NNAs8w.hApopcx8s68YZAuRAGofbboqzFwx7KikdT0Q")
EOF
    PYTHONPATH=vendor ${VENV_DIR}/bin/python -m stickytape.main ${BUILD_DIR}/entrypoint.py \
        --add-python-path ${BUILD_DIR}/vendor/skybrush \
        --add-python-module sbstudio.plugin.utils.platform \
        --add-python-module natsort \
        >${OUTPUT_DIR}/${ZIP_STEM}.py.orig
    if [ "x${MINIFY}" = x1 ]; then
      ${VENV_DIR}/bin/pyminifier --gzip ${OUTPUT_DIR}/${ZIP_STEM}.py.orig >${OUTPUT_DIR}/${ZIP_STEM}.py
      rm ${OUTPUT_DIR}/${ZIP_STEM}.py.orig
    else
      mv ${OUTPUT_DIR}/${ZIP_STEM}.py.orig ${OUTPUT_DIR}/${ZIP_STEM}.py
    fi

    # Attach the single-file entry point to the bootloader(s)
    ${VENV_DIR}/bin/python etc/scripts/_append_to_bootloader.py \
        --bootloader-dir "${BOOTLOADER_DIR}" \
        --output-dir ${OUTPUT_DIR} \
        ${OUTPUT_DIR}/${ZIP_STEM}.py

    # Remove the single-file entry point, not needed any more
    rm ${OUTPUT_DIR}/${ZIP_STEM}.py

    echo "done."

    # Create macOS launcher app in a disk image
    echo -n "--> Creating macOS disk image... "
    etc/scripts/_build_macos_dmg.sh "${BUILD_DIR}" "${OUTPUT_DIR}" >/dev/null 2>/dev/null
    echo "done."
else
    echo "[-] Skipping executables - no bootloader code present."
fi

# Clean up after ourselves
rm -rf "${BUILD_DIR}"

echo ""
echo "------------------------------------------------------------------------"
echo ""
echo "Bundle created successfully in ${OUTPUT_DIR}/${ZIP_STEM}.zip"
if [ "x${BOOTLOADER_DIR}" != x ]; then
    echo "Single-file Windows executable created successfully in ${OUTPUT_DIR}/${ZIP_STEM}-win64.exe"
    echo "macOS launcher created successfully in ${OUTPUT_DIR}"
fi
