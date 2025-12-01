from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction, models
from myApp.models import Page, Section, MediaAsset
from django.utils.text import slugify
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image, ImageOps
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Constants
MAX_BYTES = 10 * 1024 * 1024  # 10MB hard limit
TARGET_BYTES = int(9.3 * 1024 * 1024)  # 9.3MB compression target


@login_required
def dashboard_home(request):
    """Dashboard home/welcome screen"""
    # Auto-create Home page if none exist
    if not Page.objects.exists():
        Page.objects.create(
            name="Homepage",
            slug="home",
            description="Your main homepage - the first page visitors see",
            is_active=True
        )
        messages.info(request, 'Welcome! We created your Homepage to get you started.')
    
    pages = Page.objects.filter(is_active=True).order_by('name')[:5]
    total_pages = Page.objects.filter(is_active=True).count()
    total_sections = Section.objects.filter(is_enabled=True).count()
    
    return render(request, 'dashboard/index.html', {
        'pages': pages,
        'total_pages': total_pages,
        'total_sections': total_sections,
    })


@login_required
def pages_list(request):
    """List all pages - auto-create Home page if none exist"""
    pages = Page.objects.all().order_by('name')
    
    # Auto-create Home page if no pages exist (user-friendly)
    if not pages.exists():
        home_page = Page.objects.create(
            name="Homepage",
            slug="home",
            description="Your main homepage - the first page visitors see",
            is_active=True
        )
        pages = Page.objects.filter(id=home_page.id)
        messages.success(request, 'Welcome! We created your Homepage to get you started. Click "Open Page Builder" to add sections.')
    
    return render(request, 'dashboard/pages_list.html', {'pages': pages})


@login_required
@require_http_methods(["POST"])
def page_create(request):
    """Create a new page from dashboard"""
    name = request.POST.get('name', '').strip()
    slug = request.POST.get('slug', '').strip()
    description = request.POST.get('description', '').strip()
    
    if not name:
        messages.error(request, 'Page name is required')
        return redirect('dashboard:pages_list')
    
    if not slug:
        # Auto-generate slug from name
        slug = name.lower().replace(' ', '-').replace('_', '-')
    
    # Check if slug already exists
    if Page.objects.filter(slug=slug).exists():
        messages.error(request, f'A page with the slug "{slug}" already exists. Please choose a different name.')
        return redirect('dashboard:pages_list')
    
    page = Page.objects.create(
        name=name,
        slug=slug,
        description=description,
        is_active=True
    )
    
    messages.success(request, f'Page "{name}" created successfully!')
    return redirect('dashboard:page_builder', page_id=page.id)


@login_required
def page_builder(request, page_id):
    """Divi-style page builder with preview"""
    page = get_object_or_404(Page, id=page_id)
    sections = page.sections.all().order_by('sort_order')
    
    # Check if there are unpublished changes
    has_unpublished_changes = any(
        section.has_unpublished_changes() for section in sections
    )
    
    # Preview URL - adjust based on page slug
    if page.slug == 'home':
        from django.urls import reverse
        preview_url = reverse('home_preview')
    else:
        preview_url = f'/preview/{page.slug}/'  # For future pages
    
    # Section type choices for adding new sections
    section_type_choices = Section.SECTION_TYPES
    
    return render(request, 'dashboard/page_builder.html', {
        'page': page,
        'sections': sections,
        'section_type_choices': section_type_choices,
        'has_unpublished_changes': has_unpublished_changes,
        'preview_url': preview_url,
    })


@login_required
@require_http_methods(["POST"])
def section_add(request, page_id):
    """Add a new section to a page"""
    page = get_object_or_404(Page, id=page_id)
    section_type = request.POST.get('section_type')
    internal_label = request.POST.get('internal_label', f'New {section_type}')
    
    if not section_type:
        messages.error(request, 'Section type is required')
        return redirect('dashboard:page_builder', page_id=page_id)
    
    # Get the highest sort_order and add 1
    max_order = page.sections.aggregate(models.Max('sort_order'))['sort_order__max'] or 0
    
    # Create default config based on section type
    default_config = get_default_config_for_section_type(section_type)
    
    # Create section with both draft and published configs
    section = Section.objects.create(
        page=page,
        section_type=section_type,
        internal_label=internal_label,
        sort_order=max_order + 1,
        draft_config=default_config.copy(),  # Start with draft
        published_config=default_config.copy(),  # Also publish it initially
        section_config=default_config,  # Legacy field for backward compatibility
    )
    
    messages.success(request, f'Section "{internal_label}" added successfully')
    return redirect('dashboard:section_edit', section_id=section.id)


