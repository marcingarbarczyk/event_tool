from django.test import TestCase

from utils.models import Orderable


# Concrete Model For Testing
class ConcreteOrderable(Orderable):
    pass


class OrderableTest(TestCase):
    def test_order_queryset(self):
        object1 = ConcreteOrderable.objects.create(order=2)
        object2 = ConcreteOrderable.objects.create(order=1)
        object3 = ConcreteOrderable.objects.create(order=3)

        qs = ConcreteOrderable.objects.all()

        self.assertEqual(qs[0], object2)
        self.assertEqual(qs[1], object1)
        self.assertEqual(qs[2], object3)
