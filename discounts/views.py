from django.db.models import Q, F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from discounts.models import Store, PromoCode
from discounts.pagination import StorePagination, PromocodePagination
from discounts.serializers import StoreSerializer, PromoCodeSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = StorePagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    @action(detail=False, methods=['GET'])
    def filter_by_category_or_name(self, request):
        category_id = request.query_params.get('category_id')
        store_name = request.query_params.get('store_name')

        if not category_id and not store_name:
            return Response({"error": "Please provide category_id and store_name in the query parameters."}, status=400)

        queryset = Store.objects.all()

        if category_id and store_name:
            queryset = queryset.filter(Q(category_id=category_id) & ~Q(promo_codes__isnull=True) | Q(name__icontains=store_name))

        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    pagination_class = PromocodePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    @action(detail=False, methods=['GET'])
    def promocodes_filter(self, request):
        store_id = request.GET.get('store_id')

        if not store_id:
            return Response({'error': 'Missing store_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()

        query = (
                Q(store__id=store_id) & Q(is_active=True) |
                Q(store__id=store_id) & Q(expiration_date__gte=current_time) & Q(likes__gt=F('dislikes'))
        )

        promo_codes = PromoCode.objects.filter(query)
        serializer = PromoCodeSerializer(promo_codes, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def submit_feedback(self, request, pk=None):
        """
        Submit feedback (likes or dislikes) for a promo code.
        """
        promo_code = self.get_object()
        feedback_type = request.data.get('feedback_type')

        if feedback_type == 'like':
            promo_code.likes += 1
        elif feedback_type == 'dislike':
            promo_code.dislikes += 1
        else:
            return Response({'status': 'error', 'message': 'Invalid feedback type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        promo_code.save()

        return Response({'status': 'success', 'message': f'Feedback submitted. {feedback_type.capitalize()} added.'},
                        status=status.HTTP_201_CREATED)
