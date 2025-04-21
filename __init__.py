import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.device_registry import DeviceEntry
from .const import DOMAIN
from .coordinator import StarCoordinator
from dataclasses import dataclass

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type entry = ConfigEntry[RuntimeData]

@dataclass
class RuntimeData:
    """Class to hold your data."""

    coordinator: StarCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    coordinator = StarCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    entry.async_on_unload(
        entry.add_update_listener(_async_update_listener)
    )

    entry.runtime_data = RuntimeData(coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def _async_update_listener(hass: HomeAssistant, entry):
    """Handle config options update."""
    # Reload the integration when the options change.
    await hass.config_entries.async_reload(entry.entry_id)

async def async_remove_config_entry_device(
    hass: HomeAssistant, entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Delete device if selected from UI."""
    # Adding this function shows the delete device option in the UI.
    # Remove this function if you do not want that option.
    # You may need to do some checks here before allowing devices to be removed.
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when you remove your integration or shutdown HA.
    # If you have created any custom services, they need to be removed here too.

    # Unload platforms and return result
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)