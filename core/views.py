from django.shortcuts import render
from core.services import health_report
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class HealthReportView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        health = health_report()
        return render(request, 'health_report.html', health)
