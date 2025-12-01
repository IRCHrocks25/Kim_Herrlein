from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify


def validate_url_or_anchor(value):
    """
    Validates that the value is either a full URL or an anchor link (starting with #)
    or a relative path (starting with /)
    """
    if not value:
        return  # Empty is allowed (blank=True)
    
    # Allow anchor links (for one-page websites)
    if value.startswith('#'):
        return
    
    # Allow relative paths
    if value.startswith('/'):
        return
    
    # For full URLs, use the standard URLValidator
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError(
            'Enter a valid URL (http://...), anchor link (#section), or relative path (/page).'
        )


# ==================== MEDIA ASSET MODEL ====================
class MediaAsset(models.Model):
    """Stores Cloudinary image metadata - NO file storage"""
    
    # Basic Info
    title = models.CharField(max_length=200)  # Original filename
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    public_id = models.CharField(max_length=255, unique=True)  # Cloudinary ID
    
    # URLs (3 variants)
    secure_url = models.URLField(max_length=500)  # Original secure URL
    web_url = models.URLField(max_length=500)  # Optimized: f_auto,q_auto
    thumb_url = models.URLField(max_length=500)  # Thumbnail: c_fill,w_480,h_320
    
    # Metadata
    bytes_size = models.IntegerField(default=0)  # File size
    width = models.IntegerField(default=0)  # Image width
    height = models.IntegerField(default=0)  # Image height
    format = models.CharField(max_length=10)  # jpg, png, webp, etc.
    tags_csv = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    
    # Status
    is_active = models.BooleanField(default=True)  # Soft delete
    sort_order = models.IntegerField(default=0)  # Ordering
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ==================== DASHBOARD BUILDER MODELS ====================
class Page(models.Model):
    """Represents a page on the website (Home, About, etc.)"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL slug (e.g., 'home', 'about')")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Section(models.Model):
    """Represents a section on a page (Hero, Stats, Testimonials, etc.)"""
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('statistics', 'Statistics Section'),
        ('credibility', 'Credibility Section'),
        ('testimonials', 'Testimonials Section'),
        ('pain_points', 'Pain Points & Solutions Section'),
        ('what_makes_me_different', 'What Makes Me Different Section'),
        ('featured_publications', 'Featured Publications Section'),
        ('services', 'Services Section'),
        ('meet_kim', 'Meet Kim Herrlein Section'),
        ('mission', 'Mission Section'),
        ('free_resource', 'Free Resource Section'),
        ('footer', 'Footer Section'),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    internal_label = models.CharField(max_length=200, help_text="Internal label for identification (e.g., 'Homepage Hero v1')")
    sort_order = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    
    # Draft vs Published system
    draft_config = models.JSONField(default=dict, blank=True, help_text="Draft configuration (what user is editing)")
    published_config = models.JSONField(default=dict, blank=True, help_text="Published configuration (what public site shows)")
    
    # Legacy: section_config property for backward compatibility
    section_config = models.JSONField(default=dict, blank=True, help_text="DEPRECATED: Use published_config. Kept for backward compatibility.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def has_unpublished_changes(self):
        """Check if draft differs from published"""
        return self.draft_config != self.published_config
    
    def get_config_for_preview(self, preview_mode=False):
        """Get config based on mode: draft for preview, published for public"""
        # Auto-migrate: If draft_config/published_config are empty but section_config has data, copy it
        if (not self.draft_config or (isinstance(self.draft_config, dict) and len(self.draft_config) == 0)) and \
           (not self.published_config or (isinstance(self.published_config, dict) and len(self.published_config) == 0)) and \
           self.section_config and isinstance(self.section_config, dict) and len(self.section_config) > 0:
            # Migrate section_config to both draft and published
            import copy
            self.draft_config = copy.deepcopy(self.section_config)
            self.published_config = copy.deepcopy(self.section_config)
            self.save(update_fields=['draft_config', 'published_config'])
        
        if preview_mode:
            # For preview, use draft_config if it exists and is not empty, otherwise published_config
            if self.draft_config and isinstance(self.draft_config, dict) and len(self.draft_config) > 0:
                return self.draft_config
            elif self.published_config and isinstance(self.published_config, dict) and len(self.published_config) > 0:
                return self.published_config
            elif self.section_config and isinstance(self.section_config, dict) and len(self.section_config) > 0:
                return self.section_config
            return {}
        # For public, use published_config if it exists, otherwise section_config
        if self.published_config and isinstance(self.published_config, dict) and len(self.published_config) > 0:
            return self.published_config
        elif self.section_config and isinstance(self.section_config, dict) and len(self.section_config) > 0:
            return self.section_config
        return {}
    
    def get_headline_preview(self):
        """Get headline for display in section list"""
        if self.draft_config and self.draft_config.get('headline'):
            return self.draft_config.get('headline', '')
        elif self.published_config and self.published_config.get('headline'):
            return self.published_config.get('headline', '')
        elif self.section_config and self.section_config.get('headline'):
            return self.section_config.get('headline', '')
        return 'No headline'
    
    class Meta:
        ordering = ['sort_order', 'created_at']
        unique_together = [['page', 'sort_order']]
    
    def __str__(self):
        return f"{self.page.name} - {self.get_section_type_display()} ({self.internal_label})"


class ButtonConfig(models.Model):
    """Reusable button configuration"""
    label = models.CharField(max_length=200)
    url = models.CharField(max_length=500, validators=[validate_url_or_anchor])
    variant = models.CharField(
        max_length=20,
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('subtle', 'Subtle'),
            ('link', 'Link'),
        ],
        default='primary'
    )

    class Meta:
        abstract = True


class ImageConfig(models.Model):
    """Reusable image configuration"""
    url = models.CharField(max_length=1000, blank=True, help_text="Cloudinary URL or external URL")
    alt_text = models.CharField(max_length=500, blank=True)
    
    class Meta:
        abstract = True


# ==================== HERO SECTION ====================
class HeroSection(models.Model):
    section_id = models.CharField(max_length=50, default="Hero Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.TextField()
    body_text = models.TextField(blank=True)
    quote_text = models.TextField(blank=True)
    quote_attribution = models.CharField(max_length=200, blank=True)
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary')],
        default='primary'
    )
    
    # Secondary CTA (optional)
    secondary_button_label = models.CharField(max_length=200, blank=True)
    secondary_button_url = models.CharField(max_length=500, blank=True)
    secondary_button_variant = models.CharField(
        max_length=20,
        choices=[('link', 'Link'), ('subtle', 'Subtle')],
        default='link',
        blank=True
    )
    
    # Image
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    image_position = models.CharField(
        max_length=20,
        choices=[('right', 'Right'), ('left', 'Left'), ('background', 'Background')],
        default='right'
    )
    
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class, e.g. 'fa-solid fa-compass'")
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[
            ('text_left_image_right', 'Text Left, Image Right'),
            ('centered_stack', 'Centered Stack'),
        ],
        default='text_left_image_right'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('dark_band', 'Dark Band'), ('soft_gradient', 'Soft Gradient')],
        default='dark_band'
    )
    
    # Toggles
    show_section = models.BooleanField(default=True)
    show_divider_below = models.BooleanField(default=False)
    emphasize_as_key_section = models.BooleanField(default=True)
    
    order = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Hero Section"


# ==================== STATISTICS SECTION ====================
class StatItem(models.Model):
    section = models.ForeignKey('StatisticsSection', on_delete=models.CASCADE, related_name='statitem_set')
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=100, blank=True, help_text="Optional numeric value")
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class StatisticsSection(models.Model):
    section_id = models.CharField(max_length=50, default="Statistics Section", editable=False)
    headline = models.CharField(max_length=300)
    intro_text = models.TextField()
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('subtle', 'Subtle')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('centered_stack', 'Centered Stack'), ('cards_grid', 'Cards Grid')],
        default='cards_grid'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('dark_band', 'Dark Band'), ('soft_gradient', 'Soft Gradient')],
        default='dark_band'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    show_divider_below = models.BooleanField(default=False)
    
    order = models.IntegerField(default=2)
    
    class Meta:
        verbose_name = "Statistics Section"
        verbose_name_plural = "Statistics Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Statistics Section"


# ==================== CREDIBILITY SECTION ====================
class CredibilityItem(models.Model):
    section = models.ForeignKey('CredibilitySection', on_delete=models.CASCADE, related_name='credibilityitem_set')
    title = models.CharField(max_length=200)
    body_text = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    highlight = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class HighlightStat(models.Model):
    section = models.ForeignKey('CredibilitySection', on_delete=models.CASCADE, related_name='highlightstat_set')
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class CredibilitySection(models.Model):
    section_id = models.CharField(max_length=50, default="Credibility Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(blank=True)
    
    # Image
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    image_position = models.CharField(
        max_length=20,
        choices=[('right', 'Right'), ('left', 'Left'), ('full', 'Full')],
        default='right'
    )
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('subtle', 'Subtle')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('two_column_text_image', 'Two Column Text/Image'), ('centered_stack', 'Centered Stack')],
        default='two_column_text_image'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('subtle_texture', 'Subtle Texture')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    
    order = models.IntegerField(default=3)
    
    class Meta:
        verbose_name = "Credibility Section"
        verbose_name_plural = "Credibility Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Credibility Section"


# ==================== TESTIMONIALS SECTION ====================
class Testimonial(models.Model):
    section = models.ForeignKey('TestimonialsSection', on_delete=models.CASCADE, related_name='testimonial_set')
    quote = models.TextField()
    name = models.CharField(max_length=200)
    role_or_context = models.CharField(max_length=300, blank=True)
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    highlight = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class TestimonialsSection(models.Model):
    section_id = models.CharField(max_length=50, default="Testimonials Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('subtle', 'Subtle')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('cards_grid', 'Cards Grid'), ('carousel', 'Carousel')],
        default='cards_grid'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('soft_gradient', 'Soft Gradient')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    show_divider_below = models.BooleanField(default=False)
    
    order = models.IntegerField(default=4)
    
    class Meta:
        verbose_name = "Testimonials Section"
        verbose_name_plural = "Testimonials Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Testimonials Section"


# ==================== PAIN POINTS & SOLUTIONS SECTION ====================
class PainPoint(models.Model):
    section = models.ForeignKey('PainPointsSolutionsSection', on_delete=models.CASCADE, related_name='painpoint_set')
    pain_quote = models.CharField(max_length=500)
    description = models.TextField()
    what_changes_label = models.CharField(max_length=200, default="What Changes")
    what_changes_body = models.TextField()
    icon_pain = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    icon_solution = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class PainPointsSolutionsSection(models.Model):
    section_id = models.CharField(max_length=50, default="Pain Points & Solutions Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(blank=True)
    
    # Golden Thread Quote
    golden_thread_quote_text = models.TextField(blank=True)
    golden_thread_quote_attribution = models.CharField(max_length=200, blank=True)
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('stacked_pairs', 'Stacked Pairs'), ('two_column_pairs', 'Two Column Pairs')],
        default='stacked_pairs'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('dark_band', 'Dark Band'), ('soft_gradient', 'Soft Gradient')],
        default='dark_band'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    
    order = models.IntegerField(default=5)
    
    class Meta:
        verbose_name = "Pain Points & Solutions Section"
        verbose_name_plural = "Pain Points & Solutions Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Pain Points & Solutions Section"


# ==================== WHAT MAKES ME DIFFERENT SECTION ====================
class DifferentiatorCard(models.Model):
    section = models.ForeignKey('WhatMakesMeDifferentSection', on_delete=models.CASCADE, related_name='differentiatorcard_set')
    title = models.CharField(max_length=200)
    body_text = models.TextField()
    example_text = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class WhatMakesMeDifferentSection(models.Model):
    section_id = models.CharField(max_length=50, default="What Makes Me Different Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(blank=True)
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('subtle', 'Subtle')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[
            ('four_column_grid', 'Four Column Grid'),
            ('two_by_two_grid', 'Two by Two Grid'),
            ('stacked_cards', 'Stacked Cards'),
        ],
        default='four_column_grid'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('subtle_texture', 'Subtle Texture')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    
    order = models.IntegerField(default=6)
    
    class Meta:
        verbose_name = "What Makes Me Different Section"
        verbose_name_plural = "What Makes Me Different Sections"
        ordering = ['order']
    
    def __str__(self):
        return "What Makes Me Different Section"


# ==================== FEATURED PUBLICATIONS SECTION ====================
class Publication(models.Model):
    section = models.ForeignKey('FeaturedPublicationsSection', on_delete=models.CASCADE, related_name='publication_set')
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    button_label = models.CharField(max_length=200, default="Get Your Copy")
    button_url = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class FeaturedPublicationsSection(models.Model):
    section_id = models.CharField(max_length=50, default="Featured Publications Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(blank=True)
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('cards_row', 'Cards Row'), ('cards_grid', 'Cards Grid')],
        default='cards_row'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('soft_gradient', 'Soft Gradient')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    
    order = models.IntegerField(default=7)
    
    class Meta:
        verbose_name = "Featured Publications Section"
        verbose_name_plural = "Featured Publications Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Featured Publications Section"


# ==================== SERVICES SECTION ====================
class Service(models.Model):
    section = models.ForeignKey('ServicesSection', on_delete=models.CASCADE, related_name='service_set')
    name = models.CharField(max_length=200)
    short_label = models.CharField(max_length=200, help_text="e.g. '8-Week Live Online Course'")
    description = models.TextField()
    bullets = models.JSONField(default=list, help_text="Array of bullet point strings")
    cohort_details = models.TextField(blank=True)
    pricing_note = models.CharField(max_length=500, blank=True)
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary')],
        default='primary'
    )
    
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class ServicesSection(models.Model):
    section_id = models.CharField(max_length=50, default="Services Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_quote = models.TextField(blank=True)
    intro_quote_attribution = models.CharField(max_length=200, blank=True)
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('cards_grid', 'Cards Grid'), ('stacked_cards', 'Stacked Cards')],
        default='cards_grid'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('soft_gradient', 'Soft Gradient'), ('dark_band', 'Dark Band'), ('light_surface', 'Light Surface')],
        default='soft_gradient'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    emphasize_as_key_section = models.BooleanField(default=True)
    
    order = models.IntegerField(default=8)
    
    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Services Section"


# ==================== MEET KIM HERRLEIN SECTION ====================
class MeetKimHerrleinSection(models.Model):
    section_id = models.CharField(max_length=50, default="Meet Kim Herrlein Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    body_text = models.TextField()
    quote_text = models.TextField(blank=True)
    quote_attribution = models.CharField(max_length=200, blank=True)
    
    # Image
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    image_position = models.CharField(
        max_length=20,
        choices=[('left', 'Left'), ('right', 'Right'), ('full', 'Full')],
        default='left'
    )
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('subtle', 'Subtle')],
        default='primary'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('two_column_text_image', 'Two Column Text/Image'), ('centered_stack', 'Centered Stack')],
        default='two_column_text_image'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('subtle_texture', 'Subtle Texture')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    
    order = models.IntegerField(default=9)
    
    class Meta:
        verbose_name = "Meet Kim Herrlein Section"
        verbose_name_plural = "Meet Kim Herrlein Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Meet Kim Herrlein Section"


# ==================== MISSION SECTION ====================
class MissionSection(models.Model):
    section_id = models.CharField(max_length=50, default="Mission Section", editable=False)
    headline = models.CharField(max_length=300)
    body_text = models.TextField()
    
    # Supplemental link
    supplemental_link_label = models.CharField(max_length=200, blank=True)
    supplemental_link_url = models.CharField(max_length=500, blank=True)
    
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('centered_stack', 'Centered Stack'), ('narrow_column', 'Narrow Column')],
        default='centered_stack'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('soft_gradient', 'Soft Gradient')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    show_divider_below = models.BooleanField(default=False)
    
    order = models.IntegerField(default=10)
    
    class Meta:
        verbose_name = "Mission Section"
        verbose_name_plural = "Mission Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Mission Section"


# ==================== FREE RESOURCE SECTION ====================
class FreeResourceSection(models.Model):
    section_id = models.CharField(max_length=50, default="Free Resource Section", editable=False)
    headline = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=300, blank=True)
    body_text = models.TextField()
    
    # Primary CTA
    primary_button_label = models.CharField(max_length=200)
    primary_button_url = models.CharField(max_length=500)
    primary_button_variant = models.CharField(
        max_length=20,
        choices=[('primary', 'Primary'), ('secondary', 'Secondary')],
        default='primary'
    )
    
    # Image
    image_url = models.CharField(max_length=1000, blank=True)
    image_alt_text = models.CharField(max_length=500, blank=True)
    image_position = models.CharField(
        max_length=20,
        choices=[('right', 'Right'), ('left', 'Left')],
        default='right'
    )
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('two_column_text_image', 'Two Column Text/Image'), ('centered_stack', 'Centered Stack')],
        default='two_column_text_image'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('light_surface', 'Light Surface'), ('subtle_texture', 'Subtle Texture')],
        default='light_surface'
    )
    
    show_section = models.BooleanField(default=True)
    show_divider_above = models.BooleanField(default=False)
    emphasize_as_key_section = models.BooleanField(default=True)
    
    order = models.IntegerField(default=11)
    
    class Meta:
        verbose_name = "Free Resource Section"
        verbose_name_plural = "Free Resource Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Free Resource Section"


# ==================== FOOTER SECTION ====================
class SocialLink(models.Model):
    section = models.ForeignKey('FooterSection', on_delete=models.CASCADE, related_name='sociallink_set')
    platform = models.CharField(
        max_length=30,
        choices=[
            ('instagram', 'Instagram'),
            ('linkedin', 'LinkedIn'),
            ('facebook', 'Facebook'),
            ('other', 'Other'),
        ]
    )
    label = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class FooterLink(models.Model):
    section = models.ForeignKey('FooterSection', on_delete=models.CASCADE, related_name='footerlink_set')
    label = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class FooterSection(models.Model):
    section_id = models.CharField(max_length=50, default="Footer Section", editable=False)
    brand_line = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    
    # Contact
    phone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=200, blank=True)
    location_line = models.CharField(max_length=200, blank=True)
    
    legal_line = models.CharField(max_length=500, blank=True)
    copyright_text = models.CharField(max_length=500, blank=True)
    
    layout_variant = models.CharField(
        max_length=30,
        choices=[('multi_column', 'Multi Column'), ('simple_footer', 'Simple Footer')],
        default='multi_column'
    )
    background_style = models.CharField(
        max_length=30,
        choices=[('dark_band', 'Dark Band'), ('soft_gradient', 'Soft Gradient')],
        default='dark_band'
    )
    
    show_section = models.BooleanField(default=True)
    
    order = models.IntegerField(default=12)
    
    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Sections"
        ordering = ['order']
    
    def __str__(self):
        return "Footer Section"
