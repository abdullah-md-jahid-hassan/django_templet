from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core.utils.response import error_response
from core.choices import OtpPurpose
from rest_framework import status
from core.utils.validator import validate_phone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from otp.utils import get_otp_rules
from otp.enums import OtpChannel
from otp.services import OTPService
from rest_framework.throttling import AnonRateThrottle

class GetOtpRateThrottle(AnonRateThrottle):
    scope = 'get_otp'

class GetOtpView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [GetOtpRateThrottle]

    def post(self, request, *args, **kwargs):
        # ==============
        # Get purpose
        # ==============
        purpose = request.data.get('purpose', None)
        if not purpose or purpose not in OtpPurpose.values:
            return error_response(
                message='"purpose" is requeued or "purpose" is not valid ',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # Validate otp rules and get all require variables
        # =================================================
        # Get otp rules
        otp_rules = get_otp_rules(purpose)

        # Check if otp is enabled
        if not otp_rules.enable:
            return error_response(
                message='OTP is not enabled for this purpose',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if user is authenticated
        if otp_rules.require_auth and not request.user.is_authenticated:
            return error_response(
                message='You are not authenticated',
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Check if user identifier is required
        if otp_rules.require_identifier:
            user_identifier = request.data.get('user_identifier', None)
            if not user_identifier:
                return error_response(
                    message='"user_identifier" is requeued ',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        # Get otp channel
        otp_channel = otp_rules.channel
        if otp_channel == OtpChannel.all:
            otp_channel = request.data.get('otp_channel', None)
        if not otp_channel:
            return error_response(
                message='"otp_channel" is requeued ',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Ensure The user identifier is exist
        user_authenticated = request.user.is_authenticated
        if user_authenticated and not user_identifier:
            user_identifier = request.user.email if otp_channel == OtpChannel.EMAIL else request.user.phone
        if not user_identifier:
            return error_response(
                message='Failed to get user identifier',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Validate user identifier with otp channel
        match otp_channel:
            case OtpChannel.EMAIL:
                validate_email(user_identifier)                
            case OtpChannel.PHONE:
                region = request.data.get('region', None)
                if not region:
                    return error_response(
                        message='"region" is requeued ',
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                validate_phone(user_identifier, region)
            case _:
                return error_response(
                    message='"otp_channel" is not valid ',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        # ===========
        # Send OTP
        # ===========
        OTPService.send(
            user=user_identifier,
            purpose=purpose,
            channel=otp_channel
        )

        return success_response(
            message=f'OTP sent successfully. Please check {otp_channel}. Will be valid for 5 minutes.',
            status_code=status.HTTP_200_OK
        )

        
        
            

        
            

