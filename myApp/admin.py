from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Page, Section, MediaAsset,
    HeroSection,
    StatItem, StatisticsSection,
    CredibilityItem, HighlightStat, CredibilitySection,
    Testimonial, TestimonialsSection,
    PainPoint, PainPointsSolutionsSection,
    DifferentiatorCard, WhatMakesMeDifferentSection,
    Publication, FeaturedPublicationsSection,
    Service, ServicesSection,
    MeetKimHerrleinSection,
    MissionSection,
    FreeResourceSection,
    SocialLink, FooterLink, FooterSection,
)


# ==================== INLINE ADMIN CLASSES ====================
class StatItemInline(admin.TabularInline):
    model = StatItem
    extra = 1
    fields = ('order', 'label', 'value', 'description', 'icon')


class CredibilityItemInline(admin.TabularInline):
    model = CredibilityItem
    extra = 1
    fields = ('order', 'title', 'body_text', 'icon', 'highlight')


class HighlightStatInline(admin.TabularInline):
    model = HighlightStat
    extra = 1
    fields = ('order', 'label', 'value')


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = ('order', 'quote', 'name', 'role_or_context', 'image_url', 'image_alt_text', 'highlight')


class PainPointInline(admin.TabularInline):
    model = PainPoint
    extra = 1
    fields = ('order', 'pain_quote', 'description', 'what_changes_label', 'what_changes_body', 'icon_pain', 'icon_solution')


class DifferentiatorCardInline(admin.TabularInline):
    model = DifferentiatorCard
    extra = 1
    fields = ('order', 'title', 'body_text', 'example_text', 'icon')


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1
    fields = ('order', 'title', 'subtitle', 'description', 'button_label', 'button_url', 'image_url', 'image_alt_text')


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ('order', 'name', 'short_label', 'description', 'bullets', 'cohort_details', 'pricing_note', 
              'primary_button_label', 'primary_button_url', 'primary_button_variant', 'image_url', 'image_alt_text', 'icon')


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('order', 'platform', 'label', 'url', 'icon')


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('order', 'label', 'url')


# ==================== SECTION ADMIN CLASSES ====================
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'body_text', 'quote_text', 'quote_attribution')
        }),
        ('Primary CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Secondary CTA', {
            'fields': ('secondary_button_label', 'secondary_button_url', 'secondary_button_variant'),
            'classes': ('collapse',)
        }),
        ('Image', {
            'fields': ('image_url', 'image_alt_text', 'image_position')
        }),
        ('Styling', {
            'fields': ('icon', 'layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_below', 'emphasize_as_key_section', 'order')
        }),
    )


@admin.register(StatisticsSection)
class StatisticsSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [StatItemInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'intro_text')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'show_divider_below', 'order')
        }),
    )


@admin.register(CredibilitySection)
class CredibilitySectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [CredibilityItemInline, HighlightStatInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'intro_text')
        }),
        ('Image', {
            'fields': ('image_url', 'image_alt_text', 'image_position')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'order')
        }),
    )


@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [TestimonialInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'show_divider_below', 'order')
        }),
    )


@admin.register(PainPointsSolutionsSection)
class PainPointsSolutionsSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [PainPointInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'intro_text')
        }),
        ('Golden Thread Quote', {
            'fields': ('golden_thread_quote_text', 'golden_thread_quote_attribution')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'order')
        }),
    )


@admin.register(WhatMakesMeDifferentSection)
class WhatMakesMeDifferentSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [DifferentiatorCardInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'intro_text')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'order')
        }),
    )


@admin.register(FeaturedPublicationsSection)
class FeaturedPublicationsSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [PublicationInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'intro_text')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'order')
        }),
    )


@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    inlines = [ServiceInline]
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'intro_quote', 'intro_quote_attribution')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'emphasize_as_key_section', 'order')
        }),
    )


@admin.register(MeetKimHerrleinSection)
class MeetKimHerrleinSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'body_text', 'quote_text', 'quote_attribution')
        }),
        ('Image', {
            'fields': ('image_url', 'image_alt_text', 'image_position')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'order')
        }),
    )


@admin.register(MissionSection)
class MissionSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'body_text', 'supplemental_link_label', 'supplemental_link_url', 'icon')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'show_divider_below', 'order')
        }),
    )


@admin.register(FreeResourceSection)
class FreeResourceSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'headline', 'show_section', 'order')
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'subheadline', 'body_text')
        }),
        ('CTA', {
            'fields': ('primary_button_label', 'primary_button_url', 'primary_button_variant')
        }),
        ('Image', {
            'fields': ('image_url', 'image_alt_text', 'image_position')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'show_divider_above', 'emphasize_as_key_section', 'order')
        }),
    )


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'brand_line', 'show_section', 'order')
    inlines = [SocialLinkInline, FooterLinkInline]
    fieldsets = (
        ('Brand', {
            'fields': ('brand_line', 'tagline')
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'location_line')
        }),
        ('Legal', {
            'fields': ('legal_line', 'copyright_text')
        }),
        ('Styling', {
            'fields': ('layout_variant', 'background_style')
        }),
        ('Display Options', {
            'fields': ('show_section', 'order')
        }),
    )


# ==================== DASHBOARD BUILDER ADMIN ====================
class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ('section_type', 'internal_label', 'sort_order', 'is_enabled')
    ordering = ('sort_order',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SectionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('internal_label', 'page', 'section_type', 'sort_order', 'is_enabled')
    list_filter = ('section_type', 'is_enabled', 'page')
    search_fields = ('internal_label', 'page__name')
    ordering = ('page', 'sort_order')
    fieldsets = (
        ('Basic Information', {
            'fields': ('page', 'section_type', 'internal_label', 'sort_order', 'is_enabled')
        }),
        ('Configuration', {
            'fields': ('section_config',),
            'description': 'JSON configuration matching Backend Config Blueprint. Edit via Dashboard for better UX.'
        }),
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'width', 'height', 'bytes_size', 'is_active', 'created_at')
    list_filter = ('format', 'is_active', 'created_at')
    search_fields = ('title', 'public_id', 'tags_csv')
    readonly_fields = ('secure_url', 'web_url', 'thumb_url', 'public_id', 'width', 'height', 'format', 'bytes_size', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'public_id', 'is_active', 'sort_order')
        }),
        ('URLs', {
            'fields': ('secure_url', 'web_url', 'thumb_url'),
            'description': 'Three URL variants: secure_url (original), web_url (optimized), thumb_url (thumbnail)'
        }),
        ('Metadata', {
            'fields': ('width', 'height', 'format', 'bytes_size', 'tags_csv')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Make slug readonly if object exists
        if obj:
            return self.readonly_fields + ('slug',)
        return self.readonly_fields
