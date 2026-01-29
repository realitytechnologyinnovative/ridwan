from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.html import linebreaks
from .models import SiteContent, Article, StatItem, AboutMeContent, ArticleCategory


DEFAULT_ABOUT_TEXT = (
	"""
I'm an applied ecosystem ecologist passionate about bridging science and practice to tackle some of our world's biggest environmental challenges.
Currently, I lead strategy for a community-run conservation initiative in Nigeria, where I spearhead a sustainable agribusiness enterprise that empowers
local youth and women through job creation, economic and financial inclusion, and forest restoration.

Alongside my applied work, I am completing a PhD at Vrije Universiteit Brussel, where I study how large herbivores 🦓🦬🦒🦏🐘 shape ecosystems stability
and resilience. My goal is to provide actionable insights that inform environmental policy and climate resilience strategies.

My vision is to connect ecological science with development outcomes, from policy reform and nature recovery to inclusive growth and the Sustainable Development Goals.
I'm always open to collaborations, partnerships, and opportunities in ecological research, conservation, environmental consulting, and sustainable development.
	"""
).strip()

DEFAULT_RESUME_URL = "https://drive.google.com/file/d/1CZ3dgW4PeTDTCc9me2sO2iOJQMM8C44J/view?usp=sharing"


STAT_DEFAULTS = [
	{"label": "Countries", "value": 1, "order": 0},
]


def seed_stats_if_needed() -> None:
	if not StatItem.objects.exists():
		for s in STAT_DEFAULTS:
			StatItem.objects.create(**s)


def get_about_and_resume_text():
	about_entry = AboutMeContent.objects.first()
	if about_entry:
		return about_entry.content, about_entry.resume_url
	site = SiteContent.objects.first()
	if site and site.about_html:
		# legacy fallback from HTML -> strip tags minimally by trusting original about_html
		return site.about_html, site.resume_url or DEFAULT_RESUME_URL
	return DEFAULT_ABOUT_TEXT, DEFAULT_RESUME_URL


def home(request):
	seed_stats_if_needed()
	about_text, resume_url = get_about_and_resume_text()
	content = SiteContent.objects.first()
	articles = list(Article.objects.select_related('category').all())
	categories = list(ArticleCategory.objects.all())
	stats = list(StatItem.objects.all())
	context = {
		'about_text': about_text,
		'resume_url': resume_url,
		'articles_section_title': (content.articles_section_title if content and content.articles_section_title else 'Articles'),
		'articles': articles,
		'categories': categories,
		'stats': stats,
	}
	return render(request, 'index.html', context)



