from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .analysis_serializers import AnalysisSerializer
from .analysis_services import AnalysisService
from .models import Analysis



class AnalysisListView(ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 접속한 유저의 데이터만 반환하고,
        쿼리 파라미터에 따라 주간/월간 데이터를 필터링
        """
        user = self.request.user
        queryset = Analysis.objects.filter(user=user)

        # 쿼리 파라미터 추출
        analysis_type = self.request.query_params.get('type')

        if analysis_type:
            queryset = queryset.filter(type=analysis_type)

        return queryset

class AnalysisCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        사용자로부터 파라미터를 받아 분석을 실행하고 결과를 저장
        """
        # 요청 데이터 추출
        about = request.data.get('about')
        analysis_type = request.data.get('type')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')

        # 필수 값 체크
        if not all([about, analysis_type, period_start, period_end]):
            return Response(
                {"detail": "모든 필드(about, type, period_start, period_end)를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 서비스 호출
        try:
            analysis_obj = AnalysisService.create_transaction_analysis(
                user=request.user,
                about=about,
                analysis_type=analysis_type,
                period_start=period_start,
                period_end=period_end
            )

            if analysis_obj:
                serializer = AnalysisSerializer(analysis_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"detail": "해당 기간에 분석할 거래 내역이 없습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)