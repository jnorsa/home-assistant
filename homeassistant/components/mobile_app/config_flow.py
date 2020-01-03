"""Config flow for Mobile App."""
from homeassistant import config_entries
from homeassistant.components import person
from homeassistant.helpers import entity_registry

from .const import ATTR_DEVICE_ID, ATTR_DEVICE_NAME, CONF_USER_ID, DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class MobileAppFlowHandler(config_entries.ConfigFlow):
    """Handle a Mobile App config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        placeholders = {
            "apps_url": "https://www.home-assistant.io/components/mobile_app/#apps"
        }

        return self.async_abort(
            reason="install_app", description_placeholders=placeholders
        )

    async def async_step_registration(self, user_input=None):
        """Handle a flow initialized during registration."""
        # Register device tracker entity and add to person registering app
        ent_reg = await entity_registry.async_get_registry(self.hass)
        devt_entry = ent_reg.async_get_or_create(
            "device_tracker",
            DOMAIN,
            user_input[ATTR_DEVICE_ID],
            suggested_object_id=user_input[ATTR_DEVICE_NAME],
        )
        await person.async_add_user_device_tracker(
            self.hass, user_input[CONF_USER_ID], devt_entry.entity_id
        )

        return self.async_create_entry(
            title=user_input[ATTR_DEVICE_NAME], data=user_input
        )
