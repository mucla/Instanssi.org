# -*- coding: utf-8 -*-

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from .serializers import EventSerializer, SongSerializer, CompetitionSerializer, CompoSerializer,\
    ProgrammeEventSerializer, SponsorSerializer, MessageSerializer, IRCMessageSerializer, StoreItemSerializer,\
    StoreTransactionSerializer, CompoEntrySerializer, CompetitionParticipationSerializer, UserSerializer, \
    UserCompoEntrySerializer
from .utils import GroupBasePermission, CanUpdateScreenData, IsAuthenticatedOrWriteOnly, WriteOnlyModelViewSet, \
    FilterMixin, ReadUpdateModelViewSet
from Instanssi.kompomaatti.models import Event, Competition, Compo, Entry, CompetitionParticipation
from Instanssi.ext_programme.models import ProgrammeEvent
from Instanssi.screenshow.models import NPSong, Sponsor, Message, IRCMessage
from Instanssi.store.models import StoreItem
from Instanssi.store.handlers import begin_payment_process
from Instanssi.store.methods import PaymentMethod


class CurrentUserViewSet(ReadUpdateModelViewSet):
    """
    Shows data to the authenticated user about self
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class EventViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all Instanssi events. Note that ID's assigned to events are guaranteed to stay the same; they will not
    change, ever. So if you want, you can hardcode the event id's in your own code and don't need to bother fetching
    this data.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        q = Event.objects.filter(name__startswith='Instanssi')
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class SongViewSet(ReadOnlyModelViewSet, CreateModelMixin, FilterMixin):
    """
    Exposes all Instanssi songs on playlist. Note that order is order is descending by default.

    State:
    0: Playing
    1: Stopped

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is '-id'. Allowed: id, -id
    """
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated, CanUpdateScreenData, TokenHasReadWriteScope]

    def get_queryset(self):
        q = NPSong.objects.get_queryset()
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request, default='-id')
        q = self.filter_by_lim_off(q, self.request)
        return q


class CompetitionViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all sports competitions.

    Score_sort:
    0: Highest score first
    1: Lowest score first

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        q = Competition.objects.filter(active=True)
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class CompetitionParticipationViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all competition participations. This is everything that does not drop neatly to the democompo category,
    eg. sports events etc.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * competition: Filter by competition id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = CompetitionParticipationSerializer

    def get_queryset(self):
        q = CompetitionParticipation.objects.filter(competition__active=True)
        q = self.filter_by_competition(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class CompoViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all compos.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = CompoSerializer

    def get_queryset(self):
        q = Compo.objects.filter(active=True)
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class CompoEntryViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all compo entries.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * compo: Filter by compo id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = CompoEntrySerializer

    def get_queryset(self):
        q = Entry.objects.filter(compo__active=True)
        q = self.filter_by_compo(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class UserCompoEntryViewSet(ModelViewSet, FilterMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCompoEntrySerializer

    def get_queryset(self):
        q = Entry.objects.filter(compo__active=True, user=self.request.user)
        q = self.filter_by_compo(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompoEntryFileUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        print(request.data)
        file_obj = request.data['file']

        return Response(status=204)


class ProgrammeEventViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all programme events.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = ProgrammeEventSerializer

    def get_queryset(self):
        q = ProgrammeEvent.objects.filter(active=True)
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class SponsorViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all sponsors.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = SponsorSerializer

    def get_queryset(self):
        q = Sponsor.objects.get_queryset()
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class MessageViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all sponsor messages.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is 'id'. Allowed: id, -id
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        q = Message.objects.get_queryset()
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request)
        q = self.filter_by_lim_off(q, self.request)
        return q


class IRCMessageViewSet(ReadOnlyModelViewSet, FilterMixin):
    """
    Exposes all saved IRC messages. Note that order is order is descending by default.

    Allows GET filters:
    * limit: Limit amount of returned objects.
    * offset: Starting offset. Default is 0.
    * event: Filter by event id
    * order_by: Set ordering, default is '-id'. Allowed: id, -id
    """
    serializer_class = IRCMessageSerializer

    def get_queryset(self):
        q = IRCMessage.objects.get_queryset()
        q = self.filter_by_event(q, self.request)
        q = self.order_by(q, self.request, default='-id')
        q = self.filter_by_lim_off(q, self.request)
        return q


class StoreItemViewSet(ReadOnlyModelViewSet):
    """
    Exposes all available store items.  This entrypoint does not require authentication/authorization.
    """
    serializer_class = StoreItemSerializer
    queryset = StoreItem.items_available()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []


class StoreTransactionViewSet(WriteOnlyModelViewSet):
    """
    Handles saving store transactions. This entrypoint does not require authentication/authorization.
    """
    serializer_class = StoreTransactionSerializer
    permission_classes = [IsAuthenticatedOrWriteOnly]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['save']:
                ta = serializer.save()
                payment_method = PaymentMethod(serializer.validated_data['payment_method'])
                response_url = begin_payment_process(payment_method, ta)
                return Response({"url": response_url}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
