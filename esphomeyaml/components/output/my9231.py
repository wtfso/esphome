import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import output
from esphomeyaml.components.my9231 import MY9231OutputComponent
from esphomeyaml.const import CONF_CHANNEL, CONF_ID, CONF_MY9231_ID, CONF_POWER_SUPPLY
from esphomeyaml.helpers import Pvariable, get_variable

DEPENDENCIES = ['my9231']

Channel = MY9231OutputComponent.Channel

PLATFORM_SCHEMA = output.FLOAT_OUTPUT_PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID): cv.declare_variable_id(Channel),
    vol.Required(CONF_CHANNEL): vol.All(vol.Coerce(int),
                                        vol.Range(min=0, max=65535)),
    cv.GenerateID(CONF_MY9231_ID): cv.use_variable_id(MY9231OutputComponent),
})


def to_code(config):
    power_supply = None
    if CONF_POWER_SUPPLY in config:
        for power_supply in get_variable(config[CONF_POWER_SUPPLY]):
            yield
    my9231 = None
    for my9231 in get_variable(config[CONF_MY9231_ID]):
        yield
    rhs = my9231.create_channel(config[CONF_CHANNEL], power_supply)
    out = Pvariable(config[CONF_ID], rhs)
    output.setup_output_platform(out, config, skip_power_supply=True)


BUILD_FLAGS = '-DUSE_MY9231_OUTPUT'