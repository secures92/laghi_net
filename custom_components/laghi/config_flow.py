"""Config flow for the Laghi.net integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import AVAILABLE_LAKES, CONF_LAKES, DOMAIN


_LAKE_OPTIONS = [SelectOptionDict(value=lake, label=lake) for lake in AVAILABLE_LAKES]

_LAKES_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=_LAKE_OPTIONS,
        multiple=True,
        mode=SelectSelectorMode.LIST,
    )
)


class LaghiConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Laghi.net."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        # Only allow a single instance
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Laghi.net", data={}, options=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_LAKES, default=list(AVAILABLE_LAKES)): _LAKES_SELECTOR,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the options flow."""
        return LaghiOptionsFlow()


class LaghiOptionsFlow(OptionsFlow):
    """Handle options for Laghi.net."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current_lakes = self.config_entry.options.get(CONF_LAKES, AVAILABLE_LAKES)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_LAKES, default=list(current_lakes)): _LAKES_SELECTOR,
                }
            ),
        )
