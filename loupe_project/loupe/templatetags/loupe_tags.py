from django.template import Library, Node, Variable, TemplateSyntaxError
from django.core.urlresolvers import reverse
from loupe.models import Note, Image, Corkboard

register = Library()
 
class CorkNode(Node):
    def __init__(self, obj, varname):
        self.obj, self.varname = obj, varname

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        if self.varname:
            varname = self.resolve(self.varname, context)
        else:
            varname = 'corkboards'
        context[varname] = Corkboard.objects.filter(project=obj)
        return ''


@register.tag
def get_corkboards_for(parser, token):
    """
    returns corkboards for the given project object
    
    Example usage:
    {% get_corkboards_for obj as var %}

    """

    args = token.contents.split()
    if len(args) != 4:
        raise TemplateSyntaxError, "get_corkboards_for tag takes exactly 1 argument"
    if args[2] != 'as':
        raise TemplateSyntaxError, "third argument to the get_corkboards_for tag must be 'as'"

    return CorkNode(args[1], args[3])
