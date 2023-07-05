from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
