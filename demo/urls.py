from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# from .views import test_csrf_view


urlpatterns = [
     path('', views.home, name='home'),
     path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
     path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage-credits/', views.manage_credits, name='manage_credits'),
    # path('log_hours/<int:id>/', views.log_hours, name='log_hours'),
    path('log_hours/<int:service_id>/', views.log_hours, name='log_hours'),


    # path('log_hours/<int:time_credit_id>/', views.log_hours, name='log_hours'),
    path('add_service/', views.add_service, name='add_service'),
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    # path('services/book/<int:service_id>/', views.book_service, name='book_service'),
    path('bookings/manage/', views.manage_bookings, name='manage_bookings'),
    path('notification/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),

    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('calendar/', views.calendar, name='calendar'),  # Add this line for calendar view

    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    
    path('service/<int:service_id>/review/', views.add_review, name='add_review'),
    path('reviews/', views.all_reviews, name='all_reviews'), 

    path('accept-service/<int:service_id>/', views.accept_service, name='accept_service'),
     path('update_location/<int:request_id>/', views.update_location, name='update_location'),
    path('profile/', views.profile, name='profile'),


    path('service/<int:id>/approve/', views.approve_service, name='approve_service'),
    path('service/<int:id>/reject/', views.reject_service, name='reject_service'),
    path('service-moderation/', views.service_moderation, name='service_moderation'),
    path('about/', views.about_us, name='about_us'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('accept_offer/<int:service_id>/', views.accept_offer, name='accept_offer'),
    path('requests/', views.request_list, name='request_list'),
        # path('service_requests/', views.request_list, name='service_requests'),

    # path('give-time-credit/<int:worker_id>/', views.give_time_credit, name='give_time_credit'),...............

    path('requests/add/', views.add_service_request, name='add_service_request'),
    path('requests/accept/<int:request_id>/', views.accept_service_request, name='accept_service_request'),
    path('service_requests/edit/<int:request_id>/', views.edit_service_request, name='edit_service_request'),
    path('service_requests/delete/<int:request_id>/', views.delete_service_request, name='delete_service_request'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('accepted-requests/', views.accepted_requests_view, name='accepted_requests'),
    path("mark-completed/<int:request_id>/", views.mark_as_completed, name="mark_as_completed"),
    path("approve-task/<int:request_id>/", views.approve_task, name="approve_task"),
    path('approve_service_log/<int:log_id>/', views.approve_service_log, name='approve_service_log'),
    path('reject_service_log/<int:log_id>/', views.reject_service_log, name='reject_service_log'),
        path('service-request/complete/<int:request_id>/', views.complete_service_request, name='complete_service_request'),

        path('request-time-credit/<int:request_id>/', views.request_time_credit, name='request_time_credit'),
    path('approve-time-credit/<int:request_id>/', views.approve_time_credit, name='approve_time_credit'),





   



    # path('test-csrf/', test_csrf_view, name='test_csrf'),



    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    


