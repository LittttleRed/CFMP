import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from product.models import Product
from root.models import Complaint, ComplaintReview, Order

# 定义命名空间 URL 辅助函数
def get_url(view_name, **kwargs):
    return reverse(f'root:{view_name}-list', kwargs=kwargs)
@pytest.mark.django_db
class RootAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 创建管理员用户用于认证
        self.admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='password123',
            user_id=1,
            privilege=1  # 假设特权字段为 1 表示管理员
        )
        self.client.force_authenticate(user=self.admin_user)

        # 创建普通用户
        self.normal_user = User.objects.create(
            username='user',
            email='user@example.com',
            password='password123',
            user_id=2,
            privilege=0
        )

        # 创建商品
        self.product = Product.objects.create(
            product_id=1,
            title="Test Product",
            description="This is a test product",
            price=100.00,
            user=self.normal_user
        )

        # 创建订单
        self.order = Order.objects.create(
            order_id=1,
            buyer=self.normal_user,
            total_amount=100.00,
            status=0
        )

        # 创建举报
        self.complaint = Complaint.objects.create(
            complaint_id=1,
            complainer_id=self.normal_user,
            target_type=0,  # 0: 商品举报
            target_id=1,
            reason="Test complaint"
        )

    def test_user_list(self):
        url = get_url('user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_product_list(self):
        url = get_url('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_complaint_list(self):
        url = get_url('complaint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_order_list(self):
        url = get_url('order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_create_complaint_review(self):
        url = get_url('review')

        data = {
            "target_id": 1,
            "target_type": 0,
            "reviewer_id": self.admin_user.user_id,
            "result": "处理完成",
            "ban_type": "警告",
            "ban_time": 7
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ComplaintReview.objects.filter(review_id=1).exists())

    def test_update_user_status(self):
        url = get_url('user') + f'{self.normal_user.user_id}/'
        data = {"status": 1}  # 封禁用户
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.status, 1)

    def test_get_single_user(self):
        url = get_url('user') + f'{self.admin_user.user_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'admin')

    def test_search_users_by_username(self):
        url = get_url('user') + '?username=user'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data['data'])
        self.assertEqual(len(response.data['data']['results']), 1)
        self.assertEqual(response.data['data']['results'][0]['username'], 'user')

    def test_branch_update_complaint(self):
        url = reverse('root:complaint-branch', kwargs={'target_type': 0, 'target_id': 1})
        data = {"status": 1}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, 1)


