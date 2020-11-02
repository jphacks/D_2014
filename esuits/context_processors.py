"""コンテキストプロセッサ"""

def header_context_processor(request):
    return {
        'is_authenticated': request.user.is_authenticated
    }