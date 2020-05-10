from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('types/', views.TypeView().as_view()),
                  path('constructions/', views.ConstructionView().as_view()),
                  path('series/', views.SeriesView().as_view()),
                  path('states/', views.StateView().as_view()),
                  path('countries/', views.CountryView().as_view()),
                  path('regions/', views.RegionView().as_view()),
                  path('cities/', views.CityView().as_view()),
                  path('currency/', views.CurrencyView().as_view()),
                  path('roles/', views.RoleView().as_view()),

                  path('locations/', views.LocationView().as_view()),
                  path('details/', views.DetailView().as_view()),
                  path('contacts/', views.ContactView().as_view()),

                  path('comments/', views.CommentView().as_view()),
                  path('comments/<int:pk>/', views.CommentDetail().as_view()),
                  path('apartment/<int:pk>/comments/', views.CreateComment().as_view()),

                  path('own-apartments/', views.OwnerView().as_view()),
                  path('own-apartments/<int:pk>/upload/', views.UploadImage().as_view()),

                  path('own-apartments/<int:id>/upload/<int:pk>/', views.PhotoUpdate().as_view()),
                  path('own-apartments/<int:id>/booking/', views.CreateBooking().as_view()),
                  path('own-apartments/<int:id>/booking/<int:pk>/', views.BookingDetail().as_view()),
                  path('add/', views.ApartmentView().as_view()),
                  path('near/<int:pk>/', views.NearApartments().as_view()),

                  path('apartment/<int:pk>/', views.ApartmentDetail().as_view()),
                  path('apartments/', views.ApartmentListView().as_view()),
                  path('front-apartments/', views.FrontApartmentListView().as_view()),

                  path('nearby-objects/', views.NearbyObjectsListView().as_view()),
                  path('objects-in-apartment/', views.ObjectsInApartmentListView().as_view()),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