@login_required
def section_edit(request, section_id):
    """Edit a section's configuration"""
    section = get_object_or_404(Section, id=section_id)
    # Use draft_config for editing, fallback to published_config or section_config
    config = section.draft_config if section.draft_config else (section.published_config if section.published_config else (section.section_config or {}))
    
    if request.method == 'POST':
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            # Parse form data and update draft_config
            new_config = parse_form_data_to_config(request.POST, section.section_type)
            
            # Save to draft_config (not published_config)
            section.draft_config = new_config
            section.internal_label = request.POST.get('internal_label', section.internal_label)
            section.save()
            
            # For AJAX requests, return JSON instead of redirecting
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({
                    'success': True,
                    'message': 'Draft saved! Preview updated. Click "Publish All Changes" to make it live.',
                    'section_id': section.id,
                    'page_id': section.page.id
                })
            
            # For regular form submissions, redirect
            messages.success(request, 'Draft saved! Preview updated. Click "Publish All Changes" to make it live.')
            return redirect('dashboard:page_builder', page_id=section.page.id)
        except Exception as e:
            # Handle errors
            if is_ajax:
                from django.http import JsonResponse
                import traceback
                return JsonResponse({
                    'success': False,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }, status=400)
            else:
                messages.error(request, f'Error saving section: {str(e)}')
                return redirect('dashboard:page_builder', page_id=section.page.id)
    
    return render(request, 'dashboard/section_edit.html', {
        'section': section,
        'config': config,
    })


@login_required
@require_http_methods(["POST"])
def section_delete(request, section_id):
    """Delete a section"""
    section = get_object_or_404(Section, id=section_id)
    page_id = section.page.id
    section.delete()
    messages.success(request, 'Section deleted successfully')
    return redirect('dashboard:page_builder', page_id=page_id)


@login_required
@require_http_methods(["POST"])
def section_toggle(request, section_id):
    """Toggle section enabled/disabled"""
    section = get_object_or_404(Section, id=section_id)
    section.is_enabled = not section.is_enabled
    section.save()
    return JsonResponse({'is_enabled': section.is_enabled})


@login_required
@require_http_methods(["POST"])
def publish_page(request, page_id):
    """Publish all draft changes for a page"""
    page = get_object_or_404(Page, id=page_id)
    sections = page.sections.all()
    
    published_count = 0
    for section in sections:
        if section.draft_config and section.draft_config != section.published_config:
            section.published_config = section.draft_config.copy()
            section.save()
            published_count += 1
    
    if published_count > 0:
        messages.success(request, f'Published {published_count} section change(s)! The live site has been updated.')
    else:
        messages.info(request, 'No draft changes to publish.')
    
    return redirect('dashboard:page_builder', page_id=page_id)


@login_required
@require_http_methods(["POST"])
def discard_drafts(request, page_id):
    """Discard all draft changes for a page"""
    page = get_object_or_404(Page, id=page_id)
    sections = page.sections.all()
    
    discarded_count = 0
    for section in sections:
        if section.draft_config and section.draft_config != section.published_config:
            # Reset draft to match published
            section.draft_config = section.published_config.copy() if section.published_config else {}
            section.save()
            discarded_count += 1
    
    if discarded_count > 0:
        messages.info(request, f'Discarded {discarded_count} draft change(s).')
    else:
        messages.info(request, 'No draft changes to discard.')
    
    return redirect('dashboard:page_builder', page_id=page_id)


