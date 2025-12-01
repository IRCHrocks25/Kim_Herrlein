from django.core.management.base import BaseCommand
from myApp.models import Section
import copy


class Command(BaseCommand):
    help = 'Migrate section_config data to draft_config and published_config'

    def handle(self, *args, **options):
        self.stdout.write('Migrating section_config to draft_config and published_config...')
        
        migrated_count = 0
        skipped_count = 0
        
        for section in Section.objects.all():
            # Check what configs exist
            has_section_config = section.section_config and isinstance(section.section_config, dict) and len(section.section_config) > 0
            has_draft_config = section.draft_config and isinstance(section.draft_config, dict) and len(section.draft_config) > 0
            has_published_config = section.published_config and isinstance(section.published_config, dict) and len(section.published_config) > 0
            
            # Check if draft/published are empty dicts
            draft_is_empty = not section.draft_config or (isinstance(section.draft_config, dict) and len(section.draft_config) == 0)
            published_is_empty = not section.published_config or (isinstance(section.published_config, dict) and len(section.published_config) == 0)
            
            # Debug output
            self.stdout.write(f'\nChecking: {section.page.name} - {section.get_section_type_display()}')
            self.stdout.write(f'  section_config: {has_section_config} (len: {len(section.section_config) if section.section_config else 0})')
            self.stdout.write(f'  draft_config: {has_draft_config} (len: {len(section.draft_config) if section.draft_config else 0})')
            self.stdout.write(f'  published_config: {has_published_config} (len: {len(section.published_config) if section.published_config else 0})')
            
            if has_section_config and (draft_is_empty or published_is_empty):
                # Migrate section_config to both draft and published
                section.draft_config = copy.deepcopy(section.section_config)
                section.published_config = copy.deepcopy(section.section_config)
                section.save(update_fields=['draft_config', 'published_config'])
                migrated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Migrated: {section.page.name} - {section.get_section_type_display()} ({section.internal_label})'))
            elif not has_section_config and (draft_is_empty and published_is_empty):
                # Section has no config at all - show warning
                self.stdout.write(self.style.WARNING(f'  ⚠ No config data: {section.page.name} - {section.get_section_type_display()} ({section.internal_label})'))
                skipped_count += 1
            else:
                self.stdout.write(f'  → Skipped (already has configs)')
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nMigration complete!'))
        self.stdout.write(f'  Migrated: {migrated_count} sections')
        self.stdout.write(f'  Skipped: {skipped_count} sections (already have configs or no section_config data)')

