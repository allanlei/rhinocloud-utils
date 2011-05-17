from django import template
from django.conf import settings

register = template.Library()

def get_url(path, folder=None, media_root=settings.MEDIA_URL):
	if not path.startswith('http://') and not path.startswith('https://'):
		args = [media_root, folder, path]
		path = '/'.join([arg.rstrip('/') for arg in args if arg is not None])
		path = '%s%s' % (getattr(settings, 'MEDIA_SERVER', ''), path)
	return path


@register.inclusion_tag('htmlutils/javascript.html')
def javascript(src):
	return {'src': get_url(src, 'js')}

@register.inclusion_tag('htmlutils/css.html')
def css(src, media='screen'):
	return {'src': get_url(src, 'css'), 'media': media}
    
@register.inclusion_tag('htmlutils/image.html')
def image(src, caption=None, cls=None):
    return {
    	'src': get_url(src, 'images'), 
    	'cls':cls, 
    	'caption':caption
   	}

@register.inclusion_tag('htmlutils/icon.html')
def icon16(src):
	return {
		'src': get_url(src, 'images'),
		'class': 'icon16',
		'width': '16px',
		'height': '16px',
	}
