import django_filters
from django.utils import timezone
from .models import Order


class OrderFilter(django_filters.FilterSet):
    # 定义过滤参数 created_at_date（前端传递的日期，如 ?created_at_date=2023-10-20）
    day = django_filters.NumberFilter(
        method='filter_created_date',  # 自定义过滤逻辑
        label='按日期过滤 (格式: YYYY-MM-DD)',
        field_name='day',
    )
    status = django_filters.NumberFilter(
        field_name='status',
    )

    class Meta:
        model = Order
        fields = ['created_at','status']

    def filter_created_date(self, queryset, name, value):
        """
        将日期转换为当天的起止时间范围，过滤 created_at 在该范围内的订单
        """
        if value:
            # 处理时区（假设项目启用时区支持）
            value = int(value)
            start_date =value - 1
            start_time = timezone.make_aware(timezone.datetime(timezone.now().year, timezone.now().month, timezone.now().day))-timezone.timedelta(days=start_date)
            end_time = start_time + timezone.timedelta(days=value)
            # 过滤 created_at 在 [start_time, end_time) 区间内的订单
            return queryset.filter(created_at__gte=start_time, created_at__lt=end_time)
        return queryset