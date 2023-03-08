def jwt_response_handler(token,user=None,request=None):
    """
    自定义JWT认证成功以后返回的响应格式
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token':token,  # 返回jwt签发之后的token
        'id':user.id,   #返回登陆用户的id
        "username":user.username,  #返回登陆用户的用户名
    }