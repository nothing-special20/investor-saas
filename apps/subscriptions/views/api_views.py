from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.permissions import IsAuthenticatedOrHasUserAPIKey
from apps.teams.decorators import team_admin_required

from ..exceptions import SubscriptionConfigError
from ..helpers import create_stripe_checkout_session, create_stripe_portal_session
from ..metadata import get_active_products_with_metadata


class ProductWithMetadataAPI(APIView):
    permission_classes = (IsAuthenticatedOrHasUserAPIKey,)

    @extend_schema(
        operation_id='active_products_list',
    )
    def get(self, request, *args, **kw):
        products_with_metadata = get_active_products_with_metadata()
        return Response(
            data=[p.to_dict() for p in products_with_metadata]
        )


@extend_schema(
    tags=["subscriptions"]
)
class CreateCheckoutSession(APIView):

    @extend_schema(
        operation_id='create_checkout_session',
    )
    @method_decorator(team_admin_required)
    def post(self, request, team_slug):
        subscription_holder = request.team
        price_id = request.POST['priceId']
        checkout_session = create_stripe_checkout_session(
            subscription_holder, price_id, request.user,
        )
        return Response(checkout_session.url)


@extend_schema(
    tags=["subscriptions"]
)
class CreatePortalSession(APIView):

    @extend_schema(
        operation_id='create_portal_session',
    )
    @method_decorator(team_admin_required)
    def post(self, request, team_slug):
        subscription_holder = request.team
        try:
            portal_session = create_stripe_portal_session(subscription_holder)
            return Response(portal_session.url)
        except SubscriptionConfigError as e:
            return Response(str(e), status=500)
