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

Dependencies are managed with `uv`; every command runs through `uv run`.

### First-time setup
```bash
cp .env.example .env    # then fill in DJANGO_SECRET_KEY
uv sync
```

### Running the Application
```bash
uv run python manage.py runserver
```

### Database Operations
```bash
uv run python manage.py migrate
uv run python manage.py loaddata catalog/fixtures/catalog_test_data.yaml  # Load test data
uv run python manage.py loaddata catalog/fixtures/catalog_legacy_data.yaml  # Load legacy data
```

### Testing
```bash
uv run python manage.py test          # Run all tests
uv run python manage.py test catalog  # Run catalog app tests only
```

`manage.py` supplies a throwaway `SECRET_KEY`, disables the static manifest,
and redirects `MEDIA_ROOT` to a temp directory for the `test` command — so the
suite runs on a bare checkout and never writes into the real media library.

### Static Files
```bash
uv run python manage.py collectstatic
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

Push to `main`. `.github/workflows/deploy.yml` runs the test suite, then SSHes
to the host and runs `git reset --hard`, `uv sync --frozen`, `migrate`,
`collectstatic`, and `systemctl restart nincatalog`.

Serving stack, all configured from files in this repo:

- `gunicorn.conf.py` — binds `unix:/run/nincatalog/gunicorn.sock`
- `nincatalog.service` — systemd unit, reads `/var/www/nincatalog/.env`
- `nginx.conf` — TLS, `/static/` and `/media/` aliases, proxy to the socket
- `nincatalog-backup.service` / `.timer` — daily `manage.py backup_db` to
  `s3://nin-host-backups/nincatalog/db/`. Installed by copying both files to
  `/etc/systemd/system/`, then `systemctl enable --now nincatalog-backup.timer`

Layout on the host:

| Path | Contents |
|---|---|
| `/var/www/nincatalog` | Git tree, `.venv/`, `staticfiles/`, `.env`. Disposable |
| `/srv/nincatalog` | `db.sqlite3` (backed up daily to S3) and, until retired after the S3 move, `media/`. Never touched by deploys |

Media lives in the private S3 bucket `nincatalog-media`, served by CloudFront
at `media.nincatalog.com`; enabled by `DJANGO_MEDIA_S3_BUCKET` and
`DJANGO_MEDIA_DOMAIN` in `.env`. The host's EC2 instance role (shared with
nin.fan) grants S3 access — there are no AWS keys in `.env`.

Configuration comes from `.env`; see `.env.example`. Three traps:

- **Single-quote any value containing `#` or `$`.** Both django-environ and
  systemd treat an unquoted `#` as a comment and silently truncate the value.
- **nginx must reach gunicorn over the unix socket**, and must send
  `X-Forwarded-Proto`. Gunicorn derives `wsgi.url_scheme` from that header over
  a socket connection, which is what makes `request.is_secure()` true and admin
  CSRF pass. Moving to TCP on a non-loopback address breaks admin forms.
- **`.env` is read only when the service starts.** After editing it, run
  `systemctl restart nincatalog`; `reload` does not pick up changes.

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

Uploaded files use Django's default storage: disk under `MEDIA_ROOT` locally,
S3 in production (see Deployment). Object keys are identical either way:
- `item_images/` - Product photographs
- `categories/` - Category/album artwork
- `countries/` - Country flag icons
- `eras/` - Era-specific imagery
- `CACHE/` - imagekit derivatives

imagekit uses the `Optimistic` strategy: derivatives are generated when the
source image is saved and are assumed to exist when rendered. After loading
fixtures or copying media, run `uv run python manage.py generateimages`, or
thumbnails render as broken images.