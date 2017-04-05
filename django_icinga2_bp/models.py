from django.db import models



class Icinga2BusinessProcessNodeMixin(models.Model):

    @property
    def operator(self):
        return self.condition

    @property
    def info_url(self):
        return self.data.get('info_url')

    @property
    def alias(self):
        return self.data.get('alias', self.name)

    def has_info_url(self):
        return bool(self.info_url)

    def has_alias(self):
        return bool(self.alias)

    def get_display(self):
        if self.is_root():
            return 1
        return 0

    def get_child_bp_nodes(self):
        bp_nodes = list(self.descendants_set())
        return bp_nodes

    def get_child_names(self):
        return [child.name for child in self.children.all()]

    class Meta:
        abstract = True


class Icinga2BusinessProcessConditionMixin(
    models.Model
):

    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    DEG = 'DEG'

    BUSINESS_PROCESS_CONDITIONS = (
        (AND, '&'),
        (OR,  '|'),
        (NOT, '!'),
        (DEG, '<'),
        ('1', 'MIN 1'),
        ('2', 'MIN 2'),
        ('3', 'MIN 3'),
        ('4', 'MIN 4'),
        ('5', 'MIN 5'),
        ('6', 'MIN 6'),
        ('7', 'MIN 7'),
        ('8', 'MIN 8'),
        ('9', 'MIN 9'),
    )

    condition = models.CharField(
        max_length=3,
        unique=False,
        null=True,
        blank=True,
        choices=BUSINESS_PROCESS_CONDITIONS,
        default='|',
        verbose_name='Icinga2 business process condition'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.condition
