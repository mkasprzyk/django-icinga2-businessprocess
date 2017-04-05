from django.db import models 
from collections import OrderedDict



class BusinessProcessConfig(object):
    def __init__(self, meta):
        self.meta = meta
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_root_nodes(self):
        return [node for node in self.nodes if node.is_root()] 

    def get_unbound_nodes(self):
        unbound_nodes = []
        for node in self.nodes:
            if len(node.parents()):
                continue
            if node.get_display() == 0:
                unbound_nodes.append(node)
        return unbound_nodes


class Icinga2BPConfigMeta(object):
    def __init__(self, title, description, owner, add_to_menu=True, state_type='soft'):
        self.title = title
        self.description = description
        self.owner = owner
        self.add_to_menu = add_to_menu
        self.state_type = state_type

    def bool_to_decision(self, state):
        if state:
            return 'yes'
        return 'no'

    @property
    def to_dict(self):
        return OrderedDict([
            ('Title', self.title),
            ('Description', self.description),
            ('Owner', self.owner),
            ('AddToMenu', self.bool_to_decision(self.add_to_menu)),
            ('StateType', self.state_type)
        ])


class Icinga2BPConfigRenderer(object):
    def __init__(self, config):
        self.rendered_nodes = None
        self.config = config

    def render(self):
        return self.render_header() + self.render_nodes()

    def render_header(self):
        container = "### Business Process Config File ###\n#\n"
        for key, value in self.config.meta.to_dict.items():
            if not value:
                continue
            container += '# {0:15}: {1}\n'.format(key, value)
        container += "#\n###################################\n\n"
        return container

    def render_nodes(self):
        self.rendered_nodes = {}
        container = str()
        for node in self.config.get_root_nodes():
            container += self.require_rendered_bp_node(node)
        for node in self.config.get_unbound_nodes():
            container += self.require_rendered_bp_node(node)
        container += '\n'
        return container
            
    def require_rendered_bp_node(self, node):
        if node.name in self.rendered_nodes:
            return ''
        else:
            self.rendered_nodes[node.name] = True
            return self.render_bp_node(node)

    def render_bp_node(self, node):
        container = str()
        for child in node.get_child_bp_nodes():
            container += self.require_rendered_bp_node(child)
            container += '\n'
        container += self.render_single_bp_node(node)
        return container
    
    def render_equal_sign(self, node):
        if type(node.operator) == int():
            return '= {} of:'.format(node.operator)
        else:
            return '='

    def render_operator(self, node):
        if type(node.operator) == int():
            return '+'
        else:
            return node.operator

    def render_single_bp_node(self, node):
        container = str()
        container += self.render_expression(node)
        container += self.render_display(node)
        container += self.render_info_url(node)
        return container

    def render_expression(self, node):
        return '{} {} {}\n'.format(
            node.name,
            self.render_equal_sign(node),
            self.render_child_names(node),
        )
        
    def render_child_names(self, node):
        operator = ' {} '.format(self.render_operator(node))
        childrens = node.get_child_names()
        container = operator.join(childrens)
        print(childrens)
        print(container)
        if (len(childrens) < 2) and (operator != '&'):
            return operator + ' ' + container
        else:
            return container

    def render_display(self, node):
        if node.has_alias() or node.get_display() > 0:
            priority = node.get_display()
            return 'display {};{};{}\n'.format(priority, node.name, node.alias)
        return ''

    def render_info_url(self, node):
        if node.has_info_url():
            return 'info_url {};{}\n'.format(node.name, node.info_url)
        return ''

