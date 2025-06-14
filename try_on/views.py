import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TryOnResult
from django.core.files.base import ContentFile

@csrf_exempt
def tryon_api(request):
    if request.method == 'POST':
        clothing_image = request.FILES.get('clothing_image')
        avatar_image = request.FILES.get('avatar_image')

        if not clothing_image or not avatar_image:
            return JsonResponse({'error': 'الصور ناقصة'}, status=400)

        url = "https://try-on-diffusion.p.rapidapi.com/try-on-file"

        files = {
            "clothing_image": (clothing_image.name, clothing_image.read(), clothing_image.content_type),
            "avatar_image": (avatar_image.name, avatar_image.read(), avatar_image.content_type)
        }

        headers = {
            "x-rapidapi-key": "5562a07ee3msh73589be5c842986p1edaaejsn3ae0b05e0182",
            "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com"
        }

        response = requests.post(url, files=files, headers=headers)

        if response.status_code == 200:
            tryon_result = TryOnResult()
            tryon_result.result_image.save('output.jpg', ContentFile(response.content))
            tryon_result.save()

            return JsonResponse({
                'message': '✅ الصورة اتحفظت بنجاح',
                'result_id': tryon_result.id,
                'result_image_url': request.build_absolute_uri(tryon_result.result_image.url)
            })
        else:
            return JsonResponse({
                'error': 'في مشكلة في API',
                'status_code': response.status_code,
                'details': response.text
            }, status=500)
    else:
        return JsonResponse({'error': 'الطريقة غير مدعومة'}, status=405)