@login_required
@require_http_methods(["POST"])
def section_move(request, section_id, direction):
    """Move section up or down"""
    section = get_object_or_404(Section, id=section_id)
    
    with transaction.atomic():
        if direction == 'up':
            # Swap with section above
            prev_section = Section.objects.filter(
                page=section.page,
                sort_order__lt=section.sort_order
            ).order_by('-sort_order').first()
            
            if prev_section:
                section.sort_order, prev_section.sort_order = prev_section.sort_order, section.sort_order
                section.save()
                prev_section.save()
        
        elif direction == 'down':
            # Swap with section below
            next_section = Section.objects.filter(
                page=section.page,
                sort_order__gt=section.sort_order
            ).order_by('sort_order').first()
            
            if next_section:
                section.sort_order, next_section.sort_order = next_section.sort_order, section.sort_order
                section.save()
                next_section.save()
    
    return redirect('dashboard:page_builder', page_id=section.page.id)


def get_default_config_for_section_type(section_type):
    """Return default config structure for a section type"""
    # Common defaults for all sections
    common_defaults = {
        'background_image': {'url': '', 'alt_text': ''},
        'gradient': {
            'type': 'none',  # 'none', 'linear', 'radial', 'conic'
            'colors': [],  # Array of hex color codes
            'direction': 'to-right'  # Tailwind-like direction names
        }
    }
    
    defaults = {
        'hero': {
            'headline': '',
            'subheadline': '',
            'body_text': '',
            'quote_text': '',
            'quote_attribution': '',
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'secondary_button': {'label': '', 'url': '', 'variant': 'link', 'shape': 'pill'},
            'image': {'url': '', 'alt_text': ''},
            'icon': '',
            'layout_variant': 'text_left_image_right',
            'background_style': 'dark_band',
            'show_section': True,
            'show_divider_below': False,
            **common_defaults,
        },
        'statistics': {
            'headline': '',
            'intro_text': '',
            'stats': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'dark_band',
            **common_defaults,
        },
        'testimonials': {
            'headline': '',
            'subheadline': '',
            'testimonials': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'credibility': {
            'headline': '',
            'subheadline': '',
            'items': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'pain_points': {
            'headline': '',
            'subheadline': '',
            'intro_quote': '',
            'intro_quote_attribution': '',
            'pain_points': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'split_view',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'what_makes_me_different': {
            'headline': '',
            'subheadline': '',
            'golden_thread_quote_text': '',
            'golden_thread_quote_attribution': '',
            'differentiators': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'soft_gradient',
            **common_defaults,
        },
        'featured_publications': {
            'headline': '',
            'subheadline': '',
            'publications': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'services': {
            'headline': '',
            'subheadline': '',
            'services': [],
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'cards_grid',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'meet_kim': {
            'headline': '',
            'subheadline': '',
            'body_text': '',
            'image': {'url': '', 'alt_text': ''},
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'text_left_image_right',
            'background_style': 'light_surface',
            **common_defaults,
        },
        'mission': {
            'headline': '',
            'subheadline': '',
            'body_text': '',
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'centered_stack',
            'background_style': 'soft_gradient',
            **common_defaults,
        },
        'free_resource': {
            'headline': '',
            'subheadline': '',
            'body_text': '',
            'image': {'url': '', 'alt_text': ''},
            'primary_button': {'label': '', 'url': '', 'variant': 'primary', 'shape': 'rounded'},
            'layout_variant': 'text_left_image_right',
            'background_style': 'light_surface',
            **common_defaults,
        },
    }
    return defaults.get(section_type, {})


def parse_form_data_to_config(post_data, section_type):
    """Parse POST form data into section_config JSON structure matching Backend Config Blueprint"""
    config = {}
    
    # Common text fields
    if 'headline' in post_data:
        config['headline'] = post_data.get('headline', '')
    if 'subheadline' in post_data:
        config['subheadline'] = post_data.get('subheadline', '')
    if 'body_text' in post_data:
        config['body_text'] = post_data.get('body_text', '')
    if 'intro_text' in post_data:
        config['intro_text'] = post_data.get('intro_text', '')
    
    # Quote fields
    if 'quote_text' in post_data:
        config['quote_text'] = post_data.get('quote_text', '')
    if 'quote_attribution' in post_data:
        config['quote_attribution'] = post_data.get('quote_attribution', '')
    if 'intro_quote' in post_data:
        config['intro_quote'] = post_data.get('intro_quote', '')
    if 'intro_quote_attribution' in post_data:
        config['intro_quote_attribution'] = post_data.get('intro_quote_attribution', '')
    if 'golden_thread_quote_text' in post_data:
        config['golden_thread_quote_text'] = post_data.get('golden_thread_quote_text', '')
    if 'golden_thread_quote_attribution' in post_data:
        config['golden_thread_quote_attribution'] = post_data.get('golden_thread_quote_attribution', '')
    
    # Image fields
    if 'image_url' in post_data:
        config['image'] = {
            'url': post_data.get('image_url', ''),
            'alt_text': post_data.get('image_alt_text', '')
        }
        if 'image_position' in post_data:
            config['image_position'] = post_data.get('image_position', 'right')
    
    # Icon
    if 'icon' in post_data:
        config['icon'] = post_data.get('icon', '')
    
    # Primary button
    if 'primary_button_label' in post_data:
        config['primary_button'] = {
            'label': post_data.get('primary_button_label', ''),
            'url': post_data.get('primary_button_url', ''),
            'variant': post_data.get('primary_button_variant', 'primary'),
            'shape': post_data.get('primary_button_shape', 'rounded')
        }
    
    # Secondary button
    if 'secondary_button_label' in post_data:
        config['secondary_button'] = {
            'label': post_data.get('secondary_button_label', ''),
            'url': post_data.get('secondary_button_url', ''),
            'variant': post_data.get('secondary_button_variant', 'link'),
            'shape': post_data.get('secondary_button_shape', 'pill')
        }
    
    # Background image
    if 'background_image_url' in post_data:
        config['background_image'] = {
            'url': post_data.get('background_image_url', ''),
            'alt_text': post_data.get('background_image_alt', '')
        }
    
    # Gradient (always include, even if not set in form)
    gradient_colors_str = post_data.get('gradient_colors', '')
    gradient_colors = [c.strip() for c in gradient_colors_str.split(',') if c.strip()] if gradient_colors_str else []
    config['gradient'] = {
        'type': post_data.get('gradient_type', 'none'),
        'colors': gradient_colors,
        'direction': post_data.get('gradient_direction', 'to-right')
    }
    
    # Layout/background
    if 'layout_variant' in post_data:
        config['layout_variant'] = post_data.get('layout_variant', '')
    if 'background_style' in post_data:
        config['background_style'] = post_data.get('background_style', '')
    
    # Supplemental link
    if 'supplemental_link_label' in post_data:
        config['supplemental_link_label'] = post_data.get('supplemental_link_label', '')
        config['supplemental_link_url'] = post_data.get('supplemental_link_url', '')
    
    # Toggles
    config['show_section'] = post_data.get('show_section') == 'on'
    config['show_divider_above'] = post_data.get('show_divider_above') == 'on'
    config['show_divider_below'] = post_data.get('show_divider_below') == 'on'
    config['emphasize_as_key_section'] = post_data.get('emphasize_as_key_section') == 'on'
    
    # For sections with arrays (stats, testimonials, etc.), preserve existing arrays
    # These will be managed separately or via JSON editor if needed
    # For now, we keep them if they exist in the current config
    
    return config


def smart_compress_to_bytes(src_file) -> bytes:
    """
    Smart compression with iterative quality reduction - always converts to WebP
    Tries to get under TARGET_BYTES (9.3MB), but will return best attempt even if over
    """
    # Reset file pointer
    if hasattr(src_file, 'seek'):
        src_file.seek(0)
    
    # Open image
    im = Image.open(src_file)
    
    # Auto-rotate based on EXIF
    try:
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass  # If EXIF fails, continue with original
    
    # Always use WebP for best compression
    out_fmt = "WEBP"
    
    # Cap extreme dimensions (max 5000px width) - resize larger images
    max_w = 5000
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * (max_w / im.width))), Image.LANCZOS)
    
    # Convert RGBA to RGB if needed (WebP supports RGBA, but RGB is smaller)
    if im.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode == 'P':
            im = im.convert('RGBA')
        if im.mode in ('RGBA', 'LA'):
            background.paste(im, mask=im.split()[-1])
        im = background
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    
    # Iterative quality reduction - always target WebP
    q = 85  # Start quality
    min_q = 40  # Lower minimum for WebP
    step = 3
    
    best_data = None
    best_size = float('inf')
    
    while q >= min_q:
        buf = io.BytesIO()
        try:
            im.save(buf, format="WEBP", quality=q, method=6)
            data = buf.getvalue()
            
            # Track best result
            if len(data) < best_size:
                best_size = len(data)
                best_data = data
            
            # If we hit target, return immediately
            if len(data) <= TARGET_BYTES:
                return data
            
            # If we're under max, that's acceptable too
            if len(data) <= MAX_BYTES:
                return data
            
        except Exception as e:
            # If save fails, try next quality
            pass
        
        # Reduce quality and try again
        q = max(min_q, q - step)
    
    # Return best attempt
    return best_data if best_data is not None else im.tobytes()


def aggressive_compress_to_bytes(src_file) -> bytes:
    """
    More aggressive compression - reduces dimensions further and uses lower quality
    Used as fallback if smart_compress still results in file over 10MB
    """
    # Reset file pointer
    if hasattr(src_file, 'seek'):
        src_file.seek(0)
    
    # Open image
    im = Image.open(src_file)
    
    # Auto-rotate based on EXIF
    try:
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass
    
    # More aggressive dimension capping (max 3000px width)
    max_w = 3000
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * (max_w / im.width))), Image.LANCZOS)
    
    # Convert to RGB
    if im.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode == 'P':
            im = im.convert('RGBA')
        if im.mode in ('RGBA', 'LA'):
            background.paste(im, mask=im.split()[-1])
        im = background
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    
    # Very aggressive quality reduction
    q = 60  # Start lower
    min_q = 30  # Very low minimum
    step = 5  # Larger steps
    
    best_data = None
    best_size = float('inf')
    
    while q >= min_q:
        buf = io.BytesIO()
        try:
            im.save(buf, format="WEBP", quality=q, method=6)
            data = buf.getvalue()
            
            if len(data) < best_size:
                best_size = len(data)
                best_data = data
            
            if len(data) <= MAX_BYTES:
                return data
            
        except Exception:
            pass
        
        q = max(min_q, q - step)
    
    return best_data if best_data is not None else im.tobytes()


