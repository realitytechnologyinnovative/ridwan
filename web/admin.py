from django.contrib import admin
from django import forms
from .models import SiteContent, Article, StatItem, AboutMeContent, ArticleCategory


SUGGESTED_STAT_LABELS = [
	"Countries",
	"Research Papers",
	"Years Experience",
	"Scholarships",
]


class StatItemForm(forms.ModelForm):
	class Meta:
		model = StatItem
		fields = ['label', 'value', 'order']
		widgets = {
			'label': forms.TextInput(attrs={
				'list': 'stat-label-suggestions',
				'placeholder': 'e.g., Countries',
			}),
		}


class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'description', 'link_url', 'image_url', 'category']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short summary (optional)'}),
			'link_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
			'image_url': forms.URLInput(attrs={'placeholder': 'https://... (optional)'}),
		}


class AboutMeContentForm(forms.ModelForm):
	class Meta:
		model = AboutMeContent
		fields = ['content', 'resume_url']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 10, 'style': 'font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial'}),
			'resume_url': forms.URLInput(attrs={'placeholder': 'https://drive.google.com/...'}),
		}


class ArticleInline(admin.TabularInline):
	model = Article
	form = ArticleForm
	extra = 1
	fields = ('title', 'link_url', 'image_url')
	show_change_link = True


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'link_url')
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ('name',)
	inlines = [ArticleInline]


@admin.register(AboutMeContent)
class AboutMeContentAdmin(admin.ModelAdmin):
	form = AboutMeContentForm
	list_display = ('updated_at',)
	fieldsets = (
		('About Me Content', {
			'description': 'Plain text content. Line breaks will be preserved on the site.',
			'fields': ('content',),
		}),
		('Resume', {
			'fields': ('resume_url',),
		}),
	)

	def has_add_permission(self, request):
		# Allow add only if none exists
		if AboutMeContent.objects.exists():
			return False
		return super().has_add_permission(request)


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
	list_display = ('articles_section_title', 'updated_at')
	fieldsets = (
		('Articles Section', {
			'fields': ('articles_section_title',),
			'description': 'Title displayed above the Articles grid (e.g., Articles).',
		}),
	)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	list_display = ('title', 'category', 'created_at')
	list_display_links = ('title',)
	list_filter = ('category', 'created_at')
	search_fields = ('title', 'description')
	ordering = ('-created_at',)
	date_hierarchy = 'created_at'
	list_per_page = 20


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
	form = StatItemForm
	list_display = ('label', 'value', 'order')
	list_editable = ('value', 'order')
	search_fields = ('label',)
	ordering = ('order', 'id')
	list_per_page = 20

	def changelist_view(self, request, extra_context=None):
		# provide datalist suggestions to the admin template via extra_context
		extra_context = extra_context or {}
		extra_context['stat_label_suggestions'] = SUGGESTED_STAT_LABELS
		return super().changelist_view(request, extra_context=extra_context)
