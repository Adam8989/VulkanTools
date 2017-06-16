@cd "C:\Program Files (x86)\Microsoft Visual Studio 14.0"
call "Common7\Tools\VsDevCmd.bat"

set VulkanTools=C:\mew\gits\github.com\mikew-lunarg\VulkanTools

set VK_INSTANCE_LAYERS=VK_LAYER_LUNARG_device_simulation

set VK_DEVSIM_FILENAME=%VulkanTools%\tests\devsim_test1.json
set VK_DEVSIM_FILENAME=%VulkanTools%\layersvt\device_simulation_examples\tiny1.json

set VK_DEVSIM_DEBUG_ENABLE=1
set VK_DEVSIM_EXIT_ON_ERROR=1
set VK_LOADER_DEBUG=all

@set PATH=C:\Program Files\CMake\bin;%PATH%

cd %VulkanTools%
set TGT_DIR=VS_BUILD
cmake -G "Visual Studio 14 Win64" -H. -B%TGT_DIR%
cd %TGT_DIR%

set VK_LAYER_PATH=%VulkanTools%\BUILD_WIN64\libs\vkjson\Debug
set VK_LAYER_PATH=%CD%\layers\Debug;%CD%\layersvt\Debug;

start VULKAN_TOOLS.sln

REM vim: set sw=4 ts=8 et ic ai:
