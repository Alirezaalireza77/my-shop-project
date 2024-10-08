from django.test import TestCase
from .factories import OrderFactory, OrderStatusChangeLogFactory, UserFactory
from shop.tests.factories import ProductFactory, CategoryFactory
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
# Create your tests here.


class OrderTestCase(TestCase):
    def setUp(self):
        self.order = OrderFactory()

    def test_change_status_valid(self):
        order = OrderFactory()
        order.change_status('paid')
        self.assertEqual(order.status, 'paid')
        log_entry = OrderStatusChangeLogFactory(order=order, old_status='new', new_status='paid')
        self.assertEqual(log_entry.old_status, 'new')
        self.assertEqual(log_entry.new_status, 'paid')


    def test_change_status_invalid(self):
        order = OrderFactory()
        with self.assertRaises(ValidationError) as context:
            order.change_status('sent')
        self.assertEqual(str(context.exception), "['Invalid status and you cannot change status from new to sent.']")   
        self.assertEqual(order.status, 'new')

    def test_change_status_log_from_cancel(self):
        order = OrderFactory()
        order.change_status('cancel')
        log_entries = OrderStatusChangeLogFactory(order=order, old_status='new', new_status= 'cancel')
        last_log_entry = log_entries
        self.assertEqual(last_log_entry.old_status, 'new')
        self.assertEqual(last_log_entry.new_status, 'cancel')


    def test_change_status_log(self):
        order = OrderFactory()
        order.change_status('paid')
        log_entries = OrderStatusChangeLogFactory(order=order, old_status='new', new_status='paid')
        last_log_entry = log_entries
        self.assertEqual(last_log_entry.old_status, 'new')
        self.assertEqual(last_log_entry.new_status, 'paid')

    
    def test_change_status_log_from_paid(self):
        order = OrderFactory()
        order.status = 'paid'
        order.change_status('sent')
        log_entries = OrderStatusChangeLogFactory(order=order, old_status='paid', new_status='sent')
        last_log_entry = log_entries
        self.assertEqual(last_log_entry.old_status, 'paid')
        self.assertEqual(last_log_entry.new_status, 'sent')


    def test_phone_number_invalid(self):
            order = OrderFactory()
            order.phone = '08137327372'
            with self.assertRaises(ValidationError) as context:
                order.clean()
                self.assertEqual(str(context.exception),"['phone number must be started with \"09\"']")

    def test_phone_not_number(self):
        order = OrderFactory()
        order.phone = '09ft7876845'
        with self.assertRaises(ValidationError) as context:
            order.clean()
            self.assertEqual(str(context.exception), "['phone number must contain only number.']")


    def test_phone_number_valid(self):
        order = OrderFactory()
        order.quantity = 1
        order.phone = '09121212121'
        order.clean()
        
        

    def test_number_of_quantity_invalid(self):
        order = OrderFactory()
        order.quantity = 0
        with self.assertRaises(ValidationError) as context:
            order.clean()
            self.assertEqual(str(context.exception), "['quentities of order must be 1 atleast.']")


    def test_quantity_valid(self):
        order = OrderFactory()
        order.quantity = 1
        order.phone = '09121212122'
        order.clean()


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create()
        self.client.force_authenticate(user=self.user)


    def test_order_creatation(self):
        url = reverse('order-list')
        data = {
            'product': self.product.id,
            'quantity': 2,
            'address': 'tehran',
            'phone': '09121212121'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_orders_list(self):
        OrderFactory.create(user=self.user, product=self.product)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_update_order_status(self):
        order = OrderFactory.create(user=self.user, product=self.product)
        url = reverse('order-detail', args=[order.id])
        data = {
            'status': 'paid'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')


    def test_invalid_order_phone(self):
        url = reverse('order-list')
        data = {
            'product': self.product.id,
            'quantity': 2,
            'address': 'tehran',
            'phone': '12345678',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)