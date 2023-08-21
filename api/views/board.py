from rest_framework.viewsets import ViewSet


class BoardViewSet(ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...
