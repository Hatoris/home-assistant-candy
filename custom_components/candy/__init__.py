"""The Candy integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .client import CandyClient, WashingMachineStatus

from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Candy from a config entry."""

    ip_address = config_entry.data[CONF_IP_ADDRESS]
    encryption_key = config_entry.data.get(CONF_PASSWORD, "")
    use_encryption = config_entry.data.get(CONF_KEY_USE_ENCRYPTION, True)

    session = async_get_clientsession(hass)
    client = CandyClient(session, ip_address, encryption_key, use_encryption)

    async def update_status():
        try:
            async with async_timeout.timeout(40):
                status = await client.status_with_retry()
                _LOGGER.debug("Fetched status: %s", status)
                return status
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {repr(err)}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=60),
        update_method=update_status,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        DATA_KEY_COORDINATOR: coordinator
    }

    async def handle_start_program(call):
        program_key = call.data.get('program_key')
        option_key = call.data.get('option_key', 'default')
        await client.start_program(program_key, option_key)

    async def handle_stop_program(call):
        await client.stop_program()

    hass.services.async_register(
        'candy', 'start_program', handle_start_program,
        schema=vol.Schema({
            vol.Required('program_key'): str,
            vol.Optional('option_key', default='default'): str,
        })
    )

    hass.services.async_register(
        'candy', 'stop_program', handle_stop_program
    )

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN]

    return unload_ok
