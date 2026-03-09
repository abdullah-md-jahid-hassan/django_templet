from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
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

class test2(APIView): # Test Logs
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from logs.services import (
            log_debug, log_info, log_success, 
            log_warning, log_error, log_critical
        )

        # Trigger different severity logs
        log_debug(event="test_debug", message="This is a test debug log.", metadata={"test_id": 1})
        log_info(event="test_info", message="This is a test info log.")
        log_success(event="test_success", message="This is a test success log.")
        log_warning(event="test_warning", message="This is a test warning log.")

        try:
            # Simulate an exception to test traceback extraction
            x = 1 / 0
        except Exception as e:
            log_error(
                event="test_error", 
                message=f"This is a test error log: {str(e)}", 
                traceback=True,
                metadata={"custom_key": "custom_value"}
            )
            log_critical(
                event="test_critical", 
                message=f"This is a test critical log: {str(e)}", 
                traceback=True
            )

        return success_response(
            message="Test logs generated successfully",
            status_code=status.HTTP_200_OK
        )
