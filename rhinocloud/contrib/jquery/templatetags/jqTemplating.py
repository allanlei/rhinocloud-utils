from django import template
from django.template.defaulttags import IfNode, do_if
from django.template.loader import render_to_string


register = template.Library()
        	
class JQueryTemplateNode(template.Node):
    def __init__(self, nodes, ender):
        self.nodes = nodes
        self.ender = ender
        
    def render(self, context):
        for node in self.nodes:
            node['body'] = node['body'].render(context)
        context = {
            'nodes': self.nodes,
            'ender': self.ender
        }
        return render_to_string('jquery/jqTemplate.html', context)

def jquerytemplate(parser, token, tokens, ender):
    nodes = []
    while token and token.contents != ender:
        nodeName = token.split_contents()[0]
        statement = ' '.join(token.split_contents()[1:])
        del tokens[tokens.index(nodeName)]
        nodeContent = parser.parse(tokens)
        
        nodes.append({
            'name': nodeName.replace('jq', ''),
            'statement': statement,
            'body': nodeContent,
        })
        token = parser.next_token()
    return JQueryTemplateNode(nodes, ender)

@register.tag('jqif')
def jqueryif(parser, token):
    ender = 'endjqif'
    tokens = ['jqif', 'jqelse', ender]
    return jquerytemplate(parser, token, tokens, ender)

@register.tag('jqeach')
def jqueryeach(parser, token):
    ender = 'endjqeach'
    tokens = ['jqeach', ender]
    return jquerytemplate(parser, token, tokens, ender)





class JqueryTemplateNode(template.Node):
    def __init__(self, template_name, nodelist):
        self.template_name = template_name
        self.nodelist = nodelist
    def render(self, context):
        body = self.nodelist.render(context)
        return render_to_string('jquery/jqTemplatingTemplate.html', {'body': body, 'template_name': self.template_name})
        
@register.tag('jqTemplate')
def jquery_template(parser, token):
    nodelist = parser.parse(('endjqTemplate',))
    parser.delete_first_token()
    
    tag_name, arg = token.contents.split(None, 1)
    if not (arg[0] == arg[-1] and arg[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    template_name = arg[1:-1]
    return JqueryTemplateNode(template_name=template_name, nodelist=nodelist)
