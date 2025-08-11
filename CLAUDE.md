# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based catalog system for Nine Inch Nails collectibles and merchandise, featuring multi-subdomain architecture. The project manages a comprehensive database of NIN items including albums, singles, merchandise, and related materials with detailed metadata, images, and categorization.

## Architecture

### Multi-App Structure
- **catalog/** - Core catalog application for NIN releases and collectibles
- **merch/** - Merchandise-specific functionality  
- **nincatalog/** - Main Django project configuration
- **util/** - Legacy data migration utilities

### Multi-Host Configuration
The application uses django-hosts to serve different content on different subdomains:
- `www` subdomain → catalog app (main catalog)
- `merch` subdomain → merch app (merchandise)
- `admin` subdomain → Django admin interface

### Key Models (catalog/models.py)
- **Item** - Core model for catalog entries with CloneMixin support
- **Category** - Hierarchical organization (albums, singles, etc.) with halo numbers
- **Artist, MediaFormat, Country** - Reference data models
- **Track** - Individual tracks linked to items
- **ItemImage** - Multiple images per item with ordering
- **Report** - Dynamic report configurations

## Development Commands

### Running the Application
```bash
python manage.py runserver
```

### Database Operations
```bash
python manage.py migrate
python manage.py loaddata catalog/fixtures/catalog_test_data.yaml  # Load test data
python manage.py loaddata catalog/fixtures/catalog_legacy_data.yaml  # Load legacy data
```

### Testing
```bash
python manage.py test  # Run all tests
python manage.py test catalog  # Run catalog app tests only
```

### Static Files
```bash
python manage.py collectstatic
```

## Key Dependencies

- **Django 5.x** - Web framework
- **django-clone** - Model cloning functionality for Items
- **django-hosts** - Multi-subdomain routing
- **django-imagekit** - Image processing and thumbnails
- **Pillow** - Image handling
- **PyYAML** - Fixture data loading
- **Markdown2** - Text formatting (see catalog/templatetags/markdown.py)

## Search Functionality

The merch app includes a search feature with relevancy ranking:

### Search Implementation
- **Search endpoint**: `/search/` - Accepts GET parameter `q` for query
- **Relevancy scoring**: Uses Django's `Case/When` to rank results by:
  - Exact name match (score: 100)
  - Name starts with query (score: 90)
  - Name contains query (score: 80)
  - Product ID match (score: 70)
  - Material match (score: 60)
  - Category name match (score: 50)
  - Description match (score: 40)
- **Search fields**: Name, description, material, product_id, category names
- **Authorization filtering**: Excludes products with `is_authorized='N'`
- **Templates**: Search bar on index page, dedicated search results page

## Database

Uses SQLite in development (`db.sqlite3`). The database includes comprehensive catalog data with:
- Items organized by categories with halo numbers (NIN's numbering system)
- Multi-country releases with country-specific metadata
- Complex many-to-many relationships (items ↔ music labels)
- Image galleries with ordered display
- Track listings with duration metadata

## Deployment

Configured for uWSGI deployment (see uwsgi.ini) with:
- Socket-based communication
- Process management
- Logging to `/home/www/nincatalog.com/logs/`

## Legacy Data Utilities

The `util/` directory contains migration scripts for importing legacy data:
- `legacy_xml2txt.py` - XML to text conversion
- `legacy_txt2yaml.py` - Text to YAML fixture conversion
- `legacy_remap_images.py` - Image path remapping

## Template System

Uses Django's template system with custom template tags:
- `track_length.py` - Duration formatting
- `track_title.py` - Track name formatting
- `upc_url.py` - UPC code linking
- `markdown.py` - Markdown text processing

When working with templates, they are located in each app's `templates/` directory following Django conventions.

## Media Handling

Extensive media organization under `media/`:
- `item_images/` - Product photographs
- `categories/` - Category/album artwork
- `countries/` - Country flag icons
- `eras/` - Era-specific imagery

Images are processed through django-imagekit for thumbnails and optimization.