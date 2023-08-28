from django.urls import path, include
from rest_framework_nested import routers


from Softdesk.views import ProjectViewSet, IssueViewSet, CommentViewSet


router = routers.SimpleRouter()

router.register(r"projects", ProjectViewSet)

projects_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
projects_router.register(r"issues", IssueViewSet, basename="issues")


issues_router = routers.NestedSimpleRouter(projects_router, r"issues", lookup="issue")
issues_router.register(r"comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
