from django.conf.urls import include, url

from companies.views import CompanyViewSet, EmploymentViewSet
from tg_apicore.routers import Router


router = Router()

router.register('companies', CompanyViewSet)
router.register('employments', EmploymentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
