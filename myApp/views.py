from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import (
    Page, Section,
    HeroSection,
    StatisticsSection,
    CredibilitySection,
    TestimonialsSection,
    PainPointsSolutionsSection,
    WhatMakesMeDifferentSection,
    FeaturedPublicationsSection,
    ServicesSection,
    MeetKimHerrleinSection,
    MissionSection,
    FreeResourceSection,
    FooterSection,
)


def convert_section_config_to_template_format(section, config=None):
    """Convert section config to format expected by templates"""
    if config is None:
        # Use published_config if available, fallback to section_config
        if section.published_config and isinstance(section.published_config, dict) and len(section.published_config) > 0:
            config = section.published_config
        elif section.section_config and isinstance(section.section_config, dict) and len(section.section_config) > 0:
            config = section.section_config
        else:
            config = {}
    
    # Ensure config is a dict
    if not isinstance(config, dict):
        config = {}
    
    # Create mock objects for related items
    class MockRelatedItem:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    class MockRelatedManager:
        def __init__(self, items_data):
            self.items = [MockRelatedItem(item) for item in items_data]
        
        def all(self):
            return self.items
    
    # Create a mock object that mimics the old model structure
    class SectionObject:
        def __init__(self, config, section):
            # Default to True if not specified, or use section.is_enabled
            self.show_section = config.get('show_section', section.is_enabled if hasattr(section, 'is_enabled') else True)
            self.show_divider_above = config.get('show_divider_above', False)
            self.show_divider_below = config.get('show_divider_below', False)
            self.headline = config.get('headline', '')
            self.subheadline = config.get('subheadline', '')
            self.body_text = config.get('body_text', '')
            self.quote_text = config.get('quote_text', '')
            self.quote_attribution = config.get('quote_attribution', '')
            self.primary_button_label = config.get('primary_button', {}).get('label', '')
            self.primary_button_url = config.get('primary_button', {}).get('url', '')
            self.primary_button_variant = config.get('primary_button', {}).get('variant', 'primary')
            self.primary_button_shape = config.get('primary_button', {}).get('shape', 'rounded')
            self.secondary_button_label = config.get('secondary_button', {}).get('label', '')
            self.secondary_button_url = config.get('secondary_button', {}).get('url', '')
            self.secondary_button_variant = config.get('secondary_button', {}).get('variant', 'link')
            self.secondary_button_shape = config.get('secondary_button', {}).get('shape', 'pill')
            self.image_url = config.get('image', {}).get('url', '')
            self.image_alt_text = config.get('image', {}).get('alt_text', '')
            self.image_position = config.get('image_position', 'right')
            self.icon = config.get('icon', '')
            self.layout_variant = config.get('layout_variant', '')
            self.background_style = config.get('background_style', '')
            # Background image (handle missing key gracefully)
            bg_image = config.get('background_image', {})
            if not isinstance(bg_image, dict):
                bg_image = {}
            self.background_image_url = bg_image.get('url', '')
            self.background_image_alt_text = bg_image.get('alt_text', '')
            
            # Gradient (handle missing key gracefully)
            gradient = config.get('gradient', {})
            if not isinstance(gradient, dict):
                gradient = {}
            self.gradient_type = gradient.get('type', 'none')
            gradient_colors = gradient.get('colors', [])
            # Ensure gradient_colors is always a list
            if not isinstance(gradient_colors, list):
                gradient_colors = []
            self.gradient_colors = gradient_colors
            self.gradient_direction = gradient.get('direction', 'to-right')
            self.intro_text = config.get('intro_text', '')
            self.intro_quote = config.get('intro_quote', '')
            self.intro_quote_attribution = config.get('intro_quote_attribution', '')
            self.golden_thread_quote_text = config.get('golden_thread_quote_text', '')
            self.golden_thread_quote_attribution = config.get('golden_thread_quote_attribution', '')
            self.supplemental_link_label = config.get('supplemental_link_label', '')
            self.supplemental_link_url = config.get('supplemental_link_url', '')
            
            # Handle related items based on section type
            if section.section_type == 'statistics':
                self.statitem_set = MockRelatedManager(config.get('stats', []))
            elif section.section_type == 'testimonials':
                self.testimonial_set = MockRelatedManager(config.get('testimonials', []))
            elif section.section_type == 'credibility':
                self.credibilityitem_set = MockRelatedManager(config.get('credibility_items', []))
            elif section.section_type == 'pain_points':
                self.painpoint_set = MockRelatedManager(config.get('pain_points', []))
            elif section.section_type == 'what_makes_me_different':
                self.differentiatorcard_set = MockRelatedManager(config.get('differentiator_cards', []))
            elif section.section_type == 'featured_publications':
                self.publication_set = MockRelatedManager(config.get('publications', []))
            elif section.section_type == 'services':
                self.service_set = MockRelatedManager(config.get('services', []))
            elif section.section_type == 'footer':
                self.sociallink_set = MockRelatedManager(config.get('social_links', []))
                self.footerlink_set = MockRelatedManager(config.get('footer_links', []))
            
            # For debugging
            self._section = section
            self._config = config
    
    return SectionObject(config, section)


