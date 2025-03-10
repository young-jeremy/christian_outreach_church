from django.urls import path

from . import views

app_name = 'education'

urlpatterns = [

    path('trainings/',
         views.training_list,
         name='training_list'),

    path('training/<slug:slug>/',
         views.training_detail,
         name='training_detail'),

    path('training/<slug:slug>/enroll/',
         views.enroll_training,
         name='enroll_training'),

    path('session/<int:pk>/',
         views.mentorship_session_detail,
         name='mentorship_session_detail'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<slug:slug>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='course_enroll'),

    # Lesson Management
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),

    # Assignment Management
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/grade/', views.grade_assignment, name='grade_assignment'),

    # Discussion Management
    path('lesson/<int:lesson_id>/discussion/create/',
         views.DiscussionCreateView.as_view(), name='discussion_create'),
    path('discussion/<int:discussion_id>/reply/',
         views.add_discussion_reply, name='discussion_reply'),

    path('trainings/',
         views.LeadershipTrainingListView.as_view(),
         name='training_list'),

    path('training/<slug:slug>/',
         views.LeadershipTrainingDetailView.as_view(),
         name='training_detail'),

    path('training/<slug:slug>/enroll/',
         views.EnrollTrainingView.as_view(),
         name='enroll_training'),

    # Training Session URLs
    path('session/<int:pk>/',
         views.TrainingSessionDetailView.as_view(),
         name='session_detail'),

    path('assessment/<int:assessment_pk>/submit/',
         views.SubmitAssessmentView.as_view(),
         name='submit_assessment'),

    # Mentorship URLs
    path('mentorship/sessions/',
         views.MentorshipSessionListView.as_view(),
         name='mentorship_sessions'),

    path('mentorship/session/<int:pk>/',
         views.MentorshipSessionDetailView.as_view(),
         name='mentorship_session_detail'),

    # Staff/Admin URLs
    path('training/create/',
         views.CreateTrainingView.as_view(),
         name='create_training'),

    path('training/<slug:slug>/edit/',
         views.UpdateTrainingView.as_view(),
         name='edit_training'),

    path('training/<slug:slug>/enrollments/',
         views.TrainingEnrollmentListView.as_view(),
         name='training_enrollments'),

    path('enrollment/<int:pk>/review/',
         views.ReviewEnrollmentView.as_view(),
         name='review_enrollment'),

    path('assessment/<int:pk>/review/',
         views.ReviewAssessmentView.as_view(),
         name='review_assessment'),

    path('materials/', views.material_list, name='material_list'),
    path('material/<slug:slug>/', views.material_detail, name='material_detail'),
    path('material/create/', views.create_material, name='create_material'),
    path('material/<slug:material_slug>/add-activity/',
         views.add_activity, name='add_activity'),

    path('resources/', views.resource_list, name='theological_resource_list'),
    path('resource/<slug:slug>/', views.resource_detail, name='resource_detail'),
    path('resource/create/', views.create_resource, name='create_resource'),
    path('resource/<slug:resource_slug>/add-note/',
         views.add_study_note, name='add_study_note'),
    path('resource/<slug:resource_slug>/add-review/',
         views.add_review, name='add_review'),

    # Christian Education Level URLs
    path('levels/',
         views.ChristianEducationLevelListView.as_view(),
         name='education_level_list'),
    path('level/add/',
         views.ChristianEducationLevelCreateView.as_view(),
         name='education_level_add'),
    path('level/<int:pk>/',
         views.ChristianEducationLevelDetailView.as_view(),
         name='education_level_detail'),
    path('level/<int:pk>/edit/',
         views.ChristianEducationLevelUpdateView.as_view(),
         name='education_level_edit'),
    path('level/<int:pk>/delete/',
         views.ChristianEducationLevelDeleteView.as_view(),
         name='education_level_delete'),

    # Christian Course URLs
    path('courses/',
         views.ChristianCourseListView.as_view(),
         name='course_list'),
    path('course/add/',
         views.ChristianCourseCreateView.as_view(),
         name='course_add'),
    path('course/<slug:slug>/',
         views.ChristianCourseDetailView.as_view(),
         name='course_detail'),
    path('course/<slug:slug>/edit/',
         views.ChristianCourseUpdateView.as_view(),
         name='course_edit'),
    path('course/<slug:slug>/delete/',
         views.ChristianCourseDeleteView.as_view(),
         name='course_delete'),

    # Christian Module URLs
    path('course/<slug:course_slug>/modules/',
         views.ChristianModuleListView.as_view(),
         name='module_list'),
    path('course/<slug:course_slug>/module/add/',
         views.ChristianModuleCreateView.as_view(),
         name='module_add'),
    path('course/<slug:course_slug>/module/<int:pk>/',
         views.ChristianModuleDetailView.as_view(),
         name='module_detail'),
    path('course/<slug:course_slug>/module/<int:pk>/edit/',
         views.ChristianModuleUpdateView.as_view(),
         name='module_edit'),
    path('course/<slug:course_slug>/module/<int:pk>/delete/',
         views.ChristianModuleDeleteView.as_view(),
         name='module_delete'),

    # Christian Assignment URLs
    path('module/<int:module_pk>/assignments/',
         views.ChristianAssignmentListView.as_view(),
         name='assignment_list'),
    path('module/<int:module_pk>/assignment/add/',
         views.ChristianAssignmentCreateView.as_view(),
         name='assignment_add'),
    path('assignment/<int:pk>/',
         views.ChristianAssignmentDetailView.as_view(),
         name='assignment_detail'),
    path('assignment/<int:pk>/edit/',
         views.ChristianAssignmentUpdateView.as_view(),
         name='assignment_edit'),
    path('assignment/<int:pk>/delete/',
         views.ChristianAssignmentDeleteView.as_view(),
         name='assignment_delete'),

    # Christian Assignment Submission URLs
    path('assignment/<int:assignment_pk>/submit/',
         views.ChristianAssignmentSubmissionCreateView.as_view(),
         name='submit_assignment'),
    path('submission/<int:pk>/',
         views.ChristianAssignmentSubmissionDetailView.as_view(),
         name='submission_detail'),
    path('submission/<int:pk>/grade/',
         views.ChristianGradeSubmissionUpdateView.as_view(),
         name='grade_submission'),

    # Christian Discussion URLs
    path('module/<int:module_pk>/discussions/',
         views.ChristianDiscussionListView.as_view(),
         name='discussion_list'),
    path('module/<int:module_pk>/discussion/add/',
         views.ChristianDiscussionCreateView.as_view(),
         name='discussion_add'),
    path('discussion/<int:pk>/',
         views.ChristianDiscussionDetailView.as_view(),
         name='discussion_detail'),
    path('discussion/<int:pk>/edit/',
         views.ChristianDiscussionUpdateView.as_view(),
         name='discussion_edit'),
    path('discussion/<int:pk>/delete/',
         views.ChristianDiscussionDeleteView.as_view(),
         name='discussion_delete'),

    # Christian Discussion Post URLs
    path('discussion/<int:discussion_pk>/post/add/',
         views.ChristianDiscussionPostCreateView.as_view(),
         name='post_add'),
    path('post/<int:pk>/',
         views.ChristianDiscussionPostDetailView.as_view(),
         name='post_detail'),
    path('post/<int:pk>/edit/',
         views.ChristianDiscussionPostUpdateView.as_view(),
         name='post_edit'),
    path('post/<int:pk>/delete/',
         views.ChristianDiscussionPostDeleteView.as_view(),
         name='post_delete'),
    path('post/<int:pk>/reply/',
         views.ChristianDiscussionPostReplyView.as_view(),
         name='post_reply'),

    # Christian Enrollment URLs
    path('course/<slug:course_slug>/enroll/',
         views.ChristianEnrollmentCreateView.as_view(),
         name='enroll'),
    path('enrollments/',
         views.ChristianEnrollmentListView.as_view(),
         name='enrollment_list'),
    path('enrollment/<int:pk>/',
         views.ChristianEnrollmentDetailView.as_view(),
         name='enrollment_detail'),
    path('enrollment/<int:pk>/edit/',
         views.ChristianEnrollmentUpdateView.as_view(),
         name='enrollment_edit'),
    path('enrollment/<int:pk>/cancel/',
         views.ChristianEnrollmentDeleteView.as_view(),
         name='enrollment_cancel'),

    # Dashboard URLs
    path('student/dashboard/',
         views.ChristianEducationStudentDashboardView.as_view(),
         name='student_dashboard'),
    path('instructor/dashboard/',
         views.ChristianEducationInstructorDashboardView.as_view(),
         name='instructor_dashboard'),

    # API Endpoints
    path('api/module/<int:pk>/progress/',
         views.update_module_progress,
         name='update_module_progress'),
    path('api/discussion/<int:pk>/posts/',
         views.load_discussion_posts,
         name='load_discussion_posts'),

    # Mentorship URLs
    path('mentorship/sessions/',
         views.christian_mentorship_session_list,
         name='mentorship_session_list'),
    path('mentorship/session/create/',
         views.create_mentorship_session,
         name='mentorship_session_create'),

    path('mentorship/session/<int:session_id>/register/',
         views.register_for_christian_session,
         name='register_mentorship_session'),

    path('mentorship/mentor/<int:mentor_id>/apply/',
         views.apply_for_christian_mentorship,
         name='apply_mentorship'),

    path('mentorship/guidelines/',
         views.mentorship_guidelines,
         name='mentorship_guidelines'),

    path('mentorship/session/<int:session_id>/feedback/',
         views.submit_christian_session_feedback,
         name='submit_mentorship_feedback'),

    # Bible College URLs
    path('bible-college/',
         views.bible_college_dashboard,
         name='bible_college_dashboard'),

    path('bible-college/register/',
         views.bible_college_register,
         name='bible_college_register'),

    path('bible-college/programs/',
         views.bible_college_program_list,
         name='bible_college_program_list'),

    path('bible-college/programs/<int:program_id>/',
         views.bible_college_program_detail,
         name='bible_college_program_detail'),

    path('bible-college/courses/',
         views.bible_college_course_list,
         name='bible_college_course_list'),

    path('bible-college/courses/<int:course_id>/',
         views.bible_college_course_detail,
         name='bible_college_course_detail'),

    path('bible-college/assignments/<int:assignment_id>/submit/',
         views.bible_college_submit_assignment,
         name='bible_college_submit_assignment'),

]
