from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
import requests

from .models import Spin
from .forms import SpinForm

# Discogs settings
DISCOGS_BASE = "https://api.discogs.com"
HEADERS = {
    "Authorization": f"Discogs token={settings.DISCOGS_API_TOKEN}",
    "User-Agent": settings.DISCOGS_USER_AGENT,  
}

class SpinCreateView(LoginRequiredMixin, CreateView):
    model = Spin
    form_class = SpinForm
    template_name = "spins/create.html"

    def form_valid(self, form):
        spin = form.save(commit=False)
        spin.user = self.request.user
        # values come from hidden inputs the JS fills in
        spin.artist = (self.request.POST.get("artist") or "").strip()
        spin.album = (self.request.POST.get("album") or "").strip()
        spin.album_cover_url = (self.request.POST.get("album_cover_url") or "").strip()
        spin.save()
        return redirect("profile", username=self.request.user.username)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
      
        return ctx

def _ok(data, status=200):
    return JsonResponse(data, status=status, safe=False)

def _err(msg, status=400):
    return JsonResponse({"error": msg}, status=status)

@require_GET
def discogs_search_artists(request):
    """
    Proxy endpoint for artist autocomplete.
    GET /api/discogs/artists?q=radiohead
    """
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return _ok({"results": []})

    cache_key = f"discogs:artists:{q.lower()}"
    cached = cache.get(cache_key)
    if cached:
        return _ok(cached)

    try:
        r = requests.get(
            f"{DISCOGS_BASE}/database/search",
            params={"q": q, "type": "artist", "per_page": 8, "page": 1},
            headers=HEADERS,
            timeout=8,
        )
        if r.status_code == 429:
            return _err("Rate limited by Discogs. Try again soon.", 429)
        r.raise_for_status()
        payload = r.json()
        results = [
            {"id": item.get("id"), "title": item.get("title")}
            for item in payload.get("results", [])
            if item.get("id") and item.get("title")
        ]
        data = {"results": results}
        cache.set(cache_key, data, 60)
        return _ok(data)
    except requests.RequestException as e:
        return _err(f"Artist search failed: {e}", 502)

@require_GET
def discogs_artist_releases(request, artist_id: int):
    """
    Proxy endpoint for album dropdown.
    GET /api/discogs/artist/<artist_id>/releases
    """
    cache_key = f"discogs:artist:{artist_id}:releases"
    cached = cache.get(cache_key)
    if cached:
        return _ok(cached)

    try:
        r = requests.get(
            f"{DISCOGS_BASE}/artists/{artist_id}/releases",
            params={"sort": "year", "sort_order": "desc", "per_page": 100, "page": 1},
            headers=HEADERS,
            timeout=10,
        )
        if r.status_code == 429:
            return _err("Rate limited by Discogs. Try again soon.", 429)
        r.raise_for_status()
        payload = r.json()

        seen = set()
        items = []
        for rel in payload.get("releases", []):
            if rel.get("type") not in {"master", "release"}:
                continue
            title = rel.get("title")
            if not title or title in seen:
                continue
            seen.add(title)
            items.append({
                "title": title,
                "year": rel.get("year"),
                "thumb": rel.get("thumb"),
                "master_id": rel.get("master_id"),
                "id": rel.get("id"),
                "type": rel.get("type"),
            })
            if len(items) >= 75:
                break

        data = {"results": items}
        cache.set(cache_key, data, 300)
        return _ok(data)
    except requests.RequestException as e:
        return _err(f"Releases fetch failed: {e}", 502)
