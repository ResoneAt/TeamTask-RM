from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWorkSpaceOwner(BasePermission):
    message = 'permission denied, you are not the workspace owner'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsBoardOwner(BasePermission):
    message = 'permission denied, you are not the board owner'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsWorkSpaceMember(BasePermission):
    message = 'permission denied, you are not a member of this workspace'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        user = request.user
        workspace = obj.workspace
        return workspace.wsmembershipmodel_set.filter(to_user=user).exists()


class IsBoardMember(BasePermission):
    message = 'permission denied, you are not a member of this board'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        user = request.user
        board = obj.board
        return board.bmembershipmodel_set.filter(to_user=user).exists()


class IsCardMember(BasePermission):
    message = 'permission denied, you are not a member of this card'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        user = request.user
        card = obj.card
        return card.cmembershipmodel_set.filter(to_user=user).exists()
