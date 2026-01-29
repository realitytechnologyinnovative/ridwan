from django.db import models
from django.core.exceptions import ValidationError


class AboutMeContent(models.Model):
	content = models.TextField(default=(
		"""
	I'm an applied ecosystem ecologist passionate about bridging science and practice to tackle some of our world's biggest environmental challenges.
	Currently, I lead strategy for a community-run conservation initiative in Nigeria, where I spearhead a sustainable agribusiness enterprise that empowers
	local youth and women through job creation, economic and financial inclusion, and forest restoration.

	Alongside my applied work, I am completing a PhD at Vrije Universiteit Brussel, where I study how large herbivores 🦓🦬🦒🦏🐘 shape ecosystems stability
	and resilience. My goal is to provide actionable insights that inform environmental policy and climate resilience strategies.

	My vision is to connect ecological science with development outcomes, from policy reform and nature recovery to inclusive growth and the Sustainable Development Goals.
	I'm always open to collaborations, partnerships, and opportunities in ecological research, conservation, environmental consulting, and sustainable development.
	"""
	).strip())
	resume_url = models.URLField(default="https://drive.google.com/file/d/1CZ3dgW4PeTDTCc9me2sO2iOJQMM8C44J/view?usp=sharing")
	updated_at = models.DateTimeField(auto_now=True)

	def clean(self) -> None:
		if AboutMeContent.objects.exclude(pk=self.pk).exists():
			raise ValidationError('Only one AboutMeContent instance is allowed.')

	def save(self, *args, **kwargs):
		self.full_clean()
		return super().save(*args, **kwargs)

	def __str__(self) -> str:
		return 'About Me Content'


class SiteContent(models.Model):
	about_html = models.TextField()
	resume_url = models.URLField()
	articles_section_title = models.CharField(max_length=100, default='Articles')

	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return 'Site Content'


class ArticleCategory(models.Model):
	name = models.CharField(max_length=70, unique=True)
	slug = models.SlugField(max_length=80, unique=True)
	link_url = models.URLField(blank=True)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class Article(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	link_url = models.URLField(blank=True)
	image_url = models.URLField(blank=True)
	category = models.ForeignKey(ArticleCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.title


class StatItem(models.Model):
	label = models.CharField(max_length=100)
	value = models.PositiveIntegerField(default=0)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', 'id']

	def __str__(self) -> str:
		return f"{self.label}: {self.value}"
