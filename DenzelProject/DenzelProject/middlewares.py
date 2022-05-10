# from random import randint


# def modify_context(get_response):
#     def middleware(request):
        

#         response = get_response(request)
#         rand_num = randint(1, 100000)
#         response.context_data['rand_num'] = rand_num 
#         return response
#     return middleware