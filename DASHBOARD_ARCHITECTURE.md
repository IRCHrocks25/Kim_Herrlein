# Dashboard Architecture & Extension Guide

## Table of Contents
1. [Overview](#overview)
2. [How the Dashboard Works](#how-the-dashboard-works)
3. [Connection to Frontend](#connection-to-frontend)
4. [Data Flow](#data-flow)
5. [How to Extend Functionality](#how-to-extend-functionality)
6. [Examples: Adding New Features](#examples-adding-new-features)

---

## Overview

The dashboard is a custom content management system built specifically for non-technical users (like Dilay) to edit website content without touching code or using Django admin. It's completely separate from Django admin and provides a user-friendly, visual interface.

### Key Components

- **Models**: `Page` and `Section` models store all content in JSON fields
- **Views**: Custom dashboard views handle all editing operations
- **Templates**: Tailwind-based UI for the dashboard interface
- **Frontend**: Public website reads from the same database models

---

## How the Dashboard Works

### 1. **Page & Section Structure**

Every page on the website is represented by a `Page` model:
- Each page has a `slug` (e.g., "home", "about")
- Each page can have multiple `Section` objects
- Sections are ordered by `sort_order`

Each `Section` has:
- `section_type`: The type of section (hero, statistics, testimonials, etc.)
- `internal_label`: A name for the editor to identify the section
- `draft_config`: JSON field containing all editable content (what you're editing)
- `published_config`: JSON field containing live content (what visitors see)
- `is_enabled`: Whether the section is visible on the website

### 2. **Draft vs Published System**

This is a key feature that allows editors to:
- Make changes in `draft_config` without affecting the live site
- Preview changes before publishing
- Publish all changes at once with "Publish All Changes" button
- Discard drafts if they don't like the changes

**How it works:**
- When you edit a section, changes go to `draft_config`
- Preview mode (`/preview/home/`) reads from `draft_config`
- Live site reads from `published_config`
- "Publish All Changes" copies `draft_config` → `published_config` for all sections

### 3. **Section Configuration (JSON Structure)**

Each section's content is stored as JSON in `draft_config` and `published_config`. For example, a Hero section might have:

```json
{
  "headline": "Welcome to Insight Seeker",
  "subheadline": "Your journey to reinvention starts here",
  "primary_button": {
    "label": "Schedule a Call",
    "url": "#clarity-call",
    "variant": "primary"
  },
  "secondary_button": {
    "label": "Learn More",
    "url": "#about",
    "variant": "link"
  },
  "image": {
    "url": "https://cloudinary.com/...",
    "alt_text": "Woman in contemplation"
  },
  "layout_variant": "text_left_image_right",
  "background_style": "dark_band"
}
```

### 4. **Dashboard User Flow**

1. **Login** → `/accounts/login/` → Redirects to `/dashboard/`
2. **Dashboard Home** → Lists all pages
3. **Page Builder** → Shows all sections for a page
   - Left panel: Section list + edit form
   - Right panel: Live preview iframe
4. **Edit Section** → Click section → Form loads → Edit → Save
5. **Preview** → Changes appear in preview iframe immediately
6. **Publish** → Click "Publish All Changes" → Changes go live

---

## Connection to Frontend

### 1. **Database as Single Source of Truth**

Both dashboard and frontend read from the same database:

```
┌─────────────────┐
│   Dashboard     │  ← Edits draft_config
│   (Editor UI)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Database      │
│   (Page/Section)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Frontend      │  ← Reads published_config
│   (Public Site) │
└─────────────────┘
```

### 2. **How Frontend Reads Content**

The frontend view (`myApp/views.py` → `home()`) does this:

1. Gets the `Page` with slug="home"
2. Gets all `Section` objects for that page (ordered by `sort_order`)
3. For each section, calls `section.get_config_for_preview(preview_mode=False)`
   - This returns `published_config` (live content)
4. Converts JSON config to template format
5. Passes to template as context variables
6. Template includes the appropriate section partial

### 3. **Template Rendering**

The `home.html` template:
- Loops through all sections
- For each section, includes the matching partial template
- Each partial (e.g., `sections/_hero_section.html`) reads from the config
- Displays content using Tailwind CSS

**Example:**
```django
{% for section in page.sections.all %}
    {% if section.is_enabled %}
        {% include "sections/"|add:section.section_type|add:".html" with config=section_obj %}
    {% endif %}
{% endfor %}
```

### 4. **Preview Mode**

Preview mode (`/preview/home/`) works the same way, but:
- Uses `draft_config` instead of `published_config`
- Has `@xframe_options_exempt` decorator to allow iframe embedding
- Shows changes before they're published

---

## Data Flow

### Saving Changes (Dashboard → Database)

```
1. User edits form in dashboard
   ↓
2. JavaScript intercepts form submit (AJAX)
   ↓
3. POST to /dashboard/sections/{id}/edit/
   ↓
4. section_edit() view receives POST
   ↓
5. parse_form_data_to_config() converts form data to JSON
   ↓
6. Save to section.draft_config
   ↓
7. Return JSON success response
   ↓
8. JavaScript updates preview iframe
   ↓
9. User sees changes in preview (but not on live site yet)
```

### Publishing Changes (Draft → Published)

```
1. User clicks "Publish All Changes"
   ↓
2. POST to /dashboard/pages/{id}/publish/
   ↓
3. publish_page() view loops through all sections
   ↓
4. For each section: copy draft_config → published_config
   ↓
5. Save all sections
   ↓
6. Redirect back to page builder
   ↓
7. Live site now shows published_config
```

### Displaying Content (Database → Frontend)

```
1. Visitor visits homepage
   ↓
2. home() view gets Page with slug="home"
   ↓
3. Gets all enabled sections (ordered by sort_order)
   ↓
4. For each section: get_config_for_preview(preview_mode=False)
   ↓
5. Returns published_config (live content)
   ↓
6. convert_section_config_to_template_format() converts JSON to template format
   ↓
7. Template renders each section partial
   ↓
8. Visitor sees live website
```

---

## How to Extend Functionality

### Understanding the Extension Points

To add new features (like background images, gradients, button shapes), you need to understand these key areas:

#### 1. **Section Configuration Schema**

The JSON structure in `draft_config`/`published_config` defines what can be edited. To add a new field:

**Example: Adding Background Image**
- Add `background_image` to the JSON structure
- Update the form to include an image picker for this field
- Update the template to use this field

#### 2. **Form Parsing Function**

`parse_form_data_to_config()` in `dashboard/views.py` converts form data to JSON. To add a new field:

**Location:** `myProject/dashboard/views.py` → `parse_form_data_to_config()`

**What it does:**
- Takes `request.POST` (form data)
- Converts it to a dictionary/JSON structure
- Returns the config dictionary

**Example:**
```python
# Current code might have:
config['background_style'] = post_data.get('background_style', '')

# To add background_image:
config['background_image'] = {
    'url': post_data.get('background_image_url', ''),
    'alt_text': post_data.get('background_image_alt', '')
}
```

#### 3. **Default Config Function**

`get_default_config_for_section_type()` in `dashboard/views.py` provides default values for new sections.

**Location:** `myProject/dashboard/views.py` → `get_default_config_for_section_type()`

**What it does:**
- Returns a dictionary with default values for a section type
- Used when creating a new section

**Example:**
```python
# Current code might have:
'background_style': 'dark_band'

# To add default background_image:
'background_image': {
    'url': '',
    'alt_text': ''
}
```

#### 4. **Edit Form Template**

The form where users edit sections.

**Location:** `myProject/dashboard/templates/dashboard/section_edit.html`

**What it does:**
- Shows input fields for all editable properties
- Uses `{{ config.field_name }}` to show current values
- Submits form data that gets parsed by `parse_form_data_to_config()`

**Example:**
```django
<!-- Current code might have: -->
<select name="background_style">
    <option value="dark_band">Dark Band</option>
    <option value="soft_gradient">Soft Gradient</option>
</select>

<!-- To add background image picker: -->
<div>
    <label>Background Image</label>
    <input type="text" name="background_image_url" 
           value="{{ config.background_image.url|default:'' }}" 
           id="background_image_url">
    <button type="button" onclick="openImagePickerModal('background_image_url')">
        Pick Image
    </button>
</div>
```

#### 5. **Frontend Template**

The template that displays the section on the website.

**Location:** `myProject/templates/sections/_hero_section.html` (or other section partials)

**What it does:**
- Reads from `config` variable (which comes from `published_config`)
- Renders HTML with Tailwind CSS classes
- Displays the content to visitors

**Example:**
```django
<!-- Current code might have: -->
<div class="bg-navy-deep">
    <!-- content -->
</div>

<!-- To use background image: -->
<div class="bg-cover bg-center" 
     style="background-image: url('{{ config.background_image.url }}');">
    <!-- content -->
</div>
```

---

## Examples: Adding New Features

### Example 1: Adding Background Image Option

**Step 1: Update Default Config**
- **File:** `dashboard/views.py` → `get_default_config_for_section_type()`
- **Add:**
  ```python
  'background_image': {
      'url': '',
      'alt_text': ''
  }
  ```

**Step 2: Update Form Parser**
- **File:** `dashboard/views.py` → `parse_form_data_to_config()`
- **Add:**
  ```python
  config['background_image'] = {
      'url': post_data.get('background_image_url', ''),
      'alt_text': post_data.get('background_image_alt', '')
  }
  ```

**Step 3: Add Form Field**
- **File:** `dashboard/templates/dashboard/section_edit.html`
- **Add:** Image picker field (similar to existing image fields)
- **Use:** `openImagePickerModal('background_image_url')` to open image picker

**Step 4: Update Frontend Template**
- **File:** `templates/sections/_hero_section.html` (or relevant section)
- **Add:** CSS to use background image from `config.background_image.url`

---

### Example 2: Adding Gradient Background Options

**Step 1: Update Default Config**
- **File:** `dashboard/views.py` → `get_default_config_for_section_type()`
- **Add:**
  ```python
  'gradient_type': 'none',  # Options: 'none', 'linear', 'radial', 'conic'
  'gradient_colors': ['#1e3a8a', '#3b82f6'],  # Array of color codes
  'gradient_direction': 'to-right'  # to-right, to-bottom, to-top-right, etc.
  ```

**Step 2: Update Form Parser**
- **File:** `dashboard/views.py` → `parse_form_data_to_config()`
- **Add:**
  ```python
  config['gradient_type'] = post_data.get('gradient_type', 'none')
  config['gradient_colors'] = post_data.get('gradient_colors', '').split(',')
  config['gradient_direction'] = post_data.get('gradient_direction', 'to-right')
  ```

**Step 3: Add Form Fields**
- **File:** `dashboard/templates/dashboard/section_edit.html`
- **Add:**
  - Dropdown for gradient type
  - Color pickers for gradient colors
  - Dropdown for gradient direction

**Step 4: Update Frontend Template**
- **File:** `templates/sections/_hero_section.html`
- **Add:** Dynamic CSS class or inline style based on gradient config
- **Example:**
  ```django
  {% if config.gradient_type == 'linear' %}
      style="background: linear-gradient({{ config.gradient_direction }}, {{ config.gradient_colors|join:', ' }});"
  {% endif %}
  ```

---

### Example 3: Adding Button Shape Options

**Step 1: Update Default Config**
- **File:** `dashboard/views.py` → `get_default_config_for_section_type()`
- **Modify existing button config:**
  ```python
  'primary_button': {
      'label': '',
      'url': '',
      'variant': 'primary',
      'shape': 'rounded'  # NEW: Options: 'rounded', 'pill', 'square', 'custom'
  }
  ```

**Step 2: Update Form Parser**
- **File:** `dashboard/views.py` → `parse_form_data_to_config()`
- **Modify existing button parsing:**
  ```python
  config['primary_button'] = {
      'label': post_data.get('primary_button_label', ''),
      'url': post_data.get('primary_button_url', ''),
      'variant': post_data.get('primary_button_variant', 'primary'),
      'shape': post_data.get('primary_button_shape', 'rounded')  # NEW
  }
  ```

**Step 3: Add Form Field**
- **File:** `dashboard/templates/dashboard/section_edit.html`
- **Add:** Dropdown for button shape in the button configuration section
- **Example:**
  ```django
  <select name="primary_button_shape">
      <option value="rounded" {% if config.primary_button.shape == 'rounded' %}selected{% endif %}>Rounded</option>
      <option value="pill" {% if config.primary_button.shape == 'pill' %}selected{% endif %}>Pill</option>
      <option value="square" {% if config.primary_button.shape == 'square' %}selected{% endif %}>Square</option>
  </select>
  ```

**Step 4: Update Frontend Template**
- **File:** `templates/sections/_hero_section.html` (or wherever buttons are rendered)
- **Add:** Dynamic CSS classes based on shape
- **Example:**
  ```django
  {% if config.primary_button.shape == 'pill' %}
      class="px-6 py-3 rounded-full ..."
  {% elif config.primary_button.shape == 'square' %}
      class="px-6 py-3 rounded-none ..."
  {% else %}
      class="px-6 py-3 rounded-lg ..."
  {% endif %}
  ```

---

## Key Functions Reference

### `parse_form_data_to_config(post_data, section_type)`
**Location:** `dashboard/views.py`

**Purpose:** Converts form POST data into JSON config structure

**Parameters:**
- `post_data`: Django request.POST object
- `section_type`: String like 'hero', 'statistics', etc.

**Returns:** Dictionary that will be saved to `draft_config`

**When to modify:** When adding new form fields that need to be saved

---

### `get_default_config_for_section_type(section_type)`
**Location:** `dashboard/views.py`

**Purpose:** Provides default values for a new section

**Parameters:**
- `section_type`: String like 'hero', 'statistics', etc.

**Returns:** Dictionary with default values

**When to modify:** When adding new fields that need default values

---

### `convert_section_config_to_template_format(section, config=None)`
**Location:** `myApp/views.py`

**Purpose:** Converts JSON config to format expected by templates

**Parameters:**
- `section`: Section model instance
- `config`: Optional config dict (if None, uses section's config)

**Returns:** Dictionary in template-friendly format

**When to modify:** When template needs data in a different format than stored in JSON

---

### `section.get_config_for_preview(preview_mode=False)`
**Location:** `myApp/models.py` → `Section` model

**Purpose:** Returns the correct config (draft or published) based on mode

**Parameters:**
- `preview_mode`: If True, returns `draft_config`; if False, returns `published_config`

**Returns:** Dictionary with section configuration

**When to modify:** Rarely - this handles the draft/published logic

---

## Best Practices

### 1. **Always Update All Three Places**
When adding a new field, update:
- ✅ Default config function
- ✅ Form parser function
- ✅ Edit form template
- ✅ Frontend template

### 2. **Use Consistent Naming**
- Form field names should match what you expect in `parse_form_data_to_config()`
- JSON keys should be descriptive and consistent
- Use snake_case for JSON keys

### 3. **Provide Default Values**
- Always provide defaults in `get_default_config_for_section_type()`
- Use `|default:''` in templates to handle missing values

### 4. **Test Both Draft and Published**
- Test that changes appear in preview (draft)
- Test that published changes appear on live site
- Test that discarding drafts works correctly

### 5. **Use Image Picker for Images**
- Don't create new image upload mechanisms
- Reuse `openImagePickerModal(fieldId)` function
- Store image URLs in config, not file objects

---

## Common Patterns

### Pattern 1: Adding a Simple Text Field

1. **Default Config:**
   ```python
   'new_field': ''
   ```

2. **Form Parser:**
   ```python
   config['new_field'] = post_data.get('new_field', '')
   ```

3. **Form Template:**
   ```django
   <input type="text" name="new_field" 
          value="{{ config.new_field|default:'' }}">
   ```

4. **Frontend Template:**
   ```django
   {{ config.new_field }}
   ```

---

### Pattern 2: Adding a Dropdown/Select Field

1. **Default Config:**
   ```python
   'new_option': 'default_value'
   ```

2. **Form Parser:**
   ```python
   config['new_option'] = post_data.get('new_option', 'default_value')
   ```

3. **Form Template:**
   ```django
   <select name="new_option">
       <option value="option1" {% if config.new_option == 'option1' %}selected{% endif %}>Option 1</option>
       <option value="option2" {% if config.new_option == 'option2' %}selected{% endif %}>Option 2</option>
   </select>
   ```

4. **Frontend Template:**
   ```django
   {% if config.new_option == 'option1' %}
       <!-- Render option 1 -->
   {% elif config.new_option == 'option2' %}
       <!-- Render option 2 -->
   {% endif %}
   ```

---

### Pattern 3: Adding an Image Field

1. **Default Config:**
   ```python
   'new_image': {
       'url': '',
       'alt_text': ''
   }
   ```

2. **Form Parser:**
   ```python
   config['new_image'] = {
       'url': post_data.get('new_image_url', ''),
       'alt_text': post_data.get('new_image_alt', '')
   }
   ```

3. **Form Template:**
   ```django
   <div>
       <label>New Image</label>
       <input type="text" name="new_image_url" 
              value="{{ config.new_image.url|default:'' }}" 
              id="new_image_url">
       <button type="button" onclick="openImagePickerModal('new_image_url')">
           Pick Image
       </button>
       <input type="text" name="new_image_alt" 
              value="{{ config.new_image.alt_text|default:'' }}" 
              placeholder="Alt text">
   </div>
   ```

4. **Frontend Template:**
   ```django
   {% if config.new_image.url %}
       <img src="{{ config.new_image.url }}" 
            alt="{{ config.new_image.alt_text }}">
   {% endif %}
   ```

---

## Troubleshooting

### Changes Not Appearing in Preview
- ✅ Check that you're saving to `draft_config` (not `published_config`)
- ✅ Check that preview URL is `/preview/home/` (not `/`)
- ✅ Check browser console for JavaScript errors
- ✅ Verify form is submitting correctly (check Network tab)

### Changes Not Appearing on Live Site
- ✅ Check that you clicked "Publish All Changes"
- ✅ Verify `published_config` has the data (check Django admin)
- ✅ Check that section `is_enabled = True`
- ✅ Clear browser cache

### Form Not Saving
- ✅ Check browser console for errors
- ✅ Verify CSRF token is included in form
- ✅ Check that `parse_form_data_to_config()` includes your new field
- ✅ Verify form field names match what parser expects

### Image Picker Not Working
- ✅ Ensure `image_picker_modal.html` is included in `page_builder.html`
- ✅ Check that `openImagePickerModal()` is attached to `window` object
- ✅ Verify Cloudinary credentials are set in `.env` file
- ✅ Check browser console for JavaScript errors

---

## Summary

The dashboard works by:
1. **Storing content as JSON** in `draft_config` and `published_config` fields
2. **Converting form data to JSON** via `parse_form_data_to_config()`
3. **Displaying forms** that let editors edit the JSON structure
4. **Rendering content** on frontend by reading from `published_config`

To extend functionality:
1. **Add field to default config** → Provides default value
2. **Add field to form parser** → Saves form data to JSON
3. **Add field to edit form** → Lets user edit the value
4. **Add field to frontend template** → Displays the value

The key is understanding that everything flows through the JSON config structure, and you need to update all four places (default, parser, form, template) for a complete feature.

---

**Last Updated:** December 2024
**Version:** 1.0
