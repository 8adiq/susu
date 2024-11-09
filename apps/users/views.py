from django.shortcuts import render
from .serializer import UserSerializer
from .models import User
from  rest_framework import viewsets,status
from .permission import IsAgent,IsManager
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
        
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role ==  User.MANAGER:
            return User.objects.filter(role__in=[User.CLIENT,User.AGENT])
        elif self.request.user.role == User.AGENT:
            return User.objects.filter(role=User.CLIENT)
        return User.objects.none()
        
    def get_permissions(self):
        if self.request.user.role == User.MANAGER and self.action == 'create':
            return [IsAuthenticated(),IsManager()]
        elif self.request.user.role == User.AGENT and self.action == 'create':
            return [IsAuthenticated(),IsAgent()]
        return super().get_permissions()
    

    def perform_create(self, serializer):
        role = self.request.data.get('role')

        # automatically assigning user and user creator roles
        if role == User.AGENT and self.request.user.role == User.MANAGER:
            serializer.save(role=User.AGENT,manager=self.request.user)
        elif role == User.CLIENT:
            if self.request.user.role == User.MANAGER:
                serializer.save(role=User.CLIENT,manager=self.request.user)
            elif self.request.user.role == User.AGENT:
                serializer.save(role=User.CLIENT,agent=self.request.user)
        else:
            raise PermissionError('Invalid role assignment')
        
    @action(detail=False,methods=['POST'],permission_classes=[IsAuthenticated,IsAdminUser])
    def create_manager(self,request):
        """custom endpoint for creating a manager and making it a supersuer"""

        data = request.data.copy()
        data['role'] == User.MANAGER
        data['is_superuser'] = True
        data['is_staff'] = True


        serialiser = self.get_serializer(data=data)
        serialiser.is_valid(raise_exceotion=True)
        serialiser.save()

        return Response(serialiser.data,status=status.HTTP_201_CREATED)