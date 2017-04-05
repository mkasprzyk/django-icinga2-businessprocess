from django.test import TestCase

from .models import VirtualMachine
from .models import Environment, ConfigItem
from .utils import Icinga2BPConfigMeta, BusinessProcessConfig, Icinga2BPConfigRenderer

from model_mommy import mommy


class TestIcinga2BusinessProcessConfiguration(TestCase):
    def setUp(self):
        self.bpc = BusinessProcessConfig(
            Icinga2BPConfigMeta('ENV', 'ENV Monitoring', 'superadmin')
        )

        self.config_zyx = mommy.make(ConfigItem,
            condition='|',
            name='XYZ',
            data={}
        )

        self.config_SUPERCOMPONENT = mommy.make(ConfigItem,
            condition='&',
            name='SUPERCOMPONENT',
            data={},
        )

        self.config_SUB_COMPONENT = mommy.make(ConfigItem,
            condition='|',
            name='SUB_COMPONENT',
            data={},
        )

        self.config_component = mommy.make(ConfigItem,
            condition='|',
            name='COMPONENT',
            data={},
        )

        self.config_env021 = mommy.make(ConfigItem,
            name='env021',
            data={},
        )

        self.config_env022 = mommy.make(ConfigItem,
            name='env022',
            data={},
        )


        self.config_zyx.add_child(self.config_SUPERCOMPONENT)

        self.config_SUPERCOMPONENT.add_child(self.config_SUB_COMPONENT)
        self.config_SUPERCOMPONENT.add_child(self.config_component)

        self.config_SUB_COMPONENT.add_child(self.config_env021)
        self.config_SUB_COMPONENT.add_child(self.config_env022)

        self.bpc.add_node(self.config_zyx)


    def test_render(self):
        renderer = Icinga2BPConfigRenderer(self.bpc)
        print(renderer.render())

