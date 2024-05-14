from django.urls import path, include
from .views import *

urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/create/', UserView.as_view()),
    path('user/update/<str:uid>', UserView.as_view()),
    path('user/delete/<str:uid>', UserView.as_view()),
    path('user/detail/<str:uid>', UserView.as_view(), name='user_detail'),
    path('organizer/create/', OrganizerView.as_view()),
    path('organizer/json/', OrganizerListView.as_view()),
    path('organizer/<int:id>', OrganizerViewss.as_view()),
    path('organizer/content-writer/json/', UserView.get_cw, name='get_cw'),
    path('organizer/island-organizer/json/', UserView.get_io, name='get_io'),
    path('trips/create/', IslandOrganizerView.as_view()),
    path('trips/update/<int:trip_id>/', IslandOrganizerView.as_view()),
    path('trips/delete/<int:trip_id>/', IslandOrganizerView.as_view()),
    path('trips/', IslandOrganizerView.as_view()),
    path('trips/detail/<int:trip_id>/', IslandOrganizerDetail.as_view()),
    path('trip/register/', UpdateApplicationStatus.as_view()),
    path('trips/participants/<int:trip_id>/', ListParticipants.as_view()),
    path('trips/<int:trip_id>/participants/<int:user_id>/', UserDetailAPIView.as_view()),
    path('trips/<int:trip_id>/delete/<int:user_id>/', UserTripRegistration.as_view()),
    path('trips/<int:trip_id>/', UpdateApplicationStatus.as_view()),
    path('trips/<int:trip_id>/add-questions/', TripQuestionAPIView.as_view()),
    path('trips/<int:trip_id>/questions/', TripQuestionAPIView.as_view()),
    path('trip/register/<int:trip_id>/', UserTripRegistration.as_view()),
    path('signup/', UserSignUp.as_view(), name='user_signup'),
    # path('signin/', user_signin, name='user_signin'),
    # path('forget-password/', user_forget_password, name='user_forget_password'),
    path('users/', UserListView.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'), 
    # path('trips/<int:trip_id>/answers/<int:user_id>/', TripAnswerAPIView.as_view()),
    # path('trips/<int:user_id>/<int:trip_id>/', UpdateApplicationStatus.as_view()),
    path('blogs/', BlogListAPI.as_view()),
    path('blogs/<str:language>/', BlogListAPI.as_view(), name='get_blogs_by_language'),
    path('blog/<int:blog_id>', BlogAPI.as_view()),
    path('blog/create', BlogAPI.as_view()),
    path('blog/update/<int:blog_id>', BlogAPI.as_view()),
    path('blog/delete/<int:blog_id>', BlogAPI.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'), # this is for validation
    path('trips/<int:trip_id>/answers/<int:user_id>/', TripAnswerAPIView.as_view()),
    path('trips/<int:trip_id>/<int:user_id>/', UpdateApplicationStatus.as_view()),
    path('crowdfunding/create', FundApiViews.as_view()),
    path('crowdfunding/', FundApiViews.as_view()),
    path('crowdfunding/update/<int:fund_id>/', FundApiViews.as_view()),
    path('crowdfunding/<int:fund_id>/', FundApiViews.as_view()),
    path('fund/', FundLandingPageView.as_view()),
    # path('trips/<int:user_id>/<int:trip_id>/', UpdateApplicationStatus.as_view()),
    path('merchandise/', MerchandiseView.as_view()),
    path('merchandise/<int:id>/', MerchandiseView.as_view()),
    path('merchandisesection/', MerchandiseSectionView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<int:id>/', CommentView.as_view()),
    path('comments/blog/<int:blog_id>/', CommentView.get_comments_by_blog_id, name='comments_by_blog_id'),
    path('comments-report/', CommentReportView.as_view()),
    path('comments-report/<int:id>/', CommentReportView.as_view()),
    path('registered-volunteers/', ListRegisteredVolunteers.as_view(), name='list_registered_volunteers'),
    path('filter-volunteers/<str:status>/', FilterVolunteersByStatus.as_view(), name='filter_volunteers_by_status'),
    path('organizer-contact/<int:organizer_id>/', ViewOrganizerContact.as_view(), name='view_organizer_contact'),
    path('trips/<int:user_id>/<int:trip_id>/', UpdateApplicationStatus.as_view()),
    path('merchandise/', MerchandiseView.as_view()),
    path('merchandise/<int:id>/', MerchandiseView.as_view()),
    path('merchandisesection/', MerchandiseSectionView.as_view()),
    path('merchandisesection/<int:id>/', MerchandiseSectionView.as_view()),
    # need to be fixed here. wait 12.30
    path('api/verified-volunteers/', ListRegisteredVolunteers.as_view(), name='verified-volunteers'),
    path('api/volunteer-history/<str:uid>/', VolunteerHistoryView.as_view(), name='volunteer-history'),
    path('api/volunteers-by-status/<str:status>/', FilterVolunteersByStatus.as_view(), name='volunteers-by-status'),
    path('api/organizer-contact/<int:organizer_id>/', ViewOrganizerContact.as_view(), name='organizer-contact'),
    path('api/sections/', HomePageSectionListCreateView.as_view(), name='section-list-create'),
    path('api/sections/<int:pk>/', HomePageSectionDetailView.as_view(), name='section-detail'),
    path('homepage/sections/', HomePageSections.as_view(), name='home-page-sections'),
    path('trips/island-name-count/', TotalTripsByIslandView.as_view()),
    path('participants/total/', TotalParticipantsView.as_view()),
    path('trip/status-total/', TotalApplicationStatusView.as_view()),
    path('trip/total-user-nationalities/', TotalUserNationalitiesView.as_view()),
    path('trip/<int:trip_id>/total-applications/', TotalApplicationStatusTripView.as_view()),
    path('trips/<int:trip_id>/participants/count/', CountParticipants.as_view()),
    path('trips/<int:trip_id>/nationalities/count/', TotalUserNationalitiesTripView.as_view()),
    path('blogs/count/', BlogCountView.as_view()),    
    path('blogs/<int:blog_id>/total-comment-reports/', TotalCommentReportsView.as_view()),
    path('blogs/<int:blog_id>/total-comment-blog/', TotalCommentBlogView.as_view()),
    path('users/count/', TotalUserCountView.as_view()),   
    path('users/count-nationalities/', TotalNationalitiesUserView.as_view()),      
    path('users/count-domicile/', TotalDomicileUserView.as_view()),
    path('trip/count/', TotalTripView.as_view()),   
    path('merchandise/count/', TotalMerchandiseView.as_view()),   
    path('crowdfunding/count/', TotalCrowdfundingView.as_view()), 
    path('users/count-created/', UserCreatedDateView.as_view()),   
    path('crowdfunding/writing/create', FundWritingView.as_view()),
    path('crowdfunding/writing', FundWritingView.as_view()),
    path('crowdfunding/writing/update/<int:id>/', FundWritingView.as_view()),
    path('crowdfunding/writing/<int:id>/', FundWritingView.as_view()),   
    path('about-us/latest/' , AboutUsView.as_view()),
    path('about-us/new/' , AboutUsView.as_view()),
    path('about-us/update/<int:id>' , AboutUsView.as_view()),
    path('about-us/delete/<int:id>' , AboutUsView.as_view()),
    path('trip/<int:trip_id>/questions-answers/', TripQuestionAnswerListAPIView.as_view()),
    path('trips/search/?q=query', IslandSearchView.as_view()),

    

]
