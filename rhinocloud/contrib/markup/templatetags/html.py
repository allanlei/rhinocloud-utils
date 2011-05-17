from django import template
from django.conf import settings

register = template.Library()

def get_url(path, folder=None, media_root=settings.MEDIA_URL):
	if not path.startswith('http://') and not path.startswith('https://'):
		args = [media_root, folder, path]
		path = '/'.join([arg.rstrip('/') for arg in args if arg is not None])
		path = '%s%s' % (getattr(settings, 'MEDIA_SERVER', ''), path)
	return path


@register.simple_tag
def javascript(src):
    return '<script type="text/javascript" src="%(src)s"></script>' % {'src': get_url(src, 'js')}
    
@register.simple_tag
def css(src, media='screen'):
    return '<link href="%(src)s" rel="stylesheet" type="text/css" media="%(media)s" />' % {'src': get_url(src, 'css'), 'media': media}

@register.simple_tag
def image(src, caption=None, cls=None):
    return '<img src="%(src)s" title="%(title)s" class="%(cls)s" />' % {
    	'src': get_url(src, 'images'), 
    	'cls':cls, 
    	'title': caption,
   	}

@register.simple_tag
def icon16(src):
    return '<img src="%(src)s" width="%(width)s" height="%(height)s" class="%(cls)s"/>' % {
		'src': get_url(src, 'images'),
		'cls': 'icon16',
		'width': '16px',
		'height': '16px',
	}
