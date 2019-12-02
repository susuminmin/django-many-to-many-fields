from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# accounts > models.py 에서 커스터마이징 한 User Class 인식하지 못함

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        # 직접 get_user_model 함수로 User 모델 정보 넣음
        model = get_user_model() # accounts.User
        fields = UserCreationForm.Meta.fields 