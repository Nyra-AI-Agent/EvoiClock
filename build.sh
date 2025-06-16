#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status.

# --- EvoiClock Build Script for macOS using PyInstaller ---
# This script standardizes the local build process for the EvoiClock.app bundle.
# It ensures the correct Conda environment is used and all assets are included.

echo "--- EvoiClock Build Script (PyInstaller) ---"

# --- Configuration ---
CONDA_ENV_NAME="tkpy"
MAIN_SCRIPT="src/main.py"
APP_NAME="EvoiClock"
ICON="assets/EvoiClock.icns"
# Add assets and cnlunar as resources
# The format is 'source:destination_in_bundle'
ASSETS_DATA="assets:assets"
CNLUNAR_DATA="src/cnlunar:cnlunar"

# --- (1/4) Environment Checks ---
echo "\n[1/4] Checking for Conda environment '$CONDA_ENV_NAME'..."

# Check if conda is available
if ! command -v conda &> /dev/null
then
    echo "Error: conda command not found."
    echo "Please make sure Conda (or Miniforge/Anaconda) is installed and configured in your shell."
    exit 1
fi

# Check if the target environment exists
if ! conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Error: Conda environment '$CONDA_ENV_NAME' not found."
    echo "Please create it first using the instructions in DEVELOPMENT_GUIDE.md"
    exit 1
fi

echo "Environment check passed."


# --- (2/4) Cleaning up old build artifacts ---
echo "\n[2/4] Cleaning up old build artifacts..."
rm -rf dist build *.spec
echo "Cleanup complete."


# --- (3/4) Running PyInstaller build process ---
echo "\n[3/4] Running PyInstaller build process within '$CONDA_ENV_NAME' environment..."

# Run PyInstaller within the specified conda environment
conda run -n "$CONDA_ENV_NAME" pyinstaller --noconfirm --windowed --onefile \
    --name "$APP_NAME" \
    --icon "$ICON" \
    --add-data "$CNLUNAR_DATA" \
    --add-data "$ASSETS_DATA" \
    "$MAIN_SCRIPT"

echo "PyInstaller process finished."


# --- (4/4) Build Complete! ---
echo "\n[4/4] Build complete!"
echo "You can find the application bundle in the 'dist' folder:"
ls -l dist 