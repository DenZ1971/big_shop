from .models import Category

def categories(request):
   """
   Retrieves all categories with no parent category.

   Args:
       request: The HTTP request object.

   Returns:
       A dictionary containing the 'categories' key with a queryset of Category objects filtered by parent=None.
   """
   categories =  Category.objects.filter(parent=None)
   return {'categories': categories}