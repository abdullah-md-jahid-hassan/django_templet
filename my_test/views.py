from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core.utils.response import success_response, error_response
from core.utils.general import get_or_400
from rest_framework import status

class test1(APIView): # Verify Otp
    permission_classes = [AllowAny]
    
    def post(self, request):
        flag, data = get_or_400(
            data=request.data,
            required=["purpose", "otp", "email"],
            keys=["purpose", "otp", "email"]
        )

        if not flag:
            return data

        from otp.services import OTPService
        is_verified = OTPService.verify(
            user=data['email'],
            submitted_otp=data['otp'],
            purpose=data['purpose']
        )

        if not is_verified:
            return error_response(
                message='OTP is not valid',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return success_response(
            message="OTP verified successfully",
            status_code=status.HTTP_200_OK
        )
        
    
