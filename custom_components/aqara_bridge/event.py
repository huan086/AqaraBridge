from homeassistant.components.event import EventEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    BUTTON,
    CUBE,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
)
import logging

_LOGGER = logging.getLogger(__name__)

TYPE = "event"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {"default": AiotButtonEntity}
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotButtonEntity(AiotEntityBase, EventEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_event_types = list(BUTTON.values())
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    @property
    def icon(self):
        """return icon."""
        return "mdi:button-pointer"

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "firmware_version":
            return res_value
        if res_name == "zigbee_lqi":
            return int(res_value)
        if res_name == "button" and res_value not in (0, ""):
            trigger = BUTTON.get(res_value, "unknown")
            self._trigger_event(trigger)
            self.schedule_update_ha_state()
        return super().convert_res_to_attr(res_name, res_value)
