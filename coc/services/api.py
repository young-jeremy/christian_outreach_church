from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    MarriageMinistrySerializer,
    CoupleProfileSerializer,
    MarriageResourceSerializer
)


class MarriageMinistryViewSet(viewsets.ModelViewSet):
    queryset = MarriageMinistry.objects.all()
    serializer_class = MarriageMinistrySerializer
    permission_classes = [IsAuthenticated]


class CoupleProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CoupleProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CoupleProfile.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )


class MarriageResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MarriageResource.objects.all()
    serializer_class = MarriageResourceSerializer
    permission_classes = [IsAuthenticated]