def home(request, preview_mode=False):
    """Homepage view - uses Page/Section if available, falls back to legacy models
    
    Args:
        preview_mode: If True, uses draft_config. If False, uses published_config.
    """
    # Try to get Page with slug="home"
    page = Page.objects.filter(slug="home", is_active=True).first()
    
    if page:
        sections = page.sections.filter(is_enabled=True).order_by('sort_order')
        
        # Build context from sections
        context = {'page': page, 'preview_mode': preview_mode}
        
        # Map sections by type
        for section in sections:
            # Get config based on mode
            config = section.get_config_for_preview(preview_mode=preview_mode)
            
            # Convert config to template format (even if empty, we'll let template handle it)
            # Only process if config has content
            if config and isinstance(config, dict) and len(config) > 0:
                section_obj = convert_section_config_to_template_format(section, config=config)
            else:
                # Skip empty configs
                continue
            
            if section.section_type == 'hero':
                context['hero_section'] = section_obj
            elif section.section_type == 'statistics':
                context['statistics_section'] = section_obj
            elif section.section_type == 'credibility':
                context['credibility_section'] = section_obj
            elif section.section_type == 'testimonials':
                context['testimonials_section'] = section_obj
            elif section.section_type == 'pain_points':
                context['pain_points_section'] = section_obj
            elif section.section_type == 'what_makes_me_different':
                context['what_makes_me_different_section'] = section_obj
            elif section.section_type == 'featured_publications':
                context['featured_publications_section'] = section_obj
            elif section.section_type == 'services':
                context['services_section'] = section_obj
            elif section.section_type == 'meet_kim':
                context['meet_kim_herrlein_section'] = section_obj
            elif section.section_type == 'mission':
                context['mission_section'] = section_obj
            elif section.section_type == 'free_resource':
                context['free_resource_section'] = section_obj
            elif section.section_type == 'footer':
                # Only set footer if not already set (prevent duplicates)
                if 'footer_section' not in context:
                    context['footer_section'] = section_obj
        
        # Only get footer from legacy model if not already set from sections
        if 'footer_section' not in context:
            context['footer_section'] = FooterSection.objects.filter(show_section=True).first()
        
        return render(request, 'home.html', context)
    else:
        # Fall back to legacy model-based approach (for backward compatibility)
        context = {
            'hero_section': HeroSection.objects.filter(show_section=True).first(),
            'statistics_section': StatisticsSection.objects.filter(show_section=True).first(),
            'credibility_section': CredibilitySection.objects.filter(show_section=True).first(),
            'testimonials_section': TestimonialsSection.objects.filter(show_section=True).first(),
            'pain_points_section': PainPointsSolutionsSection.objects.filter(show_section=True).first(),
            'what_makes_me_different_section': WhatMakesMeDifferentSection.objects.filter(show_section=True).first(),
            'featured_publications_section': FeaturedPublicationsSection.objects.filter(show_section=True).first(),
            'services_section': ServicesSection.objects.filter(show_section=True).first(),
            'meet_kim_herrlein_section': MeetKimHerrleinSection.objects.filter(show_section=True).first(),
            'mission_section': MissionSection.objects.filter(show_section=True).first(),
            'free_resource_section': FreeResourceSection.objects.filter(show_section=True).first(),
            'footer_section': FooterSection.objects.filter(show_section=True).first(),
        }
        return render(request, 'home.html', context)


@xframe_options_exempt
def home_preview(request):
    """Preview version of homepage - uses draft_config"""
    return home(request, preview_mode=True)