def upload_to_cloudinary(file_bytes: bytes, folder: str, public_id: str, tags=None):
    """
    Upload to Cloudinary with optimization settings
    Returns: (result_dict, web_url, thumb_url)
    """
    result = cloudinary.uploader.upload(
        file=io.BytesIO(file_bytes),
        resource_type="image",
        folder=folder or "insight-seeker/uploads",
        public_id=public_id,
        overwrite=True,
        unique_filename=False,
        use_filename=False,
        access_mode="public",  # CRITICAL: Public access
        eager=[{
            "format": "webp",
            "quality": "auto",
            "fetch_format": "auto",
            "crop": "limit",
            "width": 2400
        }],
        tags=(tags or []),
        timeout=120,
    )
    
    # Generate URL variants
    secure_url = result.get("secure_url", "")
    
    # Web-optimized variant
    if "/upload/" in secure_url:
        web_url = secure_url.replace("/upload/", "/upload/f_auto,q_auto/")
        thumb_url = secure_url.replace("/upload/", "/upload/c_fill,g_face,w_480,h_320/")
    else:
        web_url = secure_url
        thumb_url = secure_url
    
    return result, web_url, thumb_url


@login_required
@require_http_methods(["POST"])
def upload_image(request):
    """Upload image to Cloudinary - complete logic with compression and MediaAsset storage"""
    try:
        # Get file (support both 'image' and 'file' field names)
        image_file = request.FILES.get('image') or request.FILES.get('file')
        if not image_file:
            return JsonResponse({'success': False, 'error': 'No image file provided'})
        
        # Get optional parameters
        folder = request.POST.get('folder', 'insight-seeker/uploads')
        tags_str = request.POST.get('tags', '')
        tags = [t.strip() for t in tags_str.split(',') if t.strip()] if tags_str else []
        
        # Always compress to WebP - accept any input size since we're converting anyway
        # Only validate the final compressed size
        try:
            file_bytes = smart_compress_to_bytes(image_file)
            
            # After compression, check if still over limit
            if len(file_bytes) > MAX_BYTES:
                # Try more aggressive compression
                file_bytes = aggressive_compress_to_bytes(image_file)
                
                # Final check - if still too large, reject
                if len(file_bytes) > MAX_BYTES:
                    return JsonResponse({
                        'success': False, 
                        'error': f'Image is too large even after compression ({len(file_bytes) / (1024*1024):.1f}MB). Maximum allowed is 10MB. Please use a smaller or less complex image.'
                    })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Image processing error: {str(e)}'})
        
        # Generate public_id from filename
        filename = image_file.name.rsplit('.', 1)[0]  # Remove extension
        public_id = slugify(filename)
        
        # Ensure unique public_id
        base_public_id = public_id
        counter = 1
        while MediaAsset.objects.filter(public_id=f"{folder}/{public_id}").exists():
            public_id = f"{base_public_id}-{counter}"
            counter += 1
        
        # Upload to Cloudinary
        try:
            result, web_url, thumb_url = upload_to_cloudinary(
                file_bytes=file_bytes,
                folder=folder,
                public_id=public_id,
                tags=tags
            )
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Cloudinary upload error: {str(e)}'})
        
        # Store in database
        try:
            asset = MediaAsset.objects.create(
                title=image_file.name,
                public_id=result.get("public_id"),
                secure_url=result.get("secure_url", ""),
                web_url=web_url,
                thumb_url=thumb_url,
                bytes_size=result.get("bytes", 0),
                width=result.get("width", 0),
                height=result.get("height", 0),
                format=result.get("format", ""),
                tags_csv=",".join(tags) if tags else "",
            )
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Database error: {str(e)}'})
        
        # Return JSON response
        return JsonResponse({
            "success": True,
            "id": asset.id,
            "title": asset.title,
            "secure_url": asset.secure_url,
            "web_url": asset.web_url,
            "thumb_url": asset.thumb_url,
            "public_id": asset.public_id,
            "width": asset.width,
            "height": asset.height,
            "format": asset.format,
            "bytes": asset.bytes_size
        })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def gallery_images(request):
    """Get list of images from MediaAsset database (preferred) or Cloudinary fallback"""
    try:
        # Try to get from database first (faster and includes all metadata)
        assets = MediaAsset.objects.filter(is_active=True).order_by('-created_at')[:100]
        
        if assets.exists():
            images = []
            for asset in assets:
                images.append({
                    'id': asset.id,
                    'url': asset.web_url,  # Use optimized web_url
                    'thumbnail': asset.thumb_url,  # Use thumbnail URL
                    'secure_url': asset.secure_url,
                    'public_id': asset.public_id,
                    'format': asset.format,
                    'bytes': asset.bytes_size,
                    'width': asset.width,
                    'height': asset.height,
                    'title': asset.title
                })
            
            return JsonResponse({
                'success': True,
                'images': images
            })
        else:
            # Fallback to Cloudinary API if no database records
            result = cloudinary.api.resources(
                type="upload",
                prefix="insight-seeker/",
                max_results=100,
                resource_type="image"
            )
            
            images = []
            for resource in result.get('resources', []):
                secure_url = resource.get('secure_url') or resource.get('url')
                # Generate variants
                if "/upload/" in secure_url:
                    web_url = secure_url.replace("/upload/", "/upload/f_auto,q_auto/")
                    thumb_url = secure_url.replace("/upload/", "/upload/c_fill,g_face,w_480,h_320/")
                else:
                    web_url = secure_url
                    thumb_url = secure_url
                
                images.append({
                    'url': web_url,
                    'thumbnail': thumb_url,
                    'secure_url': secure_url,
                    'public_id': resource.get('public_id'),
                    'format': resource.get('format'),
                    'bytes': resource.get('bytes'),
                    'width': resource.get('width', 0),
                    'height': resource.get('height', 0),
                    'title': resource.get('public_id', '').split('/')[-1]
                })
            
            return JsonResponse({
                'success': True,
                'images': images
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'images': []
        })

