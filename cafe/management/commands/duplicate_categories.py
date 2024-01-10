from django.core.management.base import BaseCommand
from cafe.models import Category, Cafe, MenuItem


class Command(BaseCommand):
    help = "Duplicate null cafe categories for an existing cafe"

    def add_arguments(self, parser):
        parser.add_argument(
            "existing_cafe_id", type=int, help="ID of the existing cafe"
        )

    def handle(self, *args, **options):
        existing_cafe_id = options["existing_cafe_id"]

        # Get Specific Cafe
        try:
            existing_cafe = Cafe.objects.get(pk=existing_cafe_id)
        except Cafe.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Cafe with ID {existing_cafe_id} does not exist")
            )
            return

        # Get Default Categories
        null_cafe_categories = Category.objects.filter(cafe__isnull=True)

        for category in null_cafe_categories:
            # Duplicate the category and associate it with the existing cafe

            # Get Menu Item By Cafe & Category
            items = MenuItem.objects.get_list_by(existing_cafe, category)

            if category.menu_items.filter(cafe=existing_cafe).count() == 0:
                continue

            duplicated_category = Category.objects.create(
                title=category.title,
                image=category.image,
                order=category.order,
                cafe=existing_cafe,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Duplicated category: {duplicated_category}")
            )

            # Assign the new category to items
            for item in items:
                item.category = duplicated_category
                item.save()

        self.stdout.write(self.style.SUCCESS("Categories duplicated successfully"))
