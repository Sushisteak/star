"""Support for STAR API."""
import logging
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    CONF_BUS_NUMBER,
    CONF_STOP,
    CONF_DIRECTION,
    LINE_API_URL,
    DIRECTIONS_API_URL,
    ARRETS_API_URL
)

_LOGGER = logging.getLogger(__name__)

class StarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle configuration of STAR integration."""
    VERSION = 1

    # Etape 1 - API + n° bus
    async def async_step_user(self, user_input=None) -> FlowResult:
        """Get the API token and line number."""
        errors = {}

        if user_input is not None:
            self._user_data = user_input  # stocke le choix API + ligne
            return await self.async_step_direction()

        raw_lines = await self._fetch_bus_lines()
        options = {code: f"{name}" for code, name in raw_lines}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_BUS_NUMBER): vol.In(options),
            }),
            errors=errors,
        )

    # Etape 2 - Direction de la ligne choisie
    async def async_step_direction(self, user_input=None):
        """Get the direction of the line."""
        errors = {}

        try:
            bus_number = self._user_data[CONF_BUS_NUMBER]
            _LOGGER.debug("Bus selected in previous step: %s", bus_number)
            directions = await self._fetch_directions(bus_number)

            if not directions:
                errors["base"] = "no_directions_found"
                return self.async_show_form(
                    step_id="direction",
                    data_schema=vol.Schema({}),
                    errors=errors,
                )

            directions = await self._fetch_directions(bus_number)

            # Crée les dictionnaires nécessaires
            direction_options = {}
            direction_arrivals = {}
            for direction_id, label, arrival in directions:
                direction_options[direction_id] = label
                direction_arrivals[direction_id] = arrival

            if user_input is not None:
                _LOGGER.debug("User selected direction: %s", user_input)
                direction_id = user_input[CONF_DIRECTION]

                self._user_data.update({
                    CONF_DIRECTION: direction_id,
                    "direction_label": direction_options[direction_id],
                    "direction_arrival_stop": direction_arrivals[direction_id],
                })
                return await self.async_step_stop()

            return self.async_show_form(
                step_id="direction",
                data_schema=vol.Schema({
                    vol.Required(CONF_DIRECTION): vol.In(direction_options),
                }),
                errors=errors,
            )

        except Exception as e:
            _LOGGER.exception("Unexpected error in async_step_direction")
            errors["base"] = "unknown"
            return self.async_show_form(
                step_id="direction",
                data_schema=vol.Schema({}),
                errors=errors,
            )

    # Etape 3 - Arret + interval
    async def async_step_stop(self, user_input=None):
        """Get the stop of the line to monitor."""
        errors = {}

        idparcours = self._user_data[CONF_DIRECTION]
        stops = await self._fetch_stops(idparcours)

        if not stops:
            errors["base"] = "no_stops_found"
            return self.async_show_form(
                step_id="stop",
                data_schema=vol.Schema({}),
                errors=errors,
            )

        stop_options = {stop: stop for stop in stops}

        if user_input is not None:
            self._user_data.update(user_input)
            title = f"{self._user_data[CONF_BUS_NUMBER]} - {self._user_data[CONF_STOP]} → \
                {self._user_data['direction_arrival_stop']}"
            return self.async_create_entry(title=title, data=self._user_data)

        return self.async_show_form(
            step_id="stop",
            data_schema=vol.Schema({
                vol.Required(CONF_STOP): vol.In(stop_options),
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
            }),
            errors=errors,
        )

    # Récupération des lignes pour l'étape 1
    async def _fetch_bus_lines(self) -> dict[str, str]:
        """Call STAR API to get all the lines."""
        async with aiohttp.ClientSession() as session:
            async with session.get(LINE_API_URL) as resp:
                data = await resp.json()
                return [
                    (item["nomcourt"], f'{item["nomcourt"]} - {item["nomlong"]}')
                    for item in data.get("results", [])
                ]

    # Récupération des directions de la ligne choisie pour l'étape 2
    async def _fetch_directions(self, nomcourt: str) -> list[tuple[str, str]]:
        """Call STAR API to get all direction of one line."""
        _LOGGER.debug("Fetching directions for line: %s", nomcourt)
        async with aiohttp.ClientSession() as session:
            async with session.get(DIRECTIONS_API_URL.format(ligne=nomcourt)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Direction API error %s: %s", resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.debug("Directions API result: %s", data)
                return [
                    (item["id"], item["libellelong"], item["nomarretarrivee"])
                    for item in data.get("results", [])
                ]

    # Récupération des arrêts de la ligne choisie pour l'étape 3
    async def _fetch_stops(self, idparcours: str) -> list[str]:
        """Call STAR API to get all stops of one line."""
        _LOGGER.debug("Fetching stops for parcours: %s", idparcours)
        async with aiohttp.ClientSession() as session:
            async with session.get(ARRETS_API_URL.format(parcours=idparcours)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Stops API error %s: %s", resp.status, text)
                    return []
                data = await resp.json()
                return [item["nomarret"] for item in data.get("results", [])]
