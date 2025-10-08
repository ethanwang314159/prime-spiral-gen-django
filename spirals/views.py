from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gen_scripts.ps_plt_gen import gen_ps_plt
from gen_scripts.rand_settings_gen import gen_random_settings
from django.views.decorators.csrf import csrf_exempt
import json

LAST_SETTINGS = None

def index(request):
    return render(request, 'spirals/index.html')

def generate_prime_spiral():
    global LAST_SETTINGS
    settings = gen_random_settings()
    LAST_SETTINGS = settings
    plt_obj = gen_ps_plt(settings)
    return plt_obj

def spiral_image(_):
    plt_obj = generate_prime_spiral()
    buf = io.BytesIO()
    plt_obj.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

LAST_SETTINGS = None

@csrf_exempt
def spiral_settings_json(request):
    global LAST_SETTINGS
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            LAST_SETTINGS = data
            plt_obj = generate_prime_spiral_with_settings(data)
            buf = io.BytesIO()
            plt_obj.savefig(buf, format='png', bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return HttpResponse(buf.getvalue(), content_type='image/png')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'GET':
        if LAST_SETTINGS is None:
            return JsonResponse({"error": "No spiral generated yet."})
        minified_settings = json.dumps(LAST_SETTINGS, separators=(',', ':'))
        print(minified_settings)
        return HttpResponse(minified_settings, content_type='application/json')

def generate_prime_spiral_with_settings(settings):
    global LAST_SETTINGS
    LAST_SETTINGS = settings
    plt_obj = gen_ps_plt(settings)
    return plt_obj
