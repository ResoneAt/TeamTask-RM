from rest_framework.viewsets import ViewSet


class MyCardViewSet(ViewSet):
    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...

    def partial_update(self, request, pk=None):
        ...


class CardViewSet(ViewSet):
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


class SubCardViewSet(ViewSet):

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...


class ListViewSet(ViewSet):

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...


class LabelViewSet(ViewSet):

    def create(self, request):
        ...

    def partial_update(self, request, pk=None):
        ...

    def destroy(self, request):
        ...
