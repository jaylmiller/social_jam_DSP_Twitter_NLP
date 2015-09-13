from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Effect
from .models import Twitter

# Create your views here.
def index(request):
    effect_list = Effect.objects.order_by('id')
    twitter = Twitter.objects.get(pk=1)
    num = len(effect_list)

    tuple_list = []
    master_tup = ()
    for i in range(num):
        temp_tup = (effect_list[i],)
        master_tup = master_tup + temp_tup
        if i % 3 == 2:
            tuple_list.append(master_tup)
            master_tup = ()
    context = {'effect_list': tuple_list, 'bird': twitter}
    return render(request, 'settings/index.html', context)

def examine(request):
    effect_list = Effect.objects.order_by('id')
    bird = Twitter.objects.get(pk=1)
    num = len(effect_list)
    output = "" + str(num) + "\n"
    for effect in effect_list:
        output += effect.name + "\n"
        output += str(effect.status) + "\n"
        output += str(effect.param) + "\n"
    output += "Twitter" + "\n"
    output += str(bird.status) + "\n"
    output += str(bird.modifier) + "\n"
    return HttpResponse(output)

def submit(request):
    bird = Twitter.objects.get(pk=1)
    try:
        status = request.POST['twitter_status']
    except Exception, e:
        print "Exception @twitter"
        pass
    else:
        if status == "ON":
            b_status = True
        else:
            b_status = False
        bird.status = b_status
        bird.save()

    for effect in Effect.objects.order_by('id'):
        range_string = "range" + effect.name
        status_string = "status" + effect.name
        try:
            slide_val = request.POST[range_string]
        except Exception, e:
            print "Exception @ slider"
            pass
        else:
            effect.param = int(slide_val)
            effect.save()

        try:
            status = request.POST[status_string]
        except Exception, e:
            print "Exception @ status"
            pass
        else:
            if status == "ON":
                b_status = True
            else:
                b_status = False

            effect.status = b_status
            effect.save()
    return HttpResponseRedirect(reverse('settings:index'))
