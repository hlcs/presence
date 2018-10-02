'''
    View dell' app hlcs
'''


from django.shortcuts import render


# TODO these views should be migrated to a separate HTML5/mobile application

# schermata dell' homepage
def homepage(request):
    if request.user.is_authenticated():
        options = 'disabled="disabled"' if _disable_internal_button(request) else ''
        return render(request, 'panel.html', {'options' : options})
    else:
        return render(request, 'index.html')

# schermata informazioni
def about(request):
    return render(request, 'about.html')


def _disable_internal_button(request):
    return True
