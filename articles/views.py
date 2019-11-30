from django.shortcuts import render


def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        pass
    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        return render(request, 'articles/create.html')
