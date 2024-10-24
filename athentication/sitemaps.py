from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap_athentication(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["athentication:log in", "athentication:sign up"]

    def location(self, item):
        return reverse(item)