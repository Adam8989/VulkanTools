set VulkanTools=C:\mew\gits\github.com\mikew-lunarg\VulkanTools

%VulkanTools%\BUILD_WIN64\demos\Debug\vulkaninfo.exe > vk0.txt
set VK_LAYER_PATH=%VulkanTools%\BUILD_WIN64\layersvt\Debug
set VK_INSTANCE_LAYERS=VK_LAYER_LUNARG_device_simulation
set VK_DEVSIM_FILENAME=%VulkanTools%\layersvt\device_simulation_examples\tiny1.json
set VK_DEVSIM_DEBUG_ENABLE=1
%VulkanTools%\BUILD_WIN64\demos\Debug\vulkaninfo.exe > vk1.txt
pause

:: vim: set sw=4 ts=8 et ic ai:
