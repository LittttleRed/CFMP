```mermaid

classDiagram
    class View {
        +dispatch()
        +http_method_not_allowed()
        +options()
    }
    class APIView {
        +initial()
        +finalize_response()
        +get_authenticate_header()
        +get_authenticators()
        +perform_authentication()
        +get_content_negotiator()
        +get_permissions()
        +get_renderers()
        +get_throttles()
        +get_view_name()
        +get_view_description()
        +handle_exception()
    }
    class GenericAPIView {
        +get_queryset()
        +get_object()
        +get_serializer()
        +get_serializer_class()
        +get_serializer_context()
        +filter_queryset()
        +paginate_queryset()
        +get_paginated_response()
    }
    class ListAPIView {
        +get()
    }
    class CreateAPIView {
        +post()
        +perform_create()
    }
    class RetrieveAPIView {
        +get()
    }
    class UpdateAPIView {
        +put()
        +patch()
        +perform_update()
    }
    class DestroyAPIView {
        +delete()
        +perform_destroy()
    }
    class ListCreateAPIView {
        +get()
        +post()
        +perform_create()
    }
    class RetrieveUpdateAPIView {
        +get()
        +put()
        +patch()
        +perform_update()
    }
    class RetrieveUpdateDestroyAPIView {
        +get()
        +put()
        +patch()
        +delete()
        +perform_update()
        +perform_destroy()
    }
    View <|-- APIView
    APIView <|-- GenericAPIView
    GenericAPIView <|-- ListAPIView
    GenericAPIView <|-- CreateAPIView
    GenericAPIView <|-- RetrieveAPIView
    GenericAPIView <|-- UpdateAPIView
    GenericAPIView <|-- DestroyAPIView
    GenericAPIView <|-- ListCreateAPIView
    GenericAPIView <|-- RetrieveUpdateAPIView
    GenericAPIView <|-- RetrieveUpdateDestroyAPIView
```

> [!TIP]
> 如果接口是非常标准的list()(get 列表),retrieve()(get 单个资源),destroy()(delete 单个资源)
> update()(put)，partial_update(patch),create(post 单个资源),其中url的设置list和create相同，
> destroy,delete,update,partial_update等需要指定单个资源的url相同,使用viewset类将会非常方便，
> viewset面向的是上面6种动作，APIView面向的是HTTP请求，现成的LISTAPIView等APIView由mixin和
> genericAPIView继承而来，意味着可以自定义根据此url对应的请求使用不同类的mixin来构建自己的
> genericAPIView
