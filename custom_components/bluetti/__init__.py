"""The BLUETTI integration."""
# from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from . import api
from .models import BluettiData

_LOGGER = logging.getLogger(__name__)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.LIGHT]

# Create ConfigEntry type alias with ConfigEntryAuth or AsyncConfigEntryAuth object
type BluettiConfigEntry = ConfigEntry[BluettiData]
# type Oauth2ConfigEntry = ConfigEntry[api.AsyncConfigEntryAuth]


async def async_setup_entry(hass: HomeAssistant, entry: BluettiConfigEntry) -> bool:
    """OAUTH2: get the access token."""
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )
    _LOGGER.debug("OAuth implementation is: %s", implementation.__class__)

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)

    # If using a requests-based API lib
    entry.runtime_data = api.ConfigEntryAuth(hass, session)

    # If using an aiohttp-based API lib
    # entry.runtime_data = api.AsyncConfigEntryAuth(
    #     aiohttp_client.async_get_clientsession(hass), session
    # )

    # await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: BluettiConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
