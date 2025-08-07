from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
import requests

from .models import Spin
from .forms import SpinForm



class SpinCreateView(LoginRequiredMixin, CreateView):
    model = Spin
    form_class = SpinForm
    template_name = 'spins/create.html'

    def form_valid(self, form):
        spin = form.save(commit=False)
        spin.user = self.request.user

        # Assign artist, album, and cover URL from hidden inputs
        spin.artist = self.request.POST.get('artist', '').strip()
        spin.album = self.request.POST.get('album', '').strip()
        spin.album_cover_url = self.request.POST.get('album_cover_url', '').strip()

        spin.save()
        return redirect('profile', username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['DISCOGS_API_TOKEN'] = settings.DISCOGS_API_TOKEN  # ✅ pass token into context
        return context

def discogs_search(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'results': []})

    url = "https://api.discogs.com/database/search"
    headers = {'User-Agent': 'NowSpinningApp/1.0'}
    params = {
        'q': query,
        'type': 'release',
        'token': settings.DISCOGS_API_TOKEN
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException:
        return JsonResponse({'results': []})

    results = []
    for item in data.get('results', []):
        title = item.get('title', '')
        artist, album = title.split(' - ') if ' - ' in title else (title, '')
        results.append({
            'title': title,
            'artist': artist.strip(),
            'album': album.strip(),
            'cover_image': item.get('cover_image')
        })

    return JsonResponse({'results': results})
