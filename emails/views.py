from rest_framework import APIView
from core.utils import get_or_400
from core.choices import OtpPorous
from rest_framework import status
from utils.response import error_response
from django.contrib.auth import get_user_model

User = get_user_model()



class EmailOtpView(APIView):
    def post(self, request):
        required_fields = ["email", "otp_porous"]
        data = get_or_400(
            request.data, 
            required_fields, 
            required_fields
        )

        if data["otp_porous"] not in OtpPorous.values:
            return error_response(
                message="Invalid otp_porous value",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if data["otp_porous"] != OtpPorous.REGISTRATION:
            user = User.objects.filter(email=data["email"]).first()
            if not user:
                return error_response(
                    message="User not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )



